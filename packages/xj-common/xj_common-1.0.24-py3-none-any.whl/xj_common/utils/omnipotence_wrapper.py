# encoding: utf-8
"""
@project: djangoModel->omnipotence_wrapper
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 万能装饰器
@created_time: 2023/6/30 14:27
"""
from .custom_tool import *

class OmnipotenceWrapper:
    """万能装饰器分发类"""

    default_wrappers = [
        {"path": "xj_role.utils.custom_tool", "function": "request_params_wrapper", "must_run": True},
        {"path": "xj_role.utils.user_wrapper", "function": "user_authentication_force_wrapper", "must_run": True},
        {"path": " xj_role.utils.api_interrupter_wrapper", "function": "api_interrupter_wrapper", "must_run": True},
    ]
    custom_run_wrappers = []  # 用户需要走执行的自定以装饰器
    run_wrappers_instance = []  # 先执行默认的装饰器，然后在执行自定义的装饰器

    def __init__(self, run_wrappers=None):
        # 获取默认执行的装饰器
        run_wrappers, err = force_transform_type(variable=run_wrappers, var_type="list")
        if run_wrappers:
            self.run_wrappers = run_wrappers

    def get_wrappers(self):
        """
        获取所有需要执行的装饰器
        :return:
        """
        for wrapper_map in self.default_wrappers:
            wrapper_function, err = dynamic_load_function(import_path=wrapper_map["path"], function_name=wrapper_map["function"])
            if err:
                continue
            self.run_wrappers_instance.append(wrapper_function)
        return self.run_wrappers_instance

    def run_wrapper(self, *args, to_run_wrapper, api_method, **kwargs):
        """
        执行装饰器方法
        :param to_run_wrapper: 需要执行的装饰器
        :param api_method: 系统的API方法
        """

        @to_run_wrapper
        def inner_run_wrapper(*args, **kwargs):
            if callable(api_method):
                return api_method(*args, **kwargs)
            else:
                return api_method

        return inner_run_wrapper(*args, **kwargs)

    def wrapper(self, *args, func_list=[], **kwargs):
        """
        万能Http接口装饰器
        :param func_list: 用户自定义的装饰器
        :param route:  调用路由
        """

        def wrapper(func):
            def route_register_decorator(*args, **kwargs):
                copy_func = func
                for to_run_wrapper_instance in self.get_wrappers():
                    copy_func = self.run_wrapper(*args, api_method=copy_func, to_run_wrapper=to_run_wrapper_instance, **kwargs)
                return copy_func

            return route_register_decorator

        return wrapper


wrapper = OmnipotenceWrapper()
omnipotence_wrapper = wrapper.wrapper
