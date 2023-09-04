import functools
import logging

from flask import make_response, jsonify, g, abort

from exceptions import PermissionDeniedError

_logger = logging.getLogger(__name__)


def get_current_user():
    if hasattr(g, 'user'):
        user = g.user
    else:
        from models.security.user import User
        user = User(id=0, login_id='SYS')
    return user


def check_permission(resource_actions=None, roles=None):
    def decorator(function):
        @functools.wraps(function)
        def wrappers(*args, **kwargs):
            is_allowed = False
            user = get_current_user()
            if resource_actions:
                user_resources = user.resource_actions
                if user_resources:
                    for res, action in resource_actions:
                        user_actions = user_resources.get(res, None)
                        if user_actions:
                            is_allowed = action in user_actions
                        if is_allowed:
                            break
            if not is_allowed:
                if roles:
                    user_roles = user.roles
                    if user_roles:
                        for role in roles:
                            is_allowed = role in user_roles
                            if is_allowed:
                                break
            if is_allowed:
                return function(*args, **kwargs)
            else:
                msg = "Permission denied for user : {0} checking for resource/action : {1} or roles : {2}".format(
                    user.login_id, str(resource_actions), str(roles))
                _logger.warning(msg=msg)
                raise PermissionDeniedError(msg)

        return wrappers

    return decorator


def return_error(http_status_code, ex):
    abort(make_response(jsonify(str(ex)), http_status_code))


def response(resp, **kwargs):
    return make_response(jsonify(resp), kwargs.get('http_status', 200))


def process_args(request, single_params=None, multi_params=None):
    args = request.args
    new_args = {}
    if single_params:
        for x in single_params:
            new_args[x] = args.get(x, None)
    if multi_params:
        for x in multi_params:
            val = args.get(x, None)
            new_args[x] = val.split(',') if val else None
    return new_args
