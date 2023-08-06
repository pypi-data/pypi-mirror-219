#!/usr/bin/env bash

#service principal id of the user
SERVICE_PRINCIPAL_ID="$1"
#service principal password
SERVICE_PRINCIPAL_PASSWORD="$2"
#name of azure container registry
ACR_NAME="$3"
#name of image to be created
IMAGE_NAME="$4"
#name of the service to be created for deployment
SERVICE_NAME="$4"
#path of the deployment scripts
SCRIPT_PATH="$5"
#name of the kubeconfig file
KUBECONFIG_FILE="$6"
#name of the cluster
CLUSTER_NAME="$7"
#number of replicas
NUM_REPLICAS="$8"

export KUBECONFIG=${SCRIPT_PATH}/${KUBECONFIG_FILE}

function kyma_deploy()
{
cat<< EOF | kubectl apply --validate=false -n $deploy_namespace -f -
apiVersion: v1
kind: Service
metadata:
  name: ${SERVICE_NAME}
  namespace: ${deploy_namespace}
  labels:
    run: ${SERVICE_NAME}
spec:
  ports:
  - name: http
    port: 5001
    protocol: TCP
  selector:
    run: ${SERVICE_NAME}

---

apiVersion: gateway.kyma-project.io/v1alpha1
kind: APIRule
metadata:
  name: ${SERVICE_NAME}-api-rule
spec:
  gateway: kyma-gateway.kyma-system.svc.cluster.local
  service:
    name: ${SERVICE_NAME}
    port: 5001
    host: ${SERVICE_NAME}
  rules:
    - path: /.*
      methods: ["GET", "POST"]
      mutators: []
      accessStrategies:
        - handler: allow
          config: {}
          
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${SERVICE_NAME}
  namespace: ${deploy_namespace}
spec:
  replicas: ${NUM_REPLICAS}
  ports:
    - name: http
      port: 5001
  selector:
    matchLabels:
      run: ${SERVICE_NAME}
  template:
    metadata:
      labels:
        run: ${SERVICE_NAME}
    spec:
      containers:
        - image: ${acr_image}
          name: ${SERVICE_NAME}
          imagePullPolicy: Always
          ports:
            - containerPort: 5001
      imagePullSecrets:
        - name: ${secret_name}
EOF

kubectl rollout status deployment/${SERVICE_NAME}
if [ $? -ne 0 ]; then
    echo "Deployment failed. Common issue could be incorrect SERVICE_PRINCIPAL_ID or SERVICE_PRINCIPAL_PASSWORD passed in deploy_args['sp_config_path'] parameter."
    kubectl describe deployment ${SERVICE_NAME}
    exit 1
else
  echo "The scoring uri is https://${SERVICE_NAME}.${CLUSTER_NAME}/score"
fi
}

function assign_acr_pull_role()
{
    acr_registry_id=$(az acr show --name $ACR_NAME --query id --output tsv)
    acr_pull_access=$(az role assignment list --assignee $SERVICE_PRINCIPAL_ID --scope $acr_registry_id --role acrpull --query "[].principalName" --output tsv)
    if [ $? -ne 0 ]; then
          echo "Ensure the Service principal is created and the SERVICE_PRINCIPAL_ID passed in deploy_args['sp_config_path'] parameter is correct. Check the error for more details."
          exit 1
    fi

    if  ! [[ $acr_pull_access ]]; then
        echo "Assigning the 'acrpull' role to the service principal $SERVICE_PRINCIPAL_ID to access the registry $acr_registry_id ."
        az role assignment create --assignee $SERVICE_PRINCIPAL_ID --scope $acr_registry_id --role acrpull
        if [ $? -ne 0 ]; then
          echo "Assigning the 'acrpull' role to the service principal $SERVICE_PRINCIPAL_ID to access the registry $acr_registry_id failed."
          echo "Assign the 'acrpull' role to the service principal $SERVICE_PRINCIPAL_ID to access the registry $acr_registry_id using the Azure Portal."
          exit 1
        else
          echo "Successfully assigned 'acrpull' role to the service principal $SERVICE_PRINCIPAL_ID to access the registry $acr_registry_id ."
        fi
    else
      echo "The 'acrpull' role to the service principal $SERVICE_PRINCIPAL_ID to access the registry $acr_registry_id already exists."
    fi
}

