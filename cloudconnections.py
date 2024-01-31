#!/usr/bin/env python
import json, re, sys, os, json, subprocess, time, logging, requests, urllib3
import boto3

from subprocess import call, check_output
from requests.structures import CaseInsensitiveDict
urllib3.disable_warnings()
APPD_SECRET = os.getenv('APPD_SECRET')
APPD_CLIENTID = os.getenv('APPD_CLIENTID')
APPD_SECRET_BAS = os.getenv('APPD_SECRET_BAS')
APPD_CLIENTID_BAS = os.getenv('APPD_CLIENTID_BAS')
base_url = os.getenv('BASE_URL')
ten_name = os.getenv('TEN_NAME')
accesskey = os.getenv('AWS_ACCESS_KEY')
secretkey = os.getenv('AWS_SECRET_KEY')
awsAccId = os.getenv('AWS_ACC_ID')
azClientId = os.getenv('AZ_CLIENT_ID')
azClientSec = os.getenv('AZ_CLIENT_SECRET')
azTenantId = os.getenv('AZ_TENANT_ID')
azSubsId = os.getenv('AZ_SUBS_ID')

monuser = "AppDynamicsCloudMonitoringRole"
testAwsConfig="TestAWSConfig"
testAzureConfig="TestAzureConfig"

# delete cloud formation template
def aws_delete_cft():
    session = boto3.Session(region_name="us-west-2")
    cftclient = session.client('cloudformation')
    cftclient.delete_stack(StackName='rolecreate')

# deploy cloud formation template
def aws_deploy_cft(extId, accId):
    script_dir = os.path.dirname(__file__)
    print(script_dir)
    session = boto3.Session(region_name="us-west-2")
    cftclient = session.client('cloudformation')
    stack = ''
    with open(f"{script_dir}/cft.yaml", 'r') as fd:
        stack = fd.read()
    print(stack)
    params = [
        {
            'ParameterKey': 'AppDynamicsExternalId',
            'ParameterValue': "" + extId
        },
        {
            'ParameterKey': 'AppDynamicsAccountId',
            'ParameterValue': "" + accId
        },
        {
            'ParameterKey': 'AWSIAMRoleName',
            'ParameterValue': "" + monuser
        }
    ]
    capabilities = [
        'CAPABILITY_NAMED_IAM'
    ]
    #Uncomment this to deploy the template
    cftclient.create_stack(StackName='rolecreate', TemplateBody=stack, Parameters=params, Capabilities=capabilities)


    #Uncomment this to describe the status of the CFT deployment
    #print(cftclient.describe_stacks())


# get http token
def get_token(ten_id):
    tokenurl = base_url + "/auth/" + ten_id + "/default/oauth2/token"
    payload='grant_type=client_credentials&client_id=' + APPD_CLIENTID + '&client_secret=' + APPD_SECRET
    print(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", tokenurl, headers=headers, data=payload)
    print(response.json)
    token_json = response.json()
    appd_token = token_json['access_token']
    print(appd_token)
    return(appd_token)

# get token with Basic auth
def get_token_basic(ten_id):
    tokenurl = base_url + "/auth/" + ten_id + "/default/oauth2/token"
    #payload='grant_type=client_credentials&client_id=' + APPD_CLIENTID + '&client_secret=' + APPD_SECRET
    payload='grant_type=client_credentials'
    #print(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic c3J2XzNSWjRNbHlKbFRkZWlDbGNsNVp1MjM6emJPTkZYVnhnNTY0ZWJmTkNSYjZIOHBaQXhLdXJvVDhOUkl6MDBGajdzUQ=='
    }
    response = requests.request("POST", tokenurl, headers=headers, data=payload)
    print(response.json)
    token_json = response.json()
    appd_token = token_json['access_token']
    print(appd_token)
    return(appd_token)



