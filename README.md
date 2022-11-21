# Monitor public cloud assets with Cloud Connections to AppD Cloud 
## Contents
        Use Cases
        Pre-requisites, Guidelines
        Python Cloud Connections Client
        Cloud Configuration Lifecycle
        Cloud Connections Lifecycle
        Observe public cloud assets in AppDynamics Cloud
        De-provisioning

### Use Cases
        * As a Cloud Admin, automate cloud connections to AWS leveraging AppD 
        Cloud Connections API to pull metrics data from AWS Services (Load 
        Balancers, Storage, Hosts, Databases)

        * As a Cloud Admin, automate cloud connections to Azure Cloud 
        leveraging AppD Cloud Connections API to pull metrics data from Azure 
        Services (Load Balancers, Storage, Hosts)

        * As DevOps, monitor cloud resources and usage for one or more of 
        your cloud native apps

        
![alt text](https://github.com/prathjan/images/blob/main/connxmain.png?raw=true)

### Pre-requisites, Guidelines
1. Requires a AWS Cloud account to set up AWS Cloud Connection. Following cloud specific data is needed to set up cloud connections:

        * AWS Account ID
        * AWS Access Key and AWS Secret key with API access
        * AppDynamics Client ID and Secret

2. Requires a Azure Cloud account to set up Azure Cloud Connection. Following cloud specific data is needed to set up cloud connections:

        * Azure Cloud Subscription ID
        * Azure Cloud Tenant ID
        * Azure Cloud Client ID and Secret

### Python Cloud Connections Client

Check out a sample python client to exercise the Cloud Connections API here: https://github.com/CiscoDevNet/connxapi/blob/main/cloudconnections.py.
Before running the python client, set up the following environment variables (sample values displayed):

        * APPD_CLIENTID="srv_xxxxxxxxxx"
        * APPD_SECRET="xxxxxxxx"
        * AWS_ACC_ID="xxxxxxxxxx"
        * BASE_URL="xxxxxxx", eg."https://cisco-devnet.observe.appdynamics.com"
        * TEN_NAME="xxxxxx", eg."cisco-devnet.observe.appdynamics.com"
        * AZ_CLIENT_ID="xxxxxxx"
        * AZ_CLIENT_SECRET="xxxxxxxx"
        * AZ_TENANT_ID="xxxxxxxxxx"
        * AZ_SUBS_ID="xxxxxxxxxxx"

 Try the API's referenced in the following sections.


### Cloud Configuration Lifecycle

Please refer to the following devnet resource for a complete API definition: https://developer.cisco.com/docs/appdynamics/cloud-connection/.

Some of the API's included in the sample python client are as follows and accounts for the configuration object lifecycle. 

        * List All Configurations

        * List AWS Configurations

        * Create AWS Configuration

        * List Azure Configurations

        * Create Azure Configuration

        * Get Configuration ID by Name

        * Update Configuration

        * Delete Configuration


### Cloud Connections Lifecycle

Please refer to the follwing devnet resources for a complete API definition: https://developer.cisco.com/docs/appdynamics/cloud-connection/.

Some of the API's included in the sample python client are as follows and accounts for the connection object lifecycle. 

* List All Connections

* List AWS/Azure Connections

* List AWS/Azure Connections filtered by name

* Get connection by conn ID

* Create AWS/Azure Access Key Connection

* Create AWS Role Delegation 

* Add AWS Conn Role

* Configure the connection

* Enable/Disable connection

* Delete Connections


### Observe public cloud assets in AppDynamics Cloud

After a successful cloud connection with your AWS/Azure account, you can view the metrics for the services you enabled in your cloud configuration:

* Summary:

![alt text](https://github.com/prathjan/images/blob/main/summobserve.png?raw=true)

* Hosts:

![alt text](https://github.com/prathjan/images/blob/main/hosts.png?raw=true)

* Load Balancers:

![alt text](https://github.com/prathjan/images/blob/main/lbs.png?raw=true)

* Storage

![alt text](https://github.com/prathjan/images/blob/main/storage.png?raw=true)

* Database

![alt text](https://github.com/prathjan/images/blob/main/dbs.png?raw=true)

### De-provisioning

* Use Delete HTTP requests to delete the cloud connections. This will automativally delete the corresponding configuration objects.

