# encoding: utf-8
"""
@project: djangoModel->access_level_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: APP的管理
@created_time: 2023/4/11 20:54
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.app_version_services import AppVersionServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper


class AppVersionView(APIView):
    @api_view(["GET"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def app_version_list(self, *args, request_params, **kwargs):
        data, err = AppVersionServices.app_version_list(
            params=request_params,
            need_pagination=request_params.get("need_pagination", True)
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["PUT"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def app_version_edit(self, *args, request_params, **kwargs):
        pk = request_params.get("id") or request_params.get("pk") or kwargs.get("pk")
        data, err = AppVersionServices.app_version_edit(
            pk=pk,
            params=request_params
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def app_version_add(self, *args, request_params, **kwargs):
        data, err = AppVersionServices.app_version_add(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["DELETE"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def app_version_del(self, *args, request_params, **kwargs):
        pk = request_params.get("id") or request_params.get("pk") or kwargs.get("pk")
        data, err = AppVersionServices.app_version_del(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def validate_version(self, *args, request_params, **kwargs):
        data, err = AppVersionServices.validate_version(
            version=request_params.get("version"),
            version_type=request_params.get("version_type"),
            system=request_params.get("system")
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
