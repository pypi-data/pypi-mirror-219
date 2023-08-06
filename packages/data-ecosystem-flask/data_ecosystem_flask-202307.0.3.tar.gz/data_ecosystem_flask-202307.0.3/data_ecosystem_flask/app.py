"""
Flask App exposing JIRA and Alation services via Swagger.

Summary:
    This Flask app provides endpoints to interact with
    JIRA and Alation services through a Swagger UI.

Returns:
    None
"""

from flask import Flask, send_file, request, render_template, Blueprint, g, jsonify, make_response, Response
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from pathlib import Path
from datetime import datetime
from io import BytesIO
from pandas import ExcelWriter
from requests.exceptions import HTTPError
from openpyxl.utils.exceptions import InvalidFileException
from flask_restx import Api, Resource, fields, Namespace, reqparse, marshal_with
from json import JSONDecodeError
from bs4 import BeautifulSoup
from data_ecosystem_flask.app_startup import create_api, create_app
from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.middleware.proxy_fix import ProxyFix
import traceback
from requests.exceptions import RequestException
import requests
import os
import time

from data_ecosystem_services.alation_service import (
    schema as pade_schema,
    datasource as pade_datasource,
    tokenendpoint as pade_tokenendpoint,
    manifest as pade_manifest
)
from data_ecosystem_services.cdc_tech_environment_service import (
    environment_file as pade_env_file
)
from data_ecosystem_services.az_key_vault_service import (
    az_key_vault as pade_az_key_vault
)
from data_ecosystem_services.cdc_self_service import (
    environment_metadata as pade_env_metadata
)
from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)
from data_ecosystem_services.cdc_security_service import (
    security_core as pade_security_core,
)

from data_ecosystem_services.posit_service import (
    posit_connect as pade_posit_connect
)

import requests
import openpyxl
import pandas as pd
import csv
import json
import sys
import os
import logging
import io
import importlib
import base64
import dotenv


TIMEOUT_5_SEC = 5
TIMEOUT_ONE_MIN = 60

# Get the currently running file name
SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))

print(f"SERVICE_NAME:{SERVICE_NAME}")
print(f"NAMESPACE_NAME: {NAMESPACE_NAME}")
sys.path.append(os.getcwd())
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(app_dir)

# app.config["PYTHONPATH"] = "../../../data_ecosystem_services/"

app = create_app()


@app.before_request
def before_request():
    g.base_url = request.url_root
    g.log_url = g.base_url + "/logs/get_log_file_tail/1000"


# Define the blueprint
cdc_admin_bp = Blueprint('logs', __name__,
                         url_prefix='/logs')

# Define the blueprint
cdc_files_bp = Blueprint('files', __name__,
                         url_prefix='/files')


def get_datetime(entry):

    date_string = entry[0]
    if date_string == '0001-01-01 00:00:00':
        # Handle the specific string and return a valid datetime object
        return datetime.min
    try:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    except Exception as ex:
        msg = f"Error processing {entry}.  Could not convert '{date_string}' to a datetime object. Please check if it matches the format %Y-%m-%d %H:%M:%S'. Error: {str(ex)}"
        print(msg)

        # return datetime.min to sort invalid dates to the beginning, or datetime.max to sort them to the end
        return datetime.min


@cdc_files_bp.route('/download')
def download():
    calling_page_url = request.args.get('calling_page')
    return render_template('download.html', calling_page_url=calling_page_url)


@cdc_files_bp.route('/upload')
def upload():
    calling_page_url = request.args.get('calling_page')
    return render_template('upload.html', calling_page_url=calling_page_url)


@cdc_admin_bp.route('/error')
def error():
    error_message = "An unexpected error occurred"
    return render_template('error.html', error_message=error_message)