# given tenant name, get ten id
def get_ten_id():
    tenurl = "https://observe-tenant-lookup-api.saas.appdynamics.com/tenants/lookup/" + ten_name

    print(tenurl)
    headers = {
      #  'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    response = requests.request("GET", tenurl, headers=headers)
    json_object = json.loads(response.text)
    ten_id = json_object['tenantId']
    print(ten_id)
    return(ten_id)

# get all tenant cloud connections
def get_all_connections(appd_token):
    url = base_url + "/cloud/v1/connections"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("All Connections:")
    print(json.dumps(json_object, indent = 3))

# get all aws cloud connections
def get_all_aws_connections(appd_token):
    url = base_url + "/cloud/v1/connections"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'filter': 'type eq "aws"'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("AWS Connections:")
    print(json.dumps(json_object, indent = 3))

# get all azure cloud connections
def get_all_azure_connections(appd_token):
    url = base_url + "/cloud/v1/connections"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'filter': 'type eq "azure"'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("Azure Connections:")
    print(json.dumps(json_object, indent = 3))

# create aws cloud connections with keys
def create_aws_connection_keys(appd_token, configid, accesskey, secretkey):
    url = base_url + "/cloud/v1/connections"
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
        "displayName": "TestAWSConnection",
        "description": "Description for this AWS access key connection without assigned configurationId",
        "type": "aws",
        "details": {
            "accessKeyId": "" + accesskey,
            "secretAccessKey": "" + secretkey,
            "accessType": "access_key"
        },
        "configurationId": configid
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response.text)

# create aws cloud connection with role
def create_aws_connection_role(appd_token, configid, awsAccId):
    url = base_url + "/cloud/v1/connections"
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
        "displayName": "TestAWSConnection",
        "description": "Description for this AWS role delegate connection without assigned configurationId",
        "type": "aws",
        "details": {
            "accountId": "" + awsAccId,
            "accessType": "role_delegation"
        },
        "configurationId": configid
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response.text)
    json_object = json.loads(response.text)
    return json_object['details']['externalId'], json_object['details']['appDynamicsAwsAccountId'], json_object['id']

# create azure cloud connection with subscription info
def create_azure_connection(appd_token, configid, clientId, clientSecret, tenantId, subsId):
    url = base_url + "/cloud/v1/connections"
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
        "displayName": "TestAzureConnection",
        "description": "Description for this Azure connection with assigned configurationId",
        "type": "azure",
        "details": {
            "clientId": "" + clientId,
            "clientSecret": "" + clientSecret,
            "tenantId": "" + tenantId,
            "subscriptionId": "" + subsId
        },
        "configurationId": configid
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response.text)
    json_object = json.loads(response.text)
    return json_object['id']

# update connection role name after its crteated in AWS
def update_role_name(appd_token, connId):
    url = base_url + "/cloud/v1/connections/" + connId
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
        "details": {
            "roleName" : "" + monuser
        }
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))
    print(response.text)

#activate cloud connection
def activate_connection(appd_token, connId):
    url = base_url + "/cloud/v1/connections/" + connId
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
            "state": "" + "ACTIVE"
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))
    print(response.text)

#get AWS connection by name
def get_aws_connection_by_name(appd_token):
    url = base_url + "/cloud/v1/connections"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'filter': 'type eq "aws" and displayName eq "TestAWSConnection"'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    return(json_object['items'][0]['id'])

#delete cloud connection, works for both AWS and azure
def delete_aws_connection(appd_token, conn_id):
    url = base_url + "/cloud/v1/connections/" + conn_id
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    response = requests.request("DELETE", url, headers=headers)
    print(response.text)

#get all cloud configs
def get_all_configurations(appd_token):
    url = base_url + "/cloud/v1/configurations"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("All Configurations:")
    print(json.dumps(json_object, indent = 3))

#get AWS cloud configs
def get_aws_configurations_by_name(appd_token):
    url = base_url + "/cloud/v1/configurations"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'filter': 'type eq "aws" and displayName eq "TestAWSConfig"'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    return(json_object['items'][0]['id'])

#get Azure cloud configs by name
def get_azure_configurations_by_name(appd_token):
    url = base_url + "/cloud/v1/configurations"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'filter': 'type eq "azure" and displayName eq "TestAzureConfig"'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    return(json_object['items'][0]['id'])

#get AWS cloud configs
def get_all_aws_configurations(appd_token):
    url = base_url + "/cloud/v1/configurations"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'filter': 'type eq "aws"'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("AWS Configurations:")
    print(json.dumps(json_object, indent = 3))

# get all Azure cloud configs
def get_all_azure_configurations(appd_token):
    url = base_url + "/cloud/v1/configurations"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'filter': 'type eq "azure"'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("Azure Configurations:")
    print(json.dumps(json_object, indent = 3))

