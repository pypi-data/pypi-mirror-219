from .script_generator_helper import ScriptGeneratorHelper
from .logger import Logger  

def _generate_model_config(workspace,filename):
    logger = Logger.get_instance()
    try:
        subscription_id,resource_group,name,workspace_id=workspace.subscription_id,workspace.resource_group,workspace.name,workspace.get_details()['workspaceid']
        code = ScriptGeneratorHelper()
        code.begin(tab='')
        
        code.write('{"accountContext":{"subscriptionId":'+'"'+subscription_id+'",'+'"resourceGroupName":'+'"'+resource_group+'",'+'"accountName":'+'"'+name+'",'+'"workspaceId":'+'"'+workspace_id+'"'+'},"models":{},"modelsInfo":{}}')
        with open(filename,'w') as f:
            f.write(code.end())
    except Exception as e:
        logger.error(e)
        raise

def _get_image_details(environment,workspace):
    logger = Logger.get_instance()
    try:
        environment.register(workspace)
        image_details=environment.get_image_details(workspace)
        if not image_details['imageExistsInRegistry']:
            result=environment.build(workspace)
            result.wait_for_completion(show_output=True)
        return image_details['dockerImage']['name'],image_details['dockerImage']['registry']['address']
    except Exception as e:
        logger.error("Unable to obtain image details.")
        logger.error(e)
        raise



def _generate_dockerfile(models,environment,workspace,entry_script,filename,source_directory_name):
    logger = Logger.get_instance()
    try:
        model,entry_script_name=models[0],entry_script.rstrip('/').split('/')[-1]
        image,registry=_get_image_details(environment,workspace)
        docker_base_image=registry+'/'+image
        azureml_model_dir='/var/azureml-app/azureml-models/'+str(model.name)+'/'+str(model.version) if len(models)==1 else '/var/azureml-app/azureml-models/'
        
        code = ScriptGeneratorHelper()
        code.begin(tab='')
        code.write('FROM '+docker_base_image+'\n')
        code.write('COPY azureml-app /var/azureml-app\n')
        if source_directory_name is not None:
            code.write('ENV AZUREML_SOURCE_DIRECTORY='+source_directory_name+'\n')
            code.write('ENV AZUREML_ENTRY_SCRIPT=/var/azureml-app/'+source_directory_name+'/'+entry_script+'\n')
        else:
            code.write('ENV AZUREML_ENTRY_SCRIPT=/var/azureml-app/'+entry_script_name+'\n')
        code.write('ENV AZUREML_MODEL_DIR='+azureml_model_dir+'\n')
        code.write('EXPOSE 5001\n')
        code.write('CMD ["runsvdir","/var/runit"]')
        with open(filename,'w') as f:
            f.write(code.end())

    except Exception as e:
        logger.error(e)
        raise

def _generate_main_file(source_directory,entry_script_path,filename):
    logger = Logger.get_instance()
    try:
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')
        code.write('import os\n')
        code.write('import inspect\n')
        code.write('import importlib.util as imp\n')
        code.write('import logging\n')
        code.write('import sys\n\n')

        code.write('sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '+"'"+source_directory+"'))\n")
        code.write('script_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), '+"'"+entry_script_path+"')\n")
        code.write('driver_module_spec = imp.spec_from_file_location('+"'"+"service_driver"+"'"+', script_location)\n')
        code.write('driver_module = imp.module_from_spec(driver_module_spec)\n')
        code.write('driver_module_spec.loader.exec_module(driver_module)\n\n')

        code.write('def run(http_body, request_headers):\n')
        code.indent()
        code.write('global run_supports_request_headers\n')
        code.write('arguments = '+'{'+'run_input_parameter_name: http_body'+'}\n')
        code.write('if run_supports_request_headers:\n')
        code.indent()
        code.write('arguments["request_headers"] = request_headers\n')
        code.dedent()
        code.write('return_obj = driver_module.run(**arguments)\n')
        code.write('return return_obj\n\n')
        code.dedent()

        code.write('def init():\n')
        code.indent()
        code.write('global run_input_parameter_name\n')
        code.write('global run_supports_request_headers\n\n')
        code.write('run_args = inspect.signature(driver_module.run).parameters.keys()\n')
        code.write('run_args_list = list(run_args)\n')
        code.write('run_input_parameter_name = run_args_list[0] if run_args_list[0] != "request_headers" else run_args_list[1]\n')
        code.write('run_supports_request_headers = "request_headers" in run_args_list\n\n')
        code.write('driver_module.init()\n')
        code.dedent()

        with open(filename,'w') as f:
            f.write(code.end())

    except Exception as e:
        logger.error(e)
        raise

    





























        

        




