#  Copyright (c) 2023 Macrometa Corp All rights reserved.
import argparse
import json
import os
import time
from importlib import import_module
from inspect import ismethod

import pkg_resources
import psycopg2
from c8connector import C8Connector, ValidationException
from fastapi import FastAPI, Body, status, HTTPException
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.pool import SimpleConnectionPool
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import uvicorn

package_filters = ['macrometa-source-', 'macrometa_source_', 'macrometa-target-', 'macrometa_target_',
                   'macrometa-integration-', 'macrometa_integration_']


class DB:
    def __init__(
            self, user: str, password: str, host: str, port: str, database: str = 'c8cws'
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.try_create_tables(database, host, password, port, user, 20)
        self.pool = SimpleConnectionPool(
            1, 25, user=user,
            password=password,
            host=host,
            port=port,
            database=database)

    @staticmethod
    def try_create_tables(database, host, password, port, user, max_tries):
        cursor, con = None, None
        backoff = 2
        done = False
        for i in range(max_tries):
            backoff = (i + 1) * backoff
            try:
                con = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
                con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = con.cursor()
                cursor.execute("CREATE TABLE workflow (uuid TEXT PRIMARY KEY, federation TEXT,"
                               " tenant TEXT, fabric TEXT, bin_workflow BYTEA, state JSONB);")
                done = True
            except OperationalError as e:
                print(f"Unable to connect to the central cloud RDS. {str(e).capitalize().strip()}."
                      f" Retrying in {backoff} seconds ...")
                time.sleep(backoff)
                continue
            except Exception as e:
                print(f"Skipping tables creation. {str(e).capitalize().strip()}.")
                done = True
                break
            finally:
                if cursor is not None:
                    cursor.close()
                if con is not None:
                    con.close()
        if not done:
            raise RuntimeError(f"Unable to connect to the central cloud RDS. "
                               f"Please check RDS connectivity and configurations.")

    def close(
            self
    ) -> None:
        self.pool.closeall()

    def update_state(self, uuid: str, state: object):
        state_json = json.dumps(state)
        conn = self.pool.getconn()
        cursor = conn.cursor()
        query = """
            UPDATE workflow
            SET state = %s
            WHERE uuid = %s;
        """
        cursor.execute(query, (state_json, uuid))
        conn.commit()
        cursor.close()
        self.pool.putconn(conn)

    def get_state(self, uuid: str):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        query = """
            SELECT state
            FROM workflow
            WHERE uuid = %s;
        """
        cursor.execute(query, (uuid,))
        result = cursor.fetchone()
        cursor.close()
        self.pool.putconn(conn)
        if result is not None and result[0] is not None:
            return result[0]
        else:
            return None


class StateFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('state.json'):
            save_state()


uuid = os.getenv("WORKFLOW_UUID")
state_save_interval = os.getenv("STATE_SAVE_INTERVAL", 60)
state_file_dir = os.getenv("STATE_DIR", "/project/eltworkflow/state")

db = DB(
    user=os.getenv("PG_USER") or os.getenv("RDS_USER"),
    password=os.getenv("PG_PASSWORD") or os.getenv("RDS_PASSWORD"),
    host=os.getenv("PG_HOST") or os.getenv("RDS_HOST"),
    port=os.getenv("PG_PORT") or os.getenv("RDS_PORT"),
    database=os.getenv("PG_DATABASE") or os.getenv("RDS_DATABASE", "c8cws")
)


def load_state():
    # Read from the db and write the state into state.json file.
    print(f"Loading the state of workflow {uuid} from the database.")
    try:
        state_content = db.get_state(uuid)
        if state_content:
            with open(f"{state_file_dir}/state.json", "w") as state_file:
                json.dump(state_content, state_file)
    except Exception as e:
        print(f"Couldn't load state of {uuid} from database. {e}")
        return


def save_state():
    # Read the state.json file and write the state to the DB.
    print(f"Saving the state of workflow {uuid} to the database.")
    try:
        with open(f"{state_file_dir}/state.json", "r") as state_file:
            state_content = json.load(state_file)
            if state_content:
                db.update_state(uuid, state_content)
    except Exception as e:
        print(f"Couldn't persist state of {uuid} to database. {e}")
        return


def start_state_observer():
    event_handler = StateFileHandler()
    observer = Observer()
    observer.schedule(event_handler, state_file_dir, recursive=False)
    print(f"Starting state observer on `{state_file_dir}/state.json`")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def expose_connector():
    # Create an argument parser with an argument for the port.
    parser = argparse.ArgumentParser(description="Expose the connector on the specified port.")
    parser.add_argument("port", type=int, help="Port number to expose the connector")
    args = parser.parse_args()
    port = args.port

    # Load all the installed packages in the current environment.
    installed_packages = pkg_resources.working_set
    for pkg in installed_packages:
        k = pkg.key
        if any(pf in k for pf in package_filters):
            try:
                # replace `-` of module name with `_`.
                k = k.replace("-", "_")
                import_module(k)
            except:
                pass

    # Discover the connector class that extends C8Connector.
    connector_classes = [cls for cls in C8Connector.__subclasses__() if issubclass(cls, C8Connector)]
    if len(connector_classes) != 1:
        raise Exception("Expected exactly one connector class, but found multiple or none.")

    # Create an instance of the connector class.
    connector_class = connector_classes[0]
    connector_instance = connector_class()

    # Create a FastAPI application.
    app = FastAPI(
        title=f"{connector_instance.name()} {connector_instance.type().title()} API",
        version=connector_instance.version()
    )

    # Expose methods as API endpoints.
    for method_name in dir(C8Connector):
        method = getattr(connector_instance, method_name)
        if ismethod(method) and method_name != "expose_connector":
            # Determine the HTTP method based on the method name
            http_method = "POST" if method_name in ("validate", "samples", "schemas") else "GET"

            # Generate a route path based on the method name
            route_path = f"/{method_name}"

            # Define a closure function to capture the method
            def create_route_handler(handler_method):
                if http_method == "POST":
                    async def route_handler(body: dict = Body(None)):
                        try:
                            return handler_method(body)
                        except ValidationException as e:
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
                        except Exception as e:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
                else:
                    async def route_handler():
                        try:
                            return handler_method()
                        except ValidationException as e:
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
                        except Exception as e:
                            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
                return route_handler

            # Create the API route and bind it to the closure function
            if http_method == "POST":
                app.post(route_path)(create_route_handler(method))
            else:
                app.get(route_path)(create_route_handler(method))

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=port)
