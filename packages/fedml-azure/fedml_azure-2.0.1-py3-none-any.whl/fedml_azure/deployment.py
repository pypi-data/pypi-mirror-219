import urllib.request,json,os,ssl
from .kyma_deployment import _kyma_deploy
from .logger import Logger
try:
    import sklearn
    from azureml.core.model import InferenceConfig
    from azureml.core.webservice import AciWebservice,LocalWebservice,AksWebservice
    from azureml.core.model import Model
    from azureml.core.resource_configuration import ResourceConfiguration
except:
    pass

def _get_inference_config(entry_script=None, runtime=None, conda_file=None, extra_docker_file_steps=None, source_directory=None, enable_gpu=None, description=None, base_image=None, base_image_registry=None, cuda_version=None, environment=None):

    logger = Logger.get_instance()
    try:
        if entry_script is None:
            raise Exception("The parameter 'entry_script' must be specified.")
        
        return InferenceConfig(entry_script=entry_script,
                               runtime=runtime,
                               conda_file=conda_file,
                               extra_docker_file_steps=extra_docker_file_steps,
                               source_directory=source_directory,
                               enable_gpu=enable_gpu,
                               description=description,
                               base_image=base_image,
                               base_image_registry=base_image_registry,
                               cuda_version=cuda_version,
                               environment=environment
                               )

    except Exception as e:
        logger.error(e)
        raise

def _get_aci_deploy_configuration(cpu_cores=None, memory_gb=None, tags=None, properties=None, description=None, location=None, auth_enabled=None, ssl_enabled=None, enable_app_insights=None, ssl_cert_pem_file=None, ssl_key_pem_file=None, ssl_cname=None, dns_name_label=None, primary_key=None, secondary_key=None, collect_model_data=None, cmk_vault_base_url=None, cmk_key_name=None, cmk_key_version=None, vnet_name=None, subnet_name=None):
    
    logger = Logger.get_instance()
    try:
        return AciWebservice.deploy_configuration(cpu_cores=cpu_cores,
                                                  memory_gb=memory_gb,
                                                  tags=tags,
                                                  properties=properties,
                                                  description=description,
                                                  location=location,
                                                  auth_enabled=auth_enabled,
                                                  ssl_enabled=ssl_enabled,
                                                  enable_app_insights=enable_app_insights,
                                                  ssl_cert_pem_file=ssl_cert_pem_file,
                                                  ssl_key_pem_file=ssl_key_pem_file,
                                                  ssl_cname=ssl_cname,
                                                  dns_name_label=dns_name_label,
                                                  primary_key=primary_key,
                                                  secondary_key=secondary_key,
                                                  collect_model_data=collect_model_data,
                                                  cmk_vault_base_url=cmk_vault_base_url,
                                                  cmk_key_name=cmk_key_name,
                                                  cmk_key_version=cmk_key_version,
                                                  vnet_name=vnet_name,
                                                  subnet_name=subnet_name
                                                  )

    except Exception as e:
        logger.error(e)
        raise

def _get_aks_deploy_configuration(autoscale_enabled=None, autoscale_min_replicas=None, autoscale_max_replicas=None, autoscale_refresh_seconds=None, autoscale_target_utilization=None, collect_model_data=None, auth_enabled=None, cpu_cores=None, memory_gb=None, enable_app_insights=None, scoring_timeout_ms=None, replica_max_concurrent_requests=None, max_request_wait_time=None, num_replicas=None, primary_key=None, secondary_key=None, tags=None, properties=None, description=None, gpu_cores=None, period_seconds=None, initial_delay_seconds=None, timeout_seconds=None, success_threshold=None, failure_threshold=None, namespace=None, token_auth_enabled=None, compute_target_name=None, cpu_cores_limit=None, memory_gb_limit=None):
    logger = Logger.get_instance()
    try:
        return AksWebservice.deploy_configuration(autoscale_enabled=autoscale_enabled,
                                                  autoscale_min_replicas=autoscale_min_replicas,
                                                  autoscale_max_replicas=autoscale_max_replicas,
                                                  autoscale_refresh_seconds=autoscale_refresh_seconds,
                                                  autoscale_target_utilization=autoscale_target_utilization,
                                                  collect_model_data=collect_model_data,
                                                  auth_enabled=auth_enabled,
                                                  cpu_cores=cpu_cores,
                                                  memory_gb=memory_gb,
                                                  enable_app_insights=enable_app_insights,
                                                  scoring_timeout_ms=scoring_timeout_ms,
                                                  replica_max_concurrent_requests=replica_max_concurrent_requests,
                                                  max_request_wait_time=max_request_wait_time,
                                                  num_replicas=num_replicas,
                                                  primary_key=primary_key,
                                                  secondary_key=secondary_key,
                                                  tags=tags,
                                                  properties=properties,
                                                  description=description,
                                                  gpu_cores=gpu_cores,
                                                  period_seconds=period_seconds,
                                                  initial_delay_seconds=initial_delay_seconds,
                                                  timeout_seconds=timeout_seconds,
                                                  success_threshold=success_threshold,
                                                  failure_threshold=failure_threshold,
                                                  namespace=namespace,
                                                  token_auth_enabled=token_auth_enabled,
                                                  compute_target_name=compute_target_name,
                                                  cpu_cores_limit=cpu_cores_limit,
                                                  memory_gb_limit=memory_gb_limit
                                                  )

    except Exception as e:
        logger.error(e)
        raise

