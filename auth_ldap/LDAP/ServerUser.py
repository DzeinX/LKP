from django_auth_ldap3.backends import LDAPUser


class ServerUser1(LDAPUser):
    def __init__(self, connection, attributes):
        super().__init__(connection, attributes)


class ServerUser2(LDAPUser):
    def __init__(self, connection, attributes):
        super().__init__(connection, attributes)
