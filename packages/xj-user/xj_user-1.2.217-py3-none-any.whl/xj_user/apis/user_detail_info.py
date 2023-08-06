# encoding: utf-8
"""
@project: djangoModel->user_detail_info
@author: 孙楷炎
@synopsis: 用户详细信息操作
@created_time: 2022/6/27 19:42
"""
from rest_framework.views import APIView

from ..services.user_detail_info_service import DetailInfoService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper, dynamic_load_class
from ..utils.user_wrapper import user_authentication_force_wrapper


# 列表
class UserListDetail(APIView):
    @request_params_wrapper
    @user_authentication_force_wrapper
    def get(self, request_params, *args, **kwargs):
        # 参数过滤
        filter_fields = request_params.pop("filter_fields", None)
        data, err_txt = DetailInfoService.get_list_detail(params=request_params, filter_fields=filter_fields)
        if not err_txt:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)


# 用户详细信息
class UserDetail(APIView):
    @user_authentication_force_wrapper
    @request_params_wrapper
    def get(self, *args, request_params=None, user_info=None, **kwargs):
        user_id = request_params.get('user_id') or user_info.get("user_id")
        filter_fields = request_params.get("filter_fields", None)
        data, error_text = DetailInfoService.get_detail(user_id=user_id, filter_fields=filter_fields)
        if error_text is None:
            return util_response(data=data)
        return util_response(err=47767, msg=error_text)


class UserDetailEdit(APIView):

    @user_authentication_force_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def post(self, *args, request_params=None, user_info=None, **kwargs):
        """
        修改用户的详细信息
        """
        if user_info is None:
            user_info = {}
        if request_params is None:
            request_params = {}
        request_params.setdefault('user_id', user_info.get('user_id'))
        # ------------------------ section 查询该用户是否存在详细信息 start -------------------
        if request_params:
            data, err_txt = DetailInfoService.create_or_update_detail(params=request_params.copy())
            if err_txt:
                return util_response(err=47767, msg=err_txt)
        # ------------------------ section 查询该用户是否存在详细信息 end   -------------------

        # ------------------------ section 角色修改联动 start --------------------------------
        try:
            # 编辑角色服务
            RoleService, err = dynamic_load_class(
                import_path="xj_role.services.role_service",
                class_name="RoleService"
            )
            if not err and request_params.get("user_role_list"):
                data, err = RoleService.bind_user_roles(
                    user_id=request_params.get("user_id"),
                    role_list=request_params.get("user_role_list"),
                )

            # # 编辑部门服务
            UserGroupService, err = dynamic_load_class(
                import_path="xj_role.services.user_group_service",
                class_name="UserGroupService"
            )
            if not err and request_params.get("user_group_list"):
                data, err = UserGroupService.user_bind_groups(
                    user_id=request_params.get("user_id"),
                    group_list=request_params.get("user_group_list"),
                )
        except Exception as e:
            pass
        # ------------------------ section 角色修改联动 end   --------------------------------
        return util_response()


# 用户必须存在才有信息编辑，所以这个接口是多余的
class UserDetailExtendFields(APIView):
    def get(self, request, *args):
        # 身份验证，传user_id使用传的，没有传使用token获取的
        # 查询该用户是否存在详细信息 TODO 需要判断修改人是否有权限
        data, err_txt = DetailInfoService.get_extend_fields()
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)
