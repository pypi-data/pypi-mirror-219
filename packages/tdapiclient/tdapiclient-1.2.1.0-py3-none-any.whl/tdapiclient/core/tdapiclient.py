# ##################################################################
#
# Copyright 2022 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: pt186002@teradata.com
# Secondary Owner:
#
# This file has definitions for TDApiClient and other related classes
# This classes help users to use Teradata with SageMaker.
# ##################################################################

import glob
import importlib
import logging
import os
import random
import shutil
import string
import tempfile
from cmath import log
import json

import boto3
import pandas as pd
import sagemaker as sg
import teradataml

from azure.mgmt.storage import StorageManagementClient
from azureml.core import Dataset, Experiment, Workspace, Model
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.data.azure_storage_datastore import AzureBlobDatastore
from azure.storage.blob import ContainerClient
from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import AciWebservice, Webservice

from teradataml import DataFrame, save_byom, retrieve_byom, set_byom_catalog, db_drop_table
from teradataml.common.exceptions import TeradataMlException

from tdapiclient.common import logger as tdsglog
from tdapiclient.common.constants import TDApiClientConstants
from tdapiclient.common.exceptions import TDApiClientException
from tdapiclient.common.messagecodes import ErrorInfoCodes, MessageCodes
from tdapiclient.common.messages import Messages
from tdapiclient.utils.validators import _Validators

logger = tdsglog._get_logger()


def create_tdapi_context(type, bucket_path=None, datastore_path=None, datastore_name=None, **options):
    """
    DESCRIPTION:
        Function creates an TDAPI Context to be used for executing TDApiClient
        functions.

        NOTE:
            Before using the module, the following environment variables should be created.

            If using AWS:

            1. AWS_ACCESS_KEY_ID
            2. AWS_SECRET_ACCESS_KEY
            3. AWS_REGION
            4. AWS_SESSION_TOKEN
            5. AWS_DEFAULT_REGION

            AWS_ACCESS_KEY_ID:
                Required Environment Variable.
                Specifies AWS Access Key ID.
                Types: str

            AWS_SECRET_ACCESS_KEY:
                Required Environment Variable.
                Specifies AWS Secret Access Key.
                Types: str

            AWS_REGION:
                Required Environment Variable.
                Specifies AWS Region. If defined,
                this environment variable overrides the values in the
                environment variable AWS_DEFAULT_REGION.
                Types: str

            AWS_SESSION_TOKEN:
                Optional Environment Variable.
                Specifies AWS Session Token.
                Types: str

            AWS_DEFAULT_REGION:
                Optional Environment Variable.
                Specifies Default AWS Region.
                Types: str

            If using Azure:

            1. AZURE_TENANT_ID
            2. AZURE_CLIENT_ID
            3. AZURE_CLIENT_SECRET
            4. AZURE_SUB_ID
            5. AZURE_RG
            6. AZURE_WS
            7. AZURE_REGION

            AZURE_TENANT_ID:
                Required Environment Variable.
                Specifies Azure tenant ID.
                Types: str

            AZURE_CLIENT_ID:
                Required Environment Variable.
                Specifies Azure client ID.
                Types: str

            AZURE_CLIENT_SECRET:
                Required Environment Variable.
                Specifies Azure client key.
                Types: str

            AZURE_SUB_ID:
                Required Environment Variable.
                Specifies Azure subscription ID.
                Types: str

            AZURE_RG:
                Required Environment Variable.
                Specifies Azure resource group.
                Types: str

            AZURE_WS:
                Required Environment Variable.
                Specifies Azure workspace.
                Types: str

            AZURE_REGION:
                Required Environment Variable.
                Specifies Azure region.
                Types: str

            EXAMPLES:
                For Linux or macOS:
                    export AWS_REGION="us-west-2"
                    export AWS_ACCESS_KEY_ID="aws_access_key_id"
                    export AWS_SECRET_ACCESS_KEY="aws_secret_access_key"
                    export AWS_SESSION_TOKEN="aws_session_token"

                For Windows Command Prompt:
                    set AWS_ACCESS_KEY_ID=aws_access_key_id
                    set AWS_SECRET_ACCESS_KEY=aws_secret_access_key
                    set AWS_REGION=us-west-2
                    set AWS_SESSION_TOKEN=aws_session_token

                For PowerShell:
                    $Env:AWS_ACCESS_KEY_ID="aws_access_key_id"
                    $Env:AWS_SECRET_ACCESS_KEY="aws_secret_access_key"
                    $Env:AWS_REGION="us-west-2"
                    $Env:AWS_SESSION_TOKEN="aws_session_token"

    PARAMETERS:
        type:
            Required Argument.
            Specifies cloud type of TDAPI context (example: "aws").
            Types: Str

        bucket_path:
            Required Argument.
            Specifies S3 bucket path.
            Note: Give just the bucket path without leading /s3 or
                  s3:// and s3.amazonaws.com at the back.
            Types: Str
            EXAMPLES:
                If the S3 bucket path is s3://test-bucket/test-folder/
                then just give test-bucket/test-folder.

        datastore_path:
            Required Argument.
            Specifies path in Azure Datastore.
            Types: str

        datastore_name:
            Optional Argument.
            Specifies name of Azure Datastore.
            If not provided, default datastore in Azure workspace will be used.
            Types: str

    RETURNS:
        Instance of TDAPI Context class.

    RAISES:
        TDApiClientException

    EXAMPLES:
        from tdapiclient import create_tdapi_context
        # Create AWS context using "s3_bucket" as parent folder in default bucket.
        create_tdapi_context("aws", bucket_path="s3_bucket")
        # Create Azure ML context using "model_data" as parent folder in default datastore.
        create_tdapi_context("azure", datastore_path="model_data")
    """

    # Below matrix is list of list, where in each row contains following elements:
    # Let's take an example of following, just to get an idea:
    #   [element1, element2, element3, element4, element5, element6]
    #   e.g.
    #       ["join", join, True, (str), True, concat_join_permitted_values]

    #   1. element1 --> Argument Name, a string. ["join" in above example.]
    #   2. element2 --> Argument itself. [join]
    #   3. element3 --> Specifies a flag that mentions argument is optional or not.
    #                   False, means required and True means optional.
    #   4. element4 --> Tuple of accepted types. (str) in above example.
    #   5. element5 --> True, means validate for empty value. Error will be raised, if empty values is passed.
    #                   If not specified, means same as specifying False.
    #   6. element6 --> A list of permitted values, an argument can accept.
    #                   If not specified, it is as good as passing None. If a list is passed, validation will be
    #                   performed for permitted values.

    if type.lower() != "aws" and type.lower() != "azure":
        err_msg = Messages.get_message(
            MessageCodes.UNSUPPORTED_CLOUD_TYPE_FOUND, type)
        error_code = ErrorInfoCodes.UNSUPPORTED_CLOUD_TYPE_FOUND
        raise TDApiClientException(err_msg, error_code)

    awu_matrix = []
    if (type.lower() == "azure"):
        if datastore_name is not None:
            awu_matrix.append(["datastore_name", datastore_name, True, (str), True])
        awu_matrix.append(["datastore_path", datastore_path, False, (str), True])

    if (type.lower() == "aws"):
        awu_matrix.append(["bucket_path", bucket_path, False, (str), True])

    awu_matrix.append(["type", type, False, (str), True])
    # Validate argument types
    _Validators._validate_function_arguments(awu_matrix)

    if "log_level" in options:
        log_level = options["log_level"].lower()
        if log_level == "debug":
            logger.setLevel(logging.DEBUG)
        elif log_level == "info":
            logger.setLevel(logging.INFO)
        elif log_level == "warn":
            logger.setLevel(logging.WARN)
        elif log_level == "error":
            logger.setLevel(logging.ERROR)
        else:
            err_msg = Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE, log_level, "log_level",
                "debug or info or warn or error")
            error_code = ErrorInfoCodes.INVALID_ARG_VALUE
            raise TDApiClientException(err_msg, error_code)
    else:
        if len(options) >= 1:
            err_msg = Messages.get_message(
                MessageCodes.INVALID_KWARG_VALUE, "create_tdapi_context",
                "log_value=warn or error or debug or info")
            error_code = ErrorInfoCodes.INVALID_KWARG_VALUE
            raise TDApiClientException(err_msg, error_code)

    if type.lower() == "aws":
        return _TDApiAwsContext(bucket_path)
    if type.lower() == "azure":
        return _TDApiAzureContext(datastore_path, datastore_name)


