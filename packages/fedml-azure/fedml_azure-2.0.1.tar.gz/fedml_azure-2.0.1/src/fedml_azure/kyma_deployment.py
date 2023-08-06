import os,shutil,subprocess,json,io
from pkg_resources import resource_filename
from ruamel.yaml import YAML
from .logger import Logger
from .script_generator import _generate_model_config,_get_image_details,_generate_dockerfile,_generate_main_file
try:
    from azureml.core import Workspace
except:
    pass

def _check_file_exists(file_path):
    logger = Logger.get_instance()
    try:
        return os.path.exists(file_path)
    except Exception as e:
        logger.error(e)
        raise

def _check_dir_exists(dir_path):
    logger = Logger.get_instance()
    try:
        return os.path.isdir(dir_path)
    except Exception as e:
        logger.error(e)
        raise

def _create_files(path,access_rights):
    logger = Logger.get_instance()
    try:
        os.makedirs(path, access_rights, exist_ok=True)
    except OSError:
        logger.error("Creation of the directory %s failed.",path)
        raise

def _get_cluster_name(kubeconfig_path):
    logger = Logger.get_instance()
    try:
        with open(kubeconfig_path,'r') as fp:
            kubeconfig_details = YAML().load(fp)
        return kubeconfig_details['clusters'][0]['name']
    except Exception as e:
        logger.error(e)
        raise

def _get_service_principal_credentials(sp_path):
    logger = Logger.get_instance()
    try:
        with open(sp_path, 'r') as f:
            sp_credentials = json.load(f)
        return sp_credentials["SERVICE_PRINCIPAL_ID"],sp_credentials["SERVICE_PRINCIPAL_PASSWORD"]
    except Exception as e:
        logger.error("Unable to get service principal credentials from file %s. Check if SERVICE_PRINCIPAL_ID and SERVICE_PRINCIPAL_PASSWORD keys are specifed in the %s file.",sp_path,sp_path)
        logger.error(e)
        raise
    

def _create_deploy_folder(deploy_folder,models,entry_script,workspace,environment,kubeconfig_path,source_directory):
    logger = Logger.get_instance()
    try:
        source_directory_name=None
        logger.info("Creating deployment folder %s.",deploy_folder)
        directory=deploy_folder+"/azureml-app/azureml-models/"
        access_rights = 0o755

        for model in models:
            model_name,model_version=model.name,str(model.version)
            model_path=directory+model_name+'/'+model_version+'/'
            _create_files(model_path,access_rights)
            model.download(target_dir=model_path,exist_ok=True)
        
        if source_directory is not None:
            source_directory_name=source_directory.rstrip('/').split('/')[-1]
            shutil.copytree(source_directory, deploy_folder+'/azureml-app/'+source_directory_name, symlinks = True)
            _generate_main_file(source_directory_name,source_directory_name+'/'+entry_script,deploy_folder+'/azureml-app/main.py')
        else:
            entry_script_name=entry_script.rstrip('/').split('/')[-1]
            shutil.copy(entry_script, deploy_folder+'/azureml-app/'+entry_script_name)
            shutil.copy(entry_script, deploy_folder+'/azureml-app/main.py')
        
        shutil.copy(kubeconfig_path,deploy_folder) 
        _generate_model_config(workspace,deploy_folder+'/azureml-app/model_config_map.json')
        logger.info("Successfully created deployment folder %s.",deploy_folder)
        logger.info("Creating docker file for deployment.")
        _generate_dockerfile(models,environment,workspace,entry_script,deploy_folder+'/Dockerfile',source_directory_name)
        logger.info("Successfully created docker file for kyma deployment.")

    except shutil.SameFileError:
        pass

    except Exception as e:
            logger.error(e)
            raise

def _run_script(cmd):
    logger = Logger.get_instance()
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
            logger.info(line)
        p.stdout.close()
        p.wait() 
        return p.returncode
    except Exception as e:
        logger.error(e)
        raise
    
def _delete_folder(foldername):
    logger = Logger.get_instance()
    try:
        logger.info("Deleting the deploy folder '%s'.",foldername)
        shutil.rmtree(foldername)
    except Exception as e:
        logger.error(e)
        raise

