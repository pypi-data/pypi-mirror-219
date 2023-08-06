import re
import os
import sys
import zlib
import base64
import hashlib
import json

from blendedUx.blended_flask.blended_hostlib.exceptions import BlendedException
from .settings import *
user_rc_file = USER_RC
DEFAULT_CHUNK_SIZE = 64 * 2 ** 10

alias = DEFAULT_ALIAS
package_list_rc_file = PACKAGE_LIST_RC

class IntermediaryNode(object):
    """
    """
    _hash = ''

    def __init__(self, location, content=None, name=None, hash=None,
                 as_hashes=False, removed=False, empty_dir=False,
                 rem_loc_dir=False, rem_from_hub_dir=False,
                 add_emp_dir_on_hub=False, path_validate_errors=None):
        """
        """
        self.location = location
        self.empty_dir = empty_dir
        self.rem_loc_dir = rem_loc_dir
        self.rem_from_hub_dir = rem_from_hub_dir
        self.add_emp_dir_on_hub = add_emp_dir_on_hub
        self.path_validate_errors = path_validate_errors or []

        if name:
            self.name = name
        else:
            self.name = location.split(os.sep, -1)[-1]
        
        if content or content=='':
            self.content = content
        elif as_hashes:
            self.content = None
        else:
            if empty_dir:
                self.content = []
            else:
                validation_error = self.validate_location(location)
                if validation_error:
                    self.path_validate_errors.append(validation_error)
                self.content = self.get_content(location)
        if hash:
            self.hash = hash
        elif removed:
            self.hash = ''
        else:
            self.hash = self.get_hash()
       
    def validate_location(self, file_location):
        """
        """
        filename, file_extension = os.path.splitext(file_location)
        rel_path = os.path.relpath(file_location)
        name = rel_path
        if os.sep == '\\':
            pattern = re.compile('[@!#$%^&*()\[\]<=>?\|}{~;,`\'\"\s+\t+]')
        else:
            pattern = re.compile('[@!#$%^&*()\[\]<=>?\|\\\\}{~:;,`\'\"\s+\t+]')
        error = 'Please enter a valid name. (White-spaces and special characters are not allowed except - and _).'
        if pattern.search(filename):
            return {'file': name, 'error' : error  }
        if os.path.isdir(file_location):
            #if '.' in name:
            #    return {'file': name, 'error' : error  }
            pass
        elif file_extension.lower() in ALLOWED_IMAGE_TYPES:
            pass
        elif file_extension.lower() == '.json':
            pass
        elif file_extension.lower() in RESTRICT_IMAGE_TYPE:
            error = 'Please enter a valid extension. (The allowed image extensions are .jpg, .jpeg, .png).'
            return {'file': name, 'error' : error  }
        elif file_extension.lower() not in ALLOWED_FILE_TYPES:
            error = 'Please enter a valid extension. (The allowed file extensions are .html, .css, .bd, .js, .json, .svg, .txt).'
            return {'file': name, 'error' : error  }
        return None

    def get_hash(self):
        """
        :return:
        """
        if self._hash:
            return self._hash
        else:
            self._hash = self.generate_hash()
            return self._hash

    def get_content(self, location):
        """
        :return:
        """
        return


class Directory(IntermediaryNode):
    """
    """
    def get_content(self, location):
        """
        """
        error_content = []
        content = []
        if (os.path.exists(location)) and (not self.empty_dir):
            directory_content = os.listdir(location)
            for each_file in directory_content:
                file_location = os.path.join(location, each_file)
                filename, file_extension = os.path.splitext(file_location)
                if(each_file.endswith(IGNORE_EXTENSIONS)):
                    continue
                if (each_file.startswith(IGNORE_PREFIXES)) and (each_file != '_package.json') and (each_file != '_index.json'):
                    continue
                content.append(self.get_content_at_path(file_location))
            return content

    def get_content_at_path(self, file_location):
        """
        """
        filename, file_extension = os.path.splitext(file_location)
        name  = os.path.basename(file_location)
        rel_path = os.path.relpath(file_location)
        nodeData = None
        if os.path.isdir(file_location):
            nodeData = Directory(file_location)
        elif file_extension.lower() in ALLOWED_IMAGE_TYPES:
            nodeData = BinaryFile(file_location)
        elif file_extension.lower() == '.json':
            nodeData = JSONFile(file_location)
        else:
            try:
                nodeData = TextFile(file_location)
            except: 
                nodeData = BinaryFile(file_location)
        if nodeData.path_validate_errors:
            self.path_validate_errors.extend(nodeData.path_validate_errors)
        return nodeData
    
    def generate_hash(self):
        """
        :return:
        """
        file_hash_list = []
        for content_file in self.content:
            file_hash_list.append('%s:%s' %
                                  (content_file.name, content_file.get_hash()))
        final_hash = hashlib.md5('::'.join(sorted(file_hash_list)).encode('utf-8')).hexdigest()
        return final_hash


class TextFile(IntermediaryNode):
    """
    """
    def get_content(self, file_location):
        """
        """
        with open(file_location, 'r', encoding='utf-8') as content_file:
            file_data = content_file.read()
        return file_data

    def generate_hash(self):
        """
        :return:
        """
        try:
            return hashlib.md5(self.content.encode('utf-8')).hexdigest()
        except UnicodeDecodeError:
            return hashlib.md5(self.content).hexdigest()


class BinaryFile(IntermediaryNode):
    """
    """
    def get_content(self, file_location):
        """
        """
        return self._get_media(file_location)

    def generate_hash(self):
        """
        :return:
        """
        # return self._compute_hash(self.content)
        hash = self._compute_hash(self.content)
        self.content.close()
        return hash

    def _get_media(self, image_path):
        """
        """
        image_path = os.path.join(image_path)
        image = open(image_path, 'rb')
        return image

    def _compute_hash(self, content):
        """
        :return:
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


class JSONFile(IntermediaryNode):
    """
    """
    def get_content(self, file_location):
        """
        """
        with open(file_location, 'r') as content_file:
            content_file_data = content_file.read()
            try:
                if not content_file_data:
                    content = ''
                else:
                    content = json.loads(content_file_data)
            except ValueError:
                raise BlendedException("Invalid JSON content in File %s" % self.name)
            return self._JSON_as_string(content)

    def generate_hash(self):
        """
        :return:
        """
        return hashlib.md5(self.content.encode('utf-8')).hexdigest()

    def _JSON_as_string(self, content):
        """
        :param content:
        :return:
        """
        return json.dumps(content, separators=(',', ':'), sort_keys=True)

