# encoding: utf-8
"""
@project: djangoModel->notice_services
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: APP的版本管理服务
@created_time: 2023/3/1 11:08
"""

from django.core.paginator import Paginator, EmptyPage

from ..models import AppVersion
from ..utils.custom_tool import format_params_handle, force_transform_type


class AppVersionServices():
    """消息提醒服务类"""

    @staticmethod
    def validate_version(system: str = None, version: str = None):
        system, void = force_transform_type(variable=system, var_type="str")
        version, void = force_transform_type(variable=version, var_type="str")
        if not version or not system:
            return {}, "请检查版本号或者系统类型"

        # 检查当前版本
        app_version_obj = AppVersion.objects.filter(app_system=system, version=version).values(
            "id", "app_system", "version", "version_type", "store_name", "store_url",
            "is_force_update", "push_time", "created_time", "version_detail"
        ).first()
        if not app_version_obj:
            return {}, "请检查版本号或者系统类型"
        # 检查最新版本
        news_version = AppVersion.objects.filter(app_system=system).order_by("-version").values(
            "id", "app_system", "version", "version_type", "store_name", "store_url",
            "is_force_update", "push_time", "created_time", "version_detail"
        ).first()

        if app_version_obj.get("version") == news_version.get("version"):
            app_version_obj["is_news"] = True
            app_version_obj["is_force_update"] = False
        else:
            app_version_obj["is_news"] = False
            app_version_obj["is_force_update"] = news_version.get("is_force_update", False)
            app_version_obj["news_version"] = news_version.get("version")
        return app_version_obj, None

    @staticmethod
    def app_version_list(params: dict = None, need_pagination: int = 0):
        if params is None:
            params = {}
        page = params.pop("page", 1)
        size = params.pop("size", 10)
        sort = params.pop("sort", "version")
        sort = sort if sort in ["version", "-version", "push_time", "-push_time", "created_time", "-created_time"] else "-version"
        # 参数过滤
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id", "app_system", "version", "version_type", "store_name", "store_url",
                "is_force_update|int", "push_time", "min_version", "max_version",
                "push_time_start", "push_time_end"
            ],
            alias_dict={
                "max_version": "version__lte", "min_version": "version__gte",
                "push_time_start": "push_time__gte", "push_time_end": "push_time__lte"
            }
        )
        # 构建ORM
        app_version_obj = AppVersion.objects.filter(**params).order_by(sort).values(
            "id", "app_system", "version", "version_type", "store_name", "store_url",
            "is_force_update", "push_time", "created_time", "version_detail"
        )
        # 不许分页直接返回
        if not need_pagination:
            app_version_list = list(app_version_obj)
            return app_version_list, None

        total = app_version_obj.count()
        paginator = Paginator(app_version_obj, size)
        try:
            app_version_obj = paginator.page(page)
        except EmptyPage:
            app_version_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'

        return {"page": int(page), "size": int(size), "total": total, "list": list(app_version_obj.object_list)}, None

    @staticmethod
    def app_version_edit(pk: int = None, params: dict = None, **kwargs):
        """
        修改系统版本
        :param pk: 修改主键
        :param params: 其他的系统参数
        :param kwargs: 聚名参数
        :return: data,err
        """
        pk, err = force_transform_type(variable=pk, var_type="int")
        if not pk:
            return None, "找不到修改的版本"
        params, void = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, void = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)

        version_obj = AppVersion.objects.filter(id=pk)
        if not version_obj.first():
            return None, "数据不存在"

        # 需要修改的字段过滤
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "app_system|str", "version|str", "version_type|str", "store_name|str", "store_url|str", "is_force_update|int", "push_time|date",
                "version_detail|str"
            ]
        )
        params.setdefault("is_force_update", 0)

        try:
            version_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def app_version_add(params: dict = None, **kwargs):
        """
        添加系统版本
        :param params: 其他的系统参数
        :param kwargs: 聚名参数
        :return: data,err
        """
        params, void = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, void = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)

        # 需要修改的字段过滤
        try:
            params = format_params_handle(
                param_dict=params,
                is_validate_type=True,
                filter_filed_list=[
                    "app_system|str", "version|str", "version_type|str", "store_name|str", "store_url|str", "is_force_update|int", "push_time|date", "version_detail|str"
                ]
            )

            # app系统
            must_key = ["app_system", "version"]
            for k in must_key:
                if not params.get(k):
                    return None, k + " 必填"
            params.setdefault("is_force_update", 0)

            # 版本
            if AppVersion.objects.filter(app_system=params.get("app_system"), version=params.get("version")).first():
                return None, "该版本已经发布，请确认版本号和系统类型"

        except ValueError as e:
            return None, str(e)

        try:
            AppVersion.objects.create(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def app_version_del(pk: int = None):
        """
        删除系统版本
        :param pk: 修改主键
        :param params: 其他的系统参数
        :param kwargs: 聚名参数
        :return: data,err
        """
        pk, err = force_transform_type(variable=pk, var_type="int")
        if not pk:
            return None, "找不到修改的版本"

        version_obj = AppVersion.objects.filter(id=pk)
        if not version_obj.first():
            return None, "数据不存在"

        # 需要修改的字段过滤
        try:
            version_obj.delete()
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None
