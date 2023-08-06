from __future__ import absolute_import,  unicode_literals
import os
import sys
import zlib
import base64
import hashlib
import json
import configparser
from PIL import Image
import shutil
from shutil import copyfile
import stat
try:
    from urllib import urlretrieve, urlopen
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlretrieve, urlopen

from blendedUx.blended_flask.blended_hostlib.exceptions import BlendedException

from .settings import SRC, LIB, CANONICAL_TXT, HASH_TXT, PROJECT_JSON, \
                      INDEX_JSON, USER_RC, CACHE_DICT, DEFAULT_ALIAS as alias, \
                      BLENDED_ACCOUNT, BLENDED_BASIC
from .settings import ALLOWED_IMAGE_TYPES, PACKAGE_LIST_RC as package_list_rc_file
from .intermediary import IntermediaryNode, Directory, \
    TextFile, BinaryFile, JSONFile

user_rc_file = USER_RC


def create_project_json(package_path, data=None):
    """
    """
    if not data:
        data = {}
    with open(package_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def update_project_json(package_path, package_details):
    """
    """
    json_file = open(package_path)
    json_data = json_file.read()
    json_file.close()
    try:
        data = json.loads(json_data)
    except ValueError:
        raise BlendedException("invalid data in _package.json")
    except Exception:
        raise BlendedException(exc.args[0])
    package_title_and_type_check(data, package_details)
    load_dependency(data, package_details)
    data.update(package_details)
    create_project_json(package_path, data)


def package_title_and_type_check(data, package_details):
    """
    data reads from backend.
    package_details come from cli commands.
    """
    try:
        pack_type = package_details['type']
    except:
        try:
            if not data['type']:
                raise BlendedException('You need to provide "Type" of package.')
        except:
            raise BlendedException('You need to provide "Type" of package.')

    try:
        title = package_details['title']
    except:
        try:
            if not data['title']:
                raise BlendedException('You need to provide "title" of package.')
        except:
            raise BlendedException('You need to provide "title" of package.')


def load_dependency(data, package_details):
    """
    """
    try:
        dependency = data['dependencies']
        if dependency:
            pack_list = dependency_check(dependency)
            item = {data['name']: data['version']}
            if item in pack_list:
                raise BlendedException("There should not be a circular dependency in package \"%s\"." % (item))
    except KeyError:
        pass
    except BlendedException as exc:
        raise BlendedException(exc.args[0])
    except Exception:
        raise BlendedException("invalid data in _package.json")


def dependency_check(dependency_list, package_list1=[]):
    """
    load the dependency based on the alias name of the theme and the uuid
    """
    alias_dict = []
    version_list = []
    package_list = []
    for dependency in dependency_list:
        theme_slug = dependency.get('name')
        dep_alias = dependency.get('alias')
        version = dependency.get('version')
        # dep_uuid = dependency.get('uuid')
        # account = dependency.get('account')
        dependencies = dependency.get('dependencies')
        if not theme_slug:
            raise BlendedException({'msg': 'Error: "name" is not defined with dependency package.', 'status_code':7777})
        if not dep_alias:
            raise BlendedException({'msg': 'Error: "alias" is not defined with dependency package "%s".' % theme_slug, 'status_code':7777})
        if not version:
            raise BlendedException({'msg': 'Error: "version" is not defined with dependency package "%s".' % theme_slug, 'status_code':7777})
        if not (version and dep_alias and theme_slug):
            raise BlendedException("Version, alias, and name are required for defining dependency.")
        package_slug = theme_slug.rsplit("/")[1]
        if dep_alias in alias_dict:
            raise BlendedException({'msg': 'Error: Duplicate entry found of "alias" with dependency package "%s".' % theme_slug, 'status_code':7777})
        if (version in version_list) and (package_slug in package_list):
            raise BlendedException({'msg': "You cannot make same version dependency multiple time: "
                                   "version \"%s\" of package \"%s\" " % (version, package_slug), 'status_code':7777})
        item = {theme_slug: version}
        if dependencies:
            if item in dependency_check(dependencies, package_list1=package_list1):
                raise BlendedException({'msg': "There should not be a circular dependency in package \"%s\"." % (item), 'status_code':7777})
        alias_dict.append(dep_alias)
        version_list.append(version)
        package_list.append(package_slug)
        package_list1.append(item)
    return package_list1


class FileSystemBackend(object):
    """
    backend class for filesystem
    """
    def __init__(self, directory_path=None, blended_dir=None,
                 current_account=None, blended_directory_path=None,
                 last_login=None):
        self.directory_path = directory_path
        self.src_or_lib = None
        self.last_login = last_login
        self.blended_dir = blended_dir
        self.current_account = current_account
        self.blended_directory_path = blended_directory_path

    def validate_package_json(self, json_obj):
        title = json_obj.get('title', {})
        name = json_obj.get('name', {})
        package_type = json_obj.get('type', {})
        reuired_fields = []
        if not title:
            reuired_fields.append('"title"')
        if not name:
            reuired_fields.append('"name"')
        if not package_type:
            reuired_fields.append('"type"')
        if reuired_fields:
            error_message = ', '.join(reuired_fields)
            raise BlendedException({'message':'%s field(s) are missing in package.json. "name", "title", '
                                    '"type" are required fields for package.' % (error_message),
                                    'status_code': 9003})
        return

    def dependency_version_check(self, dependency_list, version_list=[], action=None):
        """
        load the dependency based on the alias name of the theme and the uuid
        #['draft', 'viewlayout', 'layout', 'theme', 'canonical']
        """
        for dependency in dependency_list:
            version = dependency.get('version')
            dependencies = dependency.get('dependencies')
            if version.lower() in ['draft', 'canonical']:
                if action == 'snapshot' or action == 'transfer':
                    version_list.append(dependency.get('name'))
                else:
                    version_list.append({dependency.get('name'): version})
            if dependencies:
                self.dependency_version_check(dependencies, version_list=version_list, action=action)
        return version_list

    def update_src_copy_dst(self, response, source_package_name, package_slug, source_package, account_slug, version=None):
        """
        """
        for item in response:
            if version:
                src = item.location
                dst = item.location.replace(os.path.join('lib', source_package, version), os.path.join('src', package_slug))
            else:
                src = item.location
                dst = item.location.replace(os.path.join('src', source_package_name), os.path.join('src', package_slug))
                # dst = item.location.replace(source_package_name, package_slug)
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            except Exception as e:
                raise Exception(e)
        return package_slug

    def get_class(self, classname):
        """
        """
        classes = {"intermediary": IntermediaryNode,
                   "Directory": Directory,
                   "JSONFile": JSONFile,
                   "TextFile": TextFile,
                   "BinaryFile": BinaryFile}
        return classes[classname]

    def set_canonical(self, account, package_slug, canonical_detail=None, clone_flag=None, version=None):
        """
        """
        blended_dir = self.get_blended_directory_path()
        if not blended_dir.endswith(self.current_account):
            lib_dir = os.path.join(blended_dir, self.current_account, LIB, account, package_slug)
        elif clone_flag:
            lib_dir = account
        else:
            lib_dir = os.path.join(blended_dir, account, LIB, account, package_slug)
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)
        if canonical_detail or version:
            if version:
                label = version
            else:
                label = canonical_detail.to_dict()['label']
            canonical_file = open(lib_dir + os.sep + CANONICAL_TXT, "w")
            canonical_file.write("canonical = '%s'" % label)
            canonical_file.close()
            version_dir = os.path.join(lib_dir, label)
            if not os.path.exists(version_dir):
                return True
            return False

    def set_hash(self, dir_path, _hash=None):
        """
        """
        if dir_path.__class__.__name__ == 'Directory':
            current_account = self.get_current_account()
            src_dir = os.path.join(current_account, SRC)
            dir_path = os.path.join(self.directory_path, dir_path.name)
        if _hash:
            hash_file = open(dir_path + os.sep + HASH_TXT, "w")
            hash_file.write("hash = '%s'" % _hash)
            hash_file.close()

    def get_canonical(self, account, package_slug, **kwargs):
        """
        """
        current_account = kwargs.get('current_account', None)
        blended_dir = self.get_blended_directory_path()
        if current_account:
            lib_dir = os.path.join(blended_dir, current_account, LIB, account, package_slug, CANONICAL_TXT)
        else:
            lib_dir = os.path.join(blended_dir, account, LIB, account, package_slug, CANONICAL_TXT)

        if os.path.exists(lib_dir):
            canonical_file = open(lib_dir, "r")
            response = canonical_file.read().rsplit(" = ")[1]
            canonical_file.close()
            return response.strip("'")
        else:
            return None

    def create_account(self):
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

    def account_login(self):
        """
        method that will in filesystem for the sessionkey to
        login into the account.
        """
        pass

    def get_title(self,  account_name, slug):
        """
        """
        if not self.directory_path.endswith('src'):
            self.set_src
        current_dir = self.directory_path
        package_name = str(slug)
        package_directory = os.path.join(current_dir, package_name)
        lst = []
        try:
            lst = os.listdir(current_dir)
        except OSError:
            pass
        if package_name not in lst:
            raise BlendedException({'status_code': 5008, 'message': 'Package does not exist.'})
        package_path = os.path.join(current_dir, package_name, PROJECT_JSON)
        if not os.path.isfile(package_path):
            raise BlendedException({'status_code': 7000, 'message': 'Package does not have _package.json.'})
        json_file = open(package_path)
        json_data = json_file.read()
        json_file.close()
        try:
            data = json.loads(json_data)
        except ValueError:
            raise BlendedException({'status_code': 7000, 'message':'invalid data in "_package.json".'})
        except Exception:
            raise BlendedException(exc.args[0])
        try:
            title = data['title']
        except:
            raise BlendedException({'status_code': 7000, 'message': 'Package does not have title.'})
        return title

    def copy_validate_folder(self, account_name, package_name):
        """
        copy validator folder in created package.
        """
        # validate_folder = os.path.join(os.getcwd(), 'validation')
        current_account = self.get_current_account()
        label = self.get_canonical(BLENDED_ACCOUNT, BLENDED_BASIC, current_account=current_account)
        lib_path = os.path.dirname(self.directory_path)
        validate_folder = os.path.join(lib_path, LIB, BLENDED_ACCOUNT, BLENDED_BASIC, label, 'validation')
        package_path = os.path.join(self.directory_path, package_name, 'validation')
        if os.path.exists(validate_folder):
            try:
                shutil.copytree(validate_folder, package_path)
            except:
                pass

    def copy_validate_package(self, account_name, package_name, blended_package):
        """
        copy validator package in created package.
        """
        current_account = self.get_current_account()
        label = self.get_canonical(BLENDED_ACCOUNT, blended_package, current_account=current_account)
        lib_path = os.path.dirname(self.directory_path)
        validate_folder = os.path.join(lib_path, LIB, BLENDED_ACCOUNT, blended_package, label)
        package_path = os.path.join(self.directory_path, package_name)
        if os.path.exists(validate_folder):
            try:
                shutil.copytree(validate_folder, package_path)
            except:
                pass

    def create_package(self, account_name, package_name, package_type, description, package_title, primary_category, secondary_category=None):
        """
        """
        current_dir = self.directory_path
        package_name = str(package_name)
        package_directory = os.path.join(current_dir, package_name)
        # current_account = self.get_current_account()
        active_account = self.last_login
        if not active_account:
            active_account = account_name
        if not description:
            description = ""
        pack_details = self.read_package_json(package_name)
        name = '%s/%s' % (account_name, package_name)
        try:
            lst = os.listdir(current_dir)
        except OSError:
            os.makedirs(current_dir)
            lst = os.listdir(current_dir)
        if package_name not in lst:
            os.makedirs(package_directory)
        else:
            try:
                assert not os.path.isfile(package_directory)
            except AssertionError:
                raise BlendedException('%s can not be a file.' % (package_name,))

        package_details = {'name': name.lower(),
                           'slug': package_name.lower(),
                           'user': active_account.lower(),
                           'version': 'draft',
                           'account': account_name.lower(),
                           }
        if package_type:
            package_details.update({'type': package_type.lower()})
        if package_title:
            package_details.update({'title': package_title})
        if primary_category:
            package_details.update({'primary_category': primary_category})
        if secondary_category:
            package_details.update({'secondary_category': secondary_category})
        if pack_details and account_name == 'anonymous':
            try:
                if pack_details['name'] == name:
                    raise BlendedException("Package already present", 5011)
                else:
                    pass
            except KeyError:
                pass

        package_path = os.path.join(current_dir, package_name, PROJECT_JSON)
        if os.path.isfile(package_path):
            try:
                update_project_json(package_path, package_details)
            except BlendedException as exc:
                raise BlendedException(exc)
        else:
            create_project_json(package_path)
            try:
                package_details['description'] = description
                package_details['dependencies'] = []
                update_project_json(package_path, package_details)
            except BlendedException as exc:
                raise BlendedException(exc)

    def update_package_anonymous_to_login_user(self, package_name, current_dir, current_account):
        """
        """
        package_path = os.path.join(current_dir, package_name, '_package.json')
        package_details = self.read_package_json(package_name)
        name = '%s/%s' % (current_account, package_name)
        user = current_account.lower()
        account = current_account.lower()
        package_details.update({'name': name, 'user': user, 'account': account})
        if os.path.isfile(package_path):
            try:
                update_project_json(package_path, package_details)
            except BlendedException as exc:
                raise BlendedException(exc)
        return

    def read_package_json(self, package_name):
        """
        """
        current_dir = self.directory_path
        package_path = os.path.join(current_dir, package_name, PROJECT_JSON)
        if os.path.exists(package_path):
            json_file = open(package_path)
            json_data = json_file.read()
            json_file.close()
            try:
                data = json.loads(json_data)
            except ValueError:
                raise BlendedException("invalid data in _package.json")
            return data
        else:
            return {}

    def update_project_dot_json(self, package_path, package_details):
        """
        :param package_path:
        :param package_details:
        :return:
        """
        update_project_json(package_path, package_details)

    def create_blended_rc(self, pk, package_name, package_type):
        """
        """
        current_dir = self.directory_path
        blended_rc_path = os.path.join(current_dir, package_name, BLENDED_RC)
        config = configparser.ConfigParser()
        dot_blended_dir = blended_rc_path.rsplit(os.sep, 1)[0]
        if not os.path.isdir(dot_blended_dir):
            os.makedirs(dot_blended_dir)
        try:
            config.add_section('Package')
            config.set('Package', 'pk', str(pk))
            config.set('Package', 'name', str(package_name))
            config.set('Package', 'type', str(package_type))
        except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
            raise BlendedException(exc)

        with open(blended_rc_path, 'w') as blendedrc_file:
            config.write(blendedrc_file)

    def get_hash(self, package_name, **kwargs):
        """
        :param kwargs:
        :return:
        """
        current_dir = self.directory_path
        blended_rc_path = os.path.join(current_dir, package_name, HASH_TXT)
        if os.path.exists(blended_rc_path):
            hash_file = open(blended_rc_path, "r")
            response = hash_file.read().rsplit(" = ")[1].strip("'")
            hash_file.close()
            return response
        else:
            return ''

    def update_blendedrc(self, package_name, **kwargs):
        """
        """
        draft_id = kwargs.get('draft_id')
        version = kwargs.get('label')
        version_pk = kwargs.get('version_pk')
        description = kwargs.get('description')
        pk = kwargs.get('pk')
        package_type = kwargs.get('package_type')
        last_hash = kwargs.get('last_hash')
        slug = kwargs.get('slug')
        current_dir = self.directory_path
        blended_rc_path = os.path.join(current_dir, package_name, BLENDED_RC)
        config = configparser.ConfigParser()
        config.read(blended_rc_path)

        if slug:
            try:
                config.set('Package', 'slug', str(slug))
                config.set('Package', 'name', str(package_name))
            except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
                config.add_section('Package')
                config.set('Package', 'slug', str(slug))
                config.set('Package', 'name', str(package_name))

        if pk:
            try:
                config.set('Package', 'pk', str(pk))
                config.set('Package', 'name', str(package_name))
            except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
                config.add_section('Package')
                config.set('Package', 'pk', str(pk))
                config.set('Package', 'name', str(package_name))

        if package_type:
            try:
                config.set('Package', 'type', str(package_type))
                config.set('Package', 'name', str(package_name))
            except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
                config.add_section('Package')
                config.set('Package', 'type', str(package_type))
                config.set('Package', 'name', str(package_name))

        if description:
            try:
                config.set('Package', 'description', str(description))
                config.set('Package', 'name', str(package_name))
            except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
                config.add_section('Package')
                config.set('Package', 'description', str(description))
                config.set('Package', 'name', str(package_name))

        if last_hash:
            try:
                config.set('Package', 'last_hash', str(description))
                config.set('Package', 'name', str(package_name))
            except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
                config.add_section('Package')
                config.set('Package', 'last_hash', str(description))
                config.set('Package', 'name', str(package_name))

        if draft_id:
            try:
                config.set('Draft', 'draft_pk', str(draft_id))
            except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
                config.add_section('Draft')
                config.set('Draft', 'draft_pk', str(draft_id))

        if version:
            try:
                config.set('Version', str(version), str(version_pk))
            except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
                config.add_section('Version')
                config.set('Version', str(version), str(version_pk))

        with open(blended_rc_path, 'w') as blendedrc_file:
            config.write(blendedrc_file)

    def get_blended_directory_path(self):
        """
        :return:
        """
        return self.blended_directory_path

    def get_draft_id(self, package_name):
        """
        """
        current_dir = self.directory_path
        blended_rc_path = os.path.join(current_dir, package_name, BLENDED_RC)
        config = configparser.ConfigParser()
        try:
            config.read(blended_rc_path)
            draft_id = config.get('Draft', 'draft_pk')
        except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
            draft_id = None

        return draft_id

    def get_version_id(self, package_name, label):
        """
        """
        current_dir = self.directory_path
        blended_rc_path = os.path.join(current_dir, package_name, BLENDED_RC)
        config = configparser.ConfigParser()
        try:
            config.read(blended_rc_path)
            version_id = config.get('Version', label)
        except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError) as exc:
            raise BlendedException("There is some issue with configuration of package")
        return version_id

    def get_package_acquisition(self, package_name, license_name, new_name):
        """
        method look for the package in the filesystem
        """
        pass

    def package_push(self):
        """
        """
        pass

    def save_local(self, package_name, intermediary_object, **kwargs):
        """
        """
        files = kwargs.get('files')
        blended_dir = self.get_blended_directory_path()
        is_draft = kwargs.get('draft')
        is_owner = kwargs.get('owner', True)
        dependency = kwargs.get('dependency', False)
        version = kwargs.get('version', False)
        current_account = self.get_current_account()
        src_dir = os.path.join(blended_dir, current_account, SRC)
        lib_dir = os.path.join(blended_dir, current_account, LIB)
        identifiers = package_name.split("/")
        if len(identifiers) > 1:
            account = identifiers[0]
            package_slug = identifiers[1]
        else:
            try:
                account = self.get_current_account()
            except BlendedException as exc:
                raise BlendedException(exc)
            package_slug = identifiers[0]
        if files:
            package_name = os.path.join(self.directory_path, src_dir, package_slug)
        elif is_draft:
            package_name = os.path.join(self.directory_path, src_dir, package_slug)
        elif (not is_owner) or (dependency):
            package_name = os.path.join(self.directory_path, lib_dir, package_name, version)
        elif version:
            package_name = os.path.join(self.directory_path, lib_dir, package_name, version)
        elif self.directory_path.endswith('src'):
            package_name = os.path.join(self.directory_path, package_slug)
        else:
            # version label needs to be implemented here
            package_name = os.path.join(self.directory_path, SRC, package_slug)
        # try:
        if not files:
            try:
                shutil.rmtree(package_name)
            except:
                pass
        temp_path = os.path.join(package_name, '.temp')
        try:
            media_for_download = dict()
            self.intermediary_to_filesystem(temp_path, intermediary_object.content,
                                            media_for_download=media_for_download)
            try:
                self.download_media_concurrent_or_sequential(media_for_download=media_for_download)
            except Exception as e:
                print("Something went wrong while downloading the package media files.")
                sys.exit(1)
        except Exception as exc:
            if os.path.exists(temp_path):
                try:
                    shutil.rmtree(temp_path)
                except OSError as exc:
                    # os.system("taskkill /im explorer.exe")
                    try:
                        shutil.rmtree(temp_path)
                    except:
                        pass
            if not files:
                try:
                    shutil.rmtree(package_name)
                except OSError as exc:
                    try:
                        shutil.rmtree(package_name)
                    except:
                        pass
            raise BlendedException('Unable to download package due to Network failure. '
                                   'Please check your network connection and try again.')
        else:
            self.copy_temp_dir_to_original_package(temp_path, package_name)
            shutil.rmtree(temp_path)
        try:
            if files:
                intermediary_object = self.get_package(intermediary_object.name)
        except BlendedException as exc:
            raise BlendedException(exc)
        else:
            self.set_hash(package_name, intermediary_object.hash)
        return True
        # except BlendedException:
        #    raise BlendedException('Some file may not saved in the package')

    def copy_temp_dir_to_original_package(self, temp_path, package_name):
        """
        """
        for temp_dir in os.listdir(temp_path):
            temp_dirs = os.path.join(temp_path, temp_dir)
            package_copy_path = os.path.join(package_name, temp_dir)
            if not os.path.exists(package_copy_path):
                if os.path.isdir(temp_dirs):
                    shutil.copytree(temp_dirs, package_copy_path)
                else:
                    shutil.copy2(temp_dirs, package_copy_path)
            if os.path.isdir(temp_dirs):
                self.copy_temp_dir_to_original_package(temp_dirs, package_copy_path)
            else:
                shutil.copy2(temp_dirs, package_copy_path)

    def package_list(self, packages_dict):
        """
        """
        directory_path = self.directory_path
        # if not os.path.exists(directory_path):
        # os.makedirs(directory_path)
        path = os.path.join(directory_path, package_list_rc_file)
        config = configparser.ConfigParser()
        config.add_section('Packages')
        for k, v in packages_dict.items():
            config.set('Packages', str(k), str(v))
        with open(path, 'w') as config_file:
            config.write(config_file)

    def read_package_pk(self, package_name):
        """
        """
        config = configparser.ConfigParser()
        working_dir = self.directory_path
        path = os.path.join(working_dir, package_list_rc_file)
        try:
            config.read(path)
            package_pk = config.get('Packages', package_name)
        except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError):
            raise BlendedException()
        return int(package_pk)

    def get_current_account(self):
        """
        :return:
        """
        return self.current_account

    def create_extended_package(self, package_name, package, new_name, **kwargs):
        """
        :param package_name:
        :param description:
        :return:
        """
        description = kwargs.get('description', "")
        account_name = kwargs.get('account')
        label = kwargs.get('label')
        package_type = kwargs.get('package_type')
        package_title = kwargs.get('package_title')
        current_account = self.get_current_account()
        underscore_index_json = {}
        for item in package.content:
            key = item.name
            # if key == DOT_BLENDED:
            #     continue
            if (key == INDEX_JSON):
                try:
                    index_file_keys = list(item.content.keys())
                except AttributeError:
                    index_file_keys = list(json.loads(item.content).keys())

                for index_key in index_file_keys:
                    data = {"$ref": "@%s/%s" % (alias, index_key)}
                    underscore_index_json[index_key] = data
            elif (key != PROJECT_JSON):
                data = {"$ref": "@%s/%s" % (alias, key)}
                underscore_index_json[key] = data
            if (key == PROJECT_JSON):
                pack_json_content = json.loads(item.content)
                if not label:
                    label = pack_json_content['version']
        package_path = os.path.join(self.directory_path, new_name)

        if not os.path.exists(package_path):
            os.makedirs(package_path)

        underscore_index_dot_json_path = os.path.join(package_path, INDEX_JSON)

        with open(underscore_index_dot_json_path, 'w') as underscoreindexfile:
            json.dump(underscore_index_json, underscoreindexfile, indent=4)
        # commented code need not be in  dependency
        # dependencies_for_extend = pack_json_content.get('dependencies', [])
        underscore_project_json = {
                        'name': '%s/%s' % (current_account, new_name),
                        'description': description,
                        'version': 'draft',
                        'type': package_type,
                        'title': package_title,
                        'dependencies': [{
                                          'name': '%s/%s' % (account_name, package_name),
                                          'alias': 'parent',
                                          # 'description': pack_json_content['description'],
                                          'type': pack_json_content['type'],
                                          # 'dependencies': dependencies_for_extend,
                                          'account': account_name,
                                          'version': label
                         }]
        }
        underscore_project_dot_json_path = os.path.join(package_path, PROJECT_JSON)
        with open(underscore_project_dot_json_path, 'w') as underscoreprojectfile:
            json.dump(underscore_project_json, underscoreprojectfile, indent=4)

    def packages_in_src(self):
        """
        :return:
        """
        path = os.path.join(self.directory_path, SRC)
        if os.path.exists(path):
            return os.listdir(path)
        return []

    def packages_in_lib(self, account):
        """
        :return:
        """
        path = os.path.join(self.directory_path, LIB)
        if os.path.exists(path):
            accounts = os.listdir(path)
            if account in accounts:
                return os.listdir(os.path.join(path, account))
            return []
        return []

    @property
    def set_src(self):
        self.directory_path = os.path.join(self.directory_path, SRC)

    @property
    def src(self):
        return SRC

    @property
    def lib(self):
        return LIB

    def set_lib(self, account):
        self.directory_path = os.path.join(self.directory_path, LIB, account)

    def read_package_name(self, package_id):
        """
        """
        config = configparser.ConfigParser()
        working_dir = self.directory_path
        path = os.path.join(working_dir, package_list_rc_file)
        package_id = str(package_id)
        try:
            config.read(path)
            packages = dict(config._sections.get('Packages'))
            for key, value in packages.items():
                if value == package_id:
                    package_name = key
        except (configparser.NoSectionError, configparser.NoOptionError, OSError, IOError):
            raise BlendedException()
        return package_name

    def check_lib_or_src(self, dir_path, dependency=False, version=None, src_check=True, lib_check=True):
        """
        :param dir_path:
        :return:
        """
        identifiers = dir_path.split("/")
        if len(identifiers) > 1:
            account = identifiers[0]
            package_slug = identifiers[1]
        else:
            try:
                account = self.get_current_account()
            except BlendedException as exc:
                raise BlendedException(exc)
            package_slug = identifiers[0]
        if not self.directory_path.endswith(SRC):
            src_dir = os.path.join(self.directory_path, SRC)
        else:
            src_dir = self.directory_path
        lib_dir = os.path.join(self.directory_path, LIB)
        if (os.path.exists(src_dir)) and (package_slug in os.listdir(src_dir)) and src_check:
            self.directory_path = src_dir
        elif version and lib_check:
            version_path = os.path.join(lib_dir, account, package_slug, version)
            if (os.path.exists(lib_dir)) and (os.path.exists(version_path)):
                self.directory_path = lib_dir
            elif (dependency) and (os.path.exists(lib_dir)) and (os.path.exists(version_path)):
                self.directory_path = lib_dir
        elif (os.path.exists(lib_dir)) and (package_slug in self.packages_in_lib(account)) and lib_check:
            self.directory_path = lib_dir
        elif (dependency) and (os.path.exists(lib_dir)) and (package_slug in self.packages_in_lib(account)) and lib_check:
            self.directory_path = lib_dir
        else:
            raise OSError('First, try with a proper fully qualified name. If \"%s\" is still not found '
                          'in the filesystem, please download or install it first.' % (dir_path))

    def get_package(self, dir_path, theme_path=None, entry=True, dependency=False, version=None, action=None):
        """
        """
        intermediary_cache_name = None
        try:
            if entry:
                if version and version.lower() != 'draft':
                    self.check_lib_or_src(dir_path, dependency=dependency, version=version, src_check=False)
                else:
                    self.check_lib_or_src(dir_path, dependency=dependency, version=version, lib_check=False)

                if self.directory_path.endswith(SRC):
                    identifiers = dir_path.split("/")
                    if len(identifiers) > 1:
                        account = identifiers[0]
                        dir_path = identifiers[1]
                    else:
                        dir_path = identifiers[0]
                elif self.directory_path.endswith(LIB) and action!='pull':
                    identifiers = dir_path.split("/")
                    if not version:
                        current_account = self.get_current_account()
                        version = self.get_canonical(identifiers[0],  identifiers[1], current_account=current_account)

                    if version:
                        intermediary_cache_name = os.path.join(dir_path, version)
                        if CACHE_DICT.get(intermediary_cache_name, None):
                            return CACHE_DICT[intermediary_cache_name]
                        dir_path = os.path.join(dir_path, version)
                else:
                    self.directory_path = os.path.join(self.blended_directory_path, self.current_account)
                    raise OSError()

            dir_path = os.path.join(self.directory_path, dir_path)
            if(not theme_path):
                theme_path = dir_path
            intermediary_object = Directory(dir_path)
            path_validate_errors = intermediary_object.path_validate_errors
            if path_validate_errors and action=='push':
                raise BlendedException({'msg' : path_validate_errors, 'status_code': 5011})
            if intermediary_cache_name:
                CACHE_DICT[intermediary_cache_name] = intermediary_object
            return intermediary_object
        except BlendedException as exc:
            raise BlendedException(exc.args[0])
        except OSError as exc:
            raise OSError(exc)

    def intermediary_to_filesystem(self, package_name, intermediary_object, media_for_download=None):
        """
        """
        package_path = package_name
        if not os.path.isdir(package_path):
            os.makedirs(package_path)
        for data in intermediary_object:
            key = data.name
            value = data.content
            directory_path = os.path.join(package_path, key)
            keys = key.rsplit('.', 1)
            if(len(keys) > 1):
                with_extension = True
                extension = ('.%s' % (keys[1]))
            else:
                with_extension = False
            if isinstance(data, Directory):
                # directory_path = os.path.join(package_path, data.location)
                self.intermediary_to_filesystem(directory_path, data.content,
                                                media_for_download=media_for_download)
            directory_path = os.path.join(package_path, data.name)
            if isinstance(data, BinaryFile):
                if (with_extension and extension.lower() in ALLOWED_IMAGE_TYPES):
                    # urlretrieve(value, directory_path)
                    if isinstance(media_for_download, dict) and (directory_path not in media_for_download):
                        media_for_download[directory_path] = value
                    else:
                        image_response = urlopen(value, timeout=40)
                        image_obj = image_response.read()
                        with open(directory_path, 'wb') as imagefile:
                            imagefile.write(image_obj)
            if isinstance(data, JSONFile):
                data = json.loads(value)
                with open(directory_path, 'w') as filename:
                    json.dump(data, filename, indent=1, sort_keys=True)
            if isinstance(data, TextFile):
                with open(directory_path, 'w', encoding='utf-8') as filename:
                    try:
                        filename.write(value)
                    except UnicodeEncodeError:
                        filename.write(value.encode('utf-8'))
        return True

    def get_media(self, image_path):
        """
        """
        theme_dir = self.directory_path
        image_path = os.path.join(theme_dir, image_path)
        image = open(image_path, 'rb')
        return image

    def save_css(self, name, content):
        """
        :param name:
        :param content:
        :return:
        """
        path = self.make_directory(name)
        with open(path, 'w') as file_name:
            file_name.write(content)
        return path

    def check_package_dot_json_presense(self, package_object):
        """
        """
        try:
            package_data_list = package_object.content
            for item in package_data_list:
                if item.name == PROJECT_JSON:
                    package_dict = json.loads(item.content)
                    dependency_list = []
                    try:
                        dependency_list = package_dict['dependencies']
                    except Exception:
                        pass
                    if dependency_list:
                        load_dependency(package_dict, {})
                    return True
        except Exception as exc:
            raise BlendedException(exc.args[0])

        return False

    def make_directory(self, path):
        """
        :param path:
        :return: return file name by checking and creating directories mentioned in the path if not already exists.
        """
        split_path = path.rsplit(os.sep, 1)
        if len(split_path) > 1:
            file_dir = split_path[0]
            file_name = split_path[1] + '.css'
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
        path = os.path.join(file_dir, file_name)
        return path

    def download_media_concurrent_or_sequential(self, media_for_download=dict()):
        """
        Downloads the media files concurrently using multithreading if supported.
        media_for_download is a dictionary mapping.
        Ex. media_for_download[path] = URL hence, media_for_download.items() ---> [(path, url)...]
        If concurrent.futures is not supported, downloads media sequentially.
        """
        try:
            from concurrent.futures import ThreadPoolExecutor
        except:
            # concurrent.futures not supported. Lets download sequentially.
            for _tuple in media_for_download.items():
                self.download_and_save_media(_tuple)
        else:
            with ThreadPoolExecutor(64) as executor:
                executor.map(self.download_and_save_media, media_for_download.items())

    def download_and_save_media(self, url_path_tuple):
        """
        Downloads the image on specified path using the URL specified.
        """
        if not url_path_tuple:
            return
        path = url_path_tuple[0]
        url = url_path_tuple[1]
        response = urlopen(url, timeout=40)
        image_obj = response.read()
        with open(path, 'wb') as file:
            file.write(image_obj)