def _get_local_deploy_configuration(port=None):
    logger = Logger.get_instance()
    try:
        return LocalWebservice.deploy_configuration(port=port)
    
    except Exception as e:
        logger.error(e)
        raise
    

def _get_deploy_configuration(compute_type=None,deploy_config_args=None):
    logger = Logger.get_instance()
    try:
        if compute_type is None:
            raise Exception("The parameter 'compute_type' must be specified")
        
        if compute_type.lower()=='aci':
            return _get_aci_deploy_configuration(**deploy_config_args) if deploy_config_args is not None else _get_aci_deploy_configuration()
        
        elif compute_type.lower()=='aks':
            return _get_aks_deploy_configuration(**deploy_config_args) if deploy_config_args is not None else _get_aks_deploy_configuration()
        
        elif compute_type.lower()=='local':
            return _get_local_deploy_configuration(**deploy_config_args) if deploy_config_args is not None else _get_local_deploy_configuration()
        
        else:
            raise Exception("The specified 'compute_type' is not supported. The supported compute_type are 'ACI', 'AKS' and 'Local'.")

    except Exception as e:
        logger.error(e)
        raise

def _get_webservice(workspace=None, name=None, models=None, inference_config=None, deployment_config=None, deployment_target=None, overwrite=False, show_output=False):
    logger = Logger.get_instance()
    try:
        if workspace is None or name is None or models is None:
            raise Exception("The parameters 'workspace', 'name' and 'models' must be specified.")
        
        if not isinstance(models,list) or len(models)==0:
            raise Exception("The parameter 'models' must be of type 'list' and must contain atleast one model object.")

        return Model.deploy(workspace=workspace,
                            name=name,
                            models=models,
                            inference_config=inference_config,
                            deployment_config=deployment_config,
                            deployment_target=deployment_target,
                            overwrite=overwrite,
                            show_output=show_output)

    except Exception as e:
        logger.error(e)
        raise

def _create_resource_config(cpu=None, memory_in_gb=None, gpu=None):
    logger = Logger.get_instance()
    try:
        return ResourceConfiguration(cpu=cpu, 
                                        memory_in_gb=memory_in_gb, 
                                        gpu=gpu)
    except Exception as e:
        logger.error(e)
        raise

def _register_model(workspace=None, model_path=None, model_name=None, tags=None, properties=None, description=None, datasets=None, model_framework=None, model_framework_version=None, child_paths=None, sample_input_dataset=None, sample_output_dataset=None, resource_configuration=None):
    logger = Logger.get_instance()
    try:

        if workspace is None:
            raise Exception("The parameter 'workspace' must be specified in model_args.")
        
        if model_path is None:
            raise Exception("The parameter 'model_path' must be specified in model_args.")
        
        if model_name is None:
            raise Exception("The parameter 'model_name' must be specified in model_args.")

        return Model.register(workspace=workspace,
                              model_path=model_path,
                              model_name=model_name,
                              tags=tags,
                              properties=properties,
                              description=description,
                              datasets=datasets,
                              model_framework=model_framework,
                              model_framework_version=model_framework_version,
                              child_paths=child_paths,
                              sample_input_dataset=sample_input_dataset,
                              sample_output_dataset=sample_output_dataset,
                              resource_configuration=resource_configuration)
                              
    except Exception as e:
        logger.error(e)
        raise
    