def remove_tdapi_context(tdapi_context, delete_byom_models=False, table_name="", schema_name=None):
    """
    DESCRIPTION:
        Function removes a specified TDAPI Context.
        For AWS Sagemaker, it removes any S3 folder created during operations of TDApiClient.
        For Azure ML, it removes all blobs created during operations of TDApiClient.
        Optionally deletes the database table containing BYOM models.

    PARAMETERS:
        tdapi_context:
            Required Argument.
            Specifies the TDAPI Context which needs to be removed.
            Types: TDAPI Context class

        delete_byom_models:
            Optional Argument.
            Specifies whether the table containing BYOM models should be deleted.
            Default value: False
            Types: bool

        table_name:
            Optional Argument.
            Specifies the name of the table containing BYOM models to be deleted.
            Default value: ""
            Types: str

        schema_name:
            Optional Argument.
            Specifies schema of the table to be dropped.
            If schema is not specified, function drops table from the current database.
            Default value: None
            Types: str

    RETURNS:
        None

    RAISES:
        TDApiClientException

    EXAMPLES:
        from tdapiclient import create_tdapi_context, remove_tdapi_context
        # Create AWS context using "s3_bucket" as parent folder in default bucket.
        context = create_tdapi_context("aws", bucket_path="s3_bucket")
        remove_tdapi_context(context)
        # Create Azure ML context using "model_data" as parent folder in default datastore.
        context = create_tdapi_context("azure", datastore_path="model_data")
        remove_tdapi_context(context)
    """
    awu_matrix = []
    awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
    # Validate argument types
    _Validators._validate_function_arguments(awu_matrix)

    if (isinstance(tdapi_context, _TDApiAwsContext)):
        try:
            _remove_s3_folders(tdapi_context, tdapi_context._s3_prefixes)
        except Exception as ex:
            tdapi_context._access_id = None
            tdapi_context._access_key = None
            tdapi_context._session_token = None
            tdapi_context._bucket_path = None
            msg = Messages.get_message(MessageCodes.TDSG_S3_ERROR, str(ex))
            error_code = ErrorInfoCodes.TDSG_S3_ERROR
            raise TDApiClientException(msg, error_code) from ex
        finally:
            tdapi_context._access_id = None
            tdapi_context._access_key = None
            tdapi_context._session_token = None
            tdapi_context._bucket_path = None

    if isinstance(tdapi_context, _TDApiAzureContext):
        try:
            credential = ServicePrincipalAuthentication(
                                tdapi_context._tenant_id,
                                tdapi_context._client_id,
                                tdapi_context._client_secret)
            workspace = Workspace(tdapi_context._sub_id,
                                  tdapi_context._rg,
                                  tdapi_context._ws, auth=credential)
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.AZ_WORKSPACE_ACCESS_ISSUE)
            msg = msg.format(tdapi_context._rg)
            error_code = ErrorInfoCodes.AZ_WORKSPACE_ACCESS_ISSUE
            raise TDApiClientException(msg, error_code) from ex

        # Not possible to unregister datasets through Azure ML SDK v1

        datastore = workspace.get_default_datastore()
        container_uri = f"https://{datastore.account_name}.blob.core.windows.net/{datastore.container_name}"
        container_client = ContainerClient.from_container_url(container_uri, credential=datastore.account_key)

        for prefix in tdapi_context._datastore_prefixes:
            blobs = container_client.list_blobs(name_starts_with=prefix)
            container_client.delete_blobs(*blobs)

        if delete_byom_models:
            if table_name:
                db_drop_table(table_name, schema_name=schema_name)
            else:
                msg = Messages.get_message(MessageCodes.MISSING_ARGS)
                msg = msg.format("table_name")
                error_code = ErrorInfoCodes.MISSING_ARGS
                raise TDApiClientException(msg, error_code)

def _remove_s3_folders(tdapi_context, s3_prefix_list):
    """
    DESCRIPTION:
        A private method to remove S3 folders using credentials provided
        in TDAPI Context.

    PARAMETERS:
        tdapi_context:
            Required Argument.
            Specifies the TDAPI Context which holds the AWS credentials.
            Types: TDAPI Context Class

        s3_prefix_list:
            Required Argument.
            Specifies the list of s3 prefixes to be deleted.
            Note:
                These prefixes are searched in the bucket specified by the
                tdapi_context.
            Types: List of s3 prefixes of type Str

    RETURNS:
        None

    RAISES:
        AWS service exceptions or botocore.exception

    EXAMPLES:
        from tdapiclient import create_tdapi_context, remove_tdapi_contex
        context = create_tdapi_context("s3_bucket")
        s3_prefix_list = ["test-s3-path/"]
        _remove_s3_folders(context, s3_prefix_list)
    """
    awu_matrix = []
    awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
    awu_matrix.append(["s3_prefix_list", s3_prefix_list, False, (list), False])
    # Validate argument types
    _Validators._validate_function_arguments(awu_matrix)
    s3 = boto3.resource("s3", aws_access_key_id=tdapi_context._access_id,
                        aws_secret_access_key=tdapi_context._access_key,
                        aws_session_token=tdapi_context._session_token,
                        region_name=tdapi_context._aws_region)
    bucket_name = tdapi_context._s3_bucket_name
    bucket = s3.Bucket(bucket_name)
    for s3_prefix in s3_prefix_list:
        bucket.objects.filter(Prefix=s3_prefix).delete()


