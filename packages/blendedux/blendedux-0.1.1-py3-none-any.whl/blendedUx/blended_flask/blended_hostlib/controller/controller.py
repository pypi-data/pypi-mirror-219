from __future__ import absolute_import
import os
import re
import sys
import json
import base64
import zlib
import hashlib
import shutil
from distutils.dir_util import copy_tree
from PIL import Image
from collections import OrderedDict
from copy import copy
from copy import deepcopy
from sys import platform

if sys.version_info[0] < 3:
    from __builtin__ import raw_input as input
else:
    from builtins import input

os_name = platform.lower()
if os_name == 'linux':
    import readline
elif os_name == 'darwin':
    import readline

try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs

from blendedUx.blended_flask.blended_hostlib.exceptions import BlendedException, \
    PackageNameExistsException

ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.bmp',
                       '.gif', '.png',
                       '.ico', '.webp', '.otf',
                       '.eot', '.svg', '.ttf',
                       '.woff', '.woff2']

SAVE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "save_files/")
LOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Load_files/")

DEFAULT_CHUNK_SIZE = 64 * 2 ** 10

FILE_NOT_FOUND = "file not found "

BLENDED_ACCOUNT = 'blended'
BLENDED_BASIC = 'basic'
BLENDED_BASIC_THEME = 'basic_theme'
BLENDED_BASIC_LAYOUT = 'basic_layout'

PACKAGE_TYPES = ['theme', 'layout', 'other']