# get all AWS services
def get_all_aws_services(appd_token):
    url = base_url + "/cloud/v1/services"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'type': 'aws'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("AWS Services:")
    print(json.dumps(json_object, indent = 3))

#get all azure services
def get_all_azure_services(appd_token):
    url = base_url + "/cloud/v1/services"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'type': 'azure'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("Azure Services:")
    print(json.dumps(json_object, indent = 3))

#get all aws cloud regions
def get_all_aws_regions(appd_token):
    url = base_url + "/cloud/v1/regions"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'type': 'aws'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("AWS Regions:")
    print(json.dumps(json_object, indent = 3))

#get all azure cloud regions
def get_all_azure_regions(appd_token):
    url = base_url + "/cloud/v1/regions"
    payload={}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + appd_token
    }
    params = {'type': 'azure'}
    response = requests.request("GET", url, params=params, headers=headers, data=payload)
    json_object = json.loads(response.text)
    print("Azure Regions:")
    print(json.dumps(json_object, indent = 3))


#create aws cloud config
def create_aws_config(appd_token):
    url = base_url + "/cloud/v1/configurations"
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
        "displayName": "TestAWSConfig",
        "type": "aws",
        "details": {
            "regions": [],
            "polling": {
                "interval": 5,
                "unit": "minute"
            },
            "services": [{
                "name": "ec2",
                "polling": {
                    "interval": 5,
                    "unit": "minute"
                }
            }],
            "importTags": {
                "enabled": "true",
                "excludedKeys": []
            }
        }
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response.text)

# delete aws cloud config
def delete_aws_config(appd_token, config_id):
    url = base_url + "/cloud/v1/configurations/" + config_id
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    response = requests.request("DELETE", url, headers=headers)
    print(response.text)

# create azure cloud config
def create_azure_config(appd_token):
    url = base_url + "/cloud/v1/configurations"
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': 'Bearer ' + appd_token
    }
    data = {
        "displayName": "TestAzureConfig",
        "type": "azure",
        "details": {
            "regions": [],
            "polling": {
                "interval": 5,
                "unit": "minute"
            },
            "services": [
                {
                    "name": "vm",
                    "polling": {
                        "interval": 5,
                        "unit": "minute"
                    }
                },
                {
                    "name": "lb",
                    "polling": {
                        "interval": 5,
                        "unit": "minute"
                    },
                },
                {
                    "name": "disk",
                    "polling": {
                        "interval": 5,
                        "unit": "minute"
                    },
                },
                {
                    "name": "postgresql",
                    "polling": {
                        "interval": 5,
                        "unit": "minute"
                    },
                }
            ],
            "importTags": {
                "enabled": "true",
                "excludedKeys": []
            }
        }
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response.text)

ten_id=get_ten_id()
#appd_token = get_token(ten_id)
appd_token = get_token_basic(ten_id)

#Configurations
#get_all_configurations(appd_token)
#get_all_aws_configurations(appd_token)
#get_all_azure_configurations(appd_token)
#create_aws_config(appd_token)
#create_azure_config(appd_token)

#Connections
#get_all_connections(appd_token)
#get_all_aws_connections(appd_token)
#get_all_azure_connections(appd_token)
#config_id = get_aws_configurations_by_name(appd_token)
#create_aws_connection_keys(appd_token,config_id, accesskey, secretkey)
#extId, accId, connId = create_aws_connection_role(appd_token,config_id, awsAccId)
#print(extId, accId, connId)
#aws_deploy_cft(extId, accId)
#aws_delete_cft()
#Wait or AWS role to be created before you update in AppD
#update_role_name(appd_token, connId)
#activate_connection(appd_token, connId)

#config_id=get_azure_configurations_by_name(appd_token)
#connId=create_azure_connection(appd_token, config_id, azClientId, azClientSec, azTenantId, azSubsId)
#activate_connection(appd_token, connId)

#Services
#get_all_aws_services(appd_token)
#get_all_azure_services(appd_token)

#Regions
#get_all_aws_regions(appd_token)
#get_all_azure_regions(appd_token)

#Deletes
#config_id = get_aws_configurations_by_name(appd_token)
#delete_aws_config(appd_token, config_id)
#config_id = get_azure_configurations_by_name(appd_token)
#print(config_id)
#delete_azure_config(config_id)
#config_id = get_aws_connection_by_name(appd_token)
#delete_aws_connection(appd_token, config_id)

