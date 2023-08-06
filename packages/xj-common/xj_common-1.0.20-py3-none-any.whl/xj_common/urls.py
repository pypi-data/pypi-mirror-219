from django.urls import re_path

from .apis import notice_apis, region_api, translate_apis, access_level_apis, service_manage_api, encyclopedia_api, modules_apis, module_service_apis, app_versionl_apis
from .service_register import register

register()
urlpatterns = [
    # 地区相关API
    re_path(r'^region_list/?$', region_api.RegionAPIS.region_list, ),
    re_path(r'^region_tree/?$', region_api.RegionAPIS.get_region_tree, ),
    re_path(r'^region_add/?$', region_api.RegionAPIS.region_add, ),
    re_path(r'^region_edit/?$', region_api.RegionAPIS.region_edit, ),
    re_path(r'^region_del/?$', region_api.RegionAPIS.region_del, ),

    # 公共翻译
    re_path(r'^translate_article/?$', translate_apis.TranslateApis.translate_article, ),
    re_path(r'^translate_test/?$', translate_apis.TranslateApis.as_view(), ),

    # 提醒相关接口
    re_path(r'^notice_add/?$', notice_apis.NoticeApis.notice_add),
    re_path(r'^notice_edit/?$', notice_apis.NoticeApis.notice_edit),
    re_path(r'^notice_list/?$', notice_apis.NoticeApis.notice_list),
    re_path(r'^notice_type_list/?$', notice_apis.NoticeApis.type_list),

    # 访问级别
    re_path(r'^access_level_list/?$', access_level_apis.AccessLevelAPIView.access_level_list),

    # 服务治理
    re_path(r'^find_service_test/?$', service_manage_api.ServiceManageApis.find_service_test),  # 发现服务

    # chatGPT接口
    re_path(r'^ask_question/?$', encyclopedia_api.EncyclopediaApis.ask_question),

    # 模块与开放服务列表
    re_path(r'^module_list/?$', modules_apis.ModuleApiView.module_list),
    re_path(r'^module_register/?$', modules_apis.ModuleApiView.module_register),
    re_path(r'^services_list/?$', module_service_apis.ModuleApiView.services_list),

    # app版本管理接口
    re_path(r'^app_version_list/?$', app_versionl_apis.AppVersionView.app_version_list, name="系统版本列表"),
    re_path(r'^app_version_edit/?(?P<pk>\d+)?$', app_versionl_apis.AppVersionView.app_version_edit, name="系统版本编辑"),
    re_path(r'^app_version_add/?(?P<pk>\d+)?$', app_versionl_apis.AppVersionView.app_version_add, name="系统版本添加"),
    re_path(r'^app_version_del/?(?P<pk>\d+)?$', app_versionl_apis.AppVersionView.app_version_del, name="系统版本删除"),
    re_path(r'^validate_version/?$', app_versionl_apis.AppVersionView.validate_version, name="系统版本删除")

]
