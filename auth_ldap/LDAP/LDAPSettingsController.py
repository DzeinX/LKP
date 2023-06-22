from django_auth_ldap3.conf import LDAPSettings
from Config import LDAPSettings as LDAP


class LDAPSettingsFirstServer(LDAPSettings):
    def __init__(self):
        super().__init__()

    defaults = {
        'ADMIN_GROUP': LDAP.EduVoguDomain.ADMIN_GROUP,
        'BASE_DN': LDAP.EduVoguDomain.BASE_DN,
        'BIND_TEMPLATE': LDAP.EduVoguDomain.BIND_TEMPLATE,
        'GROUP_MAP': LDAP.EduVoguDomain.GROUP_MAP,
        'LOGIN_GROUP': LDAP.EduVoguDomain.LOGIN_GROUP,
        'UID_ATTRIB': LDAP.EduVoguDomain.UID_ATTRIB,
        'USERNAME_PREFIX': LDAP.EduVoguDomain.USERNAME_PREFIX,
        'USERNAME_SUFFIX': LDAP.EduVoguDomain.USERNAME_SUFFIX,
        'URI': LDAP.EduVoguDomain.URI,
        'TLS': LDAP.EduVoguDomain.TLS,
        'TLS_CA_CERTS': LDAP.EduVoguDomain.TLS_CA_CERTS,
        'TLS_VALIDATE': LDAP.EduVoguDomain.TLS_VALIDATE,
        'TLS_PRIVATE_KEY': LDAP.EduVoguDomain.TLS_PRIVATE_KEY,
        'TLS_LOCAL_CERT': LDAP.EduVoguDomain.TLS_LOCAL_CERT,
    }


class LDAPSettingsSecondServer(LDAPSettings):
    def __init__(self):
        super().__init__()

    defaults = {
        'ADMIN_GROUP': LDAP.AupVoguDomain.ADMIN_GROUP,
        'BASE_DN': LDAP.AupVoguDomain.BASE_DN,
        'BIND_TEMPLATE': LDAP.AupVoguDomain.BIND_TEMPLATE,
        'GROUP_MAP': LDAP.AupVoguDomain.GROUP_MAP,
        'LOGIN_GROUP': LDAP.AupVoguDomain.LOGIN_GROUP,
        'UID_ATTRIB': LDAP.AupVoguDomain.UID_ATTRIB,
        'USERNAME_PREFIX': LDAP.AupVoguDomain.USERNAME_PREFIX,
        'USERNAME_SUFFIX': LDAP.AupVoguDomain.USERNAME_SUFFIX,
        'URI': LDAP.AupVoguDomain.URI,
        'TLS': LDAP.AupVoguDomain.TLS,
        'TLS_CA_CERTS': LDAP.AupVoguDomain.TLS_CA_CERTS,
        'TLS_VALIDATE': LDAP.AupVoguDomain.TLS_VALIDATE,
        'TLS_PRIVATE_KEY': LDAP.AupVoguDomain.TLS_PRIVATE_KEY,
        'TLS_LOCAL_CERT': LDAP.AupVoguDomain.TLS_LOCAL_CERT,
    }


settings_1_server = LDAPSettingsFirstServer()
settings_2_server = LDAPSettingsSecondServer()
