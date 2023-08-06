import json

from alibabacloud_fc_open20210406.client import Client as FC_Open20210406Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_fc_open20210406 import models as fc__open_20210406_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient

class fun_client:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        user_id: str,
        access_key_id: str,
        access_key_secret: str,
    ) -> FC_Open20210406Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/FC-Open
        config.endpoint = str(user_id) + f".cn-beijing.fc.aliyuncs.com"
        return FC_Open20210406Client(config)


    @staticmethod
    def create_function(client, service_name, function_name,  code, handler, runtime, memory_size, timeout) -> None:
        create_function_headers = fc__open_20210406_models.CreateFunctionHeaders()
        # code = fc__open_20210406_models.Code(zip_file=get_zip())
        create_function_request = fc__open_20210406_models.CreateFunctionRequest(code=code,
                                                                                 function_name=function_name,
                                                                                 handler=handler,
                                                                                 runtime=runtime,
                                                                                 memory_size=memory_size,
                                                                                 timeout=timeout)
        runtime = util_models.RuntimeOptions()
        resp = client.create_function_with_options(service_name, create_function_request, create_function_headers, runtime)
        #ConsoleClient.log(UtilClient.to_jsonstring(resp))

    @staticmethod
    def update_function(client, service_name, function_name, code) -> None:
        update_function_headers = fc__open_20210406_models.UpdateFunctionHeaders()
        update_function_request = fc__open_20210406_models.UpdateFunctionRequest(code=code)
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.update_function_with_options(service_name, function_name, update_function_request, update_function_headers, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    @staticmethod
    def list_functions(client, service_name) -> list:
        list_functions_headers = fc__open_20210406_models.ListFunctionsHeaders()
        list_functions_request = fc__open_20210406_models.ListFunctionsRequest()
        runtime = util_models.RuntimeOptions()
        try:
            respones = client.list_functions_with_options(service_name, list_functions_request, list_functions_headers, runtime)
            functions = respones.body.functions
            fun_names = [f.function_name for f in functions]
            return fun_names
        except Exception as error:
            UtilClient.assert_as_string(error.message)
            return None

    @staticmethod
    def invoke_function(client, service_name, function_name, event) -> None:
        invoke_function_headers = fc__open_20210406_models.InvokeFunctionHeaders(
            x_fc_invocation_type='Async',
            x_fc_log_type='None'
        )
        invoke_function_request = fc__open_20210406_models.InvokeFunctionRequest(
            qualifier='LATEST',
            body=UtilClient.to_bytes(json.dumps(event))
        )
        runtime = util_models.RuntimeOptions()
        resp = client.invoke_function_with_options(service_name, function_name, invoke_function_request, invoke_function_headers, runtime)
        #ConsoleClient.log(UtilClient.to_jsonstring(resp))

    @staticmethod
    def get_service(client, service_name) -> str:
        get_service_headers = fc__open_20210406_models.GetServiceHeaders()
        get_service_request = fc__open_20210406_models.GetServiceRequest()
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            respones = client.get_service_with_options(service_name, get_service_request, get_service_headers, runtime)
            return None
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)
            return None