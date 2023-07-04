import datetime

from django_auth_ldap3.backends import LDAPBackend
from django.contrib.auth import get_user_model
from auth_ldap.LDAP.LDAPSettingsController import settings_1_server
from auth_ldap.LDAP.LDAPSettingsController import settings_2_server
from auth_ldap.LDAP.ServerUser import ServerUser1
from auth_ldap.LDAP.ServerUser import ServerUser2

import ldap3
import ssl


class Backend(LDAPBackend):
    def __init__(self, settings, LDAPUser):
        super().__init__()
        self.settings = settings
        self.LDAPUser = LDAPUser
        tls_config = None

        if self.settings.TLS:
            tls_opts = {
                'validate': ssl.CERT_REQUIRED if self.settings.TLS_VALIDATE else ssl.CERT_NONE
            }

            if self.settings.TLS_CA_CERTS:
                tls_opts['ca_certs_file'] = self.settings.TLS_CA_CERTS

            if self.settings.TLS_PRIVATE_KEY:
                tls_opts['local_private_key_file'] = settings.TLS_PRIVATE_KEY

            if self.settings.TLS_LOCAL_CERT:
                tls_opts['local_certificate_file'] = self.settings.TLS_LOCAL_CERT

            tls_config = ldap3.Tls(**tls_opts)

        self.backend = ldap3.Server(self.settings.URI,
                                    use_ssl=settings.TLS,
                                    tls=tls_config)

    def bind_ldap_user(self, username, password):
        ldap_bind_user = None

        if self.settings.BIND_TEMPLATE:
            # Full CN
            ldap_bind_user = self.settings.BIND_TEMPLATE.format(username=username,
                                                                base_dn=self.settings.BASE_DN)
        elif self.settings.USERNAME_PREFIX:
            ldap_bind_user = self.settings.USERNAME_PREFIX + username
        elif self.settings.USERNAME_SUFFIX:
            ldap_bind_user = username + self.settings.USERNAME_SUFFIX

        try:
            c = ldap3.Connection(self.backend,
                                 read_only=True,
                                 lazy=False,
                                 auto_bind="NO_TLS",
                                 client_strategy=ldap3.SYNC,
                                 authentication=ldap3.SIMPLE,
                                 user=ldap_bind_user,
                                 password=password)
        except ldap3.core.exceptions.LDAPSocketOpenError as e:
            return None
        except ldap3.core.exceptions.LDAPBindError as e:
            return None
        except Exception as e:
            raise

        search_filter = '({}={})'.format(self.settings.UID_ATTRIB, username)
        attributes = self.search_ldap(c, search_filter, attributes=self.LDAPUser._attrib_keys, size_limit=1)
        if not attributes:
            return None

        return self.LDAPUser(c, attributes)

    def search_ldap(self, connection, ldap_filter, **kwargs):
        connection.search(self.settings.BASE_DN, ldap_filter, **kwargs)
        entry = None
        for d in connection.response:
            if d['type'] == 'searchResEntry':
                entry = d['attributes']
                entry['dn'] = d['dn']
                break
        return entry

    def authenticate(self, username=None, password=None):
        ldap_user = self.retrieve_ldap_user(username, password)
        if ldap_user is None:
            return None
        if not self.check_group_membership(ldap_user, self.settings.LOGIN_GROUP):
            return None

        User = get_user_model()
        django_user = User.objects.filter(username__iexact=username).first()
        if not django_user:
            django_user = User(username=ldap_user.mail.split('@')[0],
                               full_name=ldap_user.cn,
                               is_active=True)
            django_user.save()
        else:
            django_user = django_user
            django_user.full_name = ldap_user.cn
            django_user.save()

        self.update_group_membership(ldap_user, django_user)

        return django_user


class Backend1(Backend):
    def __init__(self, settings, LDAPUser):
        super().__init__(settings, LDAPUser)


class Backend2(Backend):
    def __init__(self, settings, LDAPUser):
        super().__init__(settings, LDAPUser)


backend_1 = Backend1(settings_1_server, ServerUser1)
backend_2 = Backend2(settings_2_server, ServerUser2)