def _kyma_deploy(inference_config_args,deploy_args):
    logger = Logger.get_instance()
    try:
        overwrite_service,num_replicas,source_directory="false",1,None

        if 'entry_script' not in inference_config_args or 'environment' not in inference_config_args:
            raise Exception("The keys 'entry_script','environment' must be specified in the parameter 'inference_config_args'.")
        
        if 'workspace' not in deploy_args or 'name' not in deploy_args or 'models' not in deploy_args:
            raise Exception("The keys 'workspace', 'name' and 'models' must be specified in the parameter 'deploy_args'.")
        
        if 'kubeconfig_path' not in deploy_args:
            raise Exception("The key 'kubeconfig_path' must be specified in the parameter 'deploy_args'. The parameter must contain the file path to 'kubeconfig.yml' file.")
        
        if 'sp_config_path' not in deploy_args:
            raise Exception("The key 'sp_config_path' must be specified in the parameter 'deploy_args'. This parameter must contain the file path to 'sp_config.json' file.")
        
        if not isinstance(deploy_args['workspace'],Workspace):
            raise Exception("The key 'workspace' in the parameter 'deploy_args' must be of type class 'Workspace'.")
        
        if not isinstance(deploy_args['models'],list):
            raise Exception("The key 'models' specified in the parameter 'deploy_args' must be of type list.")
        
        if not _check_file_exists(deploy_args["kubeconfig_path"]):
            raise Exception("The file 'kubeconfig.yml' not found in path {}.".format(deploy_args["kubeconfig_path"]))
        
        if not _check_file_exists(deploy_args["sp_config_path"]):
            raise Exception("The file 'sp_config.json' not found in path {}.".format(deploy_args["sp_config_path"]))
        
        if 'overwrite_service' in deploy_args and deploy_args['overwrite_service'] is True:
            logger.info("The parameter deploy_args['overwrite_service'] has been set to True. This will replace the existing service.")
            overwrite_service="true"
        
        if 'num_replicas' in deploy_args:
            if not isinstance(deploy_args['num_replicas'],int):
                raise Exception("The key 'num_replicas' specified in the parameter 'deploy_args' must be of type int.")
            num_replicas=deploy_args['num_replicas']

        if 'source_directory' in inference_config_args:
            if not _check_dir_exists(inference_config_args["source_directory"]):
                raise Exception("The source_directory path {} passed in inference_config_args['source_directory'] not found.".format(inference_config_args["source_directory"]))
            
            script_path=inference_config_args["source_directory"].rstrip('/')+'/'+inference_config_args['entry_script']

            if not _check_file_exists(script_path):
                raise Exception("Entry script {} not found in source_directory {}. entry_script should be path relative to current working directory.".format(script_path,inference_config_args["source_directory"]))

            source_directory=inference_config_args["source_directory"]
        
        else:

            if not _check_file_exists(inference_config_args['entry_script']):
                raise Exception("The filepath {} specified in inference_config_args['entry_script'] not found.".format(inference_config_args['entry_script']))

        deploy_folder="deployments/"+deploy_args['name']

        if _check_dir_exists(deploy_folder):
            logger.info("The deploy directory %s already exists. Deleting it.",deploy_folder)
            _delete_folder(deploy_folder)

        #installs kubectl,jq and checks if the service name already exists
        install_validate_script_path = resource_filename(__name__, "install_validate.sh")
        install_result=_run_script(["bash",install_validate_script_path,deploy_args['name'],deploy_args['kubeconfig_path'],overwrite_service])
        if install_result==1:
            raise Exception("The service name '{}' already exists. Please provide a different 'name' for the parameter deploy_args['name']. If you want the service and deployment to be replaced, set the parameter deploy_args['overwrite_service']  to 'True'".format(deploy_args['name']))

        #creates the folders required for deployment
        _create_deploy_folder(deploy_folder,deploy_args['models'],inference_config_args['entry_script'],deploy_args['workspace'],inference_config_args['environment'],deploy_args['kubeconfig_path'],source_directory)

        registry=_get_image_details(inference_config_args['environment'],deploy_args['workspace'])[1]
        cluster_name=_get_cluster_name(deploy_args["kubeconfig_path"])
        service_principal_id,service_principal_password=_get_service_principal_credentials(deploy_args["sp_config_path"])
        kubeconfig_file_name=deploy_args["kubeconfig_path"].split('/')[-1]

        #calls the kyma_deploy.sh script
        kyma_deploy_script_path = resource_filename(__name__, "kyma_deploy.sh")
        deploy_result=_run_script(['bash',kyma_deploy_script_path,service_principal_id,service_principal_password,registry,deploy_args['name'],deploy_folder,kubeconfig_file_name,cluster_name,str(num_replicas)])
        if deploy_result==0:
            _delete_folder(deploy_folder)
            return "https://"+deploy_args['name']+"."+cluster_name+"/score"
        else:
            raise Exception("Deployment to kyma failed. Refer the deployment logs for more details.")
        
    except Exception as e:
        logger.error(e)
        raise