@cdc_admin_bp.route('/get_log_file_tail/<int:number_of_lines>')
def get_log_file_tail(number_of_lines):
    """Get the last n lines of the log file"""

    logger_singleton = pade_env_logging.LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME)
    logger = logger_singleton.get_logger()

    with tracer.start_as_current_span(f"get_log_file_tail"):

        try:

            log_data = None

            status_code, number_of_lines, log_data = logger_singleton.get_log_file_tail(
                number_of_lines)
            if status_code == 500:
                error_msg = f"Internal Server Error fetching log file: The server encountered an error. {log_data}"
                raise Exception(error_msg)

            if log_data is None:
                raise ValueError(
                    f"Internal Server Error fetching log file: Log data is None. {log_data}")

            if number_of_lines is None or number_of_lines == 0:
                raise ValueError(
                    f"Internal Server Error fetching log file: number_of_lines is missing or blank")

            log_entries = []

            for line_number, line in enumerate(log_data.strip().split('\n'), start=1):
                log_entries.append(line.split('\u001F'))

            for entry in log_entries:
                try:
                    asctime, name, module, lineno, levelname, message = entry
                    datetime_object = datetime.strptime(
                        asctime, "%Y-%m-%d %H:%M:%S")
                    asctime = datetime_object.strftime("%Y-%m-%d %I:%M:%S %p")
                    entry = [asctime, name, module, lineno, levelname, message]
                except ValueError as ex:
                    logger.warning(f"Error parsing line: {ex}")
                except IndexError:
                    logger.warning(f"Error: line has missing fields: {entry}")

            # Sort log_entries by date and time in descending order
            log_entries.sort(
                key=lambda entry: get_datetime(entry), reverse=True)

            return render_template('log_file.html', entries=log_entries)

        except Exception as ex:
            trace_msg = traceback.format_exc()
            line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
            error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
            exc_info = sys.exc_info()
            logger_singleton.error_with_exception(error_message, exc_info)
            return render_template('error.html', error_message=error_message)


app.register_blueprint(cdc_admin_bp)
app.register_blueprint(cdc_files_bp)

metric_exporter = AzureMonitorMetricExporter()

logger = app.logger
logger_singleton = pade_env_logging.LoggerSingleton.instance(
    NAMESPACE_NAME, SERVICE_NAME)
tracer = app.tracer

FlaskInstrumentor().instrument_app(app)

API_DESCRIPTION = '''
<h2>API Documentation</h2>
<p>The Program Agnostic Data Ecosystem (PADE) provides shared resources,
practices and guardrails for analysts to discover, access, link, and use
agency data in a consistent way. PADE improvements in standardized and 
streamlined workflows reduce the effort required to find, access, and
trust data.</p>
<p><a href="/files/upload">Upload Page</a></p>
<p><a href="/files/download">Download Page</a></p>
<p>For detailed logs, please visit the <a href="/logs/get_log_file_tail/1000">Log File Page</a>.</p>
'''

api, ns_welcome, ns_alation, ns_jira, ns_posit, ns_cdc_admin, ns_cdc_security = create_api(
    app, API_DESCRIPTION)

# Define a model for the metadata
metadata_model = api.model('Metadata', {
    'start_time': fields.Float,
    'end_time': fields.Float,
    'total_time': fields.Float,
    'data': fields.String
})

# Define the file link model
file_link_model = api.model('FileLink', {
    'link': fields.String(description='Download link for the metadata file')
})


def get_posit_api_key():

    with tracer.start_as_current_span(f"get_posit_api_key"):

        config = app.cdc_config

        posit_connect_base_url = config.get("posit_connect_base_url")

        logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
        az_kv_az_sub_client_secret_key = config.get(
            "az_kv_az_sub_client_secret_key")
        az_kv_az_sub_client_secret_key = az_kv_az_sub_client_secret_key.replace(
            "-", "_")
        client_secret = os.getenv(az_kv_az_sub_client_secret_key)
        tenant_id = config.get("tenant_id")
        client_id = config.get("client_id")
        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        running_interactive = False
        if not client_secret:
            running_interactive = True

        az_key_vault = pade_az_key_vault.AzKeyVault(
            tenant_id, client_id, client_secret, az_kv_key_vault_name, running_interactive)

        az_kv_posit_connect_secret_key = config.get(
            "az_kv_posit_connect_secret_key")

        az_kv_posit_connect_secret = az_key_vault.get_secret(
            az_kv_posit_connect_secret_key)

        return az_kv_posit_connect_secret