class TDApiClient:
    """
    TDApiClient class in case of AWS SageMaker is used to create SageMaker estimator class which in turn
    can be used to create SageMaker predictor. SageMaker estimator class
    can take input data from teradataml DataFrame for training the model. And
    SageMaker predictor can use Teradata tables or queries (using teradataml
    DataFrame) for scoring.

    TDApiClient class in case of Azure-ML is used to create Azure-ML RunConfig
    class. This class can be configured with teradataml DataFrame as the input and start the training operation
    using 'fit' method and deploy the trained model either in azure-ml OR in Vantage using 'deploy' method.
    """

    def __init__(self, tdapi_context):
        """
        DESCRIPTION:
            Initializer for TDApiClient.

        PARAMETERS:
            tdapi_context:
                Required Argument.
                Specifies an instance of TDAPI Context created using
                create_tdapi_context to be used with TDApiClient.
                Types: TDAPI Context

       RETURNS:
            Returns an instance of TDApiClient.

        EXAMPLES:
            from TDApiClient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "s3_bucket")
            TDApiClient = TDApiClient(context)

        RAISES:
            None
        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        self._tdapi_context: _TDApiContext = tdapi_context

    def __getattr__(self, name):
        def __sgClassFinder(*c, **kwargs):
            sagemaker_module_list = TDApiClientConstants.SG_MODULE_LIST.value
            for module in sagemaker_module_list:
                lib_object = importlib.import_module(module)
                try:
                    logger.debug(
                        "Searching for '{}' class in module '{}'.".format(
                            name, module))
                    class_instance = getattr(lib_object, name)
                    logger.debug("Found '{}' class in module '{}'.".format(
                        name, module))
                except Exception:
                    continue
                set_sg_session = False
                if "sagemaker_session" in kwargs:
                    if kwargs["sagemaker_session"] is None:
                        set_sg_session = True
                else:
                    set_sg_session = True

                if class_instance.__module__ == "sagemaker.image_uris":
                    return class_instance(*c, **kwargs)

                if set_sg_session:
                    session = boto3.Session(
                        aws_access_key_id=self._tdapi_context._access_id,
                        aws_secret_access_key=self._tdapi_context._access_key,
                        aws_session_token=self._tdapi_context._session_token,
                        region_name=self._tdapi_context._aws_region)
                    sagemaker_session = sg.Session(boto_session=session)
                    kwargs["sagemaker_session"] = sagemaker_session
                    logger.debug("Created new sagemaker_session object "
                                 + "and passed it to '{}''s constructor.".format(
                                     name))
                sg_object = class_instance(*c, **kwargs)
                return _TDSagemakerObjectWrapper(sg_object, self._tdapi_context)
            error_code = ErrorInfoCodes.SG_CLASS_NOT_FOUND
            msg = Messages.get_message(MessageCodes.SG_CLASS_NOT_FOUND, name)
            raise TDApiClientException(msg, error_code)

        def __azClassFinder(*c, **kwargs):
            azureml_module_list = TDApiClientConstants.AZ_MODULE_LIST.value
            for module in azureml_module_list:
                lib_object = importlib.import_module(module)
                try:
                    logger.debug(
                        f"Searching for '{name}' class in module '{module}'.")
                    class_instance = getattr(lib_object, name)
                    logger.debug(f"Found '{name}' class in module '{module}'.")
                except Exception:
                    continue
                return _TDAzureObjectWrapper(class_instance, c, kwargs, self._tdapi_context)
            error_code = ErrorInfoCodes.AZ_CLASS_NOT_FOUND
            msg = Messages.get_message(MessageCodes.AZ_CLASS_NOT_FOUND, name)
            raise TDApiClientException(msg, error_code)

        if isinstance(self._tdapi_context, _TDApiAwsContext):
            return __sgClassFinder
        if isinstance(self._tdapi_context, _TDApiAzureContext):
            return __azClassFinder
        
    @staticmethod
    def API_Request(dataframe: DataFrame, api_type, authorization, **options):
        """
        DESCRIPTION:
            A static helper function to invoke in-db function API_Request.

        PARAMETERS:
            dataframe:
                Required Argument.
                Specifies input teradataml DataFrame which will act as
                input query for API_Request UDF.
                Types: DataFrame

            api_type:
                Required Argument.
                Specifies an API_Type argument for API_Request UDF.
                Types: str

            authorization:
                Required Argument.
                Represents AUTHORIZTION parameter in API_Request UDF
                Types: str in json format.

            options:
                Optional Argument.
                Specifies key-value arguments to be passed to API_Request UDF.
                Mapping between key-value arguments to UDF arguments is as follows.

                content_type:
                    Optional Argument.
                    Represents CONTENT_TYPE parameter in API_Request UDF
                    Default Value: csv
                    Types: str

                key_start_index:
                    Optional Argument.
                    Represents KEY_START_INDEX parameter in API_Request UDF
                    Default Value: 0
                    Types: int

                endpoint:
                    Optional Argument.
                    Represents ENDPOINT parameter in API_Request UDF
                    Default Value: ""
                    Types: str

                text_column:
                    Optional Argument.
                    Represents TEXT_COLUMN parameter in API_Request UDF
                    Default Value: ""
                    Types: int

       RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            from TDApiClient import TDApiClient

            auth_info_fmt_str = ('{{ "Access_ID": "{}", "Access_Key": '
                                 + '"{}", "Region" : "{}"}}')
            auth_info = auth_info_fmt_str.format(access_id, access_key,
                                                 aws_region)
            df = TDApiClient.API_Request(reviews_df, "aws-sagemaker",
                                 authorization=auth_info,
                                 endpoint='td-sagemaker-xgboost',
                                 key_start_index=1)
        """
        content_type = options.get("content_type", "csv")
        key_start_index = options.get("key_start_index", 0)
        text_column = options.get("text_column", "")
        endpoint = options.get("endpoint", "")

        arg_info_matrix = []
        arg_info_matrix.append(["dataframe", dataframe, False, (DataFrame), True])
        arg_info_matrix.append(["api_type", api_type, False, (str), True])
        arg_info_matrix.append(["authorization", authorization, False, (str), True])
        arg_info_matrix.append(["content_type", content_type, True, (str), True])
        arg_info_matrix.append(["key_start_index", key_start_index, True, (int), True])
        arg_info_matrix.append(["text_column", text_column, True, (str), False])
        arg_info_matrix.append(["endpoint", endpoint, True, (str), False])

        # Validate argument types
        _Validators._validate_function_arguments(arg_info_matrix)
        input_query = dataframe.show_query(True)

        udf_name = "tapidb.API_Request"
        udf_query = ("SELECT * FROM {}( ON ({}) USING AUTHORIZATION('{}')"
                     + " API_TYPE('{}') ENDPOINT('{}') "
                     + " CONTENT_TYPE('{}') KEY_START_INDEX('{}') TEXT_COLUMN('{}') ) "
                     "as \"DT\" ")
        udf_query = udf_query.format(udf_name, input_query, authorization,
                                     api_type, endpoint, content_type,
                                     key_start_index, text_column)
        return DataFrame.from_query(query=udf_query)


class _TDApiContext:
    """
    This is a class for holding TDAPI Context information. This is used while
    creating TDApiClient object. Based on cloud type, it may be of type AWS
    or Azure or GCP.
    """

    def __init__(self):
        """
        DESCRIPTION:
            An initializer for _TDApiContext.

        RETURNS:
            Instance of TDAPI Context class.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = _TDApiContext()
        """


class _TDApiAwsContext(_TDApiContext):
    """
    This is a class for holding TDAPI Context information. This is used while
    creating TDApiClient object. This class is used in case of AWS Sagemaker
    related operation.
    """

    def __init__(self, bucket_path):
        """
        DESCRIPTION:
            An initializer for _TDApiAwsContext.

        PARAMETERS:
            bucket_path:
                Required Argument.
                Specifies S3 bucket path.
                Note: Give just the bucket path without leading /s3 or
                    s3:// and s3.amazonaws.com at the back.
                Types: Str
                EXAMPLES:
                    If the S3 bucket path is s3://test-bucket/test-folder/
                    then just give test-bucket/test-folder.

        RETURNS:
            Instance of TDAPI AWS Context class.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = _TDApiAwsContext("s3_bucket")
        """
        super().__init__()
        awu_matrix = []
        awu_matrix.append(["bucket_path", bucket_path, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if "AWS_REGION" in os.environ:
            self._aws_region = os.environ["AWS_REGION"]
        else:
            self._aws_region = os.environ["AWS_DEFAULT_REGION"]

        if bucket_path.endswith("/"):
            bucket_path = bucket_path[:-1]
        s3_bucket_name = bucket_path.split("/")[0]
        s3_bucket_folder = ""
        s3_bucket_folder = bucket_path.split(s3_bucket_name, 1)[1]
        if s3_bucket_folder.startswith("/"):
            s3_bucket_folder = s3_bucket_folder[1:]
        self._s3_bucket_name = s3_bucket_name
        self._s3_bucket_folder = s3_bucket_folder
        self._bucket_path = "/s3/{}.s3.amazonaws.com/{}".format(s3_bucket_name, s3_bucket_folder)
        logger.debug("Generated bucket name in write_nos format is {}".format(
            self._bucket_path))

        if "AWS_ACCESS_KEY_ID" in os.environ:
            self._access_id = os.environ["AWS_ACCESS_KEY_ID"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AWS_ACCESS_KEY_ID")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AWS_SECRET_ACCESS_KEY" in os.environ:
            self._access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AWS_SECRET_ACCESS_KEY")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        self._session_token = ""  # Default value for session token
        if "AWS_SESSION_TOKEN" in os.environ:
            self._session_token = os.environ["AWS_SESSION_TOKEN"]

        self._s3_prefixes = []


class _TDApiAzureContext(_TDApiContext):
    """
    This is a class for holding TDAPI Context information. This is used while
    creating TDApiClient object. This class is used in case of Azure ML
    related operation.
    """

    def __init__(self, datastore_path, datastore_name):
        """
        DESCRIPTION:
            An initializer for _TDApiAzureContext.

        PARAMETERS:

        RETURNS:
            Instance of TDAPI Azure Context class.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = _TDApiAzureContext("azure_datastore")
        """
        super().__init__()
        awu_matrix = []
        awu_matrix.append(["datastore_path", datastore_path, False, (str), True])
        if datastore_name is not None:
            awu_matrix.append(["datastore_name", datastore_name, True, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        self._datastore_path = datastore_path
        if datastore_name is not None:
            self._datastore_name = datastore_name

        self._datastore_path = self._datastore_path.strip("/")

        if "AZURE_TENANT_ID" in os.environ:
            self._tenant_id = os.environ["AZURE_TENANT_ID"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AZURE_TENANT_ID")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AZURE_CLIENT_ID" in os.environ:
            self._client_id = os.environ["AZURE_CLIENT_ID"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AZURE_CLIENT_ID")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AZURE_CLIENT_SECRET" in os.environ:
            self._client_secret = os.environ["AZURE_CLIENT_SECRET"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AZURE_CLIENT_SECRET")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AZURE_SUB_ID" in os.environ:
            self._sub_id = os.environ["AZURE_SUB_ID"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AZURE_SUB_ID")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AZURE_RG" in os.environ:
            self._rg = os.environ["AZURE_RG"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AZURE_RG")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AZURE_WS" in os.environ:
            self._ws = os.environ["AZURE_WS"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AZURE_WS")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AZURE_REGION" in os.environ:
            self._azure_region = os.environ["AZURE_REGION"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AZURE_REGION")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        self._datastore_prefixes = []


class _TDCloudObjectWrapper:
    """
    This is an interface for holding cloud object information. This is used when
    invoking a method from the chosen cloud API. Based on cloud type, it may
    be of type AWS or Azure or GCP.
    """

    def __init__(self):
        """
        DESCRIPTION:
            An initializer for _TDCloudObjectWrapper.

        RETURNS:
            Instance of Cloud Object Wrapper class.

        RAISES:
            None
        """
        pass

    def fit(self):
        """
        DESCRIPTION:
            Method used to train a model.

        RETURNS:
            Instance of cloud API object.

        RAISES:
            None
        """
        pass

    def deploy(self):
        """
        DESCRIPTION:
            Method used to deploy a model.

        RETURNS:
            Instance of TDApiClient Predictor class.

        RAISES:
            None
        """
        pass

    def __getattr__(self, name):
        """
        DESCRIPTION:
            A private method used to invoke a method from chosen cloud API.

        RETURNS:
            Instance of object from cloud API.

        RAISES:
            None
        """
        if self.cloudObj is None:
            return None

        def __cloud_method_invoker(*c, **kwargs):
            return atrribute_instance(*c, **kwargs)

        atrribute_instance = getattr(self.cloudObj, name)
        if callable(atrribute_instance):
            return __cloud_method_invoker
        return atrribute_instance


class _TDAzureObjectWrapper(_TDCloudObjectWrapper):
    """
        This class is a wrapper over Azure ML RunConfig classes, it provides
        a way for integration with Teradata in following ways
        1. It introduces fit method which can be used to train on azure-ml using
           Teradata Dataframes
        2. It also introduces deploy method which can be used to deploy trained
           models on azure-ml OR on teradata database using BYOM solution.
    """

    def __init__(self, class_instance, pargs, kwargs, tdapi_context) -> None:
        """
        DESCRIPTION:
            This method is used for creating objects of _TDAzureObjectWrapper.
            This class is used internally by tdapiclient library to wrap Azure ML
            classes.

        PARAMETERS:
            class_instance:
                Required Argument.
                Specifies the instance of user specified Azure ML RunConfig class.
                Types: Varies as per user specified Azure ML class.

            pargs:
                Required Argument.
                Specifies the positional arguments required to instantiate
                Azure ML class using class instance parameter.
                Types: Positional argument list

            kwargs:
                Required Argument.
                Specifies the key-value arguments required to instantiate
                Azure ML class using class instance parameter.
                Types: Key-Value argument list

            tdapi_context:
                Required Argument.
                Specifies the TDApiContext representing Azure ML Credentials.
                Types: _TDApiContext

        RETURNS:
            _TDAzureObjectWrapper

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            # Script run config takes all the parameters as
            # required by azure-ml script run config
            skLearnObject = tdapiclient.ScriptRunConfig() # This call refers to _init_ call above.

        RAISES:
            TeradataMlException
            TDApiClientException
        """

        self._class_instance = class_instance
        self._pargs = pargs
        self._kwargs = kwargs
        self.cloudObj = None
        self._tdapi_context: _TDApiAzureContext = tdapi_context

    def fit(self, content_type='parquet', mount=True, wait=True):
        """
        DESCRIPTION:
            Execute Azure ML training API with teradataml DataFrame as input.

            This method exports teradataml dataframe objected present in
            RunConfig's parameters to Azure ML datastore, wraps it in DataSet
            and then create Azure ML Experiment based on RunConfig's paramter
            and submit it to workspace.

        PARAMETERS:
            content_type:
                Optional Argument.
                Specifies content type for inputs.
                Supported formats for azure-ml dataset object: parquet, csv
                Default Value: parquet
                Types: Str

            mount:
                Optional Argument.
                Specifies whether input data frame is to be exported as mount
                point or just plain azure ml DatSet.
                Default Value: True
                Types: Boolean

            wait:
                Optional Argument.
                Specifies whether the function should wait for experiement to
                finish.
                Default Value: True
                Types: Boolean

        RETURNS:
            Azure ML Run Object

        RAISES:
            TeradataMlException
            TDApiClientException

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            # Script run config takes all the parameters as
            # required by azure-ml script run config
            skLearnObject = tdapiclient.ScriptRunConfig()
            train = DataFrame(tableName='train_data')
            skLearnObject.fit(mount=True)

        """
        try:
            credential = ServicePrincipalAuthentication(
                                self._tdapi_context._tenant_id,
                                self._tdapi_context._client_id,
                                self._tdapi_context._client_secret)
            workspace = Workspace(self._tdapi_context._sub_id,
                                  self._tdapi_context._rg,
                                  self._tdapi_context._ws, auth=credential)
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.AZ_WORKSPACE_ACCESS_ISSUE)
            msg = msg.format(self._tdapi_context._rg)
            error_code = ErrorInfoCodes.AZ_WORKSPACE_ACCESS_ISSUE
            raise TDApiClientException(msg, error_code) from ex

        for i in range(0, len(self._pargs)):
            logger.debug(self._pargs[i])
            if isinstance(self._pargs[i], DataFrame):
                self._pargs[i] = self.__convert_df_to_az_dataset_mount(
                                    self._pargs[i], workspace, credential, content_type, mount)
                logger.info(f"Replaced position arg dataframe object with mount point {self._pargs[i]}")
        for key in self._kwargs:
            value = self._kwargs[key]
            logger.debug(f"Key={key}, Value={value}, Type={type(value)}")
            if isinstance(value, DataFrame):
                self._kwargs[key] = self.__convert_df_to_az_dataset_mount(
                                        value, workspace, credential, content_type, mount)
                logger.info(f"Replaced kw arg dataframe object with mount point or dataset {self._kwargs[key]}")
            if isinstance(value, list):
                new_list = []
                for v in value:
                    if isinstance(v, DataFrame):
                        data_mount = self.__convert_df_to_az_dataset_mount(
                                            v, workspace, credential, content_type, mount)
                        logger.info(f"Replaced kw arg dataframe object with mount point {data_mount}")
                        new_list.append(data_mount)
                    else:
                        new_list.append(v)
                self._kwargs[key] = new_list

        self.cloudObj = self._class_instance(*self._pargs, **self._kwargs)
        experiment_name = 'tdapi_experiment'
        experiment = Experiment(workspace=workspace, name=experiment_name)

        run = experiment.submit(config=self.cloudObj)
        if wait:
            run.wait_for_completion(show_output=True)
        return run

    def __convert_df_to_az_dataset_mount(self, input, ws, credential, content_type, mount=True):
        """
        DESCRIPTION:
            Converts teradataml dataframe into azure ml dataset object by
            uploading dataframe content to Azure ML workspace's default blob store.

        PARAMETERS:
            input:
                Required Argument.
                Specifies teradataml dataframe to be exported to azure ml.
                Types: teradataml DataFrame

            ws:
                Required Argument.
                Specifies azure ml workspace. Workspace is used for selecting
                blob storage to put dataframe content and also registering dataset later.
                Types: Workspace

            credential:
                Required Argument.
                Specifies azure ml credential object to be used for
                connecting to azure.
                Types: ServicePrincipalAuthentication

            content_type:
                Required Argument.
                Specifies the content type to be used while creating azure ml
                dataset.
                Types: Str

            mount:
                Required Argument.
                Specifies whether dataset object should be given as a mount
                point OR just plain dataset.
                Default Value: True
                Types: Boolean


        RETURNS:
            Azure ML Run Object

        RAISES:
            TeradataMlException
            TDApiClientException

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            # Script run config takes all the parameters as
            # required by azure-ml script run config
            skLearnObject = tdapiclient.ScriptRunConfig()
            train = DataFrame(tableName='train_data')
            skLearnObject.fit(mount=True)

        """
        datastore = ws.get_default_datastore()

        if not isinstance(datastore, AzureBlobDatastore):
            msg = Messages.get_message(MessageCodes.AZ_INVALID_DATASTORE)
            error_code = ErrorInfoCodes.AZ_INVALID_DATASTORE
            raise TDApiClientException(msg, error_code)

        storage_name = datastore.account_name
        try:
            storage_client = StorageManagementClient(credential, self._tdapi_context._sub_id)
            storage_keys = storage_client.storage_accounts.list_keys(self._tdapi_context._rg, storage_name)
            storage_keys = {v.key_name: v.value for v in storage_keys.keys}

            from teradataml import WriteNOS
            auth_info = f'{{"Access_ID" : "{storage_name}", "Access_Key" : "{storage_keys["key1"]}"}}'
            datastore_path = f"{datastore.container_name}/{self._tdapi_context._datastore_path}"
            az_folder_name = 'tdaz-{}'.format(
                ''.join(random.choices(string.ascii_lowercase, k=10)))
            self._tdapi_context._datastore_prefixes.append(f"{self._tdapi_context._datastore_path}/{az_folder_name}/")

            storage_path = f"/az/{storage_name}.blob.core.windows.net/{datastore_path}/{az_folder_name}/"
            storedAs = "parquet"
            obj = WriteNOS(data=input, location=storage_path, authorization=auth_info, stored_as=storedAs)
            writenos_df = obj.result.to_pandas(all_rows=True)
            object_list = []
            datastore_object_list = []
            logger.info("Exported input dataframe to azure on following path")
            for row in writenos_df["ObjectName"]:
                logger.info(f"Path: {row}")
                row = row[row.find(f"/{self._tdapi_context._datastore_path}/{az_folder_name}"):]
                object_list.append(row)
                datastore_object_list.append((datastore, row))
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.WRITE_NOS_ERROR)
            msg = msg.format("azure blob store")
            error_code = ErrorInfoCodes.WRITE_NOS_ERROR
            raise TDApiClientException(msg, error_code) from ex

        try:
            dataset = Dataset.Tabular.from_parquet_files(path=datastore_object_list)
            dataset.register(ws, name=az_folder_name,
                             description='tdapi azure table data')
            logger.info(f"Created dataset {dataset} and registered in workspace")
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.AZ_ERROR_CREATING_OR_REGISTERING_DS)
            error_code = ErrorInfoCodes.AZ_ERROR_CREATING_OR_REGISTERING_DS
            raise TDApiClientException(msg, error_code) from ex

        if mount:
            if content_type == "csv":
                return dataset.to_csv_files().as_named_input('tdaz_input').as_mount()
            elif content_type == "parquet":
                return dataset.to_parquet_files().as_named_input('tdaz_input').as_mount()
            else:
                msg = Messages.get_message(MessageCodes.AZ_UNSUPPORTED_CONTENT_TYPE)
                msg = msg.format(content_type, "csv or parquet")
                error_code = ErrorInfoCodes.AZ_UNSUPPORTED_CONTENT_TYPE
                raise TDApiClientException(msg, error_code)
        else:
            return dataset

    def deploy(
        self, model: Model, model_type, platform,
        model_id="", save_byom_kwargs={}, retrieve_byom_kwargs={}, model_deploy_kwargs={}):
        """
        DESCRIPTION:
            Deploy given Azure ML model to Vantage.

            This method downloads the given model from Azure ML and saves it in Vantage.

        PARAMETERS:
            model:
                Required Argument.
                Specifies Azure ML model.
                Types: azureml.core.Model

            model_type:
                Required Argument.
                Specifies the type of the model.
                Accepted values: "pmml", "onnx", "h2o".
                Types: String (str)

            platform:
                Required Argument.
                Specifies platform to which the given model will be deployed.
                Accepted values: "vantage", "az-webservice".
                Types: String (str)

            model_id:
                Optional Argument.
                Specifies the id of the model for Teradata table.
                If no value is given, the id of the given Azure ML model will be used.
                Types: String (str)

            save_byom_kwargs:
                Optional Argument.
                Specifies the keyword arguments of teradataml save_byom() function.
                If neither table_name is provided nor BYOM catalog set using set_byom_catalog,
                a table with name "tdapiclient_byom_models" will be created in the current schema.
                Types: Dictionary (dict)

            retrieve_byom_kwargs:
                Optional Argument.
                Specifies the keyword arguments of teradataml retrieve_byom() function.
                Types: Dictionary (dict)

            model_deploy_kwargs:
                Optional Argument.
                Specifies the keyword arguments to deploy the Azure ML webservice.
                Types: Dictionary (dict).

        RETURNS:
            Instance of _BYOMPredictor.
            Instance of TDAzurePredictor.

        RAISES:
            TeradataMlException
            TDApiClientException

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            # ScriptRunConfig takes all the parameters as
            # required by Azure ML ScriptRunConfig.
            train = DataFrame(tableName='train_data')
            skLearnObject = tdapiclient.ScriptRunConfig(arguments=[train])
            # Train the model in Azure ML.
            run = skLearnObject.fit(mount=True)
            # Register model in Azure ML.
            model = run.register_model(model_name='example', model_path='outputs/example.pmml')
            # Deploy model to Vantage.
            model_predictor = skLearnObject.deploy(model, platform="vantage")
            model_predictor = skLearnObject.deploy(model, platform="az-webservice")
        """

        if platform.lower() == "vantage":

            if model_type.lower() in ["pmml", "onnx", "h2o"]:
                model_dir = tempfile.TemporaryDirectory()
                model_path = model.download(target_dir=model_dir.name)
                model_format = model_path.split(".")[-1]

                if model_format in ["pmml", "onnx", "zip"]:
                    id = model_id if model_id else model.id

                    try:
                        save_byom(id, model_path, **save_byom_kwargs)
                    except ValueError:
                        save_byom(id, model_path, table_name="tdapiclient_byom_models", **save_byom_kwargs)
                        set_byom_catalog("tdapiclient_byom_models")

                    model_df = retrieve_byom(id, **retrieve_byom_kwargs)
                    return _BYOMPredictor(model_df, model_type)

            msg = Messages.get_message(MessageCodes.UNSUPPORTED_MODEL_TYPE)
            error_code = ErrorInfoCodes.UNSUPPORTED_MODEL_TYPE
            raise TDApiClientException(msg, error_code)

        if platform.lower() == "az-webservice":
            try:
                predictor_object = Model.deploy(**model_deploy_kwargs)
                return TDAzurePredictor(predictor_object, self._tdapi_context)
            except Exception as ex:
                error_code = ErrorInfoCodes.AZ_DEPLOY_ERROR
                msg = Messages.get_message(MessageCodes.AZ_DEPLOY_ERROR, ex)
                raise TDApiClientException(msg, error_code) from ex


class _TDSagemakerObjectWrapper(_TDCloudObjectWrapper):
    """
        This class is a wrapper over SageMaker Estimator class, which provides
        a way for integration between estimator class and Teradata
        in following ways:
        1. For fit method, user can specify teradataml DataFrame objects to
           specify input for training.
        2. For deploy method, it returns predictor object which provides option
           for in-db prediction.
    """

    def __init__(self, sageObj, tdapi_context) -> None:
        """
        DESCRIPTION:
            Initializer for _TDSagemakerObjectWrapper.

        PARAMETERS:
            sageObj:
                Required Argument.
                Specifies instance of SageMaker estimator class.
                Types: SageMaker Estimator instance

            tdapi_context:
                Required Argument.
                Specifies instance of TDAPI Context class.
                Types: TDAPI Context

        RETURNS:
            A _TDSagemakerObjectWrapper instance.

        RAISES:
            None

        EXAMPLES:
            # This class is created by the library in following
            # type of operation.

            context = create_tdapi_context("s3_bucket")
            tdapiclient = TDApiClient(context)
            # SKlearn takes all parameters that AWS SageMaker Library requires
            skLearnObject = tdapiclient.SKLearn()
            # skLearnObject will be of type _TDSagemakerObjectWrapper

        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        awu_matrix.append(["sageObj", sageObj, False, (object), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        self.cloudObj = sageObj
        self._tdapi_context: _TDApiContext = tdapi_context

    def fit(self, inputs, content_type='csv', convert_at_local_node=False, **sg_kw_args):
        """
        DESCRIPTION:
            Execute SageMaker.fit method using the teradataml DataFrame as
            source for training.

        PARAMETERS:
            inputs:
                Required Argument.
                Specifies a teradataml Dataframe or S3 path as a string.
                Types: Can be one of the following
                       1. Single object of teradataml DataFrame
                       2. String
                       3. Dict of string to object of teradataml Dataframe

            content_type:
                Optional Argument.
                Specifies content type for inputs.
                Default Value: CSV
                Types: Str

            convert_at_local_node:
                Optional Argument.
                Specifies whether to automatically download parquet data from S3,
                convert it to json at client, and upload the result to S3.
                Ignored when content_type is not JSON.
                Default Value: False
                Types: Bool

            **sg_args:
                Optional Argument.
                Specifies any additional argument required for SageMaker.fit.
                These parameters are directly supplied to SageMaker.fit method.
                Types: Multiple

        RETURNS:
            SageMaker.fit's return value.

        EXAMPLES:
            from tdapiclient import create_tdapi_context,TDApiClient
            context = create_tdapi_context("s3_bucket")
            tdapiclient = TDApiClient(context)
            # SKlearn takes all parameters that AWS SageMaker Library requires
            skLearnObject = tdapiclient.SKLearn()
            train = DataFrame(tableName='train_data')
            test = DataFrame(tableName='test_data')
            skLearnObject.fit(inputs={'train': train, 'test': test},
                              content_type='csv', wait=False)

        RAISES:
            TeradataMlException
            TDApiClientException
        """
        awu_matrix = []
        awu_matrix.append(["content_type", content_type, True, (str), False])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if content_type == "json" and not convert_at_local_node:
            msg = Messages.get_message(MessageCodes.DATA_FORMAT_CONVERSION_ERROR)
            error_code = ErrorInfoCodes.DATA_FORMAT_CONVERSION_ERROR
            raise TDApiClientException(msg, error_code)

        updated_inputs = inputs
        if isinstance(inputs, dict):
            for inputName, object in inputs.items():
                if isinstance(object, DataFrame):
                    newObj = self.__get_s3_address_for_df(object, content_type)
                    inputs[inputName] = sg.TrainingInput(newObj, content_type=content_type)
        if isinstance(inputs, DataFrame):
            newObj = self.__get_s3_address_for_df(inputs, content_type)
            updated_inputs = sg.TrainingInput(newObj, content_type=content_type)
        # TODO: modify logging, access S3 URI from TrainingInput
        # logger.info("Updated input is : {}".format(updated_inputs))
        method_instance = getattr(self.cloudObj, self.fit.__name__)
        try:
            return method_instance(updated_inputs, **sg_kw_args)
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex

    def __get_s3_address_for_df(self, input: DataFrame, content_type):
        """
        DESCRIPTION:
            Private method to convert the teradataml DataFrame to S3 path using
            Write_NOS functionality and conversion to the specified content
            type.

        PARAMETERS:
            input:
                Required Argument.
                Specifies the teradataml DataFrame which needs to be exported
                to S3.
                Types: teradataml DataFrame

            content_type:
                Required Argument.
                Specifies the content type for DataFrame content when it is
                exported to S3.
                Types: str

        RETURNS:
            Returns S3 path information.

        EXAMPLES:
            train = DataFrame(tableName='train_data')
            s3Path = self.__get_s3_address_for_df(train, 'csv')

        RAISES:
            TeradataMlException
            TDApiClientException
        """
        awu_matrix = []
        awu_matrix.append(["content_type", content_type, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        s3_address_details = self._export_df_to_s3(input, content_type)
        s3BucketPath = self._tdapi_context._bucket_path
        if s3_address_details[5]:
            return self._convert_format_and_upload_data(s3BucketPath,
                                                        s3_address_details[2],
                                                        s3_address_details[4],
                                                        content_type)
        else:
            return s3_address_details[0]

    #  TODO: Replace this with teradataml call when support for write_nos is
    #  there in teradataml
    def _export_df_to_s3(self, input_data_frame: DataFrame, content_type):
        """
        DESCRIPTION:
            Private method for exporting input data frame to S3 using Write_NOS
            functionality.

        PARAMETERS:
            input_data_frame:
                Required Argument.
                Specifies teradataml DataFrame which needs to be exported
                to S3.
                Types: teradataml DataFrame

            content_type:
                Required Argument.
                Specifies content_type for teradataml DataFrame content
                when it is exported to S3.
                Types: str

        RETURNS:
            Returns a tuple of 6 values, with details as follows
            [0] -> S3 Address
            [1] -> S3 Bucket Name
            [2] -> S3 Folder Name
            [3] -> Requestd content type
            [4] -> Current Content type
            [5] -> Conversion needed

        EXAMPLES:
            from teradataml.dataframe import DataFrame

            train = DataFrame(tableName='train_data')
            s3AddressInfo = self._export_df_to_s3(train, 'csv')
            print(s3AddressInfo[0])
        RAISES:
            TeradataMlException
        """
        awu_matrix = []
        awu_matrix.append(["content_type", content_type, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        input_query = None
        try:
            input_query = input_data_frame.show_query(True)
        except TeradataMlException as tdml_ex:
            msg = Messages.get_message(MessageCodes.TDML_OPERATION_ERROR,
                                       "show_query")
            error_code = ErrorInfoCodes.TDML_OPERATION_ERROR
            raise TDApiClientException(msg, error_code) from tdml_ex
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex
        requested_content_type = content_type
        conversion_needed = False
        if content_type == "json":
            content_type = "parquet"
            conversion_needed = True
        s3_address = self._tdapi_context._bucket_path
        if s3_address[-1] != '/':
            s3_address += "/"
        s3_address += "{}/"
        s3_folder_name = 'tdsg-{}'.format(
            ''.join(random.choices(string.ascii_lowercase, k=10)))
        self._tdapi_context._s3_prefixes.append(s3_folder_name + "/")
        s3_address = s3_address.format(''.join(s3_folder_name))
        storedAs = content_type
        session_token_str = ""
        token_str = self._tdapi_context._session_token
        msg = "Using '{}' folder under s3 bucket '{}' for write_nos."
        logger.debug(msg.format(s3_folder_name,
                                self._tdapi_context._bucket_path))
        if len(token_str) > 0:
            session_token_str = ', "Session_Token" : "{}"'.format(token_str)
        auth_info_str = '{{ "Access_ID": "{}", "Access_Key": "{}" {} }}'
        auth_info = auth_info_str.format(self._tdapi_context._access_id,
                                         self._tdapi_context._access_key,
                                         session_token_str)
        try:
            from teradataml import WriteNOS
            obj = WriteNOS(data=input_data_frame, location=s3_address,
                           authorization=auth_info, stored_as=storedAs)
            address = s3_address
            address = address.replace('/s3/', 's3://')

            if content_type in ["parquet", "csv"]:
                bucket_name = (self._tdapi_context._bucket_path.split("/")[2]).split(".")[0]
                address = f"s3://{bucket_name}/{s3_folder_name}"

            return (address, self._tdapi_context._bucket_path, s3_folder_name,
                    requested_content_type, content_type, conversion_needed)
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.WRITE_NOS_ERROR)
            msg = msg.format("aws s3")
            error_code = ErrorInfoCodes.WRITE_NOS_ERROR
            raise TDApiClientException(msg, error_code) from ex

    def _convert_format_and_upload_data(self, bucket_path, folder_name,
                                        original_format, requested_format):
        """
        DESCRIPTION:
            Private method for converting format of files in S3 path and
            uploading converted data to new S3 folder.

        PARAMETERS:
            bucket_path:
                Required Argument.
                Specifies S3 bucket path where input data/files can be found.
                Types: str

            folder_name:
                Required Argument.
                Specifies S3 folder name where files can be found.
                This function will read all files in this folder and convert
                them to requested_format.
                Types: str

            original_format:
                Required Argument.
                Specifies original format for the content in S3 folder.
                Types: str

            requested_format:
                Required Argument.
                Specifies new format required for the content in S3 folder.
                Types: str

        RETURNS:
            Returns a S3 path where files can be found in the requested_format.

        EXAMPLES:
            newS3Path =
                self._convert_format_and_upload_data('s3-test-bucket',
                         'table-data', 'paraquet',   'csv' )
            print(newS3Path)

        RAISES:
            TDApiClientException - INVALID_ARG_VALUE
        """
        awu_matrix = []
        awu_matrix.append(["bucket_path", bucket_path, False, (str), True])
        awu_matrix.append(["folder_name", folder_name, False, (str), True])
        awu_matrix.append(["original_format", original_format, False, (str), True])
        awu_matrix.append(["requested_format", requested_format, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        if bucket_path.endswith("/"):
            bucket_path = bucket_path[:-1]
        # Convert /s3/pp.amazon.com/test-folder to pp
        bucket_path = bucket_path.split("/")[2]
        bucket_path = bucket_path.split(".")[0]
        bucket_name = bucket_path
        if original_format == "parquet":
            if requested_format != "json":
                error_code = ErrorInfoCodes.INVALID_ARG_VALUE
                msg = Messages.get_message(
                    MessageCodes.INVALID_ARG_VALUE, requested_format,
                    'requested_format', 'json')
                raise TDApiClientException(msg, error_code)

            s3 = boto3.resource(
                "s3",
                aws_access_key_id=self._tdapi_context._access_id,
                aws_secret_access_key=self._tdapi_context._access_key,
                aws_session_token=self._tdapi_context._session_token,
                region_name=self._tdapi_context._aws_region)
            bucket = s3.Bucket(bucket_name)
            dirpath = tempfile.mkdtemp()
            s3_obj = bucket.objects
            if self._tdapi_context._s3_bucket_folder:
                s3_obj_prefix = self._tdapi_context._s3_bucket_folder + "/" + folder_name + "/"
            else:
                s3_obj_prefix = folder_name + "/"
            for file in s3_obj.filter(Prefix=s3_obj_prefix):
                s3_key_path = file.key
                input_file_name = s3_key_path.split("/")[-1]
                output_file_name = "{}.{}"
                output_file_name = "{}.{}".format(
                    input_file_name.split(".")[0],
                    requested_format)
                bucket.download_file(s3_key_path,
                                     "{}/{}".format(dirpath, input_file_name))
                df = pd.read_parquet("{}/{}".format(dirpath, input_file_name))
                df.to_json("{}/{}".format(dirpath, output_file_name))
            new_dir_path = "{}/*.{}".format(dirpath, requested_format)
            list_of_new_formatted_files = glob.glob(new_dir_path)
            if self._tdapi_context._s3_bucket_folder:
                new_folder_name = self._tdapi_context._s3_bucket_folder + "/" + folder_name + "-" + requested_format
            else:
                new_folder_name = folder_name + "-" + requested_format
            self._tdapi_context._s3_prefixes.append(new_folder_name + "/")
            s3 = boto3.resource(
                's3',
                aws_access_key_id=self._tdapi_context._access_id,
                aws_secret_access_key=self._tdapi_context._access_key,
                aws_session_token=self._tdapi_context._session_token,
                region_name=self._tdapi_context._aws_region)
            for file in list_of_new_formatted_files:
                s3FileName = "{}/{}".format(new_folder_name,
                                            file.split("/")[-1])
                s3.Bucket(bucket_name).upload_file(file, s3FileName)
            shutil.rmtree(dirpath)  # Delete tmp directory
            # After conversion, we no longer need s3 folder with content
            # in earlier format, Delete that folder
            if self._tdapi_context._s3_bucket_folder:
                folder_name = self._tdapi_context._s3_bucket_folder + "/" + folder_name + "/"
            else:
                folder_name = folder_name + "/"
            s3_prefix_for_write_nos_op = folder_name
            # Also remove it from s3 prefix list
            self._tdapi_context._s3_prefixes = list(
                filter(lambda a: a != folder_name,
                       self._tdapi_context._s3_prefixes))
            _remove_s3_folders(self._tdapi_context, [s3_prefix_for_write_nos_op])
            return "s3://{}/{}".format(bucket_name, new_folder_name)
        error_code = ErrorInfoCodes.INVALID_ARG_VALUE
        msg = Messages.get_message(
            MessageCodes.INVALID_ARG_VALUE, original_format, 'original_format',
            "parquet")
        raise TDApiClientException(msg, error_code)

    def deploy(self, platform, model_type="", model_s3_key="", model_id="",
               sagemaker_p_args=[], save_byom_kwargs={},
               retrieve_byom_kwargs={}, sagemaker_kw_args={}):
        """
        DESCRIPTION:
            Deploy Sagemaker model to Vantage or AWS.
            If platform is Vantage, model is saved in Teradata database
            using BYOM functionality.

            If platform is AWS, SageMaker.deploy method of AWS SageMaker
            estimator class is executed, allowing integration
            with Teradata at the time of scoring.

        PARAMETERS:
            platform:
                Required Argument.
                Specifies platform to which the given model will be deployed.
                Accepted values: "vantage", "aws-endpoint".
                Types: String (str)

            model_type:
                Optional Argument.
                Specifies the type of the model.
                Required when platform is Vantage.
                Accepted values: "pmml", "onnx", "h2o".
                Types: String (str)

            model_s3_key:
                Optional Argument.
                Specifies S3 key of model to deploy in Vantage.
                Required when platform is Vantage.
                Types: String (str)
                
            model_id:
                Optional Argument.
                Specifies the id of the model for Teradata table.
                If no value is given, the id of the given Azure ML model will be used.
                Types: String (str)

            sagemaker_p_args:
                Required Argument.
                Specifies all posititonal parameters required for original
                SageMaker.deploy method.
                Types: Multiple

            save_byom_kwargs:
                Optional Argument.
                Specifies the keyword arguments of teradataml save_byom() function.
                If neither table_name is provided nor BYOM catalog set using set_byom_catalog,
                a table with name "tdapiclient_byom_models" will be created in the current schema.
                Types: Dictionary (dict)

            retrieve_byom_kwargs:
                Optional Argument.
                Specifies the keyword arguments of teradataml retrieve_byom() function.
                Types: Dictionary (dict)

            sagemaker_kw_args:
                Required Argument.
                Specifies all kwarg parameters required for original
                SageMaker.deploy method.
                Types: Multiple

        RETURNS:
            Instance of TDSagemakerPredictor or BYOMPredictor.

        EXAMPLES:
            predictor =
                td_apiclient.deploy(instance_type="ml.c5.large",
                                    initial_instance_count=1)

        RAISES:
            TDApiClientException - SG_DEPLOY_ERROR
            TDApiClientException - UNSUPPORTED_MODEL_TYPE
        """
        if platform.lower() == "vantage":
            if model_type.lower() in ["pmml", "onnx", "h2o"]:

                model_format = model_s3_key.split(".")[-1]
                model_dir = tempfile.TemporaryDirectory()
                model_path = f"{model_dir.name}/model.{model_format}"

                s3 = boto3.resource(
                    "s3",
                    aws_access_key_id=self._tdapi_context._access_id,
                    aws_secret_access_key=self._tdapi_context._access_key,
                    aws_session_token=self._tdapi_context._session_token,
                    region_name=self._tdapi_context._aws_region,
                    )

                bucket = s3.Bucket(self._tdapi_context._s3_bucket_name)
                bucket.download_file(model_s3_key, model_path)

                if model_format in ["pmml", "onnx", "zip"]:
                    new_model_id = f"tdapiclient-sg-{''.join(random.choices(string.ascii_lowercase, k=5))}"
                    id = model_id if model_id else new_model_id

                    try:
                        save_byom(id, model_path, **save_byom_kwargs)
                    except ValueError:
                        save_byom(id, model_path, table_name="tdapiclient_byom_models", **save_byom_kwargs)
                        set_byom_catalog("tdapiclient_byom_models")

                    model_df = retrieve_byom(id, **retrieve_byom_kwargs)
                    return _BYOMPredictor(model_df, model_type)

            msg = Messages.get_message(MessageCodes.UNSUPPORTED_MODEL_TYPE)
            error_code = ErrorInfoCodes.UNSUPPORTED_MODEL_TYPE
            raise TDApiClientException(msg, error_code)
        
        if platform.lower() == "aws-endpoint":
            try:
                method_instance = getattr(self.cloudObj, self.deploy.__name__)
                predictor_object = method_instance(*sagemaker_p_args, **sagemaker_kw_args)
                return TDSagemakerPredictor(predictor_object, self._tdapi_context)
            except Exception as ex:
                error_code = ErrorInfoCodes.SG_DEPLOY_ERROR
                msg = Messages.get_message(MessageCodes.SG_DEPLOY_ERROR, ex)
                raise TDApiClientException(msg, error_code) from ex


class TDCloudPredictor:
    """
    This is a parent class for cloud and Vantage model predictors.
    The classes TDAzurePredictor and TDSagemakerPredictor
    are subclasses of the TDCloudPredictor class.
    """

    def __init__(self, cloud_obj, tdapi_context):
        """
        DESCRIPTION:
            Initializer for TDCloudPredictor.

        PARAMETERS:
            cloud_obj:
                Required Argument.
                Specifies instance of cloud API predictor class.
                Types: cloud API predictor Object

            tdapi_context:
                Required Argument.
                Specifies TDAPI Context object holding cloud credentials
                information.
                Types: _TDApiContext object

        RETURNS:
            A TDCloudPredictor instance.

        RAISES:
            None

        EXAMPLES:
            # This class is instantiated by the library in following
            # type of operation.

            from tdapiclient import create_tdapi_context, TDApiClient
            from teradataml import DataFrame
            context = create_tdapi_context("s3_bucket")
            tdapiclient = TDApiClient(context)
            # SKlearn takes all parameters that AWS SageMaker Library requires
            skLearnObject = tdapiclient.SKLearn()
            df = DataFrame(tableName='t')
            skLearnObject.fit(df)
            predictor = skLearnObject.deploy(instance_type="ml.m5.large",
                            initial_instance_count=1)
            # predictor will be of type TDSagemakerPredictor
        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        awu_matrix.append(["cloud_obj", cloud_obj, False, (object), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        self.cloudObj = cloud_obj
        self._tdapi_context: _TDApiContext = tdapi_context

    @classmethod
    def from_predictor(cls):
        """
        DESCRIPTION:
            A constructor for TDCloudPredictor using a cloud predictor object.

        RETURNS:
            Instance of Predictor class.

        RAISES:
            None
        """
        pass

    def predict(self, input: DataFrame, mode, **options):
        """
        DESCRIPTION:
            This method performs prediction using teradataml DataFrame and
            cloud endpoint represented by this predictor object.

        PARAMETERS:
            input:
                Required Argument.
                Specifies the teradataml DataFrame for scoring.
                Types: teradataml DataFrame

            mode:
                Required Argument.
                Specifies the mode for scoring.
                Permitted Values:
                    * 'UDF': Score in database using a Teradata UDF.
                             Faster scoring with the data from Teradata.
                    * 'CLIENT': Score at client using a library. Data will be
                                pulled from Teradata and serialized for
                                scoring at client.
                Default Value: 'UDF'
                Types: Str

            options:
                Optional Argument.
                Specifies the predict method with the following key-value
                arguments:
                udf_name: Specifies the UDF name used to invoke predict with
                          UDF mode.
                          Default Value: tapidb.API_Request
                content_type: Specifies content type required for
                              Azure ML endpoint present in the predictor.
                              Default Value: json
                key_start_index: Specifies the index in DataFrame columns to
                                 be the key for scoring starts.
                                 Default Value: 0
                content_format: Specifies the content_format required for
                              Azure ML endpoint present in the predictor.
                              Types: Dict
                Types: kwarg

        RETURNS:
            A teradataml DataFrame, when mode is set to 'UDF'; otherwise
            an array or JSON.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            # Script run config takes all the parameters as
            # required by azure-ml script run config
            skLearnObject = tdapiclient.ScriptRunConfig() # This call refers to _init_ call above.
            train = DataFrame(tableName='train_data')
            skLearnObject.fit(mount=True)
            predictor = skLearnObject.deploy(model, mode='az-webservice')
            df = DataFrame(tableName='inputTable')
            output = td_predictor.predict(df, mode='udf', content_type='json')
        """
        options = {k.lower(): v for k, v in options.items()}
        self._set_default_options(options)
        if mode.lower() == "client":
            return self._run_prediction_at_client(input, options)
        elif mode.lower() == "udf":
            return self._run_udf(input, options)
        else:
            errMsg = Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE, mode, "mode", "client or udf")
            error_code = ErrorInfoCodes.INVALID_ARG_VALUE
            raise TDApiClientException(errMsg, error_code)

    def _set_default_options(self, options: dict):
        """
        DESCRIPTION:
            A private method for getting default options for predict API.

        PARAMETERS:
            options:
                Required Argument.
                Specifies options given by User.
                Types: dict

        RETURNS:
            None
            It fills the input options with default option parameters.

        RAISES:
            None

        EXAMPLE:
            options = {}
            self.__fillDefaultOptions(options)
        """
        awu_matrix = []
        awu_matrix.append(["options", options, False, (dict), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if "udf_name" not in options:
            options["udf_name"] = "tapidb.API_Request"
        if "content_type" not in options:
            options["content_type"] = "csv"
        if "key_start_index" not in options:
            options["key_start_index"] = 0

    def _run_prediction_at_client(self):
        """
        DESCRIPTION:
            A private method for running a client-side prediction.

        RETURNS:
            List or JSON object.

        RAISES:
            None
        """
        pass

    def _run_udf(self, data: DataFrame, options: dict):
        """
        DESCRIPTION:
            A private method for runing predict operation inside DB using UDF.

        PARAMETERS:
            data:
                Required Argument.
                Specifies input teradataml dataframe which holds input data
                for scoring.
                Types: teradataml DataFrame
            options:
                Required Argument.
                Specifies options dictionary which holds user given or default
                options for predict API.
                Types: dict

        RETURNS:
            It returns teradataml DataFrame object containing output column
            for prediction.

        RAISES:
            TeradataMlException
            TDApiClientException

        EXAMPLE:
            options = {}
            self._set_default_options(options)
            inputDataFrame = DataFrame(tableName='customer_data')
            output = self._run_udf(inputDataFrame, options)
        """
        awu_matrix = []
        awu_matrix.append(["options", options, False, (dict), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        input_query = None
        try:
            input_query = data.show_query(True)
        except TeradataMlException as tdml_ex:
            msg = Messages.get_message(MessageCodes.TDML_OPERATION_ERROR,
                                       "show_query")
            error_code = ErrorInfoCodes.TDML_OPERATION_ERROR
            raise TDApiClientException(msg, error_code) from tdml_ex
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex
        
        for option in options.keys():
            logger.debug(f"{option} is {options[option]}")

        try:
            udf_query = self._prepare_udf_query(input_query, options)
            queryDf = DataFrame(query=udf_query)
            return queryDf
        except TeradataMlException as tdml_ex:
            msg = Messages.get_message(MessageCodes.TDML_OPERATION_ERROR,
                                       "DataFrame")
            error_code = ErrorInfoCodes.TDML_OPERATION_ERROR
            raise TDApiClientException(msg, error_code) from tdml_ex
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex

    def _prepare_udf_query(self):
        """
        DESCRIPTION:
            A private method for creating a UDF query string.

        RETURNS:
            Query string.

        RAISES:
            None
        """
        pass

    def __getattr__(self, name):
        """
        DESCRIPTION:
            A private method used to invoke a method from chosen cloud API.

        RETURNS:
            Instance of object from cloud API.

        RAISES:
            None
        """
        if self.cloudObj is None:
            return None

        def __cloud_method_invoker(*c, **kwargs):
            return atrribute_instance(*c, **kwargs)

        atrribute_instance = getattr(self.cloudObj, name)
        if callable(atrribute_instance):
            return __cloud_method_invoker
        return atrribute_instance


class TDSagemakerPredictor(TDCloudPredictor):
    """
    This is a wrapper over SageMaker.Predictor class. It allows for
    integration with Teradata at the time of scoring using predict method.
    """

    @classmethod
    def from_predictor(cls, sagemaker_predictor_obj, tdapi_context):
        """
        DESCRIPTION:
            This method creates TDSagemakerPredictor from the sagemaker predictor
            object to allow for prediction using teradataml DataFrame and
            SageMaker endpoint represented by this predictor object.

        PARAMETERS:
            sagemaker_predictor_obj:
                Required Argument.
                Specifies the instance of SageMaker predictor class.
                Types: SageMaker predictor Object

            tdapi_context:
                Required Argument.
                Specifies the TDAPI Context object holding aws credentials
                information.
                Types: _TDApiContext object

        RETURNS:
            A TDSagemakerPredictor instance.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import TDSagemakerPredictor, create_tdapi_context
            import sagemaker
            from sagemaker.xgboost.estimator import XGBoost
            from sagemaker.session import s3_input, Session

            # Initialize hyperparameters
            hyperparameters = {
                    "max_depth":"5",
                    "eta":"0.2",
                    "gamma":"4",
                    "min_child_weight":"6",
                    "subsample":"0.7",
                    "verbosity":"1",
                    "objective":"reg:linear",
                    "num_round":"50"}

            # Set an output path where the trained model will be saved
            bucket = sagemaker.Session().default_bucket()
            prefix = 'DEMO-xgboost-as-a-framework'
            output_path = 's3://{}/{}/{}/output'.format(bucket, prefix,
              'abalone-xgb-framework')

            # Construct a SageMaker XGBoost estimator
            # Specify the entry_point to your xgboost training script
            estimator = XGBoost(entry_point = "your_xgboost_abalone_script.py",
                                framework_version='1.0-1',
                                hyperparameters=hyperparameters,
                                role=sagemaker.get_execution_role(),
                                train_instance_count=1,
                                train_instance_type='ml.m5.2xlarge',
                                output_path=output_path)

            # Define the data type and paths to the training and validation
            # datasets
            content_type = "json"
            train_input = s3_input("s3://{}/{}/{}/".format(bucket, prefix,
              'train'), content_type=content_type)
            validation_input = s3_input("s3://{}/{}/{}/".format(bucket,
                 prefix, 'validation'), content_type=content_type)

            # Execute the XGBoost training job
            estimator.fit({'train': train_input,
                   'validation': validation_input})
            sagemaker_predictor = estimator.deploy()
            context = create_tdapi_context("aws_region", "s3_bucket" "access_id",
                                          "access_key", "session_token_if_any")

            tdsg_predictor = TDSagemakerPredictor.from_predictor(
                sagemaker_predictor, context)

        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        awu_matrix.append(["sagemaker_predictor_obj", sagemaker_predictor_obj, False, (object), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return TDSagemakerPredictor(sagemaker_predictor_obj, tdapi_context)

    def _run_prediction_at_client(self, data: DataFrame, options):
        """
        DESCRIPTION:
            A private method for runing predict operation at the client side.

        PARAMETERS:
            data:
                Required Argument.
                Specifies input teradataml dataframe which holds input data
                for scoring.
                Types: teradataml DataFrame

            options:
                Required Argument.
                Specifies options dictionary which holds user given or default
                options for predict API.
                Types: dict

        RETURNS:
            It returns array or json as per SageMaker model.

        RAISES:
            SagemakerException

        EXAMPLE:
            options = {}
            self._set_default_options(options)
            inputDataFrame = DataFrame(tableName='customer_data')
            output = self._run_prediction_at_client(inputDataFrame, options)
        """
        awu_matrix = []
        awu_matrix.append(["options", options, False, (dict), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        content_type = options["content_type"].lower()
        pdf = data.to_pandas()
        if content_type == "json":
            row_data = pdf.to_json(orient="values")
            return (self.cloudObj.predict(row_data))
        elif content_type == "csv":
            row_data = pdf.to_csv(index=False, header=False)
            return (self.cloudObj.predict(row_data))
        else:
            errMsg = Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE, content_type, "content_type",
                "json or csv")
            error_code = ErrorInfoCodes.INVALID_ARG_VALUE
            raise TDApiClientException(errMsg, error_code)

    def _prepare_udf_query(self, input_query, options: dict):
        """
        DESCRIPTION:
            A private method for creating a UDF query string for AWS Sagemaker.

        PARAMETERS:
            input_query:
                Required Argument.
                Specifies SQL query string for input teradataml dataframe
                which holds data for scoring.
                Types: SQL query string
            options:
                Required Argument.
                Specifies options dictionary which holds user given or default
                options for predict API.
                Types: dict

        RETURNS:
            UDF query string.

        RAISES:
            None.

        EXAMPLE:
            options = {}
            self._set_default_options(options)
            inputDataFrame = DataFrame(tableName='customer_data')
            input_query = inputDataFrame.show_query(True)
            output = self._prepare_udf_query(input_query, options)
        """
        session_token_str = ""
        token_str = self._tdapi_context._session_token
        if len(token_str) > 0:
            session_token_str = '"Session_Token" : "{}"'.format(token_str)

        auth_info_fmt_str = ('{{ "Access_ID": "{}", "Access_Key": '
                             + '"{}", "Region" : "{}", {} }}')
        auth_info = auth_info_fmt_str.format(self._tdapi_context._access_id,
                                             self._tdapi_context._access_key,
                                             self._tdapi_context._aws_region,
                                             session_token_str)
        
        udf_query = ("SELECT * FROM {}( ON ({}) USING AUTHORIZATION('{}')"
                     + " API_TYPE('aws-sagemaker') ENDPOINT('{}') "
                     + " CONTENT_TYPE('{}') KEY_START_INDEX('{}')) "
                     "as \"DT\" ")

        return udf_query.format(
            options["udf_name"], input_query, auth_info,
            self.cloudObj.endpoint_name,
            options["content_type"], options["key_start_index"]
            )


class TDAzurePredictor(TDCloudPredictor):
    """
    This is a wrapper over AciWebservice class. It allows for
    integration with Teradata at the time of scoring using predict method.
    """

    @classmethod
    def from_predictor(cls, azureml_predictor_obj, tdapi_context):
        """
        DESCRIPTION:
            This method creates TDAzurePredictor from the AciWebservice
            object to allow for prediction using teradataml DataFrame and
            azureml endpoint represented by this predictor object.

        PARAMETERS:
            azureml_predictor_obj:
                Required Argument.
                Specifies the Azure ML predictor object.
                Types: AciWebservice

            tdapi_context:
                Required Argument.
                Specifies the TDAPI Context object holding azure credentials
                information.
                Types: _TDApiContext object

        RETURNS:
            A TDAzurePredictor instance.

        RAISES:
            None.

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            # Script run config takes all the parameters as
            # required by azure-ml script run config
            skLearnObject = tdapiclient.ScriptRunConfig() # This call refers to _init_ call above.
            train = DataFrame(tableName='train_data')
            skLearnObject.fit(mount=True)
            tdaz_predictor = AzurePredictor.from_predictor(skLearnObject, context)
        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        awu_matrix.append(["azureml_predictor_obj", azureml_predictor_obj, False, (AciWebservice), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return TDAzurePredictor(azureml_predictor_obj, tdapi_context)

    def _run_prediction_at_client(self, data: DataFrame, options):
        """
        DESCRIPTION:
            A private method for runing predict operation at the client side.

        PARAMETERS:
            data:
                Required Argument.
                Specifies input teradataml dataframe which holds input data
                for scoring.
                Types: teradataml DataFrame

            options:
                Required Argument.
                Specifies options dictionary which holds user given or default
                options for predict API.
                Types: dict

        RETURNS:
            It returns array or json as per Azureml model.

        RAISES:
            TDApiClientException.

        EXAMPLE:
            options = {}
            self._set_default_options(options)
            inputDataFrame = DataFrame(tableName='customer_data')
            output = self._run_prediction_at_client(inputDataFrame, options)
        """
        awu_matrix = []
        awu_matrix.append(["options", options, False, (dict), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        content_type = options["content_type"].lower()
        content_format = {}
        content_format = options["content_format"]
        pdf = data.to_pandas()
        pdf_dict = {}
        if content_type == "json":
            row_data = pdf.to_json(orient="values")
            parsed_obj = json.loads(row_data)
            pdf_dict = {k: parsed_obj for k, v in content_format.items()}
            run_obj = json.dumps(pdf_dict)
            return (self.cloudObj.run(run_obj))
        else:
            errMsg = Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE, content_type, "content_type",
                "json")
            error_code = ErrorInfoCodes.INVALID_ARG_VALUE
            raise TDApiClientException(errMsg, error_code)
        
    def _prepare_udf_query(self, input_query, options: dict):
        """
        DESCRIPTION:
            A private method for creating a UDF query string for Azure ML.

        PARAMETERS:
            input_query:
                Required Argument.
                Specifies SQL query string for input teradataml dataframe
                which holds data for scoring.
                Types: SQL query string
            options:
                Required Argument.
                Specifies options dictionary which holds user given or default
                options for predict API.
                Types: dict

        RETURNS:
            UDF query string.

        RAISES:
            None.

        EXAMPLE:
            options = {}
            self._set_default_options(options)
            inputDataFrame = DataFrame(tableName='customer_data')
            input_query = inputDataFrame.show_query(True)
            output = self._prepare_udf_query(input_query, options)
        """
        keys = self.cloudObj.get_keys()
        primary_key = keys[0]
        auth_key = primary_key
        endpoint = self.cloudObj.scoring_uri
        region = self.cloudObj.location
        auth_info_fmt_str = ('{{ "Key": "{}", "Region" : "{}"}}')
        auth_info = auth_info_fmt_str.format(auth_key, region)
        
        udf_query = ("SELECT * FROM {}( ON ({}) USING AUTHORIZATION('{}')"
                     + " API_TYPE('azure-ml') ENDPOINT('{}') "
                     + " CONTENT_TYPE('{}') KEY_START_INDEX('{}') "
                     + " CONTENT_FORMAT('{}')) "
                     "as \"DT\" ")

        content_format = options["content_format"]
        for k,v in content_format.items():
            content_format_key = k
            content_format_value = json.dumps(v)
        content_format_str = ('{{ "{}" : {}}}'.format(content_format_key, content_format_value))

        return udf_query.format(
            options["udf_name"], input_query, auth_info, endpoint,
            options["content_type"], options["key_start_index"], content_format_str
            )
    

class _BYOMPredictor:
    """
    This class is used to hold the model teradataml DataFrame and its type
    obtained in _TDAzureObjectWrapper.deploy.
    """

    def __init__(self, model_df, model_type):
        """
        DESCRIPTION:
            Constructor for BYOMPredictor class.

        PARAMETERS:
            model_df:
                Required Argument.
                Specifies the teradataml DataFrame containing the model data
                to be used for scoring.
                Types: teradataml DataFrame

            model_type:
                Required Argument.
                Specifies the type of the model.
                Accepted values: "pmml", "onnx", "h2o".
                Types: String (str)

        RETURNS:
            Instance of _BYOMPredictor.

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            # Script run config takes all the parameters as
            # required by azure-ml script run config
            skLearnObject = tdapiclient.ScriptRunConfig()
            train = DataFrame(tableName='train_data')
            run = skLearnObject.fit(mount=True)
            model = run.register_model(model_name='example', model_path='outputs/example.pmml')
            # Deploy model to Vantage.
            model_predictor = skLearnObject.deploy(model, platform="vantage")
            # Score model in Vantage, show "id" column of test data in output.
            test = DataFrame(tableName='test_data')
            model_predictor.predict(test, ['id'])
        RAISES:
            TeradataMlException
            TDApiClientException
        """

        self.model_df = model_df
        self._model_type = model_type.lower()

    def predict(self, input: DataFrame, input_cols, **byom_kwargs):
        """
        DESCRIPTION:
            Score data in Vantage with a model that has been created
            outside Vantage and exported to Vantage using the deploy method.

            Supports prediction using the models in following formats:
            * PMML
            * ONNX
            * MOJO (H2O)

        PARAMETERS:
            input:
                Required Argument.
                Specifies the teradataml DataFrame containing the input test data.
                Types: teradataml DataFrame

            input_cols:
                Required Argument.
                Specifies the name(s) of input teradataml DataFrame column(s) to copy to the output.
                Types: str OR list of Strings (str)

            **byom_kwargs:
                Optional Argument.
                Specifies additional keyword arguments which PMMLPredict, H2OPredict, or ONNXPredict accept.
                Below are the keyword arguments:
                    model_output_fields:
                        Optional Argument.
                        Specifies the column(s) of the json output that the user wants to
                        specify as individual columns instead of the entire json_report.
                        Types: str OR list of Strings (str)

                    overwrite_cached_models:
                        Optional Argument.
                        Specifies the model name that needs to be removed from the cache.
                        "*" can also be used to remove the models.
                        Default Value: "false"
                        Permitted Values: true, t, yes, y, 1, false, f, no, n, 0, *,
                                        current_cached_model
                        Types: str

                    modeldata_order_column:
                        Optional Argument.
                        (PMML/H2O only.) Specifies Order By columns for "modeldata".
                        Values to this argument can be provided as a list, if multiple
                        columns are used for ordering.
                        Types: str OR list of Strings (str)

                    newdata_partition_column:
                        Optional Argument
                        (PMML/H2O only.) Specifies Partition By columns for "newdata".
                        Values to this argument can be provided as a list, if multiple
                        columns are used for partition.
                        Default Value: ANY
                        Types: str OR list of Strings (str)

                    newdata_order_column:
                        Optional Argument.
                        (PMML/H2O only.) Specifies Order By columns for "newdata".
                        Values to this argument can be provided as a list, if multiple
                        columns are used for ordering.
                        Types: str OR list of Strings (str)

                    model_type:
                        Optional Argument.
                        (H2O only.) Specifies the model type for H2O model prediction.
                        Default Value: "OpenSource"
                        Permitted Values: DAI, OpenSource
                        Types: str OR list of Strings (str)

                    enable_options:
                        Optional Argument.
                        (H2O only.) Specifies the options to be enabled for H2O model prediction.
                        Permitted Values: contributions, stageProbabilities, leafNodeAssignments
                        Types: str OR list of Strings (str)

                    show_model_input_fields_map:
                        Optional Argument.
                        (ONNX only.) Specifies to show default or expanded "model_input_fields_map" based on input
                        model for defaults or "model_input_fields_map" for expansion.
                        Default Value: False
                        Types: bool

                    model_input_fields_map:
                        Optional Argument.
                        (ONNX only.) Specifies the mapping of input columns to tensor input names.
                        Types: str OR list of Strings (str)

        RETURNS:
            teradataml DataFrame.

        RAISES:
            TeradataMlException
            TDApiClientException

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("azure", "/td-tables")
            tdapiclient = TDApiClient(context)
            train = DataFrame(tableName='train_data')
            # ScriptRunConfig takes all the parameters as
            # required by Azure ML ScriptRunConfig.
            skLearnObject = tdapiclient.ScriptRunConfig(arguments=[train])
            # Train the model in Azure ML.
            run = skLearnObject.fit(mount=True)
            # Register model in Azure ML.
            model = run.register_model(model_name='example', model_path='outputs/example.pmml')
            # Deploy model to Vantage.
            model_predictor = skLearnObject.deploy(model, platform="vantage")
            # Score model in Vantage, show "id" column of test data in output.
            test = DataFrame(tableName='test_data')
            model_predictor.predict(test, ['id'])
        """

        byom_function_name = ""
        if self._model_type == "pmml":
            byom_function_name = "PMMLPredict"
        elif self._model_type == "h2o":
            byom_function_name = "H2OPredict"
        elif self._model_type == "onnx":
            byom_function_name = "ONNXPredict"
        else:
            msg = Messages.get_message(MessageCodes.UNSUPPORTED_MODEL_TYPE)
            error_code = ErrorInfoCodes.UNSUPPORTED_MODEL_TYPE
            raise TDApiClientException(msg, error_code)

        byom_func = getattr(teradataml, byom_function_name)
        obj = byom_func(
            newdata=input,
            modeldata=self.model_df,
            accumulate=input_cols,
            **byom_kwargs)

        return obj.result