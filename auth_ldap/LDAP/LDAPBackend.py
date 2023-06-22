from django_auth_ldap3.backends import LDAPBackend
# from django_auth_ldap3.conf import settings as s
from auth_ldap.LDAP.LDAPSettingsController import settings_1_server
from auth_ldap.LDAP.LDAPSettingsController import settings_2_server
from auth_ldap.LDAP.ServerUser import ServerUser1
from auth_ldap.LDAP.ServerUser import ServerUser2

import ldap3
import ssl


class Backend1(LDAPBackend):
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


class Backend2(LDAPBackend):
    def __init__(self, settings, LDAPUser):
        super().__init__()
        self.LDAPUser = LDAPUser
        self.settings = settings
        tls_config = None

        if settings.TLS:
            tls_opts = {
                'validate': ssl.CERT_REQUIRED if settings.TLS_VALIDATE else ssl.CERT_NONE
            }

            if settings.TLS_CA_CERTS:
                tls_opts['ca_certs_file'] = settings.TLS_CA_CERTS

            if settings.TLS_PRIVATE_KEY:
                tls_opts['local_private_key_file'] = settings.TLS_PRIVATE_KEY

            if settings.TLS_LOCAL_CERT:
                tls_opts['local_certificate_file'] = settings.TLS_LOCAL_CERT

            tls_config = ldap3.Tls(**tls_opts)

        self.backend = ldap3.Server(settings.URI,
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


backend_1 = Backend1(settings_1_server, ServerUser1)
backend_2 = Backend2(settings_2_server, ServerUser2)
