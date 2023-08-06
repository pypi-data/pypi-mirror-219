from __future__ import absolute_import
import os
import sys
import json
import configparser

from blendedUx.blended_flask.blended_hostlib.swagger_client.apis.packages_api import PackagesApi
from blendedUx.blended_flask.blended_hostlib.swagger_client.apis.accounts_api import AccountsApi
from blendedUx.blended_flask.blended_hostlib.swagger_client.rest import ApiException

from blendedUx.blended_flask.blended_hostlib.exceptions import BlendedException, \
    PackageNameExistsException, AccountActivationException

import urllib3
from .settings import DIRECTORY, USER_SESSION as user_rc_file
# urllib3.disable_warnings()
# import logging


class Network(object):
    """
    class to interact with client api.
    """
    def __init__(self, *args, **kwargs):
        """
        """
        self.account_client = AccountsApi()
        self.package_client = PackagesApi()
        self.session_key = kwargs.get('session_key', None)
        if not self.session_key:
            self.session_key, self.user_pk = self.get_sessionkey()

    def login(self, username, password, active_account=''):
        """
        """
        body = {'user_name': username, 'password': password, 'active_account':active_account}
        try:
            response = self.account_client.login(body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                if error_dict['status_code'] == 5018:
                    raise AccountActivationException(error_dict['errors'])
                else:
                    raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def logout(self):
        """
        """
        sessionkey = self.session_key
        body = {'sessionkey': sessionkey}
        try:
            response = self.account_client.logout(body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                if error_dict['status_code'] == 5018:
                    raise AccountActivationException(error_dict['errors'])
                else:
                    raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def create_account(self, body):
        """
        """
        try:
            response = self.account_client.create_account(body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def update_account(self, pk, body):
        """
        """
        sessionkey=self.session_key
        try:
            response = self.account_client.update_account(pk, body, sessionkey=sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_current_account(self, pk):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.get_current_account(pk, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_account_list(self, pk):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.get_account_list(sessionkey, pk)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_account_users(self, slug):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.get_account_users(slug, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def remove_account(self, slug, account_slug,):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.remove_account(slug, account_slug, sessionkey)
            response = "TODO"
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def resend_account_verification_email(self, body):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.resend_account_verification_email(sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                if error_dict['status_code'] == 5086:
                    raise AccountActivationException(error_dict['message'])
                elif error_dict['status_code'] == 4035:
                    raise AccountActivationException(error_dict['errors']['email'][0])
                else:
                    raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_sessionkey(self):
        """
        Read session key from user config file
        """
        config = configparser.ConfigParser()
        working_dir = DIRECTORY
        user_rc_path = os.path.join(working_dir, user_rc_file)
        try:
            config.read(user_rc_path)
            session_key = config.get('USER', 'sessionkey')
            user_pk = config.get('USER', 'user_pk')
        except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError):
            session_key = None
            user_pk = None
        return session_key, user_pk

    def set_sessionkey(self, session_key, user_pk):
        """
        Stores sessionkey in filesystem.
        """
        self.session_key = session_key
        self.user_pk = user_pk
        config = configparser.ConfigParser()
        working_dir = DIRECTORY
        user_rc_path = os.path.join(working_dir, user_rc_file)
        config.read(user_rc_path)
        try:
            config.set('USER', 'sessionkey', str(session_key))
            config.set('USER', 'user_pk', str(user_pk))
        except (configparser.NoSectionError, configparser.NoOptionError):
            config.add_section('USER')
            config.set('USER', 'sessionkey', str(session_key))
            config.set('USER', 'user_pk', str(user_pk))

        with open(user_rc_path, 'w') as config_file:
            config.write(config_file)

    def set_user_pk(self, user_pk):
        """
        Stores user_pk in filesystem.
        """
        self.user_pk = user_pk
        config = configparser.ConfigParser()
        working_dir = DIRECTORY
        user_rc_path = os.path.join(working_dir, user_rc_file)
        config.read(user_rc_path)
        try:
            config.set('USER', 'user_pk', str(user_pk))
        except (configparser.NoSectionError, configparser.NoOptionError):
            config.add_section('USER')
            config.set('USER', 'user_pk', str(user_pk))
        with open(user_rc_path, 'w') as config_file:
            config.write(config_file)

    def get_user_pk(self):
        """
        Read session key from user config file
        """
        config = configparser.ConfigParser()
        working_dir = DIRECTORY
        user_rc_path = os.path.join(working_dir, user_rc_file)
        try:
            config.read(user_rc_path)
            user_pk = config.get('USER', 'user_pk')
        except (configparser.NoSectionError, configparser.NoOptionError):
            user_pk = 'anonymous'
            # raise BlendedException('user is not created yet')
        return user_pk

    def invite_user(self, slug, body):
        """
        :param slug:
        :param body:
        :return:
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.invite_user(slug, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def change_account_user_privilege(self, slug, user_slug, body):
        """
        :param slug:
        :param body:
        :return:
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.change_account_user_privilege(slug, user_slug, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

        

    def add_account_user(self, slug, body):
        """
        :param slug:
        :param body:
        :return:
        """
        sessionkey = self.session_key
        try:
            response = self.account_client.add_account_user(slug, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def set_current_account(self, body):
        """
        :param body:
        :return:
        """
        slug = self.user_pk
        sessionkey = self.session_key
        try:
            response = self.account_client.set_current_account(slug, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def create_package(self, account_slug, body):
        """
        """
        sessionkey = self.session_key
        # if description:
        #     body = {'name': package_name,
        #             'type': package_type,
        #             'description': description}
        # else:
        #     body = {'name': package_name,
        #             'type': package_type
        #            }
        try:
            response = self.package_client.create_package(account_slug, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def acquire_package(self, account_slug, pk, body):
        """
        method interacts with the client api for getting a
        package from hub
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.acquire_package(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                # with open('shareerror.html', 'w') as filename:
                #     filename.write(exc.body)
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                if ((error_dict['status_code'] == 5999) and
                        (error_dict['message'] == 'package with given slug already exists in account')):
                    raise PackageNameExistsException()
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_package_details(self, account_slug, pk):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_package_details(account_slug, pk, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_version_details(self, account_slug, pk, label):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_version_details(account_slug, pk, label, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_detail_document(self, account_slug, slug, name):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_detail_document(account_slug, slug, name, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def snapshot(self, account_slug, pk, body):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.snapshot(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def set_canonical(self, account_slug, pk, label, body):
        """
        """
        body['label'] = label
        sessionkey = self.session_key
        try:
            response = self.package_client.canonical_set(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def create_draft(self, account_slug, pk, body):
        """
        method interacts with the client api for saving a
        package draft to the hub
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.create_draft(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                # {'status_code': 5059, 'message': 'Draft has been changed. Please pull it first'}
                # if error_dict['status_code'] == 5059:
                #     raise BlendedException('Package with given slug already exists in account.')
                # else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def update_draft(self, account_slug, pk, body):
        """
        method interacts with the client api for saving a
        package draft to the hub
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.update_draft(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                with open('shareerror.html', 'w') as filename:
                    filename.write(exc.body)
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def package_list(self, account_slug, slug=None, share=None, transfer_to_me=None,
                     transfer_by_me=None, organization=None, published=None, purchased=None):
        """
        """
        body = {'slug': slug}
        sessionkey = self.session_key
        try:
            if share:
                response = self.package_client.get_packages(account_slug, sessionkey, share='1')
            elif transfer_to_me:
                response = self.package_client.get_packages(account_slug, sessionkey, transfer_to_me='1')
            elif transfer_by_me:
                response = self.package_client.get_packages(account_slug, sessionkey, transfer_by_me='1')
            elif organization:
                response = self.package_client.get_packages(account_slug, sessionkey, org_packages='1')
            elif purchased:
                response = self.package_client.get_packages(account_slug, sessionkey, purchased='1')
            elif published:
                response = self.package_client.get_packages(account_slug, sessionkey, published='1')
            else:
                response = self.package_client.get_packages(account_slug, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_versions_list(self, account_slug, slug):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_versions(account_slug, slug, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def package_accounts_list(self, account_slug, package_name):  # package_accounts_list(self, account_slug, slug, package_name)
        """
        :param slug:
        :param package_name:
        :return:
        """
        body = {'slug': account_slug, 'package_name': package_name}
        sessionkey = self.session_key
        try:
            response = self.package_client.package_account_list(account_slug, package_name, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_dependencies(self, account_slug, slug):
        """
        :param slug:
        :return:
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_dependencies(account_slug, slug, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def update_package(self, account_slug, pk, body):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.update_package(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def add_license(self, account_slug, slug, label, body):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.add_license(account_slug, slug, label, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                if error_dict['status_code'] == 9999:
                    raise BlendedException(error_dict['message'])
                else:
                    raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def remove_license(self, pk, name):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.remove_license(sessionkey, pk, name)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def download(self, account_slug, pk, label, as_hashes='0'):
        """
        """
        sessionkey = self.session_key
        try:
            if sessionkey:
                response = self.package_client.download(account_slug, pk, label, sessionkey=sessionkey, as_hashes=as_hashes)
            else:
                response = self.package_client.download(account_slug, pk, label, as_hashes=as_hashes)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def download_canonical(self, account_slug, pk):  # download_canonical(self, account_slug, pk, as_hashes='0')
        """
        """
        sessionkey = self.session_key
        try:
            if sessionkey:
                response = self.package_client.download_canonical(account_slug, pk, sessionkey=sessionkey)
            else:
                response = self.package_client.download_canonical(account_slug, pk)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def download_draft(self, account_slug, pk, as_hashes='0'):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.download_draft(account_slug, pk, sessionkey, as_hashes=as_hashes)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_canonical(self, account_slug, package_slug):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_canonical(account_slug, package_slug, sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def upload_media(self, account_name, pk, hash_value, **kwargs):
        """
        """
        try:
            if(not kwargs.get('token', None)):
                # if kwargs is having token and it's value is NOne then remove token from kwargs
                del kwargs['token']
            response = self.package_client.upload_media(account_name, pk, self.session_key, hash_value, **kwargs)
            return response
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")

    def get_package_initial(self):
        """
        """
        try:
            response = self.package_client.get_package_initial()
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def get_publication(self, account_slug, pk):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_publication(account_slug, pk, sessionkey=sessionkey)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def update_publication(self, account_slug, pk, body, commit='1'):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.update_publication(account_slug, pk, body, sessionkey=sessionkey, commit=commit)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def validate_publication(self, account_slug, pk, body):
        """
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.validate_publication(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def revoke_acquired_package(self, account_slug, pk, body):
        """
        method interacts with the client api for getting a
        package from hub
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.revoke_acquired_package(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict) 
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response


    def accept_acquisition(self, account_slug, pk, body):
        """
        method interacts with the client api for getting a
        package from hub
        """
        sessionkey = self.session_key
        
        try:
            response = self.package_client.accept_acquisition(account_slug, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict) 
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response


    def get_acquired_package_account_list(self, account_slug, pk):
        """
        method interacts with the client api for getting a
        package from hub
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.get_acquired_package_account_list(account_slug, pk, sessionkey, share='1')
        except ApiException as exc:
            try:
                 error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict)
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response

    def reject_acquisition_invite(self, account_slug, rejected_account, pk, body):
        """
        method interacts with the client api to reject package acquisition.
        """
        sessionkey = self.session_key
        try:
            response = self.package_client.reject_acquisition_invite(rejected_account, pk, sessionkey, body)
        except ApiException as exc:
            try:
                error_dict = json.loads(exc.body)
            except ValueError:
                raise BlendedException("Something went wrong on the Server")
            else:
                raise BlendedException(error_dict) 
        except urllib3.exceptions.MaxRetryError:
            raise BlendedException("\nFailed to establish connection. Please try again.")
        return response 