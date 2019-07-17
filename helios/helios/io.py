# -*- coding: utf-8 -*-

""" Saves data from EOS db """

import abc
import gzip
import json
import os
import tarfile
import uuid
from io import BytesIO

from astraeus.core import Astraeus


class Hasher:
    """ Something that hashes something """

    @abc.abstractmethod
    def hash_key(self, key):
        return 0


class UUIDHasher(Hasher):
    """ Hashing based on UUID4 """

    def hash_key(self, key):
        hashed = str(uuid.uuid4())
        hashed = hashed.replace('-', '')
        return hashed


class DataSaver:
    def __init__(self, config, hasher=UUIDHasher()):
        """
        :param hasher: stuff to hash stuff
        :param config: {} with options. There MUST be a 'out folder' key
        """

        self.hasher = hasher
        self.config = config

    def _get_output_file(self, key, extension):
        key = self.hasher.hash_key(key)
        out_folder = self.config['folder']
        out_file = key + '.' + extension
        out_file = os.path.join(out_folder, out_file)

        # create out folder if necessary
        out_folder = os.path.dirname(out_file)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        # there is already a file
        if os.path.exists(out_file):
            return None  # cannot save here

        return out_file

    def save_data(self, data):
        out_file = self._get_output_file(None, 'data')
        with open(out_file, 'w') as writer:
            writer.write(data)

        return out_file

    def store_data(self, data):
        """
        :param data: bytes
        """

        out_file = self._get_output_file(None, 'tar.gz')
        with gzip.GzipFile(out_file, 'w') as writer:
            writer.write(data)

        return out_file


class JsonDataSaver(DataSaver):
    def save_json(self, data):
        json_data = json.dumps(data)
        return self.save_data(json_data)

    def store_as_json(self, data):
        json_data = json.dumps(data)
        json_bytes = json_data.encode('utf-8')
        return self.store_data(json_bytes)


class AstraeusDataSaver(JsonDataSaver):
    def get_key_for(self, val):
        astraeus = Astraeus()
        download_key = astraeus.save(val)  # save real path
        root_url = self.config['url']
        full_url = root_url + download_key
        return full_url

    def download_multiple(self, lst):
        out_file = self._get_output_file(None, 'tar.gz')  # create file
        tar = tarfile.TarFile(out_file, 'w')  # open

        for i, data in enumerate(lst):
            buff = BytesIO()
            buff.write(json.dumps(data).encode())
            buff.seek(0)

            file_name = '{}.json'.format(i)  # todo better name
            info = tarfile.TarInfo(name=file_name)
            info.size = len(buff.getbuffer())
            tar.addfile(tarinfo=info, fileobj=buff)

        tar.close()

    def download_as_json(self, data):
        out_file = self.store_as_json(data)
        return self.get_key_for(out_file)