class WelcomeSwagger(Resource):
    def get(self):
        """
        Returns the Swagger API documentation.

        Returns:
            dict: The Swagger API documentation schema.
        """
        with tracer.start_as_current_span("/api/swagger"):
            return api.__schema__


class Task(Resource):
    """
    Represents the endpoint for retrieving tasks related to a specific project.

    This class is used as a Flask-RESTful resource to handle requests related
    to retrieving tasks for a specific JIRA project.

    Args:
        Resource (type): The base class for implementing Flask-RESTful
        resources.

    Attributes:
        project (str): The name or identifier of the project associated with
        the tasks.
    """

    def get(self, project=None):
        """
        Retrieves tasks associated with a specific project from JIRA.

        Args:
            project (str, optional): The name or identifier of the project. If
            not provided, retrieves tasks for all projects.

        Returns:
            dict: A dictionary containing the retrieved tasks.

        Note:
            This method communicates with JIRA to fetch the tasks.

        Example: DTEDS

        """

        with tracer.start_as_current_span(f"tasks/{project}"):
            try:

                config = app.cdc_config

                jira_client_secret_key = config.get("jira_client_secret_key")
                az_kv_jira_env_var = jira_client_secret_key.replace("-", "_")
                jira_client_secret = os.getenv(az_kv_jira_env_var)
                logger.info(
                    f"jira_client_secret_length:{str(len(jira_client_secret))}")

                if project is None:
                    project = "DTEDS"  # Set your default project value here

                jira_base_url = config.get("jira_base_url")
                api_url = "/rest/api/latest/search"

                url = f"{jira_base_url}{api_url}"

                headers = {
                    "Authorization": f"Bearer {jira_client_secret}",
                    "Content-Type": "application/json"
                }
                logger.info(f"headers:{headers}")

                params = {
                    "jql": f"project = {project} AND issuetype = Task",
                    "fields": ["summary", "status", "assignee"],
                }

                logger.info(f"Retrieving tasks for project {project}")
                logger.info(f"url: {url}")
                logger.info(f"params: {params}")
                response_jira_tasks = requests.get(url,
                                                   headers=headers,
                                                   params=params,
                                                   timeout=TIMEOUT_5_SEC)
                response_jira_tasks_status_code = response_jira_tasks.status_code
                msg = "response_jira_tasks_status_code:"
                msg = msg + f"{response_jira_tasks_status_code}"
                logger.info(msg)
                content_t = response_jira_tasks.content.decode("utf-8")
                response_jira_tasks_content = content_t
                error_message = msg
                if response_jira_tasks_status_code in (200, 201):
                    msg = "response_jira_tasks_content:"
                    msg = msg + f"{response_jira_tasks_content}"
                    logger.info(msg)
                    try:
                        tasks = response_jira_tasks.json()["issues"]
                        logger.info(f"tasks: {tasks}")
                        # Process the retrieved tasks as needed
                        logger_singleton.force_flush()
                        return {"tasks": tasks}
                    except ValueError:
                        msg = f"Failed to retrieve json tasks from url: {url}."
                        msg = msg + f" parms:{params}"
                        msg = msg + "response_jira_tasks_content:"
                        msg = msg + f"{response_jira_tasks_content}"
                        exc_info = sys.exc_info()
                        logger_singleton.error_with_exception(msg, exc_info)
                        logger_singleton.force_flush()
                        return {"error": msg}
                else:
                    msg = f"Failed to retrieve tasks from url:{url}"
                    msg = msg + \
                        f": status_code: {response_jira_tasks.status_code}"
                    msg = msg + ": response_jira_tasks_content:"
                    msg = msg + f"{response_jira_tasks_content}"
                    if response_jira_tasks.status_code == 500:
                        try:
                            error_message = response_jira_tasks.json()[
                                "message"]
                        except ValueError:
                            error_message = "Failed to retrieve json from url:"
                            error_message = error_message + \
                                f"{url}: params: {params}."
                    msg = msg + ": error_message: " + error_message
                    exc_info = sys.exc_info()
                    logger_singleton.error_with_exception(msg, exc_info)
                    logger_singleton.force_flush()
                    return {"error": msg}
            except Exception as ex:
                msg = f"An unexpected error occurred: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(msg, exc_info)
                logger_singleton.force_flush()
                return {"error": f"An unexpected error occurred: {msg}"}


