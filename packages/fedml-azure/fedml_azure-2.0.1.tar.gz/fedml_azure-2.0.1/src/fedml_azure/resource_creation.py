from .compute_creation import ComputeFactory
from .environment_creation import EnvironmentFactory 
from .logger import Logger  
try:
    from azureml.core import Workspace 
except:
    pass

def create_workspace(workspace_args):
    logger = Logger.get_instance()
    try:
        if not isinstance(workspace_args,dict):
            raise Exception("The parameter 'workspace_args' must be of type 'dict'.")
        
        return _get_existing_workspace(**workspace_args)
    
    except TypeError as t:
        logger.error("Specify the correct parameters and correct parameter values for 'workspace_args'.")
        logger.error(t)
        raise

    except Exception as e:
        logger.error(e)
        raise
        

    
    
def _get_existing_workspace(subscription_id=None,resource_group=None,workspace_name=None,auth=None,tags=None,sku='basic',_location=None, _disable_service_check=False, _workspace_id=None,_cloud='AzureCloud'):
    logger = Logger.get_instance()
    try:
        if subscription_id is None or resource_group is None or workspace_name is None:
            raise Exception("The parameters 'subscription_id','resource_group','workspace_name' must be specified in 'workspace_args'.")

        logger.info("Getting existing Workspace")
        ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name,auth=auth,tags=tags,sku=sku,_location=_location, _disable_service_check=_disable_service_check, _workspace_id=_workspace_id,_cloud=_cloud)
        ws.write_config()
        return ws
    except Exception as e:
        logger.error("Workspace not accessible.Change your parameters while creating workspace or create a new workspace.")
        logger.error(e)
        raise
    


def create_compute(workspace,compute_type,compute_args):
    logger = Logger.get_instance()
    try:
        logger.info("Creating Compute_target.")

        if not isinstance(compute_args,dict):
            raise Exception("The parameter 'compute_args' must be of type 'dict'.")
        
        return ComputeFactory.get_compute(compute_type).create_compute_target(ws=workspace,**compute_args)

    except TypeError as t:
        logger.error("Specify the correct parameters and correct parameter values for 'compute_args'.")
        logger.error(t)
        raise

    except Exception as e:
        logger.error(e)
        raise
            
            
def create_environment(workspace,environment_type,environment_args):
    logger = Logger.get_instance()
    try:
        logger.info("Creating Environment.")

        if not isinstance(environment_args,dict):
            raise Exception("The parameter 'environment_args' must be of type 'dict'.")
            
        return EnvironmentFactory.get_environment(environment_type).create_environment(workspace,**environment_args)
        
    except TypeError as t:
        logger.error("Specify the correct parameters and correct parameter values for 'environment_args'.")
        logger.error(t)
        raise
    
    except Exception as e:
        logger.error(e)
        raise




    