def register_model(model_args,resource_config_args=None,is_sklearn_model=False):

    logger = Logger.get_instance()
    try:
        logger.info("Registering the model")
        if is_sklearn_model:
            logger.info("Configuring parameters for sklearn model")
            model_args["model_framework"]=Model.Framework.SCIKITLEARN
            if 'model_framework_version' not in model_args:
                model_args["model_framework_version"]=sklearn.__version__

        if resource_config_args is not None:
            if isinstance(resource_config_args,dict):
                model_args["resource_configuration"]=_create_resource_config(**resource_config_args)
            else:
                raise Exception("The parameter 'resource_config' must be of type 'dict'.")

        return _register_model(**model_args)


    except Exception as e:
        logger.error(e)
        raise

def deploy(compute_type=None,deploy_args=None,inference_config_args=None,deploy_config_args=None):

    logger = Logger.get_instance()
    try:
        inference_config,deployment_config,api_key,endpoint_url=None,None,None,None

        if compute_type is None:
            raise Exception("The parameter 'compute_type' must be specified.The supported compute_type are 'ACI', 'AKS', 'Local' and 'Kyma'.")

        if deploy_args is None or not isinstance(deploy_args,dict):
            raise Exception("The parameter 'deploy_args' must be specified and should be of type 'dict'.")
        
        if compute_type.lower()=="kyma":
            return _kyma_deploy(inference_config_args,deploy_args)
        
        if inference_config_args is not None:
            inference_config=_get_inference_config(**inference_config_args)
        else:
            logger.info("The parameter 'inference_config_args' is not specified. It is recommended to pass the parameter 'inference_config_args' with the appropriate arguments.")

        if deploy_config_args is None:
            logger.info("The parameter 'deploy_config_args' is not specified. An empty configuration object will be used based on the desired target.")


        deployment_config=_get_deploy_configuration(compute_type,deploy_config_args)
        deploy_args['inference_config'],deploy_args['deployment_config']=inference_config,deployment_config
        service=_get_webservice(**deploy_args)
        service.wait_for_deployment(show_output=True)
        endpoint_url=service.scoring_uri
        logger.info("The service endpoint url is %s.",endpoint_url)

        if compute_type.lower()=='aks':
            api_key=service.get_keys()[0]
            logger.info("The service api key is %s.",api_key)

        return endpoint_url,api_key,service
    
    except TypeError as t:
        t_str=str(t)
        argument='inference_config_args' if '_get_inference_config' in t_str else ('deploy_config_args' if '_deploy_configuration' in t_str else ('deploy_args' if '_get_webservice' in t_str else ''))
        logger.error("Try specifying the correct parameters and correct parameter values for the %s argument",argument)
        logger.error(t)
        raise
        
    except Exception as e:
        logger.error(e)
        raise


def predict(data,compute_type=None,api_key=None,allowed=True,service=None,endpoint_url=None):
    
    logger = Logger.get_instance()
    try:
        if service is not None:
            logger.info("Using the webservice for inferencing. It can be used for compute types ACI, AKS and Local. ")
            return service.run(data)

        else:
            logger.info("Using the parameters 'endpoint_url' and 'compute_type' for inferencing.")

            if endpoint_url is None or compute_type is None:
                raise Exception("The parameters 'endpoint_url' and 'compute_type'  needs to be passed as parameter 'service' is not passed. ")

            if compute_type.lower()=='aks' or compute_type.lower()=='aci':
                # bypass the server certificate verification on client side
                if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                    ssl._create_default_https_context = ssl._create_unverified_context

            body = str.encode(data)
            url,apikey = endpoint_url,''

            if compute_type.lower()=='aks':
                if api_key is None:
                    raise Exception("The parameter 'api_key' must be passed for compute_type 'aks'.")
                apikey = api_key

            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ apikey)}
            req = urllib.request.Request(url, body, headers)


            response = urllib.request.urlopen(req)
            result = response.read()
            try:
                res=json.loads(json.loads(result))
                return res
            except Exception as e:
                logger.info("Deserialization of result failed. The result returned is of type byte array.")
                logger.info(e)
                return result       

    except urllib.error.HTTPError as error:
        logger.error("The request failed with status code: %s",str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        logger.error(error.info())
        logger.error(error.read())
    
    except Exception as e:
        logger.error(e)
        raise