class MetadataJsonFileDownload(Resource):
    """
    A Flask-RESTful resource responsible for downloading metadata JSON files.

    This class handles HTTP requests to the corresponding endpoint. It likely
    implements methods such as GET to handle the downloading of a metadata
    JSON file. Each method corresponds to a standard HTTP method
    (e.g., GET, POST, PUT, DELETE) and carries out a specific operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.
    """

    def get(self, schema_id):
        """
        Retrieves the JSON metadata file from Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            JSON file.

        Returns:
            dict: A dictionary containing the downloaded JSON metadata file.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks): ocio_pade_dev
            Use schema_id 1464 to test Acme Bookstore (Synapse SQL Warehouse): EDAV.alation
        """

        with tracer.start_as_current_span(f"metadata_json_file_download/{schema_id}"):
            try:

                start_time = time.time()  # Record the start time

                config = app.cdc_config

                schema = pade_schema.Schema()
                manifest_json_file = schema.download_schema_manifest_json_file(
                    schema_id, config)

                # Return the file as a download
                file_name = os.path.basename(manifest_json_file)

                end_time = time.time()  # Record the start time

                total_time = end_time - start_time  # Calculate the total time

                # Return the file as a response
                return send_file(manifest_json_file, as_attachment=True, download_name=file_name)

            except Exception as ex:
                msg = f"An unexpected error occurred for download file for schema_id: {schema_id}: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(msg, exc_info)
                logger_singleton.force_flush()
                response = make_response(jsonify({"error": str(ex)}), 500)
                return response


class MetadataExcelFileDownload(Resource):
    """
    A Flask-RESTful resource responsible for handling requests for downloading
    metadata Excel files with a specific schema id.

    This class corresponds to the endpoint
    '/metadata_excel_file_download/<int:schema_id>'.
    It handles HTTP requests that include a specific schema id in the URL, and
    it likely implements methods like GET to manage the download of the
    associated metadata Excel file.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating
        new RESTful resources.
    """

    def get(self, schema_id):
        """
        Retrieves the Excel metadata file from Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            Excel file.

        Returns:
            dict: A dictionary containing the downloaded Excel metadata file.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks): ocio_pade_dev
            Use schema_id 1464 to test Acme Bookstore (Synapse SQL Warehouse): EDAV.alationn
        """

        with tracer.start_as_current_span(f"metadata_excel_file_download/{schema_id}"):
            try:

                start_time = time.time()  # Record the start time

                config = app.cdc_config

                schema = pade_schema.Schema()
                manifest_excel_file = schema.download_schema_manifest_excel_file(
                    schema_id, config)

                # Return the file as a download
                file_name = os.path.basename(manifest_excel_file)
                logger.info(f"file_name:{file_name}")

                end_time = time.time()  # Record the start time

                total_time = end_time - start_time  # Calculate the total time

                # Create the return message with the start, end, and total time
                message = {
                    'start_time': start_time,
                    'end_time': end_time,
                    'total_time': total_time,
                    'data': 'Success'
                }

                mime_type = "application/vnd.openxmlformats"
                mime_type = mime_type + "-officedocument.spreadsheetml.sheet"

                # Return the file as a response
                return send_file(manifest_excel_file, as_attachment=True, download_name=file_name)

            except Exception as ex:
                msg = f"An unexpected error occurred for download file for schema_id: {schema_id}: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(msg, exc_info)
                logger_singleton.force_flush()
                response = make_response(jsonify({"error": str(ex)}), 500)
                return response


