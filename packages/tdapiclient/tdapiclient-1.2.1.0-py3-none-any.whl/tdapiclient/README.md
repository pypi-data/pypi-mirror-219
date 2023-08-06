## tdapiclient - Teradata Third Party Analytics Integration Python Library

 tdapiclient Python library allows AWS SageMaker and Teradata users to use AWS SageMaker Python library's interface to train/predict using teradataml DataFrame. tdapiclient will transparantly convert teradataml DataFrame in S3 address to be used for training and it will also allow user to use teradataml DataFrame as input for inference.

 tdapiclient also allows Azure-ML and Teradata Users to use easier interface to train/predict using teradataml DataFrame. tdapiclient will transparantly convert teradataml DataFrame to azure-ml dataset or blob store to be used for training and it will allow users to use teradataml DataFrame as input for inference.
 Additinally, tdapiclient also allows to deploy azure-ml trained models in Teradata Vantage system for in-database scoring using BYOM functionality.

For community support, please visit the [Connectivity Forum](http://community.teradata.com/t5/Tools/bd-p/DevXToolsBoard).
For Teradata customer support, please visit [Teradata Access](https://access.teradata.com/).

Copyright 2022, Teradata. All Rights Reserved.

### Table of Contents
- [tdapiclient - Teradata Third Party Analytics Integration Python Library](#tdapiclient---teradata-third-party-analytics-integration-python-library)
- [Release Notes](#release-notes)
- [Installation and Requirements](#installation-and-requirements)
- [Using the tdapiclient Python Package with Sagemaker](#using-the-tdapiclient-python-package-with-sagemaker)
- [Using the tdapiclient Python Package with Azure-ML](#using-the-tdapiclient-python-package-with-azure-ml)
- [Documentation](#documentation)
- [License](#license)

## Release Notes
#### tdapiclient 1.2.1.0
* `tdapiclient 1.2.1.00` is the third release version. This release adds BYOM deployment support for SageMaker and optimizes fit method for CSV data format. Please refer to the _API Integration Guide for Cloud Machine Learning_ for a list of Limitations and Usage Considerations.

#### tdapiclient 1.1.1.0
* `tdapiclient 1.1.1.00` is the second release version. This release adds a support for AzureML integration with Teradata vantage. Please refer to the _API Integration Guide for Cloud Machine Learning_ for a list of Limitations and Usage Considerations.

#### tdapiclient 1.0.0.0
* `tdapiclient 1.00.00.00` is the first release version. Please refer to the _API Integration Guide for Cloud Machine Learning_ for a list of Limitations and Usage Considerations.

## Installation and Requirements

### Package Requirements
* Python 3.6 or later

Note: 32-bit Python is not supported.

### Minimum System Requirements
* Windows 7 (64Bit) or later
* macOS 10.9 (64Bit) or later
* Red Hat 7 or later versions
* Ubuntu 16.04 or later versions
* CentOS 7 or later versions
* SLES 12 or later versions
* Teradata Vantage Advanced SQL Engine:
    * Advanced SQL Engine 17.05 Feature Update 1 or later

### Installation

Use pip to install the tdapiclient - Teradata Sagemaker Python Library

Platform       | Command
-------------- | ---
macOS/Linux    | `pip install tdapiclient`
Windows        | `py -3 -m pip install tdapiclient`

## Using the tdapiclient Python Package with Sagemaker

Your Python script must import the `tdapiclient` package in order to use the tdapiclient Python Library
```
>>> from tdapiclient import create_aws_context,TDApiClient
>>> from teradataml import create_context, DataFrame, copy_to_sql

>>> # Create connection to Teradata Vantage System
>>> host = input("Host: ")
>>> username = input("Username: ")
>>> password = getpass.getpass("Password: ")
>>> td_context = create_context(host=host, username=username, password=password)

# Create AWS Context to be used in TDApiClient
>>> s3_bucket = input("S3 Bucket(Please give just the bucket name) :")
>>> access_id = input("Access ID:")
>>> access_key = getpass.getpass("Acess Key: ")
>>> region = input("AWS Region: ")

>>>   os.environ["AWS_ACCESS_KEY_ID"] = access_id
>>>   os.environ["AWS_SECRET_ACCESS_KEY"] = access_key
>>>   os.environ["AWS_REGION"] = region

>>> aws_context = create_tdapi_context("aws", bucket_name=s3_bucket)
# Create TDApiClient Instance
>>> td_apiclient = TDApiClient(aws_context)

# Load data in teradata tables
>>> from sklearn.model_selection import train_test_split
>>> from sklearn.datasets import fetch_california_housing

>>> data = fetch_california_housing()
>>> X_train, X_test, y_train, y_test = train_test_split(
     data.data, data.target, test_size=0.25, random_state=42)

>>> trainX = pd.DataFrame(X_train, columns=data.feature_names)
>>> trainX["target"] = y_train

>>> testX = pd.DataFrame(X_test, columns=data.feature_names)
>>> testX["target"] = y_test

>>> train_table = "housing_data_train"
>>> test_table = "housing_data_test"

>>> column_types = {"MedInc": FLOAT, "HouseAge": FLOAT,
                "AveRooms": FLOAT, "AveBedrms": FLOAT, "Population": FLOAT,
                "AveOccup": FLOAT, "Latitude": FLOAT, "Longitude": FLOAT,
                "target" : FLOAT}

>>> copy_to_sql(df=trainX, table_name=train_table, if_exists="replace", types=column_types)
>>> copy_to_sql(df=testX, table_name=test_table, if_exists="replace", types=column_types)

# Create teradataml DataFrame for input tables

>>> test_df = DataFrame(table_name=test_table)
>>> train_df = DataFrame(table_name=train_table)

>>> exec_role_arn = "arn:aws:iam::XX:role/service-role/AmazonSageMaker-ExecutionRole-20210112T215668"
>>> FRAMEWORK_VERSION = "0.23-1"
# Create an estimator object based on sklearn sagemaker class
>>> sklearn_estimator = td_apiclient.SKLearn(
    entry_point="sklearn-script.py",
    role=exec_role_arn,
    instance_count=1,
    instance_type="ml.m5.large",
    framework_version=FRAMEWORK_VERSION,
    base_job_name="rf-scikit",
    metric_definitions=[{"Name": "median-AE", "Regex": "AE-at-50th-percentile: ([0-9.]+).*$"}],
    hyperparameters={
        "n-estimators": 100,
        "min-samples-leaf": 3,
        "features": "MedInc HouseAge AveRooms AveBedrms Population AveOccup Latitude Longitude",
        "target": "target",
    },
)
>>> # Start training using DataFrame objects
>>> sklearn_estimator.fit({"train": test_df, "test": train_df}, content_type="csv", wait=True)

>>> from sagemaker.serializers import CSVSerializer
>>> from sagemaker.deserializers import CSVDeserializer
>>> csv_ser = CSVSerializer()
>>> csv_dser = CSVDeserializer()
>>> predictor = sklearn_estimator.deploy(instance_type="ml.m5.large", initial_instance_count=1,serializer=csv_ser,  deserializer=csv_dser)

>>> # Now let's try prediction with UDF and Client options.
>>> input = DataFrame(table_name='housing_data_test')
>>> column_list = ["MedInc","HouseAge","AveRooms","AveBedrms","Population","AveOccup","Latitude","Longitude"]
>>> input = input.sample(n=5).select(column_list)

>>> output = predictor.predict(input, mode="UDF",content_type='csv')

```

## Using the tdapiclient Python Package with Azure-ML
Your Python script must import the `tdapiclient` package in order to use the tdapiclient Python Library
```
>>> import os
>>> import getpass
>>> from teradataml import create_context, DataFrame, read_csv
>>> import pandas as pd
>>> from teradatasqlalchemy.types import  *
>>> from tdapiclient import create_tdapi_context,TDApiClient, remove_tdapi_context
>>> # Create the connection.
>>> host = input("Host: ")
>>> username = input("Username: ")
>>> password = getpass.getpass("Password: ")
>>> # Create Azure Context and TDApiClient object.

>>> datastore_path = input(
>>>    "DataStore path : Please give path within data store of azure-ml workspace.")
>>> tenant_id = input("Azure Tenant ID:")
>>> client_id = getpass.getpass("Azure Client ID: ")
>>> client_secret = input("Azure Client Secret: ")
>>>
>>> azure_sub = input("Azure Subscription id: ")
>>> azure_rg = input("Azure resource group: ")
>>> azureml_ws = input("Azure-ML workspace: ")
>>> azure_region = input("Azure region: ")

>>> os.environ["AZURE_TENANT_ID"] = tenant_id
>>> os.environ["AZURE_CLIENT_ID"] = client_id
>>> os.environ["AZURE_CLIENT_SECRET"] = client_secret
>>>
>>> os.environ["AZURE_SUB_ID"] = azure_sub
>>> os.environ["AZURE_RG"] = azure_rg
>>> os.environ["AZURE_WS"] = azureml_ws
>>> os.environ["AZURE_REGION"] = azure_region

>>> tdapi_context = create_tdapi_context("azure", datastore_path="td-tables")
>>> td_apiclient = TDApiClient(tdapi_context)
>>> from collections import OrderedDict
>>>
>>> from collections import OrderedDict
>>>
>>> types = OrderedDict(bustout=INTEGER, rec_id=INTEGER, acct_no=INTEGER, as_of_dt_day=DATE, avg_pmt_05_mth=FLOAT,>>> days_since_lstcash=INTEGER, max_utilization_05_mth=INTEGER, maxamt_epmt_v7day=INTEGER, times_nsf=INTEGER,
>>>  totcash_to_line_v7day=INTEGER,totpmt_to_line_v7day=INTEGER,totpur_to_line_v7day=INTEGER,  totpurcash_to_line_v7day=INTEGER, credit_util_cur_mth=FLOAT, credit_util_prior_5_mth=FLOAT, credit_util_cur_to_prior_ratio=FLOAT, days_since_lst_pymnt=INTEGER, num_pymnt_lst_7_days=INTEGER, num_pymnt_lst_60_days=INTEGER,
>>>     pct_line_paid_lst_7_days=INTEGER, pct_line_paid_lst_30_days=INTEGER, num_pur_lst_7_days=INTEGER, num_pur_lst_60_days=INTEGER,
>>>     pct_line_pur_lst_7_days=INTEGER, pct_line_pur_lst_30_days=INTEGER, tot_pymnt_chnl=INTEGER, tot_pymnt=INTEGER, tot_pymnt_am=INTEGER, pay_by_phone=CHAR, elec_pymnt=CHAR,
>>>     pay_in_bank=CHAR, pay_by_check=CHAR, pay_by_othr=CHAR, last_12m_trans_ct=INTEGER, Sample_ID=INTEGER)

>>> # Check this csv file in Teradata Vantage Documentation site under azureml-usercases.zip
>>> df:DataFrame = read_csv(r'financial_data.csv', table_name="financial_data", types=types, use_fastload=False)
>>> # training dataframe.
>>> selected_df = df.select(["bustout", "rec_id", "avg_pmt_05_mth", "max_utilization_05_mth","times_nsf"
,"credit_util_cur_mth","credit_util_prior_5_mth","num_pur_lst_7_days","num_pur_lst_60_days","tot_pymnt_chnl","last_12m_trans_ct"])
>>> # Setup compute target for Azure ML.
>>> from azureml.core.compute import AmlCompute, ComputeTarget
>>> from azureml.core.authentication import ServicePrincipalAuthentication
>>> from azureml.core import Workspace, Environment

>>> credential = ServicePrincipalAuthentication(
>>>         tenant_id=tenant_id,
>>>         service_principal_id=client_id, service_principal_password=client_secret)

>>> ws = Workspace(subscription_id=azure_sub, resource_group=azure_rg, workspace_name=azureml_ws, auth=credential)

>>> vm_size = "Standard_DS3_v2"
>>> min_node = 1
>>> max_node = 1
>>> cluster_name = "test-td-cluster-new"
>>> provisioning_config = AmlCompute.provisioning_configuration(
>>>         vm_size=vm_size, min_nodes=min_node,
>>>         max_nodes=max_node)

>>> # Creating Compute cluster in Azure ML.
>>> compute_target = ComputeTarget.create(
>>>         ws, cluster_name, provisioning_config)
>>> compute_target.wait_for_completion(show_output=True)

>>> compute_target = ws.compute_targets["test-td-cluster-new"]
>>> from azureml.automl.core.featurization import FeaturizationConfig
>>> import logging

>>> # Selecting the target column.
>>> target_column_name = "bustout"

>>> forecast_horizon=14

>>> featurization_config = FeaturizationConfig()
>>> # Force the target column, to be integer type.
>>> featurization_config.add_prediction_transform_type("Integer")

>>> automl_config = td_apiclient.AutoMLConfig(
>>>     task="classification",
>>>     primary_metric="accuracy",
>>>     featurization=featurization_config,
>>>     blocked_models=["ExtremeRandomTrees"],
>>>     experiment_timeout_hours=0.3,
>>>     training_data=selected_df,
>>>     label_column_name=target_column_name,
>>>     compute_target=compute_target,
>>>     enable_early_stopping=True,
>>>     n_cross_validations=3,
>>>     max_concurrent_iterations=4,
>>>     max_cores_per_iteration=-1,
>>>     verbosity=logging.INFO
>>> )

>>> # Execute Azure ML training API with teradataml DataFrame as input which returns Azure ML Run Object.
>>> run = automl_config.fit(mount=False)
>>> # Get the best run after Auto ML job has completed.
>>> run_best = run.get_best_child()
>>> from azureml.core.environment import Environment
>>>
>>> # Creating an Azure ML Environment from a Dockerfile and requirements.txt.
>>> # myenv = Environment.from_dockerfile(name="new_project_env_7", dockerfile="./Dockerfile", pip_requirements="./>>> requirements.txt")
>>> myenv = Environment.from_dockerfile(name="new_project_env_18", >>> dockerfile=r'C:\Projects\AzureML-jupyter-notebooks\test-ignite-azureml-api-demo\Dockerfile', pip_requirements=r'C:\Projects\AzureML-jupyter-notebooks\test-ignite-azureml-api-demo\requirements.txt')
>>> myenv_b = myenv.build(workspace=ws)
>>> myenv_b.wait_for_completion(show_output=True)
>>> # curated_env_name = "AzureML-sklearn-0.24.1-ubuntu18.04-py37-cpu-inference"
>>> # myenv = Environment.get(workspace=ws, name=curated_env_name)
>>> myenv = Environment.get(workspace=ws, name="new_project_env_18")
>>> # Register an Azure ML model from the best run.
>>> from azureml.core import Model
>>> model:Model = run_best.register_model(model_name='voting_ensemble_model_1', model_path='outputs/model.pkl',>>> model_framework=Model.Framework.SCIKITLEARN)
>>> from azureml.core.model import Model
>>> model = Model(workspace=ws, name="voting_ensemble_model_1", version=1)

>>> from enum import auto
>>> from operator import mod
>>> from platform import platform
>>> from azureml.core import Model
>>> from azureml.core.model import InferenceConfig, Model
>>> from azureml.core.webservice import AciWebservice, Webservice
>>> from azureml.core.environment import Environment
>>> print(myenv)
>>> # Combine scoring script & environment in Inference configuration
>>> # inference_config = InferenceConfig(entry_script="scoring.py",
>>> #                                    environment=myenv)
>>> myenv.inferencing_stack_version = 'latest'
>>> inference_config = InferenceConfig(entry_script=r'C:\Projects\test-tdapiclient\tdapiclient\notebooks\azureml-az-webservice\scoring.py',
                                   environment=myenv)
>>> # Set deployment configuration
>>> deployment_config = AciWebservice.deploy_configuration(cpu_cores = 2,
>>>                                                        memory_gb = 4, auth_enabled=True)

>>> # Creating azmodel_deploy_kwargs dictionary to pass as a keyword argument for deploy method.
>>> azmodel_deploy_kwargs = {}
>>> azmodel_deploy_kwargs["name"] = "tdapiclient-endpoint-29"
>>> azmodel_deploy_kwargs["models"] = [model]
>>> azmodel_deploy_kwargs["workspace"] = ws
>>> azmodel_deploy_kwargs["inference_config"] = inference_config
>>> azmodel_deploy_kwargs["deployment_config"] = deployment_config
>>> azmodel_deploy_kwargs["overwrite"] = True

>>> # Deploying the model to Azure ML Compute cluster if the platform is az-webservice.
>>> webservice = automl_config.deploy(platform="az-webservice", model=model, model_type="",
>>>                         model_deploy_kwargs=azmodel_deploy_kwargs)
>>> webservice.wait_for_deployment(show_output=True)
>>> # Creating an options dictionary to pass the content_format for scoring.
>>> options = {}
>>> content_format = {}
>>> content_format["Inputs"] = [["%row"]]
>>> options["content_format"] = content_format
>>> print(webservice.predict(test_df, **options, mode="udf", content_type='json'))
......
......
```

## Documentation

General product information, including installation instructions, is available in the [Teradata Documentation website](https://docs.teradata.com/)

## License

Use of the Teradata Python Package is governed by the *License Agreement for the Teradata Sagemaker Python Library*.
After installation, the `LICENSE` and `LICENSE-3RD-PARTY` files are located in the `tdapiclient` directory of the Python installation directory.

