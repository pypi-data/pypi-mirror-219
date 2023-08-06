class RBAC(object):

    def __init__(self):
        pass

    # Check if the given user has the given permission
    @staticmethod
    def has_permission(user_roles, permissions):
        for permission in permissions:
            for user_role in user_roles:
                if user_role == permission:
                    return True
        return False