class MetadataExcelFileUpload(Resource):
    """
    A Flask-RESTful resource for handling the upload of metadata Excel files.

    This class corresponds to the endpoint '/metadata_excel_file_upload'.
    It handles HTTP requests for uploading metadata Excel files.
    Each method in this class corresponds to a specific HTTP
    method (e.g., POST) and carries out the upload operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.

    Returns:
        Response: The response of the HTTP request after processing the
        uploaded file. The specific content and status code of the response
        will depend on the implementation.
    """

    def post(self):
        """
        Uploads the Excel metadata file to Alation via direct upload based on
        the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            Excel file.

        Returns:
            dict: A dictionary containing the response data.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks): ocio_pade_dev
            Use schema_id 1464 to test Acme Bookstore (Synapse SQL Warehouse): EDAV.alation
        """

        args = upload_parser.parse_args()

        file = args["file"]
        logger.info(f"file: {file}")
        msg = "Metadata_Excel_File_Upload: POST method called successfully."
        return {
            "message": msg
        }


class AzSubscriptionClientSecretVerification(Resource):
    """
    A Flask-RESTful resource for handling the verification of API keys.

    """

    def get(self):
        """
        Verifies the key stored in key vault based on configuration setting: az_kv_az_sub_client_secret_key

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"verify_az_sub_client_secret"):

            config = app.cdc_config
            az_kv_az_sub_client_secret_key = config.get(
                "az_kv_az_sub_client_secret_key")
            az_kv_az_sub_client_secret_key = az_kv_az_sub_client_secret_key.replace(
                "-", "_")
            client_secret = os.getenv(az_kv_az_sub_client_secret_key)
            tenant_id = config.get("tenant_id")
            client_id = config.get("client_id")

            security_core = pade_security_core.SecurityCore()
            status_code, response_content = security_core.verify_az_sub_client_secret(
                tenant_id, client_id, client_secret)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content
            }


class ConnectApiKeyVerification(Resource):
    """
    A Flask-RESTful resource for handling the verification of API keys.

    """

    def get(self):
        """
        Verifies the key stored in key vault based on configuration setting: az_kv_posit_connect_secret_key

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"connect_api_key_verification"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            connect_api_key = get_posit_api_key()
            posit_connect = pade_posit_connect.PositConnect()
            status_code, response_content, api_url = posit_connect.verify_api_key(
                connect_api_key, posit_connect_base_url)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'posit_connect_base_url': posit_connect_base_url,
                'api_url': api_url,
                "connect_api_key": connect_api_key,
                'response_content': response_content
            }


class DeploymentBundle(Resource):
    """
    A Flask-RESTful resource for handling POSIT Deployment Bundle.

    """

    def get(self, content_id, bundle_id):
        """
        Generates DeploymentBundle

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"build_deployment_bundle"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()
            posit_connect = pade_posit_connect.PositConnect()
            status_code, response_content, api_url = posit_connect.build_deployment_bundle(
                connect_api_key, posit_connect_base_url, content_id, bundle_id)

            # Handle the verification logic
            return {
                'posit_connect_base_url': posit_connect_base_url,
                'api_url': api_url,
                'response_content': response_content
            }


class PythonInformation(Resource):
    """
    A Flask-RESTful resource for handling POSIT Python Information.

    """

    def get(self):
        """
        Generates python information about POSIT

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"api_key_verification"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()
            posit_connect = pade_posit_connect.PositConnect()
            status_code, response_content, api_url = posit_connect.get_python_information(
                connect_api_key, posit_connect_base_url)

            # Handle the verification logic
            return {
                'posit_connect_base_url': posit_connect_base_url,
                'api_url': api_url,
                "az_kv_posit_connect_secret_key": az_kv_posit_connect_secret_key,
                'response_content': response_content
            }