class Controller(object):
    """
    Controller class
    """
    def __init__(self, network, backend):
        """
        Initialization method of controller class.
        """
        self.network = network
        self.backend = backend
        self.root_directory = backend.directory_path
        self.src_or_lib = None

    def package_version(self, current_account, package_name, **kwargs):
        """
        It will collect version list from HUB!!!
        """
        version_list = []
        canonical = kwargs.get('canonical', False)
        identifiers = package_name.split("/")
        if len(identifiers) > 1:
            if (current_account == identifiers[0]):
                package_name = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])

        if canonical:
            try:
                info = self.network.get_canonical(current_account, package_name)
                version = info.to_dict()['label']
                date = (info.to_dict()['created_date']).strftime("%b %d %Y %H:%M:%S")
            except BlendedException as exc:
                raise BlendedException(exc)
            return [{'canonical_version': version, 'date': date}]
        try:
            response = self.network.get_versions_list(current_account, package_name)
        except BlendedException as exc:
            raise BlendedException(exc)
        else:
            package_version_items = response.items
            for item in package_version_items:
                version_list.append({'canonical':item.canonical, 'is_set_canonical': item.is_set_canonical,
                                     'version': item.label, 'date': (item.created_date).strftime("%b %d %Y %H:%M:%S")})
        pack_detail  = self.network.get_package_details(current_account, package_name)
        version_list.append({'canonical':0, 'is_set_canonical': 0,
                             'version': 'draft', 'date': (pack_detail.created_date).strftime("%b %d %Y %H:%M:%S")})
        return version_list

    def update_package(self, package_name, source_package_name, **kwargs):
        """
        It will compare package and update package. It will replace a package.
        source_package_name, #source package name
        package_slug,         #destination package name
        source_package,       # fully qualified name of package
        """
        force = kwargs.get('force', False)
        version = kwargs.get('label', None)
        current_account = kwargs.get('current_account')
        source_package = source_package_name
        account = current_account
        if package_name:
            identifiers = package_name.split("/")
            if len(identifiers) > 1:
                if (account == identifiers[0]):
                    package_slug = identifiers[1]
                else:
                    raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])
            else:
                package_slug = identifiers[0]

        if source_package_name:
            identifiers = source_package_name.rsplit("/")
            if len(identifiers) > 1:
                account_slug = identifiers[0]
                source_package_name = identifiers[1]
            else:
                account_slug = current_account
                source_package_name = identifiers[0]
        try:
            if version or (current_account != account_slug):
                source_package = account_slug+'/'+source_package_name
                # source = os.path.join(account_slug,source_package_name)
                if not version:
                    try:
                        info = self.network.get_canonical(account_slug, source_package_name)
                        version = info.to_dict()['label']
                    except (BlendedException, ValueError) as e:
                        raise BlendedException(e.args)
                hub_package = self.backend.get_package(source_package, version=version)
            else:
                hub_package = self.backend.get_package(source_package_name)
        except (IndexError, OSError, BlendedException)as exc:
            try:
                if version:
                    self.install_package(source_package, user_slug=account_slug,
                                         label=version, current_account=current_account)
                    hub_package = self.backend.get_package(source_package, version=version)
                else:
                    self.pull_package(source_package_name,
                                      True, draft=True, user_slug=account_slug,
                                      label=None, current_account=current_account)
                    hub_package = self.backend.get_package(source_package_name)
            except BlendedException as exc:
                raise BlendedException(exc)
            except ValueError:
                raise ValueError('Package \"%s\" is not present in local.' % source_package_name)
        if package_name == source_package:
            return package_name
        for item1 in hub_package.content:
            if item1.name == '_package.json':
                hub_package.content.remove(item1)
        if self.backend.directory_path.endswith('lib'):
            # self.backend.directory_path= self.backend.directory_path.split('/lib')[0]
            self.backend.directory_path = self.backend.directory_path.split('lib')[0].rstrip(os.sep)
        try:
            package = self.backend.get_package(package_slug)
        except (OSError, BlendedException)as exc:
            try:
                self.pull_package(package_slug,
                                  True, draft=True, user_slug=account,
                                  label=version, current_account=current_account)
                package = self.backend.get_package(package_slug)
            except BlendedException as exc:
                raise BlendedException(exc)
            except ValueError:
                raise ValueError('Package \"%s\" is not present in local.' % package_slug)
        local_last_hash = self.backend.get_hash(package_slug)
        for item in package.content:
            if item.name != '_package.json':
                try:
                    os.remove(item.location)
                except:
                    try:
                        shutil.rmtree(item.location)  # will delete a directory and all its contents.
                    except:
                        pass

        response = ''
        if hub_package:
            response = self.backend.update_src_copy_dst(hub_package.content,
                                                        source_package_name,  # source package name
                                                        package_slug,         # destination package name
                                                        source_package,       # fully qualified name of package
                                                        account_slug,
                                                        version=version)
        return response

    def install_initial_packages(self, anonymous_user, anonymous_path):
        """
        install all free package when we install pip server.
        """
        file_list = []
        if os.path.exists(anonymous_path):
            file_list = os.listdir(anonymous_path)
        response = self.network.get_package_initial()
        response = response.to_dict()
        pack_list = response.get('items', None)
        if pack_list:
            for package in pack_list:
                package_name = package.get('name')
                pack_slug = package.get('slug')
                try:
                    label = package.get('version')
                except:
                    label = None
                if anonymous_user == "anonymous":
                    if pack_slug not in file_list:
                        try:
                            response = self.package_clone(
                                           package_name, new_name=None,
                                           draft=False, label=label,
                                           description="", current_account=anonymous_user)
                        except (BlendedException, OSError):
                            pass

    def copy_anonymous_to_login_user(self, anonymous_account, current_account):
        """
        copy src folder of Anonymous to first login user's folder!!!
        """
        canonical_type = None
        diff_package = []
        response = self.network.get_package_initial()
        response = response.to_dict()
        ini_pack_list = response.get('items', None)
        dir_path = self.backend.blended_dir
        anonymoss_dir = os.path.join(dir_path, anonymous_account, 'src')
        current_dir = os.path.join(dir_path, current_account, 'src')
        new_list = []
        self.backend.set_src
        if os.path.exists(anonymoss_dir):
            pack_list = os.listdir(anonymoss_dir)
            for pack in pack_list:
                try:
                    new_list.append(pack)
                    copy_tree(os.path.join(anonymoss_dir, pack), os.path.join(current_dir, pack))
                    self.backend.update_package_anonymous_to_login_user(pack, current_dir, current_account)
                except:
                    pass

            for pack in new_list:
                try:
                    package = self.backend.get_package(pack)
                    self.backend.set_hash(package, package.hash)
                    try:
                        hub_package = self.network.download_draft(current_account, pack, as_hashes="1")
                        hub_jptf, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
                        if self.backend.directory_path.endswith('src'):
                            package_slug_temp = os.path.join(self.backend.directory_path, pack)
                        else:
                            package_slug_temp = os.path.join(self.backend.directory_path, self.backend.src, pack)
                        hub_package = self.de_jptf(hub_jptf, as_hashes=True, package_slug=package_slug_temp)
                        hub_package = self.backend.get_class('intermediary')(
                                       pack, content=hub_package,
                                       name=pack, hash=package_hash)
                        if package_hash == package.hash:
                            pass
                        else:
                            #title = ""
                            #for item in hub_package.content:
                            #    if item.name == '_package.json':
                            #        package_dict = json.loads(item.content)
                            #        title = package_dict['title']
                            title = ''
                            try:
                                title = self.get_title(current_account, pack)
                            except Exception:
                                pass
                            try:
                                differences = self.compare_package(hub_package, package, package.hash, "push")
                                diff_package.append('"' + title +'" ('+ pack +')')
                            except TypeError:
                                pass
                    except BlendedException as exc:
                        # response = self.push_package(pack, force=False, user_slug=current_account, current_account=current_account)
                        pass
                except BlendedException as exc:
                    raise BlendedException(exc.args)
        return diff_package

    def account_login(self, username, password):
        """
        account login call and stores sessionkey in filesystem.
        """
        pass

    def create_account(self, **kwargs):
        """
        """
        try:
            response = self.network.create_account(kwargs)
        except BlendedException as exc:
            raise BlendedException(exc)
        return response

    def activation_solution(self, challenge):
        """
        :param challenge:
        :return: solution
        """
        operands = challenge['operands']
        operator = challenge['operator']
        if operator == 'SQUARE':
            num = operands[0]
            return num ** 2

        num1, num2 = operands

        if operator == 'DIVIDE':
            solution = int(num1 / num2)
        elif operator == 'MULTIPLY':
            solution = num1 * num2
        elif operator == 'SUM':
            solution = num1 + num2
        elif operator == 'SUBTRACT':
            solution = num1 - num2
        elif operator == 'MODULO':
            solution = int(num1 % num2)

        return solution

    def update_account(self, user_pk, **kwargs):
        """
        """
        try:
            response = self.network.update_account(user_pk, kwargs)
        except BlendedException as exc:
            raise BlendedException(exc)

    def get_current_account(self, user_pk):
        """
        """
        try:
            response = self.network.get_current_account(user_pk)
        except BlendedException as exc:
            raise BlendedException(exc)
        return response

    def get_account_list(self, user_pk):
        """
        """
        try:
            response = self.network.get_account_list(user_pk)
        except BlendedException as exc:
            raise BlendedException(exc)
        return response

    def invite_user(self, user_slug, **kwargs):
        """
        :param user_slug:
        :param kwargs:
        :return:
        """
        try:
            response = self.network.invite_user(user_slug, kwargs)
        except BlendedException as exc:
            raise BlendedException(exc.args[0])
        return response

    def accept_invite(self, user_slug, **kwargs):
        """
        :param user_slug:
        :param kwargs:
        :return:
        """
        try:
            response = self.network.add_account_user(user_slug, kwargs)
        except BlendedException as exc:
            raise BlendedException(exc)
        return response

    def get_account_users(self, slug):
        """
        """
        try:
            response = self.network.get_account_users(slug)
        except BlendedException as exc:
            raise BlendedException(exc)
        return response

    def revoke_account(self, slug, account_slug):
        """
        """
        try:
            response = self.network.remove_account(slug, account_slug)
        except BlendedException as exc:
            raise BlendedException(exc)
        return response

    def set_current_account(self, account_name):
        """
        :param account_name:
        :return:
        """
        body = {'slug': account_name}
        try:
            response = self.network.set_current_account(body)
        except BlendedException as exc:
            raise BlendedException(exc)

        return response

    def account_email_verification(self, email):
        """
        """
        body = {'email': email}
        try:
            response = self.network.resend_account_verification_email(body)
        except BlendedException as exc:
            raise BlendedException(exc)
        return

    def create_package(self, account_name, package_name, package_type, description, package_title,
                       primary_category, secondary_category=None):
        """
        """
        error_list = []
        body = {}
        identifiers = package_name.rsplit("/")
        if not self.backend.directory_path.endswith('src'):
            self.backend.set_src
        if len(identifiers) > 1:
            if (account_name == identifiers[0]):
                package_name = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0], 5011)
        get_local_package = None
        try:
            get_local_package = self.backend.get_package(package_name)
        except Exception:
            pass
        try:
            # we have to add some validation sso anonynomus should restrict
            # multiple time package creation
            # create a  package which already exist.
            if not (get_local_package):
                try:
                    if package_type=='theme':
                        self.install_package(BLENDED_ACCOUNT+"/"+BLENDED_BASIC_THEME,
                                            label="canonical", current_account=account_name)
                        self.backend.copy_validate_package(account_name, package_name, BLENDED_BASIC_THEME)
                    elif package_type=='layout':
                        self.install_package(BLENDED_ACCOUNT+"/"+BLENDED_BASIC_LAYOUT,
                                            label="canonical", current_account=account_name)
                        self.backend.copy_validate_package(account_name, package_name, BLENDED_BASIC_LAYOUT)
                    elif package_type=='other':
                        self.install_package(BLENDED_ACCOUNT+"/"+BLENDED_BASIC,
                                            label="canonical", current_account=account_name)
                        self.backend.copy_validate_package(account_name, package_name, BLENDED_BASIC)
                except Exception:
                    pass
            self.backend.create_package(account_name, package_name, package_type, description,
                                        package_title, primary_category, secondary_category)
        except BlendedException as exc:
            if account_name == 'anonymous':
                try:
                    if exc.args[1] == 5011:
                        raise BlendedException('Package \"%s\" is already present in local.' % package_name, 5011)
                except IndexError:
                    raise BlendedException('Package \"%s\" is not present in local.' % package_name, 5011)
            raise BlendedException(exc)
        else:
            if account_name == 'anonymous':
                return package_name, error_list
            package_obj = self.backend.get_package(package_name, entry=False, action='push')
            package = self.as_jptf(package_obj)
            body.update({'documents': package})
            # if description:
            #     body.update({'slug': package_name, 'type': package_type, 'description': description})
            # else:
            body.update({'name': package_name, 'hash_as_token': ''})
            try:
                response = self.network.create_draft(account_name, package_name, body)
            except BlendedException as exc:
                if (isinstance(exc.args[0], dict) and (exc.args[0]['status_code'] == 5092)):
                    shutil.rmtree(os.path.join(self.backend.directory_path, package_name))
                raise BlendedException(exc)
            else:
                tokens = response.to_dict().get('tokens', None)
                media_response, error_list = self.upload_media(account_name, tokens, package_name)
        if media_response:
            package_hash = media_response.to_dict()['package_hash']
            self.backend.set_hash(package_obj, package_hash)
        else:
            package_hash = response.to_dict()['package_hash']
            self.backend.set_hash(package_obj, package_hash)
        return package_name, error_list

    def get_package_acquisition(self, package_name, **kwargs):
        """
        method to get package from hub.
        """
        body = {}
        license_name = kwargs.get('license_name')
        new_name = kwargs.get('new_name')
        identifiers = package_name.split("/")
        label = kwargs.get('label')

        if len(identifiers) > 1:
            account = identifiers[0]
            package_slug = identifiers[1]
        else:
            account = kwargs.get('current_account')
            package_slug = identifiers[0]
        if label:
            body.update({'label': label})

        if new_name:
            body.update({'new_package_slug': new_name})

        if license_name:
            body.update({'type': 'get', 'license_name': license_name})
        else:
            body.update({'type': 'get'})

        try:
            response = self.network.acquire_package(account, package_slug, body)
        except PackageNameExistsException as ex:
            raise PackageNameExistsException(ex)
        except BlendedException as exc:
            raise BlendedException(exc)

        return response

    def package_detail(self, account_slug, package_name):
        """
        """
        identifiers = package_name.split("/")
        if len(identifiers) > 1:
            if (account_slug == identifiers[0]):
                package_name = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])
        try:
            response = self.network.get_package_details(account_slug, package_name)
        except BlendedException as exc:
            raise BlendedException(exc)
        return response

    def package_share(self, account_slug, package_id, **kwargs):
        """
        """
        account_name = kwargs.get('account_name')
        email = kwargs.get('email')
        get = kwargs.get('get')
        auto_share_packages = kwargs.get('auto_share_packages', [])
        identifiers = package_id.split("/")
        if len(identifiers) > 1:
            if (account_slug == identifiers[0]):
                package_id = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])

        if get:
            try:
                response = self.network.get_acquired_package_account_list(account_slug, package_id)
                return response
            except BlendedException as exc:
                raise BlendedException(exc)
        
        try:
            self.network.get_canonical(account_slug, package_id)
        except BlendedException as exc:
            raise BlendedException(exc)

        if account_name:
            body = {'type': 'share', 'account_slug': account_name}
        elif email:
            body = {'type': 'share', 'email': email}
        else:
            body = {'type': 'share', 'account_slug': account_name}

        if auto_share_packages:
            body['auto_share_packages'] = auto_share_packages

        try:
            package = self.backend.get_package(package_id)
        except (OSError, AttributeError):
            try:
                response = self.network.acquire_package(account_slug, package_id, body)
            except BlendedException as exc:
                raise BlendedException(exc)
            return True
        try:
            hub_package = self.network.download_draft(account_slug, package_id, as_hashes="1")
        except BlendedException:
            raise BlendedException("Before sharing a package, please Push package \"%s\"." % (package_id))
        try:
            response = self.network.acquire_package(account_slug, package_id, body)
        except BlendedException as exc:
            raise BlendedException(exc)
        return True

    def package_transfer(self, account_slug, package_id, **kwargs):
        """
        """
        auto_share_packages = kwargs.get('auto_share_packages', [])
        purchase_packages = kwargs.get('purchase_packages', [])
        account_name = kwargs.get('account_name')
        email = kwargs.get('email')
        identifiers = package_id.split("/")
        if len(identifiers) > 1:
            if (account_slug == identifiers[0]):
                package_id = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])

        if account_name:
            body = {'type': 'transfer', 'account_slug': account_name}
        elif email:
            body = {'type': 'transfer', 'email': email}
        else:
            body = {'type': 'transfer', 'account_slug': account_name}
        if auto_share_packages:
            body['auto_share_packages'] = auto_share_packages
        if purchase_packages:
            body['purchase_packages'] = purchase_packages
        try:
            package = self.backend.get_package(package_id)
        except (OSError, AttributeError):
            try:
                response = self.network.acquire_package(account_slug, package_id, body)
            except BlendedException as exc:
                raise BlendedException(exc)
            if os.path.exists(os.path.join(self.backend.blended_directory_path, account_slug, 'lib', account_slug, package_id)):
                try:
                    shutil.rmtree(os.path.join(self.backend.blended_directory_path, account_slug, 'lib', account_slug, package_id))
                except:
                    pass
            return True
        try:
            hub_package = self.network.download_draft(account_slug, package_id, as_hashes="1")
            hub_jptf, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
        except BlendedException as exc:
            try:
                if exc.args[0]['status_code'] == 5002:
                    raise BlendedException(exc)
            except (KeyError, AttributeError):
                pass
            raise BlendedException("Before transferring a package, please Push package \"%s\"." % (package_id))
        if package_hash == package.hash:
            try:
                for item in package.content:
                    if item.name == '_package.json':
                        package_dict = json.loads(item.content)
                        dependency_list = []
                        try:
                            dependency_list = package_dict['dependencies']
                        except Exception:
                            pass
                        package_name_list_in_string = ''
                        if dependency_list:
                            version_list = self.backend.dependency_version_check(package_dict['dependencies'], action='transfer')
                            if version_list:
                                for i, item in enumerate(version_list):
                                    package_name_list_in_string += item
                                    if (len(version_list)) != (i+1):
                                        package_name_list_in_string += ', '
                                raise BlendedException("Operation not allowed with dependency as draft version, "
                                                       "for dependency package \"%s\"." % (package_name_list_in_string))
            except BlendedException as exc:
                raise BlendedException(exc)
            try:
                response = self.network.acquire_package(account_slug, package_id, body)
            except BlendedException as exc:
                raise BlendedException(exc)
        else:
            title = ''
            try:
                title = self.get_title(account_slug, package_id)
            except Exception:
                pass
            error_msg = ('\nWarning: Package is out-of-sync\n'
                        'Your local copy of Package "%s" (%s) is out-of-sync with the Hub. '
                        'Before transfer, you need to pull or push in order to sync up with '
                        'the Hub.' % (title, package_id))
            raise BlendedException(error_msg)
        if os.path.exists(os.path.join(self.backend.blended_directory_path, account_slug, 'lib', account_slug, package_id)):
            try:
                shutil.rmtree(os.path.join(self.backend.blended_directory_path, account_slug, 'lib', account_slug, package_id))
            except:
                pass
        if os.path.exists(os.path.join(self.backend.directory_path, package_id)):
            try:
                shutil.rmtree(os.path.join(self.backend.directory_path, package_id))
            except:
                pass
        return True

    def lib_to_src_clone(self, account, current_account, package_slug, body):
        """
        """
        canonical_type = None
        package_name = package_slug
        try:
            package_title = body['package_title']
            new_name = body['new_package_slug']
            action = body['action']
            primary_category = body['primary_category']
            label = body['label'].lower()
            lib_path = os.path.join(self.backend.directory_path, 'lib', account, package_slug)
            src_path = os.path.join(self.backend.directory_path, 'src')
            if label == "draft":
                try:
                    pack_path_in_src = os.path.join(self.backend.directory_path, 'src', package_slug)
                    if os.path.exists(pack_path_in_src):
                        package_name = self.copy_lib_to_src(
                                           current_account, account,
                                           package_slug, pack_path_in_src,
                                           src_path,  new_name=new_name,
                                           package_title=package_title,
                                           primary_category=primary_category,
                                           )
                    else:
                        if current_account == 'anonymous':
                            # raise BlendedException("Package \"%s\" is Not present in local. Please login!" % package_slug)
                            raise BlendedException("Package \"%s\" is not present in your local. "
                                                   "Please login to check it on HUB." % package_slug)
                        hub_package = self.network.download_draft(account, package_slug)
                        hub_package, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
                        hub_package = self.de_jptf(hub_package)
                        hub_package = self.backend.get_class('intermediary')(
                                          package_slug, content=hub_package,
                                          name=package_slug, hash=package_hash
                                          )
                        self.save_local(package_name, intermediary_object=hub_package, draft=True)
                        package_name = self.copy_lib_to_src(
                                           current_account, account, package_slug,
                                           pack_path_in_src, src_path, new_name=new_name,
                                           package_title=package_title,
                                           primary_category=primary_category,
                                           )
                except BlendedException as exc:
                    raise BlendedException(exc)
            elif label:
                if package_slug in self.backend.packages_in_lib(account):
                    if os.path.exists(os.path.join(lib_path, label)):
                        pass
                    else:
                        self.install_package(package_slug, label=label, current_account=account, anonymous_user=current_account)
                else:
                    self.install_package(package_slug, label=label, current_account=account, anonymous_user=current_account)
                if label == 'canonical':
                    label = self.backend.get_canonical(account,  package_slug, current_account=current_account)
                lib_path = os.path.join(lib_path, label)
                package_name = self.copy_lib_to_src(current_account, account,
                                                    package_slug, lib_path, src_path,
                                                    new_name=new_name, action=action,
                                                    label=label, package_title=package_title,
                                                    primary_category=primary_category,)
        except BlendedException as e:
            raise BlendedException(e)
        except OSError as e:
            raise OSError(e.args[0])

        return package_name

    def copy_lib_to_src(self, current_account, account,
                        package_name, lib_path, src_path,
                        new_name=None, action=None, label=None,
                        package_title=None, primary_category=None):
        """
        """
        if new_name:
            package_name = new_name
        if self.backend.directory_path.endswith('src'):
            src_path = os.path.join(self.backend.directory_path, package_name)
        else:
            src_path = os.path.join(self.backend.directory_path, 'src', package_name)
        res = {}
        try:
            res = self.package_detail(current_account, package_name)
        except Exception as e:
            res = None
        try:
            if ((not res) or (current_account == 'anonymous')) and (not os.path.exists(src_path)):
                if self.backend.directory_path.endswith('src'):
                    src_path = os.path.join(self.backend.directory_path, package_name)
                elif self.backend.directory_path.endswith(package_name):
                    src_path = src_path
                else:
                    src_path = os.path.join(self.backend.directory_path, 'src', package_name)
                copy_tree(lib_path, src_path)
                if current_account == 'anonymous':
                    try:
                        self.backend.set_src
                        self.backend.create_package(current_account, package_name, '', '', package_title, primary_category)
                    except BlendedException as exc:
                        raise BlendedException(exc)
                elif action == 'pull':
                    pass
                else:
                    self.create_package(current_account, package_name, '', '', package_title, primary_category)
            else:
                # This is pull by verion force copy from lib!
                # we will restrict here to pull shared package.!
                if action == 'pull':
                    try:
                        copy_tree(lib_path, src_path)
                        return label
                    except Exception as exc:
                        raise BlendedException(exc)
                else:
                    raise OSError("Package with this name already Exist.\n ")
        except BlendedException as e:
            try:
                if e.args[0]['status_code'] == 5011:
                    shutil.rmtree(src_path)
            except Exception:
                # either keyError or not removed file error exception occur so we may pass.
                pass
            raise BlendedException(e)
        except OSError as e:
            raise OSError(e.args[0])
        return package_name

    def package_clone(self, package_name, **kwargs):
        """
        """
        body = {}
        new_name = kwargs.get('new_name')
        draft = kwargs.get('draft')
        label = kwargs.get('label')
        description = kwargs.get('description')
        current_account = kwargs.get('current_account')
        package_title = kwargs.get('package_title')
        primary_category = kwargs.get('primary_category')
        secondary_category = kwargs.get('secondary_category') #package.primary_category
        
        action = kwargs.get('action', None)
        identifiers = package_name.split("/")
        if len(identifiers) > 1:
            account = identifiers[0]
            package_slug = identifiers[1]
        else:
            account = current_account
            package_slug = identifiers[0]
        if label == 'canonical':
            try:
                label = self.network.get_canonical(account, package_slug).to_dict()['label']
            except Exception as e:
                pass

        body.update({'action': action})
        if new_name:
            body.update({'new_package_slug': new_name})
        else:
            body.update({'new_package_slug': None})
        if draft:
            body.update({'type': 'clone', 'label': 'draft'})
        elif label:
            body.update({'type': 'clone', 'label': label})
        else:
            if account == current_account:
                body.update({'type': 'clone', 'label': 'draft'})
            else:
                label = 'canonical'
                try:
                    label = self.network.get_canonical(account, package_slug).to_dict()['label']
                except Exception as e:
                    pass
                body.update({'type': 'clone', 'label': label})
        # if package_title:
        body.update({'package_title': package_title, 'primary_category': primary_category})

        try:
            response = self.lib_to_src_clone(account, current_account, package_slug, body)
        except BlendedException as exc:
            raise BlendedException(exc)
        except OSError as e:
            raise OSError(e.args[0])
        return response

    def get_type(self, package_name, **kwargs):
        """
        """
        draft = kwargs.get('draft')
        label = kwargs.get('label')
        current_account = kwargs.get('current_account')
        identifiers = package_name.split("/")
        if len(identifiers) > 1:
            account = identifiers[0]
            package_slug = identifiers[1]
        else:
            account = current_account
            package_slug = identifiers[0]
        if label == 'canonical':
            try:
                package_type = self.network.get_canonical(account, package_slug).to_dict()['type']
                return package_type
            except Exception as e:
                pass
        try:
            if label:
                response = self.network.get_version_details(account, package_slug, label)
            else:
                response = self.network.get_package_details(account, package_slug)
            package_type = response.to_dict()['type']
        except BlendedException as exc:
            raise BlendedException(exc)
        return package_type


    def install_package(self, package_name, **kwargs):
        """
        :param package_name:
        :param kwargs:
        :return:
        """
        canonical_type = None
        package = []
        hub_package = []
        label = kwargs.get('label')
        anonymous_account = kwargs.get('anonymous_user')
        current_account = kwargs.get('current_account')
        identifiers = package_name.rsplit("/")
        if len(identifiers) > 1:
            account = identifiers[0]
            package_slug = identifiers[1]
        else:
            account = current_account
            package_slug = identifiers[0]

        if (label) and (not ((label == 'draft') or (label == 'canonical'))):
            try:
                hub_package = self.network.download(account, package_slug, label)
            except BlendedException as exc:
                raise BlendedException(exc)
        elif label == 'draft':
            try:
                hub_package = self.network.download_draft(account, package_slug)
            except BlendedException as exc:
                raise BlendedException(exc)
        else:
            try:
                hub_package = self.network.download_canonical(account, package_slug)
            except BlendedException as exc:
                raise BlendedException(exc)

        hub_package, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
        package = self.de_jptf(hub_package)
        package = self.backend.get_class('intermediary')(
                                         package_slug, content=package,
                                         name=package_slug, hash=package_hash
                                         )
        if (not label) or (label == 'canonical'):
            label = canonical_type
        if (anonymous_account == 'anonymous') or (current_account == 'anonymous'):
            # current_account = account
            if not label:
                label = 'canonical'
            self.save_local(package_slug, intermediary_object=package,
                            dependency=True, current_account=current_account,
                            account=account, version=label)
            self.backend.set_canonical(account, package_slug, version=canonical_type)
            self.download_dependencies(package, current_account=current_account)
        elif label == 'draft':
            self.save_local(package_slug, intermediary_object=package,
                            dependency=True, account=account,
                            current_account=current_account, draft=True)
            self.download_dependencies(package)
        else:
            self.save_local(package_slug, intermediary_object=package,
                            dependency=True, current_account=current_account,
                            account=account, version=label)
            self.backend.set_canonical(account, package_slug, version=canonical_type)
            self.download_dependencies(package)

    def download_dependencies(self, intermediary_object, current_account=None):
        dependencies = []
        project_dot_json = {}
        if not current_account:
            current_account = self.backend.get_current_account()
        if not intermediary_object:
            return None
        project_dot_json = json.loads([item.content for item in intermediary_object.content
                                      if (item.name in ('_project.json', '_package.json'))][0])
        # project_dot_json = json.loads([item.content for item in intermediary_object.content
        #                                if (item.name == '_package.json')][0])  TO-DO
        dependencies = project_dot_json.get('dependencies')
        if dependencies:
            for dependent_packages in dependencies:
                package_name = dependent_packages.get('name')
                version = dependent_packages.get('version')
                try:
                    self.install_package(package_name,
                                         label=version,
                                         current_account=current_account)
                except BlendedException as exc:
                    try:
                        exc.args[0].args[0]['message'] = ("Acquisition was not found while installing dependency package "
                                                          "\"%s\"." % (package_name))
                        raise BlendedException(exc.args[0])
                    except (AttributeError, KeyError):
                        raise BlendedException("\n%s while installing dependency package "
                                               "\"%s\".\n" % (exc.args[0].args[0].get('message'), package_name))
                                           
                                           
    def pull_package(self, package_name, force=False, **kwargs):
        """
        """
        canonical_type = None
        version = kwargs.get('version')
        replace_from_local_list = kwargs.get('replace_from_local_list', None)
        # package_id = kwargs.get('package_id')
        files = kwargs.get('files')
        is_draft = kwargs.get('draft')
        user_slug = kwargs.get('user_slug')
        label = kwargs.get('label')
        current_account = kwargs.get('current_account')
        if package_name:
            identifiers = package_name.rsplit("/")
            if len(identifiers) > 1:
                account = identifiers[0]
                package_slug = identifiers[1]
            else:
                account = current_account
                package_slug = identifiers[0]
        # if account=='anonymous':
        #     raise BlendedException("You are not logged in. Please log in or create an account.", 5012)
        if files:
            files_intermediary = []
            for item in files:
                item = item.replace(os.sep, '/')
                checkin = self.network.get_detail_document(account, package_slug, item)
                try:
                    hub_package, package_hash, canonical_type = self._remove_root_from_jptf(checkin)
                    hub_package = self.de_jptf(hub_package)
                    hub_package = self.backend.get_class('intermediary')(
                                                         package_slug, content=hub_package,
                                                         name=package_slug, hash=package_hash)
                except BlendedException as exc:
                    raise BlendedException(exc)
                if hub_package.content:
                    files_intermediary.append(hub_package.content[0])
                else:
                    raise BlendedException("\"%s\" is not present on hub "
                                           "please give correct file name." % item, 5012)
            hub_package = self.backend.get_class('intermediary')(
                                                 package_slug, content=files_intermediary,
                                                 name=package_slug, hash=package_hash)
            try:
                if hub_package.content:
                    self.save_local(package_slug, intermediary_object=hub_package, files=True)
                else:
                    raise BlendedException("\"%s\" is not present on hub "
                                           "please give correct file name." % item, 5012)
            except BlendedException as exc:
                    raise BlendedException(exc)
            # try:
            #     self.download_dependencies(hub_package)
            # except BlendedException as exc:
            #     raise BlendedException(exc)
            return []

        if replace_from_local_list:
            try:
                hub_package, package_hash, canonical_type = self._remove_root_from_jptf(replace_from_local_list)
                hub_package = self.de_jptf(hub_package)
                hub_package = self.backend.get_class('intermediary')(
                                                      package_slug, content=hub_package,
                                                      name=package_slug, hash=package_hash)
            except BlendedException as exc:
                raise BlendedException(exc)
            try:
                if is_draft:
                    self.save_local(package_slug, intermediary_object=hub_package, draft=True)
                else:
                    self.save_local(package_slug, intermediary_object=hub_package,
                                    current_account=current_account, account=account)
                self.download_dependencies(hub_package)
            except BlendedException as exc:
                raise BlendedException(exc)
            else:
                return []

        if force:
            try:
                hub_package = self.network.download_draft(account, package_slug)
            except BlendedException as exc:
                raise BlendedException(exc)
        elif is_draft:
            try:
                hub_package = self.network.download_draft(account, package_slug, as_hashes="1")
                hub_jptf, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
                if self.backend.directory_path.endswith('src'):
                    package_slug_temp = os.path.join(self.backend.directory_path, package_slug)
                else:
                    package_slug_temp = os.path.join(self.backend.directory_path, self.backend.src, package_slug)
                hub_package = self.de_jptf(hub_jptf, as_hashes=True, package_slug=package_slug_temp)
                hub_package = self.backend.get_class('intermediary')(
                                                      package_slug, content=hub_package,
                                                      name=package_slug, hash=package_hash,
                                                      as_hashes=True)
            except BlendedException as exc:
                raise BlendedException(exc)
        elif label:
            try:
                hub_package = self.network.download(account, package_slug, label, as_hashes="1")
            except BlendedException as exc:
                raise BlendedException(exc)
        else:
            try:
                hub_package = self.network.download_canonical(account, package_slug)
                # account ,version , as_hash must be here in above line.
            except BlendedException as exc:
                raise BlendedException(exc)
        if force:
            try:
                hub_package, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
                hub_package = self.de_jptf(hub_package)
                hub_package = self.backend.get_class('intermediary')(
                                                     package_slug, content=hub_package,
                                                     name=package_slug, hash=package_hash)
            except BlendedException as exc:
                raise BlendedException(exc)

            try:
                if is_draft:
                    self.save_local(package_slug, intermediary_object=hub_package, draft=True)
                else:
                    self.save_local(package_slug, intermediary_object=hub_package,
                                    current_account=current_account, account=account)
                self.download_dependencies(hub_package)
            except BlendedException as exc:
                raise BlendedException(exc)
            else:
                return []
        # I should use hub package for this FILE_NOT_FOUND/ local package have dependecy as_hashes==1 need to change
        if is_draft:
            package = self.get_package(package_name, "as_hash", version='draft', action='pull')
            if isinstance(package, list):
                self.download_dependencies(package[0])
                return FILE_NOT_FOUND
        else:
            package = self.get_package(package_name, "as_hash", version=label, action='pull')
            if isinstance(package, list):
                self.download_dependencies(package[0])
                return FILE_NOT_FOUND
        local_last_hash = self.backend.get_hash(package_slug)
        differences = self.compare_package(hub_package, package, local_last_hash, "pull")
        if differences:
            return [differences, package]
        else:
            self.download_dependencies(package)
            return ''

    def as_partial_jptf(self, diff_list, package_obj):
        """
        """
        package_name = package_obj.name
        _hash = package_obj.hash
        for item in diff_list:
            for key, value in item.items():
                if key == 'removed':
                    removed = value
                if key == 'added':
                    added = value
                if key == 'update':
                    update = value
                if key == 'total':
                    total = value
        obj_list = []
        obj = self.as_jptf(total)
        return obj

    def push_package(self, package_name, **kwargs):
        """
        """
        canonical_type = None
        force = kwargs.get('force')
        files = kwargs.get('files')
        version = kwargs.get('version')
        partial_jptf = kwargs.get('replace_from_hub_list')
        package_id = kwargs.get('package_id')
        user_slug = kwargs.get('user_slug')
        account = kwargs.get('current_account')
        if package_name:
            identifiers = package_name.split("/")
            if len(identifiers) > 1:
                if (account == identifiers[0]):
                    package_slug = identifiers[1]
                else:
                    raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0], 5011)
            else:
                package_slug = identifiers[0]
        try:
            package = self.backend.get_package(package_slug, action='push')
        except BlendedException as exc:
            raise BlendedException(exc)
        except OSError as exc:
            raise BlendedException(exc)
        if package:
            same_name_file_folder = self.intermediary_check_dublicate(package)
            if same_name_file_folder:
                raise BlendedException({"message": same_name_file_folder, 'status_code': 6000})

        local_last_hash = self.backend.get_hash(package_slug)

        if partial_jptf:
            return self.save_hub(account, package_slug,
                                 package, local_last_hash=local_last_hash,
                                 partial_jptf=partial_jptf, force=force)
        # if force:
        #     try:
        #         return self.save_hub(account, package_slug, package, force=True)
        #    except BlendedException as exc:
        #         raise BlendedException(exc)
        try:
            hub_package = self.network.download_draft(account, package_slug, as_hashes="1")
            hub_jptf, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
            if self.backend.directory_path.endswith('src'):
                package_slug_temp = os.path.join(self.backend.directory_path, package_slug)
            else:
                package_slug_temp = os.path.join(self.backend.directory_path, self.backend.src, package_slug)
            hub_package = self.de_jptf(hub_jptf, as_hashes=True, package_slug=package_slug_temp)
            hub_package = self.backend.get_class('intermediary')(
                                       package_slug, content=hub_package,
                                       name=package_slug, hash=package_hash, as_hashes=True)
        except BlendedException as exc:
            try:
                if exc.args[0]['status_code'] == 5008:
                    package_details = self.backend.read_package_json(package_slug)
                    try:
                        package_type = package_details['type']
                    except KeyError:
                        package_type = False
                    try:
                        description = package_details['description']
                    except KeyError:
                        description = ''
                    try:
                        package_title = package_details['title']
                    except KeyError:
                        # raise BlendedException("Invalid JSON. You need to provide title of package.")
                        package_title = ''
                    try:
                        primary_category = package_details['primary_category']
                    except KeyError:
                        # raise BlendedException("Invalid JSON. You need to provide title of package.")
                        primary_category = ''
                    try:
                        secondary_category = package_details['secondary_category']
                    except KeyError:
                        # raise BlendedException("Invalid JSON. You need to provide title of package.")
                        secondary_category = ''
                    if package_type:
                        package_type = package_type.lower()
                        if package_type in PACKAGE_TYPES:
                            # need to handle erro_list
                            try:
                                self.create_package(account, package_slug.lower(), package_type, description, 
                                                    package_title, primary_category, secondary_category)
                            except BlendedException as e:
                                raise BlendedException(e)
                            return "package_create"
                        else:
                            raise BlendedException('Error: Please enter valid package type. '
                                                   'Choose between "theme", "layout" and "other".', 5010)
                    else:
                        raise BlendedException('Error: Invalid JSON. Please enter package type. '
                                               'Choose between "theme", "layout" and "other".', 5010)
                else:
                    raise BlendedException(exc)
            except BlendedException as exc:
                raise BlendedException(exc.args[0])
            except Exception:
                raise BlendedException(exc)
        if not self.backend.check_package_dot_json_presense(package):
            raise BlendedException("Invalid package. \"_package.json\" file not found. "
                                   "This file must be present on root directory. ", 5010)
        differences = self.compare_package(hub_package, package, local_last_hash, "push")
        file_obj = ''
        if files and not differences:
            file_obj = self.file_flag_diff(differences, files, package)
            if len(file_obj) > 1:
                return file_obj
            else:
                return [file_obj[0], package]
        if differences:
            if len(differences) > 1:
                if files:
                    file_obj = self.file_flag_diff(differences[1], files, package)
                    if len(file_obj) > 1:
                        return file_obj
                    return [file_obj[0], package]
                else:
                    return [differences, package]
            else:
                if files:
                    return ['False_flag', differences]
        else:
            return ''

    def file_flag_diff(self, diff_list, files, package_obj):
        """
        """
        removed = ''
        file_obj = []
        not_exist = []
        package_name = package_obj.name
        for item in diff_list:
            for key, value in item.items():
                if key == 'removed':
                    removed = value
                if key == 'added':
                    added = value
                if key == 'update':
                    update = value
                if key == 'total':
                    total = value

        if removed:
            for item in files:
                # files_obj  = [l_item for l_item in  removed if l_item.location.split(package.name)[-1]==item.split(package.name)[-1]]
                for l_item in removed:
                    if l_item.location.split(package_name)[-1] == item.split(package_name)[-1]:
                        files.remove(item)
                        file_obj.append(l_item)
        if files:
            for item in files:
                res = self.check_in_local(item, package_obj.content, package_name)
                if res:
                    file_obj.append(res)
                else:
                    not_exist.append(item)
        if not_exist:
            return [True, not_exist]
        else:
            diff_list = []
            if file_obj:
                diff_list = self._partial_intermediary_obj(file_obj, package_name, diff_list)
            file_obj = diff_list
            return [file_obj]

    def check_in_local(self, _file, project_object, package_name=None):
        """
        """
        for index, item in enumerate(project_object):
            if(type(item.content) is list):
                if not item.content:
                    continue
                else:
                    item = self.check_in_local(_file, item.content, package_name=package_name)
                    if item:
                        return item
            else:
                location = item.location.split(os.path.join('src', package_name))[-1]
                location = location.split(os.sep, 1)[1]
                if location == _file.split((package_name+'/'))[-1]:
                    return item
        return None

    def compare_package(self, hub_package, current_package, local_last, action):
        """
        """
        hub_hash = hub_package.hash
        local_current = current_package.hash
        if action == "push":
            if local_current == local_last:
                if hub_hash == local_last:
                    return []  # nothing to change
                else:
                    return ['overwrite', self.differences(hub_package, current_package)]
            else:
                if local_last == hub_hash:
                    return ['force', self.differences(hub_package, current_package)]
                else:
                    if hub_hash == local_current:
                        self.backend.set_hash(current_package, hub_hash)
                        return []
                    else:
                        return ['all', self.differences(hub_package, current_package)]
        if action == "pull":
            if local_current == local_last:
                if hub_hash == local_last:
                    return []
                else:
                    return ['force', self.differences(current_package, hub_package)]
            else:
                if local_last == hub_hash:
                    return ['overwrite', self.differences(current_package, hub_package)]
                else:
                    if hub_hash == local_current:
                        self.backend.set_hash(current_package, hub_hash)
                        return []
                    else:
                        return ['all', self.differences(current_package, hub_package)]

        if action == "compare":
            if local_current == local_last:
                if hub_hash == local_last:
                    return []
                else:
                    return ['hub', self.differences(hub_package, current_package)]
            else:
                if local_last == hub_hash:
                    return ['local', self.differences(hub_package, current_package)]
                else:
                    if hub_hash == local_current:
                        self.backend.set_hash(current_package, hub_hash)
                        return []
                    else:
                        return ['total', self.differences(hub_package, current_package)]

    def differences(self, hub_package_intermediary, local_package_intermediary):
        """
        """
        hub_pack_slug = hub_package_intermediary.name
        package_slug = local_package_intermediary.name
        src_hub_pack_slug = os.path.join(self.backend.src, hub_pack_slug)
        src_package_slug = os.path.join(self.backend.src, package_slug)
        hub_differences = self.blendedRecursiveDiff(src_hub_pack_slug,
                                                    src_package_slug,
                                                    hub_package_intermediary.content,
                                                    local_package_intermediary.content, hub_diff=True)

        local_differences = self.blendedRecursiveDiff(src_package_slug,
                                                      src_hub_pack_slug,
                                                      local_package_intermediary.content,
                                                      hub_package_intermediary.content, local_diff=True)

        diff_list = []

        # Below loop gives list of path of files which are removed
        removed = set([doc.location.split(src_hub_pack_slug, 1)[1] for doc in hub_differences]).difference(
                      [doc.location.split(src_package_slug, 1)[1] for doc in local_differences])
        # Below loop gives list of intermediary objects  of files which are removed
        removed_obj = [l_item for l_item in hub_differences
                       if l_item.location.split(src_package_slug, 1)[-1] in [item for item in removed]]
        self._partial_removed_object(removed_obj)

        # Below loop gives list of path of files which are added
        added = set([doc.location.split(src_package_slug, 1)[1] for doc in local_differences]).difference(
                    [doc.location.split(src_hub_pack_slug, 1)[1] for doc in hub_differences])
        # Below loop gives list of intermediary objects of files which are added
        added_obj = [l_item for l_item in local_differences
                     if l_item.location.split(src_package_slug, 1)[-1] in [item for item in added]]
        total_added = added_obj

        # Below loop gives list of path of files which are update
        update = set([doc.location.split(src_package_slug, 1)[1] for doc in local_differences]).intersection(
                     [doc.location.split(src_hub_pack_slug, 1)[1] for doc in hub_differences])
        # Below loop gives list of intermediary objects of files which are update
        update_obj = [l_item for l_item in local_differences
                      if l_item.location.split(src_package_slug, 1)[-1] in [item for item in update]]
        diff_list = self._partial_intermediary_obj(added_obj, package_slug, diff_list)
        diff_list = self._partial_intermediary_obj(update_obj, package_slug, diff_list)
        diff_list = self._partial_intermediary_obj(removed_obj, package_slug, diff_list)
        unique_diff = []
        total_differences = []
        for item in diff_list:
            if item.location not in [doc.location for doc in unique_diff]:
                # if item.__class__.__name__ == 'Directory':
                #    rm_doc = [rm for rm in removed_obj if rm.location==item.location]
                #    if rm_doc:
                #        item.rem_from_hub_dir = rm_doc[0].rem_from_hub_dir
                #   added_doc = [ad for ad in added_obj if ad.location==item.location]
                #    if added_doc:
                #        item.add_emp_dir_on_hub = added_doc[0].add_emp_dir_on_hub
                unique_diff.append(item)

        if removed_obj:
            total_differences.append({'removed': removed_obj})
        if added_obj:
            total_differences.append({'added': total_added})
        if update_obj:
            total_differences.append({'update': update_obj})
        total_differences.append({'total': unique_diff})
        return total_differences

    def _partial_removed_object(self, removed_obj):
        """
        """
        for deleted in removed_obj:
            if deleted.__class__.__name__ == 'Directory':
                if not deleted.content:
                    deleted.rem_loc_dir = True
                self._partial_removed_object(deleted.content)
            if deleted.__class__.__name__ == 'BinaryFile':
                deleted.hash = None

    def _partial_intermediary_obj(self, obj, package_slug, diff_list):
        """
        """
        src_package_slug = os.path.join(self.backend.src, package_slug)
        for item in obj:
            location = item.location.split(src_package_slug, 1)[1]
            path = location.split(os.sep)
            if len(path) <= 2:
                diff_list.append(item)
            else:
                diff_list.append(self._create_partial_directory(path[1:], item, package_slug, diff_list))
                pass
        return diff_list

    def _create_partial_directory(self, path, item, package_slug, diff_list, location=None):
        """
        """
        if not location:
            location = os.path.join(package_slug, path.pop(0))
        else:
            path.pop(0)
            location = location

        diff_obj = [doc for doc in diff_list
                    if doc.location.split(package_slug, 1)[1] == location.split(package_slug, 1)[1] and not doc.empty_dir]
        if len(path) > 1:
            if diff_obj:
                dir_obj = diff_obj[0]
                obj = self._create_partial_directory(path, item, package_slug,
                                                     dir_obj.content, location=os.path.join(location, path[0]))
                dir_obj.content.append(obj)
            else:
                obj = self._create_partial_directory(
                          path, item, package_slug, diff_list,
                          location=os.path.join(location, path[0])
                          )
                dir_obj = self.backend.get_class('Directory')(location, content=[obj], removed=True)
        else:
            if diff_obj:
                dir_obj = diff_obj[0]
                sub_dir = [sub_dir for sub_dir in dir_obj.content if sub_dir.name == item.name]
                if ((sub_dir) and
                        (sub_dir[0].rem_from_hub_dir == item.rem_from_hub_dir) and
                        (sub_dir[0].add_emp_dir_on_hub == item.rem_from_hub_dir)):
                    sub_dir = sub_dir[0]
                    sub_dir.content = item.content
                else:
                    dir_obj.content.append(item)
            else:
                dir_obj = self.backend.get_class('Directory')(location, content=[item], removed=True)
        return dir_obj

    def blendedRecursiveDiff(self, hub_pack_slug, package_slug,
                             hub_package, project_object, file_list=None,
                             hub_diff=False, local_diff=False):
        """
        """
        if not file_list:
            file_list = []
        Directory_Class = self.backend.get_class('Directory')
        try:
            for item in hub_package:
                key = item.name
                value = item.content
                path = item.location.split(hub_pack_slug, 1)[-1]
                local_item = [l_item for l_item in project_object if l_item.location.split(package_slug, 1)[-1] == path]

                if isinstance(item, Directory_Class):
                    if local_item:
                        local_item_obj = local_item[0]
                        if local_item_obj.hash != item.hash:
                            local_item_content = local_item_obj.content
                            if item.empty_dir and hub_diff:
                                item.rem_from_hub_dir = True
                                file_list.append(item)

                            if (local_diff) and (not item.content):
                                item.add_emp_dir_on_hub = True
                                item.empty_dir = True
                                file_list.append(item)
                            if not local_item_content:
                                for i in item.content:
                                    i.empty_dir = True
                                file_list.extend(item.content)
                            else:
                                file_list = self.blendedRecursiveDiff(hub_pack_slug, package_slug, value,
                                                                      local_item_content, file_list=file_list,
                                                                      hub_diff=hub_diff, local_diff=local_diff)
                        else:
                            continue
                    else:
                        file_list.append(item)
                else:
                    if local_item:
                        local_item_obj = local_item[0]
                        if item.hash != local_item_obj.hash:
                            file_list.append(item)
                        else:
                            continue
                    else:
                        file_list.append(item)
            return file_list
        except AttributeError:
            return None

    def merge_package(self, final_package, replace_package, replace_list):
        """
        """
        for file_to_replace in replace_list:
            for file_in_replace_package in replace_package:
                if file_to_replace == file_in_replace_package:
                    pass
            # file = find file_to_replace in replace_package
            # final_package[file_to_replace location] = file
        return final_package

    def intermediary_check_dublicate(self, project_object, unique_file_folder_name=[]):
        """
        """  
        seen = []
        try:
            if project_object.__class__.__name__ == 'Directory':
                project_object = project_object.content
            for index, item in enumerate(project_object):
                key = item.name
                value = item.content
                keys = key.rsplit('.', 1)
                if(len(keys) > 1):
                    key = keys[0]
                if key in seen:
                    location = os.path.dirname(item.location)
                    unique_file_folder_name.append({'name': key, 'path': location})
                else:
                    seen.append(key)
                
                if(type(value) is list):
                    value = self.intermediary_check_dublicate(value, unique_file_folder_name=unique_file_folder_name)
                else:
                    pass
            return unique_file_folder_name
        except AssertionError as exc:
            return None
    
    def context_loader(self, theme_name, current_account='blended', url_query_string='', **kwargs):
        """
        :param url:
        :return:
        """
        #backend = self.backend
        blended_dir = self.backend.blended_dir
        blended_directory_path = os.path.join(blended_dir, current_account)
        self.backend.directory_path = blended_directory_path
        self.backend.current_account = current_account
        self.backend.blended_dir = blended_dir
        self.backend.blended_directory_path = blended_dir
        self.root_directory = self.backend.directory_path
        version = 'blendeddefault'
        if version and url_query_string:
            url = os.path.join(theme_name, version, url_query_string)
        elif version and not url_query_string:
            url = os.path.join(theme_name, version)
        elif not version and url_query_string:
            url = os.path.join(theme_name, url_query_string)
        else:
            url = os.path.join(theme_name)

        url_split = url.split(os.sep)
        account = kwargs.get('account')
        url_path = kwargs.get('path', '')
        length_of_url = len(url_split)
        theme = url_split[0]
        if version == 'blendeddefault':
            version = None
        if length_of_url == 3:
            q_string = url_split[2]
        else:
            q_string = ''
        query_dict = parse_qs(q_string)
        query_string = {}
        if query_dict:
            list_of_query_string = [{key: value[0]} for key, value in query_dict.items()]
            for query in list_of_query_string:
                query_string.update(query)

        if account:
            theme = '%s/%s' % (account, theme)
        context = dict(self.get_package(theme, "context", version))
        if query_string:
            for key, value in query_string.items():
                location = key.split(".")
                location.pop(0)
                context = self.context_change(context, location, value)

        preview_template = ""
        if url_path:    
            keys = url_path.split("/")
            preview_template_dir = context.get('preview')
            preview_template = self.get_page_template(preview_template_dir, keys, 0)      
        else:
            preview_template = context.get('preview').get('home') 
        if not preview_template:
            preview_template = '<div id="main"><div class="fof"><h1>Error 404</h1></div></div>'
        context = {'theme': context}
        # return render_code(preview_template, context)
        return context

    def preview(self, url, **kwargs):
        """
        :param url:
        :return:
        """
        url_split = url.split(os.sep)
        account = kwargs.get('account')
        url_path = kwargs.get('path')
        cached_context = kwargs.get('cached_context')
        length_of_url = len(url_split)
        theme = url_split[0]
        version = url_split[1]
        if version == 'blendeddefault':
            version = None
        if length_of_url == 3:
            q_string = url_split[2]
        else:
            q_string = ''
        query_dict = parse_qs(q_string)
        query_string = {}
        if query_dict:
            list_of_query_string = [{key: value[0]} for key, value in query_dict.items()]
            for query in list_of_query_string:
                query_string.update(query)

        if account:
            theme = '%s/%s' % (account, theme)
        # import pdb;pdb.set_trace()
        if not cached_context:
            context = dict(self.get_package(theme, "context", version))
        else:
            context = cached_context.get('theme')
        if query_string:
            for key, value in query_string.items():
                location = key.split(".")
                location.pop(0)
                context = self.context_change(context, location, value)
        preview_template = ""
        if url_path:    
            keys = url_path.split("/")
            preview_template_dir = context.get('preview')
            preview_template = self.get_page_template(preview_template_dir, keys, 0)      
        else:
            preview_template = context.get('preview').get('home') 
        if not preview_template:
            preview_template = '<div id="main"><div class="fof"><h1>Error 404</h1></div></div>'
        context = {'theme': context}
        # return render_code(preview_template, context)
        return preview_template, context

    def get_page_template(self, intermediary, key, idx):
        """
        # This would be used on flask URL /<string:path>/
        """
        theme_obj = intermediary.get(key[idx])
        if not theme_obj:
            # Directory path given
            # raise Exception(404)
            return ""
        if theme_obj and idx==len(key)-1:
            if isinstance(theme_obj, dict):
                # Directory path given
                # raise Exception(404)
                return ""
        if isinstance(theme_obj, dict):
            return self.get_page_template(theme_obj, key, idx+1)
        elif idx==len(key)-1:
            return theme_obj
        else:
            return ""

    def context_change(self, theme_object, location_array, new_value):
        """
        :param theme_object:
        :param location_array:
        :param new_value:
        :return:
        """
        while(location_array):
            index_value = location_array.pop(0)
            if len(location_array) > 0:
                self.context_change(theme_object[index_value], location_array, new_value)
            else:
                theme_object[index_value] = new_value

        return theme_object

    # def render_code(self, file_content, context):
    #   """
    #   :param file_content: compiled template content
    #   :param context: theme_object or context
    #   :return: rendered content of template.
    #   """
    #   template = env.from_string(file_content, context)
    #   return template.render(context)

    @property
    def set_backend_root(self):
        self.backend.directory_path = self.root_directory

    def download_package(self, package_id, package_name):
        """
        """
        try:
            response = self.network.download(package_id)
        except BlendedException as exc:
            raise BlendedException(exc)
        try:
            intermediary_object = self.de_jptf(response)
            self.backend.save_local(package_name, intermediary_object)
        except BlendedException as exc:
            raise BlendedException(exc)

    def download_package_draft(self, package_id, package_name):
        """
        """
        try:
            response = self.network.download_draft(package_id)
        except BlendedException as exc:
            raise BlendedException(exc)
        try:
            intermediary_object = self.de_jptf(response)
            self.backend.save_local(package_name, intermediary_object)
        except BlendedException as exc:
            raise BlendedException(exc)

    def package_accounts_list(self, slug=None, package_name=None):
        """
        :param slug: Account Name or Account Slug
        :param package_name: Package Name or Package Slug
        :return:
        """
        package_account_list = []
        package_items = []
        try:
            response = self.network.package_accounts_list(slug, package_name)
        except BlendedException as exc:
            raise BlendedException(exc)
        else:
            package_items = response.items
        return package_items

    def packages_list(self, slug=None, **kwargs):
        """
        """
        transfer_by_me = kwargs.get('transfer_by_me')
        transfer_to_me = kwargs.get('transfer_to_me')
        share = kwargs.get('share')
        organization = kwargs.get('organization')
        published = kwargs.get('published')
        purchased = kwargs.get('purchased')
        package_items = []
        if slug == 'anonymous':
            try:
                dir_path = self.backend.blended_dir
                anonymoss_dir = os.path.join(dir_path, slug, 'src')
                if os.path.exists(anonymoss_dir):
                    package_items = os.listdir(anonymoss_dir)
            except Exception as exc:
                raise Exception(exc)
        else:
            try:
                if slug:
                    response = self.network.package_list(
                                   slug, transfer_to_me=transfer_to_me,
                                   transfer_by_me=transfer_by_me, share=share,
                                   organization=organization,published=published,
                                   purchased=purchased,
                                   )
                else:
                    response = self.network.package_list(
                                   transfer_to_me=transfer_to_me,
                                   transfer_by_me=transfer_by_me, share=share,
                                   organization=organization,published=published,
                                   purchased=purchased,
                                   )
            except BlendedException as exc:
                raise BlendedException(exc)
            else:
                package_items = response.items
        return package_items

    def read_package_pk(self, package_name):
        """
        """
        try:
            package_pk = self.backend.read_package_pk(package_name)
        except BlendedException:
            raise BlendedException()
        return package_pk

    def package_extend(self, package_name, **kwargs):
        """
        :param package_name:
        :param kwargs:
        :return:
        """
        canonical_type = None
        new_name = kwargs.get('new_name')
        is_draft = kwargs.get('draft')
        label = kwargs.get('label')
        description = kwargs.get('description')
        current_account = kwargs.get('current_account')
        package_type = kwargs.get('package_type')
        package_title = kwargs.get('package_title')
        hub_package = None
        if not (label or is_draft):
            label = 'canonical'
          
        if package_name:
            identifiers = package_name.rsplit("/")
            if len(identifiers) > 1:
                account = identifiers[0]
                package_slug = identifiers[1]
            else:
                try:
                    account = current_account
                except BlendedException as exc:
                    raise BlendedException(exc)
                package_slug = identifiers[0]
        try:
            if label == 'canonical':
                canonical_info = self.network.get_canonical(account, package_slug)
                label = canonical_info.to_dict()['label']
        except BlendedException as exc:
            raise BlendedException(exc)

        packages = self.backend.packages_in_src()
        lib_packages = self.backend.packages_in_lib(account)
        if (package_slug in packages) and (not label):
            self.backend.set_src
            package = self.backend.get_package(package_slug, entry=False)
            self.set_backend_root
        # elif package_slug in lib_packages:
        #     self.backend.set_lib(account)
        #     package = self.backend.get_package(package_slug, entry=False)
        #     self.set_backend_root
        else:
            if is_draft:
                try:
                    label = 'draft'
                    hub_package = self.network.download_draft(account, package_slug)  # account must be here
                except BlendedException as exc:
                    raise BlendedException(exc)
            else:
                try:
                    hub_package = self.network.download(account, package_slug, label)  # account, version_label  must be here
                except BlendedException as exc:
                    raise BlendedException(exc)
            try:
                hub_package, package_hash, canonical_type = self._remove_root_from_jptf(hub_package)
                package = self.de_jptf(hub_package)
                package = self.backend.get_class('intermediary')(
                                       package_slug, content=package,
                                       name=package_slug, hash=package_hash)
            except BlendedException as exc:
                raise BlendedException(exc)
            try:
                if is_draft:
                    self.save_local(package_slug, intermediary_object=package, draft=True)
                else:
                    self.save_local(package_slug, intermediary_object=package,
                                    dependency=True, current_account=current_account,
                                    account=account, version=label)
                    self.backend.set_canonical(account, package_slug, version=canonical_type)
                    self.download_dependencies(package)
                    # self.save_local(package_slug, intermediary_object=package,
                    #                 current_account=current_account, account=account, version=label)
            except BlendedException as exc:
                raise BlendedException(exc)

        self.backend.set_src
        self.backend.create_extended_package(package_slug, package, new_name, account=account,
                                             description=description, label=label, package_type=package_type,
                                             package_title=package_title)
        self.set_backend_root
        # dependency_packages = self.network.get_dependencies(package_name)
        return True

    def package_snapshot(self, account_slug, slug, **kwargs):
        """
        # here package_id is Package_slug/package_name
        """
        auto_share_packages = kwargs.get('auto_share_packages', [])
        purchase_packages = kwargs.get('purchase_packages', [])
        #skip_validation = kwargs.get('skip_validation', False)
        label = kwargs.get('label')
        identifiers = slug.split("/")
        if len(identifiers) > 1:
            if (account_slug == identifiers[0]):
                slug = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])
        package_name = "%s/%s" % (account_slug, slug)
        current_hash_value = ''
        package = ''
        try:
            package = self.backend.get_package(package_name)
            current_hash_value = package.hash
        except (BlendedException, OSError) as exc:
            try:
                # why we are doing this?
                # To check if it contains multiple/multilevel dependencies.
                # If any version is draft version in dependency list.
                #commented below code in 24cli version
                #self.pull_package(slug, True, draft=True, user_slug=account_slug,
                #                  label=None, current_account=account_slug)
                #package = self.backend.get_package(slug)
                hub_package = self.network.download_draft(account_slug, slug, as_hashes="1")
                hub_jptf, current_hash_value, canonical_type = self._remove_root_from_jptf(hub_package)
            except Exception as exc:
                raise BlendedException(exc.args[0])
        body = {'label': label, 'hash_as_token': current_hash_value}
        if kwargs.get('skip_validation', False):
            body.update({"skip_validation": True})
        if auto_share_packages:
            body['auto_share_packages'] = auto_share_packages
        if purchase_packages:
            body['purchase_packages'] = purchase_packages
        if package:
            try:
                for item in package.content:
                    if item.name == '_package.json':
                        package_dict = json.loads(item.content)
                        dependency_list = []
                        try:
                            dependency_list = package_dict['dependencies']
                        except Exception:
                            pass
                        package_name_list_in_string = ''
                        if dependency_list:
                            version_list = self.backend.dependency_version_check(package_dict['dependencies'], action='snapshot')
                            if version_list:
                                for i, item in enumerate(version_list):
                                    package_name_list_in_string += item
                                    if (len(version_list)) != (i+1):
                                        package_name_list_in_string += ', '
                                raise BlendedException("Operation not allowed with dependency as draft version, "
                                                       "for dependency package \"%s\"." % (package_name_list_in_string))
            except BlendedException as exc:
                raise BlendedException(exc)
        try:
            response = self.network.snapshot(account_slug, slug, body)
        except BlendedException as exc:
            raise BlendedException(exc)
        self.backend.set_src
        return label

    def read_package_name(self, package_id):
        """
        """
        try:
            package_name = self.backend.read_package_name(package_id)
        except BlendedException:
            raise BlendedException()
        return package_name

    def package_canonical(self, account_slug, slug, **kwargs):
        """
        """
        label = kwargs.get('label')
        body = {'is_canonical': True}
        try:
            response = self.network.set_canonical(account_slug, slug, label, body)
        except BlendedException as exc:
            try:
                if exc.args[0]['status_code'] == 5066:
                    pack_detail  = self.network.get_package_details(account_slug, slug)
                    msg = ("You are not allowed to set snapshot version \"%s\" as canonical, "
                           "because it is not included in all the listed licenses of the package "
                           "\"%s\" (%s)." % (label, pack_detail.title, pack_detail.name))
                    exc.args[0]['message'] = msg
            except BlendedException as exc:
                raise BlendedException(exc)
            raise BlendedException(exc)
        return label

    def update_publication(self, response, body, validate_hash_body):
        """
        """
        local_publish_body = body['publication'][0]
        hash_as_token = response['hash_value']
        response.update({'hash_as_token': hash_as_token})
        validate_hash_body.update({'hash_as_token': hash_as_token})
        if not response['publication']:
            response['publication'].append(local_publish_body)
        license_name_exist = False
        
        for item in response['publication']:
            if item['upgrades'] == 'no upgrades':
                item['upgrades'] = None
            if item['license_name'] == local_publish_body['license_name'] and item['license_type']==local_publish_body['license_type']:
                license_name_exist = True
                for key in item.keys():
                    if key == 'versions':
                        item[key] = local_publish_body['versions']
                    else:
                        try:
                            item[key] = local_publish_body[key]
                        except Exception:
                            pass
            else:
                canonical_label = None
                for check_canonical in local_publish_body['versions']:
                    if check_canonical['canonical']:
                        canonical_label  = check_canonical['label']
                if canonical_label:
                    for item1 in item['versions']:
                        if canonical_label and canonical_label == item1['label']:
                            item1['canonical'] = True
                        else:
                            item1['canonical'] = False
        if not license_name_exist:
            response['publication'].append(body['publication'][0])
        return response

    def package_publication(self, account_slug, slug, body, canonical=False, validate=False, get_publish=False):
        """
        Publication of package with version and license.
        For multiple version we need update the publication object.
        """
        identifiers = slug.split("/")
        if len(identifiers) > 1:
            if (account_slug == identifiers[0]):
                slug = identifiers[1]
            else:
                raise BlendedException('Account name \"%s\" is not Current account or valid account.' % identifiers[0])
        response_body = body
        validate_hash_body = {}
        try:
            if canonical and not get_publish:
                canonical_info = self.network.get_canonical(account_slug, slug)
                version = canonical_info.to_dict()['label']
                return version
        except BlendedException as exc:
            raise BlendedException(exc)
        try:
            response = self.network.get_publication(account_slug, slug)
            response = response.to_dict()
            if get_publish:
                return response
            response_body = self.update_publication(response, body, validate_hash_body)
        except BlendedException as exc:
            raise BlendedException(exc)
        
        try:
            self.network.validate_publication(account_slug, slug,  validate_hash_body)
            if validate:
                response = self.network.update_publication(account_slug, slug,  response_body,  commit='0')
                return response
            response = self.network.update_publication(account_slug, slug,  response_body)
            if (response_body['hash_value']==response['hash_value']):
                title = ''
                try:
                    title = self.get_title(account_slug, slug)
                except Exception:
                    pass
                return ('\nAlert: Package Already Published\n'
                        'A package with the exact same settings as '
                        '"%s" (%s) is already published. '
                        'You cannot publish the same package with the same '
                        'settings twice.' % (title, slug))
        except BlendedException as exc:
            try:
                if exc.args[0]['status_code'] == 5100:
                    error_list = self.publication_error_handling(exc.args[0], body, account_slug, slug)
                    return error_list
                else:
                    raise BlendedException(exc)
            except Exception:
                raise BlendedException(exc)
        return "Package \"%s\" is successfully published." % (slug)

    def publication_error_handling(self, error, body, account_slug, slug):
        """
        """
        pack = []
        package_list = []
        error_object = []
        package_name =  ''
        l_type = body['publication'][0]['license_type']
        l_name = body['publication'][0]['license_name']
        error_compatiblity = []
        title = ''
        try:
            title = self.get_title(account_slug, slug)
        except Exception:
            pass
        try:
            if error['errors']:
                error_object.append(error['errors'][0])
            for item in error['publication']:
                package_name = item['package']
                if item['ERROR']:
                    if item['ERROR'][0].get('license_type'):
                        item['ERROR'][0]['license_type'] = ("License Type: More than one license with the same license type \"%s (%s)\", cannot be published when \"Allow to be listed, making it show in search\" is set to YES. However, you will be allowed to add the same license type multiple times when \"Allow to be listed, making it show in search\" is set to NO." % (item['license_type'], item['license_name']))
                    elif item['ERROR'][0].get('license_name'):
                        item['ERROR'][0]['license_name'] = ('You are already using license type "%s" with the license name "%s". You cannot use the same license name twice. Please choose a different license name.'% (item['license_type'], item['license_name']))
                    elif item['ERROR'][0].get('downstream_publication_license_error'):
                        item['ERROR'][0]['downstream_publication_license_error'] = ('Incompatible License: Downstream dependency package "%s" is published with license type "%s" (%s). You can only publish this package  "%s"(%s) with license type %s.'% (item['dependency_of_package'], item['license_type_dependency_of_package'], item['license_name'],title, package_name, item['license_type_dependency_of_package']))
                    error_object.append(item['ERROR'][0])
            versions = error['publication'][0]['versions']
            for item in versions:
                try:
                    if item['ERROR']:
                        if item['ERROR'][0].get('version_validation_status_error'):
                            item['ERROR'][0]['version_validation_status_error'] = item 
                        error_object.append(item['ERROR'][0])
                    elif item['bundle_packages']:
                        for bundle_item in item['bundle_packages']:
                            if bundle_item['ERROR']:
                                if bundle_item['ERROR'][0].get('publication_license_does_not_exist_error'):
                                    bundle_item['ERROR'][0]['publication_license_does_not_exist_error'] = ('Publication License Error: Your upstream dependency package "%s" with specified snapshot label "%s" is not published yet. Please publish your upstream dependencies packages first to proceed with it.' % (bundle_item['package'], bundle_item['label']))
                                elif bundle_item['ERROR'][0].get('license_compatibility_error'):
                                    if bundle_item['package'] in pack:
                                        continue
                                    pack.append(bundle_item['package'])
                                    error_compatiblity.append(('Incompatible License: Upstream dependency package %s contains an incompatible license type, %s (%s), to this publication license type, %s (%s).\nYou can publish package "%s" (%s) if its upstream dependencies are published with license type %s. Still you can publish package "%s" (%s) only with compatible license type %s.\n' % (bundle_item['package'], bundle_item['license_type'], bundle_item['license_name'], l_type, l_name, title, package_name, l_type, title, package_name, bundle_item['license_type'])))
                                    continue
                                    #pack.append(bundle_item['package'])
                                    #package_list.append({'package' : bundle_item['package'], 'label' : bundle_item['label'],
                                    #                     'license_name': bundle_item['license_name'], 
                                    #                     'license_type': bundle_item['license_type'],
                                    #                     'title': bundle_item['title_dependency_of_package']})
                                    #continue
                                error_object.append(bundle_item['ERROR'][0])
                except Exception:
                    pass
            if  error_compatiblity:
                error_object.append({'license_compatibility_error':  error_compatiblity}) 
        except Exception:
            raise BlendedException(error)
        return error_object

    def package_publish(self, account_slug, slug, **kwargs):
        """
        """
        label = kwargs.get('label')
        # package_name = self.read_package_name(package_id)
        # version_id = int(self.backend.get_version_id(package_name, label))
        body = {'publish': True}
        try:
            response = self.network.set_canonical(account_slug, slug, label, body)
        except BlendedException as exc:
            raise BlendedException(exc)
        return "Package \"%s\" is published with version label \"%s\"." % (slug, label)

    def package_addlicense(self, account_slug, slug, license_name, license_price, label):
        """
        """
        body = {'name': license_name, 'price': license_price}
        try:
            response = self.network.add_license(account_slug, slug, label, body)
        except BlendedException as exc:
            raise BlendedException(exc)

    def package_deletelicense(self, package_id, license_name):
        """
        """
        try:
            response = self.network.remove_license(package_id, license_name)
        except BlendedException as exc:
            raise BlendedException(exc)

    def get_package(self, package_name=None, format=None, version=None, trim=True, dependency=False, action=None, download=True):
        """
        it will load the intermediary project object in the jptf structure or in the proper context structure of the json format
        it will call the backend based on the backend name passed to it.for default it will use memory ...#todo
        """
        # package = self.get_package(package_name, "as_hash", version='draft')
        canonical_type = None
        package = {}
        current_account = self.backend.get_current_account()
        if package_name:
            identifiers = package_name.rsplit("/")
            if len(identifiers) > 1:
                account = identifiers[0]
                package_slug = identifiers[1]
            else:
                account = current_account
                package_slug = identifiers[0]
        try:
            if version == 'draft':
                package = self.backend.get_package(package_name, dependency=dependency, action=action)
            elif version == "canonical":
                info = self.backend.get_canonical(account, package_slug)
                if info:
                    package = self.backend.get_package(package_name, dependency=dependency, version=info, action=action)
                else:
                    try:
                        info = self.network.get_canonical(account, package_slug)
                    except BlendedException as exc:
                        raise BlendedException(exc)
                        os._exit(0)
                    self.backend.set_canonical(account, package_slug, info)
                    package = self.backend.get_package(package_name, dependency=dependency,
                                                       version=info.to_dict()['label'], action=action)
            else:
                package = self.backend.get_package(package_name, dependency=dependency, version=version)
        except Exception:
            raise BlendedException("NETWORK NOT AVAILABLE FOR PACKAGE '%s' WITH VERSION '%s'!" %(package_name, version))
        
        if format == "jptf":
            return self.as_jptf(package)
        elif format == "context":
            package = self.as_context(package, trim=trim, dependency=dependency)
            src_or_lib = self.src_or_lib
            if (src_or_lib) and (src_or_lib.endswith('lib') or src_or_lib.endswith('src')):
                backend_directory_path = src_or_lib
            else:
                backend_directory_path = self.backend.directory_path
            package.update({'theme_name': package_slug,
                            'account': account, 'current_account': current_account,
                            'theme_path': backend_directory_path,
                            'root_path': self.root_directory})
            if version and version.lower() != 'draft':
                package.update({'label': version})
            return package
        elif format == "as_hash":
            return package  # self.as_hash(package)
        else:
            return package

    def save_local(self, package_slug, **kwargs):
        """
        save the project in intermediary structure in the local backend based on the backedn used.
        call the backend and use it to save the file in backend (fileystem)
        """
        # package_id = kwargs.get('package_id')
        # draft = kwargs.get('draft')
        # label = kwargs.get('label')
        files = kwargs.get('files')
        intermediary_object = kwargs.get('intermediary_object')
        is_draft = kwargs.get('draft')
        version = kwargs.get('version')
        current_account = kwargs.get('current_account')
        dependency = kwargs.get('dependency')
        account_name = kwargs.get('account')
        try:
            if files:
                self.backend.save_local(package_slug, intermediary_object, files=files)
                return
            if is_draft:
                self.backend.save_local(package_slug, intermediary_object, draft=is_draft)
            elif dependency and version:
                package_name = os.path.join(account_name, package_slug)
                self.backend.save_local(package_name, intermediary_object, dependency=dependency, version=version)
            elif account_name != current_account:
                package_name = os.path.join(account_name, package_slug)
                self.backend.save_local(package_name, intermediary_object, owner=False, version=version)
            else:
                self.backend.save_local(package_slug, intermediary_object, version=version)

        except BlendedException as exc:
            raise BlendedException(exc)

    def save_hub(self, account_name, package_name, blended_package, **kwargs):
        """
        convert intermediary package object into jptf and send it to Hub.
        """
        force = kwargs.get('force', False)
        local_last_hash = kwargs.get('local_last_hash', False)
        partial_jptf = kwargs.get('partial_jptf', None)

        if partial_jptf:
            package = partial_jptf
        else:
            package = self.as_jptf(blended_package)
        body = {'name': package_name, 'documents': package, 'hash_as_token': local_last_hash, 'force': force}
        try:
            response = self.network.update_draft(account_name, package_name, body)
        except BlendedException as exc:
            raise BlendedException(exc)

        tokens = response.to_dict().get('tokens', None)
        media_response, error_list = self.upload_media(account_name, tokens, package_name)
        if media_response:
            package_hash = media_response.to_dict()['package_hash']
            self.backend.set_hash(blended_package, package_hash)
        else:
            package_hash = response.to_dict()['package_hash']
            self.backend.set_hash(blended_package, package_hash)
        return response, error_list

    def upload_media(self, account_name, tokens, package_name):
        """
        """
        response = None
        error_list = []
        for token in tokens.items():
            media_path = os.path.join(package_name, token[0])
            image = self.backend.get_media(media_path)
            hash_value = self.compute_hash(image)
            try:
                response = self.network.upload_media(account_name, str(package_name),
                                                     hash_value, name=token[0],
                                                     image=image.name, token=token[1])
            except BlendedException:
                error_list.append(image.name)   # print("\nsome error in uploading image %s" % (image.name))
                continue
            image.close()
        return response, error_list

    def validate_local(self, project_object):
        """
        """
        # todo in near future
        backend = BackendLoader.get_backend("filebase")
        project = self.as_jptf(project_object)
        backend.validate(project)

    def validate_hub(self, project_object):
        """
        """
        project = self.as_jptf(project_object)
        # client.validate(project)

    def save_js(self, name, content):
        """
        save the javascript file with name and content of the file and return the url of save location
        """
        url = self.backend.save_js(name, content)
        return url

    def save_css(self, name, content):
        """
        save the css file with name and content of the file and return the url of save location
        """
        url = self.backend.save_css(name, content)
        return url

    def get_image(self, image_name):
        """
        image_name is searched in the theme/media directory.
        """
        backend = BackendLoader.get_backend("filebase")
        url = backend.get_image(image_name)
        return url

    def load_image(self, image_url):
        """
        load the image as PIL Object form from the image_url full path of the image location
        and returns the pil object used by transform
        """
        backend = BackendLoader.get_backend()
        image = backend.load_image(image_url)
        return image

    def save_image(self, image_name, image_content):
        """
        save the image_content(pil object) using the backend in a particular save directory and returns the path
        """
        backend = BackendLoader.get_backend()
        url = backend.save_image(image_name, image_content)
        return url

    def compute_hash(self, content):
        """
        """
        hasher = hashlib.sha1()
        cursor = content.tell()
        content.seek(0)
        try:
            while True:
                data = content.read(DEFAULT_CHUNK_SIZE)
                if not data:
                    break
                hasher.update(data)
            return hasher.hexdigest()
        finally:
            content.seek(cursor)

    def as_jptf(self, intermediary):
        """
        """
        jptf = self.intermediary_to_jptf(intermediary)
        obj = [{"/": {"type": "directory", "content": jptf}}]
        return obj

    def intermediary_to_jptf(self, project_object):
        """
        """
        package = []
        try:
            if project_object.__class__.__name__ == 'Directory':
                project_object = project_object.content
            for index, item in enumerate(project_object):
                key = item.name
                value = item.content
                try:
                    if item.empty_dir:
                        empty_directory = True
                except:
                    pass
                keys = key.rsplit('.', 1)
                if(len(keys) > 1):
                    with_extension = True
                    extension = ('.%s' % (keys[1]))
                else:
                    with_extension = False
                if(type(value) is list):
                    if not value and item.rem_loc_dir:
                        # empty_direcoty removed from local
                        package.append({key: {"type": "directory"}})
                    elif item.rem_from_hub_dir:
                        package.append({key: {"type": "directory"}})
                    elif item.add_emp_dir_on_hub and (not item.content):
                        package.append({key: {"content": [], "type": "directory", "hash": item.hash}})
                    elif not value:
                        # empty_direcoty
                        package.append({key: {"type": "directory", "content": value, "hash": item.hash}})
                    else:
                        value = self.intermediary_to_jptf(value)
                        package.append({key: {"type": "directory", "content": value, "hash": item.hash}})
                elif(with_extension and extension.lower() in ALLOWED_IMAGE_TYPES):
                    if not item.hash:
                        package.append({key: {"type": "media"}})
                    else:
                        package.append({key: {"type": "media", "hash": item.hash}})
                elif item.__class__.__name__ == 'JSONFile':
                    if value is None:
                        package.append({key: {"type": "file"}})
                    else:
                        value = base64.b64encode(zlib.compress(value.encode('utf-8'))).decode('utf-8')
                        package.append({key: {"type": "file", "content": value, "hash": item.hash}})
                elif item.__class__.__name__ == 'TextFile':
                    # (not value) and (value is not '')
                    if value is None:
                        package.append({key: {"type": "file"}})
                    else:
                        if(not type(value) is bytes):
                            value = value.encode('utf-8')
                        value = base64.b64encode(zlib.compress(value)).decode('utf-8')
                        package.append({key: {"type": "file", "content": value, "hash": item.hash}})
            return package
        except AssertionError as exc:
            return None

    def _remove_root_from_jptf(self, project_object):
        """
        :param project_object:
        :return:
        """
        jptf = project_object[0]['/']['content']
        package_hash = project_object[0]['/']['hash']
        canonical = project_object[0]['/']['canonical']
        return jptf, package_hash, canonical

    def de_jptf(self, project_object, as_hashes=False, package_slug=''):
        """
        """
        location = package_slug
        data = []
        for i in project_object:
            dict_copy = {}
            project_object_iter = i
            keys = list(project_object_iter.keys())
            for j_key in keys:
                key = j_key
                value = project_object_iter[key]
                location = os.path.join(location, key)
                if value['type'] == 'directory':
                    content = self.de_jptf(value['content'], as_hashes=as_hashes, package_slug=location)
                    if not content:
                        # Empty Dir so location must return [] not None!
                        data.append(self.backend.get_class("Directory")(location, content=content,
                                                                        name=key, hash=value['hash'],
                                                                        empty_dir=True))
                    else:
                        data.append(self.backend.get_class("Directory")(location, content=content,
                                                                        name=key, hash=value['hash']))
                    location = package_slug
                elif key[-5:] == '.json':
                    content = None
                    if not as_hashes:
                        content = zlib.decompress(base64.b64decode(value['content'])).decode('utf-8')
                    data.append(self.backend.get_class("JSONFile")(location, content=content,
                                                                   name=key, hash=value['hash'],
                                                                   as_hashes=as_hashes))
                elif value['type'] == 'media':
                    content = None
                    if not as_hashes:
                        content = value['href']
                    data.append(self.backend.get_class("BinaryFile")(location, content=content,
                                                                     name=key, hash=value['hash'],
                                                                     as_hashes=as_hashes))
                elif (value['type'] == 'file') and (key[-5:] != '.json'):
                    content = None
                    if not as_hashes:
                        content = zlib.decompress(base64.b64decode(value['content'])).decode('utf-8')
                    data.append(self.backend.get_class("TextFile")(location, content=content,
                                                                   name=key, hash=value['hash'],
                                                                   as_hashes=as_hashes))
            location = package_slug
        return data

    def intermediary_to_context(self, package, obj_to_return=None):
        """
        :param obj_to_return:
        :return:
        """
        image_class = self.backend.get_class('BinaryFile')
        package = package.content
        if not obj_to_return:
            obj_to_return = {}
        for item in package:
            value = item
            key = item.name

            if isinstance(value.content, list):
                obj_to_return[key] = {}
                obj_to_return.update({key: self.intermediary_to_context(value, obj_to_return[key])})
            elif isinstance(value, image_class):
                path = value.location
                image = Image.open(path)
                width = image.width
                height = image.height
                img_type = image.format
                img_hash = value.hash
                name = image.filename.rsplit("/")[-1]
                # buffer = BytesIO()
                # image.save(buffer, format=img_type)
                # img_str = base64.b64encode(buffer.getvalue())
                image.close()
                image_dict_object = {
                          "height ": height,
                          "width": width,
                          "fileName": name,
                          "path": path,
                          "type": img_type,
                          "hash": img_hash
                          }
                obj_to_return.update({key: image_dict_object})
            else:
                if key.endswith('.json'):
                    value = json.loads(value.content)
                else:
                    value = value.content
                obj_to_return.update({key: value})
        return obj_to_return
     
    def as_context(self, project, trim=True, dependency=False):
        """
        as_context function is used to turn a project object in intermediary format into context format.
        It also resolves all the json pointers including those pointing to dependencies before it returns it
        """
        dependency_dict = {}
        package = self.intermediary_to_context(project)
        project_json = package.get('_package.json', {})
        if project_json:
            dependency_list = project_json.get('dependencies', {})
            if(dependency_list):
                dependency_dict = self.load_dependency(dependency_list, dependency=dependency)
        # project.update(dependency_dict)
        try:
            package.pop('_package.json')
        except KeyError:
            pass
            
        package = self.order_project_dict(package)
        self.resolve(None, package, dependency_dict, None, None)
        if trim:
            self.trim_context(package)
        self.remove_index(package)
        return package

    def order_project_dict(self, project_object):
        """
        make the dict in ordered dict
        """
        return OrderedDict(sorted(list(project_object.items()), reverse=True))

    def remove_index(self, project_object):
        """
        remove the _index.json and _index the content to directly project object
        #not right now used was use in host doc vol 1
        """
        # project_object.update(project_object.pop('_index.json', {}))
        # project_object.update(project_object.pop('_index', {}))
        from copy import deepcopy
        unchanged_project_object = deepcopy(project_object)
        for key, value in unchanged_project_object.items():
            if (key == '_index') or (key == '_index.json'):
                project_object.update(project_object.pop(key, {}))
            elif isinstance(project_object.get(key), dict):
                self.remove_index(project_object.get(key))
        return self.order_project_dict(project_object)

    def trim_context(self, current_node):
        """
        trim context is make the _index json contents to outer loop and remove the key starting with _
        also it remove the file extension from the file name (key in dict)
        """
        from copy import copy
        current_node_iter = copy(current_node)
        if isinstance(current_node_iter, dict) and current_node_iter:
            for key, value in current_node_iter.items():
                if key == '_index':
                    for index_key, index_value in value.items():
                        current_node[index_key] = index_value
                    if key in current_node.keys():
                        current_node.update(current_node.pop(key, {}))
                        # current_node.popitem(key)
                else:
                    if key.startswith("_"):
                        if key in current_node_iter:
                            del current_node[key]
                z = key.rfind('.')
                if z >= 0:
                    new_key = key[:z]
                    current_node[new_key] = value
                    if key in current_node:
                        del current_node[key]
                self.trim_context(value)

    def dict_extension_remove(self, json_file):
        """
        do the same work as trim_context used in host doc vol-1 not now in use in host doc vol -2
        """
        new = {}
        for k, v in json_file.items():
            if k:
                z = k.rfind(".")
                if z >= 0:
                    k = k[:z]
            if isinstance(v, dict):
                var = {}
                var.update(self.dict_extension_remove(v))
                new[k] = var
            else:
                new[k] = v
        return new

    def load_dependency(self, dependency_list, dependency=False):
        """
        load the dependency based on the alias name of the theme and the uuid
        """
        dependency_dict = {}
        if not dependency:
            self.src_or_lib = self.backend.directory_path

        for dependency in dependency_list:
            dep_uuid = dependency.get('uuid')
            theme_slug = dependency.get('name')
            account = dependency.get('account')
            dep_alias = dependency.get('alias')
            version = dependency.get('version')
            package_slug = theme_slug.rsplit("/")[1]
            if not version:
                version = 'draft'
            if version == "canonical":
                info = self.network.get_canonical(account, package_slug)
                self.backend.set_canonical(account, package_slug, info)
            if dep_alias in dependency_dict:
                raise Exception("Alias: %s is not unique .please give unique alias " % dep_alias)
            self.set_backend_root
            dependency_dict[dep_alias] = dict(self.get_package(theme_slug, 'context', version, trim=False, dependency=True))
            self.set_backend_root

        if not dependency:
            self.backend.directory_path = self.src_or_lib

        return dependency_dict

    def resolve(self, current_node, project_object, dependency_dict, current_json_file, ref_path):
        """
        The resolve function uses a few helper functions (get_value_at_path, ref_get, resolve_pointer) in order to
        resolve all Json Pointers used in the json files of the project_object
        pattern is {"$ref":"#/meta/config.json"}
        """
        is_dict = lambda var: isinstance(var, (dict))
        is_list = lambda var: isinstance(var, (list))
       
        if (not current_node):
            current_node = project_object

        if not ref_path:
            ref_path = []
        
        if is_list(current_node):
            for item in current_node:
                if item:
                    self.resolve(item, project_object, dependency_dict,
                                current_json_file, ref_path)
        elif is_dict(current_node):
            rand_list = current_node.items()
            for key, value in rand_list:
                ref_path.append(key)
                if key[-5:] == '.json':
                    current_json_file = current_node[key]    
                current_value = current_node[key]
                if is_dict(current_value):
                    if '$ref' in value:
                        set_val = set()
                        ref_path_copy = copy(ref_path)
                        ref_location_ptr = current_node
                        current_node[key] = self.resolve_pointer(current_value,
                                                                project_object, dependency_dict,
                                                                set_val, current_json_file, ref_path_copy,
                                                                ref_location_ptr, key, None)
                        
                    else:
                        if not value:
                            continue
                        self.resolve(value, project_object, dependency_dict,
                                    current_json_file, ref_path)
                elif value and is_list(value):
                    self.resolve(value, project_object, dependency_dict,
                                current_json_file, ref_path)
                ref_path.pop()

    def resolve_pointer(self, json_ref, project_object, dependency_dict,
                        visited_set, current_json_file, ref_path, ref_location, ref_loc_key, curr_alias):
        """
        This function receives the dict containing the ref, checks if the ref has already been encountered or not by use of the visited_set.
        It then simply forwards the ref address for further processing
        The set is used to determine if a cycle is being entered.
        if we get a ref we store it in a set to recognize a case of json pointer cycle
        """
        is_array = lambda var: isinstance(var, (dict))
        if (is_array(json_ref) and '$ref' in json_ref):
            pointer = json_ref['$ref']
            if pointer in visited_set:
                raise Exception('A Json Pointer cycle has been detected')
            else:
                visited_set.add(pointer)
                json_ref = self.ref_get(pointer, project_object, current_json_file, dependency_dict, visited_set,
                                        ref_path, ref_location, ref_loc_key, curr_alias)
                if (not json_ref):
                    raise Exception('An empty/null value has been returned')

        return json_ref

    def multiple_replace(self, dic, text):
        """
        Replaces multiple instances of characters such as # or @ in the ref path
        """
        pattern = "|".join(map(re.escape, dic.keys()))
        return re.sub(pattern, lambda m: dic[m.group()], text)

    def ref_get(self, ref_value, project_object, json_file, dependency_dict,
                visited_set, ref_path, ref_location, ref_loc_key, curr_alias):
        """
        ref_get extracts the ref path string and creates resolve_path that has the path from project_object to the location where the ref points
        path is extracted based on what kind of ref it is, like #/ (same file) ref or @ (dependency) ref
        It forwards it to get_value_at_path function
        """

        dicti_replace = {'#/': ''}
        dicti_replace1 = {'#': ''}
        dicti_replace2 = {'#/': '/'}

        if ref_value.find('@') == 0:
            ref_point = ref_value.find('/')
            if ref_point == -1:
                ref_point = len(ref_value)
            path = ref_value
            alias_name = ref_value[1:ref_point]
            path = ref_value.split('@', 1)[1]
            path = self.multiple_replace(dicti_replace2, path)
            if (path == ''):
                return dependency_dict
            resolve_path = path.split('/')
            ref_value = self.get_value_at_path(dependency_dict, json_file, project_object, resolve_path, visited_set,
                                               ref_location, ref_loc_key, '@')
            return ref_value
        elif (ref_value.find("#/") == 0):
            while not (ref_path[-1][-5:] == '.json'):
                ref_path.pop()
            path = self.multiple_replace(dicti_replace, ref_value)
            if (path == ''):
                return json_file
            resolve_path = path.split('/')
            resolve_path = ref_path + resolve_path
            if (curr_alias and curr_alias == '@'):
                ref_alias = '@'
            else:
                ref_alias = '#'
            ref_value = self.get_value_at_path(dependency_dict, json_file, project_object, resolve_path, visited_set,
                                               ref_location, ref_loc_key, ref_alias)
            return ref_value
        else:
            if ref_value.startswith('/'):
                ref_value = ref_value.split('/', 1)[1]
            path = self.multiple_replace(dicti_replace1, ref_value)
            if (path == ''):
                return project_object
            resolve_path = path.split('/')
            ref_value = self.get_value_at_path(dependency_dict, json_file, project_object, resolve_path, visited_set,
                                               ref_location, ref_loc_key, '/')
        return ref_value

    def get_value_at_path(self, dependency_dict, json_file, project_object, resolve_path,
                          visited_set, ref_location, ref_loc_key, ref_identifier):
        """
        Utilizes resolve_path to traverse to the location where the ref points to
        temp_value will contain the value requested by the ref_get
        If the final value is again a dict and contains a $ref, it is sent back to resolve_pointer to resolve it
        If it is a dict but has nor ref directly as a key, it is sent to clear_dep to traverse through the dict DF and resolve all the refs in it
        """
        is_array = lambda var: isinstance(var, (dict))

        unchanged_project_object = copy(project_object)
        if (ref_identifier == '@'):
            temp_value = dependency_dict
        else:
            temp_value = project_object
        prev_ptr = None
        curr_path = []
        current_json_file = json_file
        for value in resolve_path:
            try:
                if '$ref' in temp_value:
                    if (temp_value['$ref'].find("#/") == 0):
                        new_resolve_path = copy(resolve_path)
                        while not (new_resolve_path[-1][-5:] == '.json'):
                            new_resolve_path.pop()
                        temp_value = self.resolve_pointer(temp_value, project_object, dependency_dict, visited_set,
                                                          current_json_file,
                                                          new_resolve_path, prev_ptr, curr_path[-1], ref_identifier)
                    else:
                        temp_value = self.resolve_pointer(temp_value, project_object, dependency_dict, visited_set,
                                                          current_json_file,
                                                          resolve_path, prev_ptr, curr_path[-1], None)
                    prev_ptr[curr_path[-1]] = temp_value
                if value[-5:] == '.json':
                    current_json_file = temp_value[value]
                prev_ptr = temp_value
                curr_path.append(value)
                temp_value = temp_value[value]
            except KeyError:
                return '%s not found' % (value,)

        ref_location[ref_loc_key] = temp_value

        if is_array(temp_value):
            if '$ref' in temp_value:
                if (temp_value['$ref'].find("#/") == 0):
                    new_resolve_path = copy(resolve_path)
                    while not (new_resolve_path[-1][-5:] == '.json'):
                        new_resolve_path.pop()
                    temp_value = self.resolve_pointer(temp_value, project_object, dependency_dict, visited_set,
                                                      current_json_file, new_resolve_path, prev_ptr, curr_path[-1],
                                                      ref_identifier)
                else:
                    temp_value = self.resolve_pointer(temp_value, project_object, dependency_dict, visited_set,
                                                      current_json_file, resolve_path, prev_ptr, curr_path[-1], None)
            else:
                temp_value = self.clear_dep(None, project_object, dependency_dict, current_json_file, resolve_path,
                                            None, ref_identifier, True)

        return temp_value

    def clear_dep(self, current_node, project_object, dependency_dict, current_json_file,
                  resolve_path, ref_path, curr_alias, path_flag=False):

        '''
        Recursive util that clears all the dependencies found in the dict/value requested by the $ref currently being processed
        '''
        is_array = lambda var: isinstance(var, (dict))
        if (not current_node):
            if (curr_alias and curr_alias == '@'):
                current_node = dependency_dict
            else:
                current_node = project_object

        ref_point_object = None

        if not ref_path:
            ref_path = []

        if path_flag:
            for value in resolve_path:
                ref_path.append(value)
                current_node = current_node[value]
            ref_point_object = current_node

        for key, value in current_node.items():
            ref_path.append(key)
            if key[-5:] == '.json':
                current_json_file = current_node[key]

            current_value = current_node[key]

            if is_array(current_value):
                if '$ref' in value:
                    set_val = set()
                    ref_path_copy = copy(ref_path)
                    ref_location = current_node
                    current_node[key] = self.resolve_pointer(current_value,
                                                             project_object, dependency_dict,
                                                             set_val, current_json_file, ref_path_copy, ref_location,
                                                             key, None)
                else:
                    if not value:
                        continue
                    self.clear_dep(value, project_object, dependency_dict,
                                   current_json_file, None, ref_path, None)
            ref_path.pop()

        return ref_point_object

    def get_theme_data(theme_object, template, block):
        """
        get theme data is to be moved to blendedhostfunction class
        # todo
        """
        grid = theme_object['meta']['grid']['all']
        if block in theme_object['meta']['grid']['blocks']:
            grid.update(theme_object['meta']['grid']['blocks'][block])
        if template in theme_object['meta']['grid']['templates']:
            grid.update(theme_object['meta']['grid']['templates'][template]['all'])
            if block in theme_object['meta']['grid']['templates'][template]['blocks']:
                grid.update(theme_object['meta']['grid']['templates'][template]['blocks'][block])
        theme_object['meta']['grid'].update(grid)
        return theme_object

    def get_directory(self, dep_uuid):
        """
        """
        uuid_map = self.get_uuid_map()
        if bool(uuid_map.get(dep_uuid)):
            directory = uuid_map.get(dep_uuid)
        else:
            raise Exception("Directory dependency uuid not found" + dep_uuid_)
        return directory

    def get_uuid_map(self):
        global BLENDED_DIR
        global ACTIVE_ORGANIZATION
        global UUID_MAP
        if UUID_MAP:
            return UUID_MAP
        layouts = BLENDED_DIR.strip('\'') + '/blended/' + ACTIVE_ORGANIZATION.strip('\'') + '/layouts'
        themes = BLENDED_DIR.strip('\'') + '/blended/' + ACTIVE_ORGANIZATION.strip('\'') + '/themes'
        theme_groups = BLENDED_DIR.strip('\'') + '/blended/' + ACTIVE_ORGANIZATION.strip('\'') + '/theme_groups'
        UUID_MAP.update(self.get_uuids(layouts))
        UUID_MAP.update(self.get_uuids(themes))
        UUID_MAP.update(self.get_uuids(theme_groups))
        return UUID_MAP

    def get_uuids(self, directory_path):
        """
        """
        uuid_map = {}
        project_json = {}
        project_json_file = '_package.json'
        projects = os.listdir(directory_path)
        try:
            projects = projects.remove('.')
            projects = projects.remove('..')
        except ValueError:
            pass
        for project in projects:
            if os.path.isfile(os.path.join(directory_path, project, project_json_file)):
                with open(os.path.join(directory_path, project, project_json_file), 'r') as content_file:
                    project_json = json.load(content_file)

                project_json_uuid = project_json.get('uuid', None)
                if(project_json_uuid):
                    uuid = project_json_uuid
                if(uuid):
                    uuid_map[uuid] = os.path.join(directory_path, project)
        return uuid_map

    def validate_package_json(self, package_json):
        
        reuired_fields = ['title', 'name', 'type']
        missing_fields = []

        for i in reuired_fields:
            if not (i in package_json):
                missing_fields.append("'" + i + "'")
                
        if missing_fields:
            if len(missing_fields) == 1:
                message = missing_fields[0] + ' field is missing in package.json'
            else:
                message = ', '.join(missing_fields) + ' fields are missing in package.json'

            return {'error': {'message': message}}

        return {}

    def package_validate(self, account_slug, slug, label="draft"):
        """
        """
        title = ''
        try:
            title = self.get_title(account_slug, slug)
        except Exception:
            pass
        
        inter = self.get_package(slug, version="draft", download=False)
        package_json = {}

        for item in inter.content:
            if item.name == '_package.json':
                package_json = item.content
        
        if not package_json:
            msg = ('Error: Your package "%s" (%s) does not contain a "_package.json" file. '
                   'This is required for successful validation. Please check and try again.' % (title, slug))
            return {'error': {'message': msg}}

        output = self.validate_package_json(package_json)

        if 'error' in output:
            return {'error': output['error']}
        
        theme = self.as_context(inter) # getting as context

        # setting validation object in theme, if validation folder is not present in theme
         
        if not ('validation' in theme):
            msg = ('Error: Your package "%s" (%s) does not contain a "validation" folder.'
                   ' This is required for successful validation. Please check and try again.' % (title, slug))
            return {'error': {'message': msg}}
        
        if not (('src' in theme['validation']) or ('lib' in theme['validation'])):
            msg = ('Error: Your package "%s" (%s) does not contain a "lib" and "src" folder inside the "validation" folder.'
                   ' This is required for successful validation. Please check and try again.' % (title, slug))
            return {'error': {'message': msg}}

        if not ('src' in theme['validation']):
            msg = ('Error: Your package "%s" (%s) does not contain an "src" folder inside the "validation" folder.'
                   ' This is required for successful validation. Please check and try again.' % (title, slug))
            return {'error': {'message': msg}}

        if not ('lib' in theme['validation']):
            msg = ('Error: Your package "%s" (%s) does not contain an "lib" folder inside the "validation" folder.'
                   ' This is required for successful validation. Please check and try again.' % (title, slug))
            return {'error': {'message': msg}}

        
        # converting theme object to json
        themeInString = json.dumps(theme)

        # require function code
        requireFunctionCode = '''
        const theme = %s;
        function require(libName) {
            var code = `
            (function a(){
                var module = { exports: {} };
                var exports = module.exports;
                var global = {};
                
                ` + theme['validation']['lib'][libName] + `;

                return module.exports;})()`;
            return eval(code);
        };
        '''% themeInString

        os_name = sys.platform.lower()

        if os_name.startswith('linux') or os_name.startswith('darwin'):
            from py_mini_racer import py_mini_racer
            ctx = py_mini_racer.MiniRacer()
            ctx.eval(requireFunctionCode)
        else:
            import execjs
            ctx = execjs.get() # getting best runtime
            if not ctx.name.lower().startswith('node'):
                return {'error':{'message': 'Error: Please install "Node.js" first to validate your package.'}}
            ctx = ctx.compile(requireFunctionCode)

        results = {}
        # running all validator code one by one
        for i in theme['validation']['src'] :
            try:
                results[i] = ctx.eval('(function(theme){' + theme['validation']['src'][i] + 'return validate(theme)})(theme)')
            except Exception as exc:
                return {'error':{'message': 'Error during running validator ' + i}}
            
        return {'results': results}
     
    def get_title(self, account_slug, slug):
        """
        """
        if slug:
            identifiers = slug.rsplit("/")
            if len(identifiers) > 1:
                account_slug = identifiers[0]
                slug = identifiers[1]
            else:
                slug = identifiers[0]
        title = ''
        try:
            title = self.backend.get_title(account_slug, slug)
        except BlendedException as exc:
            try:
                package_json = self.network.get_detail_document(account_slug, slug, '_package.json')
                package_json, package_hash, canonical_type = self._remove_root_from_jptf(package_json)
                package_json = self.de_jptf(package_json)
                title = json.loads(package_json[0].content)['title']
            except Exception:
                raise BlendedException(exc.args[0])
        return title


    def package_revoke(self, account_slug, package_name, account_name, **kwargs):
        """
        """
        body = {}
        email = kwargs.get('email')
        if account_name:
            body.update({'account_slug': account_name})
        elif email:
            body.update({'email': email})
        
        if kwargs.get('share'):
            body.update({'type': 'share'})
        elif kwargs.get('transfer'):
            body.update({'type': 'transfer'})

        try:
            response = self.network.revoke_acquired_package(account_slug, package_name, body)
        except BlendedException as exc:
            raise exc 
        return response

    def package_accept(self, account_slug, package_name, account_name, new_name=None):
        """
        """
        body = {"type": "transfer"}
        if new_name:
            body.update({'new_package_slug': new_name}) 
        try:
            response = self.network.accept_acquisition(account_name, package_name, body)
        except BlendedException as exc:
            raise exc 
        return response
        
    def check_package(self, account_slug, slug):
        if slug:
            identifiers = slug.rsplit("/")
            if len(identifiers) > 1:
                account_slug = identifiers[0]
                slug = identifiers[1]
            else:
                slug = identifiers[0]
        try:
            self.network.download_draft(account_slug, slug, as_hashes="1")
        except BlendedException:
            raise BlendedException("\nError: This package cannot be found in your library. "
                                   "You may need to push before performing this operation. Please check and try again.")

    def package_reject(self, account_slug, package_name, account_name, **kwargs):
        """
        """
        body = {}
        if kwargs.get('share'):
            body.update({'action': 'share'})
        elif kwargs.get('transfer'):
            body.update({'action': 'transfer'})

        try:
            response = self.network.reject_acquisition_invite(account_slug, account_name, package_name, body)
        except BlendedException as exc:
            raise exc 
        return response