function update_secret()
{
      echo "Updating the secret $secret_name password."
      kubectl -n $deploy_namespace delete secret $secret_name
      kubectl create secret docker-registry ${secret_name} --docker-server=$ACR_NAME --docker-username=${SERVICE_PRINCIPAL_ID} --docker-password=${SERVICE_PRINCIPAL_PASSWORD} -n ${deploy_namespace} 
      if [ $? -ne 0 ]; then
          echo "Creation of secret with name $secret_name for acr registry $ACR_NAME in the namespace $deploy_namespace failed."
          exit 1
      fi
      echo "Successfully updated $secret $secret_name."
}


function create_secret()
{
    secret_name=$(echo ${ACR_NAME}-${SERVICE_PRINCIPAL_ID}-secret)
    echo "Searching if the secret $secret_name exists in namespace $deploy_namespace."
    secret_exists=$(kubectl -n $deploy_namespace get secret -o json | jq -r ".items[].metadata.name" | grep -E "^${secret_name}$")
    if  ! [[ $secret_exists ]]; then
        echo "Creating secret with name $secret_name for acr registry $ACR_NAME in the namespace $deploy_namespace."
        kubectl create secret docker-registry ${secret_name} --docker-server=${ACR_NAME} --docker-username=${SERVICE_PRINCIPAL_ID} --docker-password=${SERVICE_PRINCIPAL_PASSWORD}  -n ${deploy_namespace} 
        if [ $? -ne 0 ]; then
          echo "Creation of secret with name $secret_name for acr registry $ACR_NAME in the namespace $deploy_namespace failed."
          exit 1
        fi
        echo "Secret $secret_name for acr registry $ACR_NAME created in the namespace $deploy_namespace."
    else
        dockerconfig=$(kubectl -n $deploy_namespace get secret $secret_name -o json | jq '.data[".dockerconfigjson"]'| base64 -di)
        if [ $? -ne 0 ]; then
            echo "Could not retrieve the secret $secret_name credentials. Updating the secret with current password."
            update_secret
            return 0
        fi
        sp_password=$(echo $dockerconfig | jq --arg acr $ACR_NAME '.auths[$acr]["password"]')
        if [ $? -ne 0 ]; then
            echo "Could not retrieve the secret $secret_name password. Updating the secret with current password."
            update_secret
            return 0
        fi
        
        if [ \"${SERVICE_PRINCIPAL_PASSWORD}\" == "$sp_password" ]; then
          echo "Using the same secret $secret_name for the deployment."
        else
            update_secret
        fi
    fi
    return 0
}


#Push the image to ACR
echo "Building and pushing the docker image to acr."
timestamp=$(date +%s%3N)
acr_image=$(echo ${ACR_NAME}/fedml/fedml_${timestamp})
az acr build  --registry ${ACR_NAME} --image ${acr_image} ${SCRIPT_PATH}
if [ $? -ne 0 ]; then
  echo "Build and push to ACR failed. Ensure that the command 'az login --use-device-code' has been run for interactive authentication."
  exit 1
fi

#Getting the namespace and current context to deploy to
deploy_namespace=$(kubectl config view --minify --output 'jsonpath={..namespace}'; echo)
if [ $? -ne 0 ]; then
  echo "Failed to retrieve the kubectl config."
  exit 1
fi
[ -z "$deploy_namespace" ] && deploy_namespace=$(echo 'default')

#check if a deploy namespace exists if not creates it
echo "Checking if the deploy namespace $deploy_namespace exists."
deploy_namespace_exists=$(kubectl get namespaces -o json | jq -r ".items[].metadata.name" | grep -E "^${deploy_namespace}$")
if [ $? -ne 0 ]; then
  echo "Failed to check if the deploy namespace exists."
  exit 1
fi

if  ! [[ $deploy_namespace_exists ]]; then
    echo "Creating deploy namespace $deploy_namespace."
    kubectl create namespace $deploy_namespace
    if [ $? -ne 0 ]; then
      echo "Failed to create namespace $deploy_namespace."
      exit 1
    fi
    echo "Namespace deploy $deploy_namespace created."
else
  echo "Using existing deploy namespace $deploy_namespace."
fi

#Adding ACR Pull role to Service Principal to access ACR
assign_acr_pull_role

#Check if the secret exists. if it exists use it or create a new secret. If the updated secret password is passed then it is updated.
create_secret

#deploy to kyma
kyma_deploy
exit 0



    


  