class GeneratedManifest(Resource):
    """
    A Flask-RESTful resource for handling POSIT Manifest Generation

    """

    def get(self):
        """
        Generates manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"generate_manifest"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            # Get the full URL
            full_url = request.url
            # Split the URL by '/'
            url_parts = full_url.split('/')
            # Remove the last 2 parts (i.e., the file name or the route)
            url_parts = url_parts[:-2]
            # Join the parts back together
            url_without_filename = '/'.join(url_parts)
            base_url = url_without_filename
            environment = config.get("environment")
            obj_file = pade_env_file.EnvironmentFile()

            app_dir = os.path.dirname(os.path.abspath(__file__))

            manifest_path = (
                app_dir + "/" + environment + "_posit_manifests/"
            )

            swagger_path = (
                app_dir + "/" + environment + "_swagger_manifests/"
            )

            yyyy = str(datetime.now().year)
            dd = str(datetime.now().day).zfill(2)
            mm = str(datetime.now().month).zfill(2)

            json_extension = (
                "_"
                + yyyy
                + "_"
                + mm
                + "_"
                + dd
                + ".json"
            )
            manifest_json_file = manifest_path + "manifest" + json_extension
            # swagger_file = swagger_path + "swagger" + json_extension
            # use cached json file for now
            # having issues downloading
            swagger_file = swagger_path + "swagger_2023_06_22.json"
            connect_api_key = get_posit_api_key()
            requirements_file = app_dir + "/requirements.txt"

            # headers = {
            #     "Authorization": f"Bearer {connect_api_key}",
            # }
            swagger_url = f"{base_url}/swagger.json"
            # response = requests.get(swagger_url, headers=headers)

            # response_data = None
            # error_message = None
            # if response.status_code == 200:  # HTTP status code 200 means "OK"
            #     try:
            #         response_data =  response.json()
            #         response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            #   except requests.HTTPError as http_err:
            #        error_message = f"HTTP error occurred: {http_err}"
            #        soup = BeautifulSoup(response.text, 'html.parser')
            #        error_message = (soup.prettify())
            #    except JSONDecodeError:
            #        error_message = "The response could not be decoded as JSON."
            #        soup = BeautifulSoup(response.text, 'html.parser')
            #        error_message = (soup.prettify())
            #    except Exception as err:
            #        error_message = f"An error occurred: {err}"
            #        error_message = "Response content:"+ response.content.decode()
            # else:
            #    error_message = f"Request failed with status code {response.status_code}"
            # if error_message is not None:
            #    return {
            #        'headers' : headers,
            #        'swagger_url' :  swagger_url,
            #        'manifest_json': "",
            #        'status_message': error_message
            #    }, 500
            # with open(swagger_file, 'w') as f:
            #    f.write(response_data)

            logger.info(f"swagger_file:{swagger_file}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            manifest_json = posit_connect.generate_manifest(
                swagger_file, requirements_file)

            with open(manifest_json_file, 'w') as f:
                f.write(manifest_json)

            # Handle the verification logic
            return {
                'swagger_url': swagger_url,
                'manifest_json': manifest_json,
                'status_message': 'success'
            }


class PublishManifest(Resource):
    """
    A Flask-RESTful resource for handling POSIT Manifest Publication

    """

    def get(self):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"publish_manifest"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            # Get the full URL
            full_url = request.url
            # Split the URL by '/'
            url_parts = full_url.split('/')
            # Remove the last 2 parts (i.e., the file name or the route)
            url_parts = url_parts[:-2]
            # Join the parts back together
            url_without_filename = '/'.join(url_parts)
            base_url = url_without_filename
            environment = config.get("environment")
            obj_file = pade_env_file.EnvironmentFile()

            app_dir = os.path.dirname(os.path.abspath(__file__))

            manifest_path = (
                app_dir + "/" + environment + "_posit_manifests/"
            )

            manifest_json_file = obj_file.get_latest_file(
                manifest_path, "json")

            logger.info(f"manfiest_file:{manifest_json_file}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.publish_manifest(
                connect_api_key, posit_connect_base_url, manifest_json_file)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }


class ContentList(Resource):
    """
    A Flask-RESTful resource for handling POSIT Content Lists

    """

    def get(self):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"list_conent"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.list_content(
                connect_api_key, posit_connect_base_url)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }


class DeploymentBundleList(Resource):
    """
    A Flask-RESTful resource for handling POSIT Bundle Lists

    """

    def get(self, content_id):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"list_conent"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.list_deployment_bundles(
                connect_api_key, posit_connect_base_url, content_id)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }


class TaskStatus(Resource):
    """
    A Flask-RESTful resource for handling POSIT Bundle Lists

    """

    def get(self, task_id):
        """
        Gets Task Status

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"get_task_status"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.get_task_details(
                connect_api_key, posit_connect_base_url, task_id)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

# Define the API description with a hyperlink to the log file page
api.description = API_DESCRIPTION


ns_welcome.add_resource(WelcomeSwagger, '/')
ns_welcome.add_resource(WelcomeSwagger, "/api/swagger")
ns_jira.add_resource(Task, '/tasks/<string:project>')

# This model is used for swagger documentation


ns_alation.add_resource(MetadataJsonFileDownload,
                        "/metadata_json_file_download/<int:schema_id>")
ns_alation.add_resource(MetadataExcelFileDownload,
                        "/metadata_excel_file_download/<int:schema_id>")
ns_alation.add_resource(MetadataExcelFileUpload,
                        "/metadata_excel_file_upload")


class MetadataJsonFileUpload(Resource):
    """
    A Flask-RESTful resource for handling the upload of metadata JSON files.

    This class corresponds to the endpoint '/metadata_json_file_upload'. It
    handles HTTP requests for uploading metadata JSON files.
    Each method in this class corresponds to a specific HTTP
    method (e.g., POST) and carries out the upload operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.

    Returns:
        Response: The response of the HTTP request after processing the
        uploaded file.
        The specific content and status code of the response will depend on
        the implementation.
    """

    @api.expect(upload_parser, validate=True)
    def post(self):
        """Uploads JSON metadata file via direct upload to Alation
        based on schema_id.
        Use 106788 to test OCIO_PADE_DEV (DataBricks)"""

        with tracer.start_as_current_span(f"metadata_json_file_upload"):
            try:
                start_time = time.time()  # Record the start time

                # Get the uploaded file
                args = upload_parser.parse_args()
                file = args['file']
                # Read the contents of the file as JSON
                file_contents = file.read()
                metadata_json_data = json.loads(file_contents)

                schema = pade_schema.Schema()
                config = app.cdc_config

                content_result = schema.upload_schema_manifest_json_file(
                    metadata_json_data, config)

                logger.info(f"content_result: {content_result}")

                end_time = time.time()  # Record the end time

                total_time = end_time - start_time  # Calculate the total time

                # Create the return message with the start, end, and total time
                message = {
                    'start_time': start_time,
                    'end_time': end_time,
                    'total_time': total_time,
                    'data': 'Success'
                }

                response = make_response(jsonify(message), 200)
                return response

            except RequestException as ex:
                msg = f"RequestException occurred: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(msg, exc_info)
                # Create the return message with the start, end, and total time
                message = {
                    'start_time': start_time,
                    'end_time': end_time,
                    'total_time': total_time,
                    'data': msg
                }

                response = make_response(jsonify(message), 500)
                return response


ns_alation.add_resource(MetadataJsonFileUpload,
                        "/metadata_json_file_upload")

ns_posit.add_resource(ConnectApiKeyVerification,
                      "/connect_api_key_verification")
ns_posit.add_resource(PythonInformation, "/python_information")
ns_posit.add_resource(GeneratedManifest, "/generate_manifest")
ns_posit.add_resource(PublishManifest, "/publish_manifest")
ns_posit.add_resource(ContentList, "/list_content")
ns_posit.add_resource(
    DeploymentBundle, "/build_deployment_bundle/<string:content_id>/<string:bundle_id>")
ns_posit.add_resource(DeploymentBundleList,
                      "/list_deployment_bundles/<string:content_id>")
ns_posit.add_resource(TaskStatus, "/get_task_status/<string:task_id>")

ns_cdc_security.add_resource(
    AzSubscriptionClientSecretVerification, "/verify_az_sub_client_secret")


if __name__ == "__main__":
    app.run(debug=True)
