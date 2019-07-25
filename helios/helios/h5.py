# -*- coding: utf-8 -*-

""" Interface to deal with .h5 files in EOS database """
import json
import os
import tarfile

import h5py
from astraeus.core import UUIDHasher


def create_if_necessary(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_random_folder(from_folder):
    folder_name = UUIDHasher().hash_key()  # random folder
    out = os.path.join(from_folder, folder_name)
    create_if_necessary(out)
    return out


def get_output_file(file_name, extension, from_folder):
    create_if_necessary(from_folder)
    return os.path.join(from_folder, file_name + extension)


class MongoH5:
    """ .h5 saved in MongoDB """

    def _get_out_folder(self):
        out_folder = self.config["folder"]  # root folder out
        return get_random_folder(out_folder)

    def __init__(self, mongo_doc, config):
        self.data = mongo_doc
        self.config = config
        self.out_folder = self._get_out_folder()

    def _get_path(self):
        return self.data['path']

    def _get_output_file(self):
        return get_output_file(
            self.data['_id'],
            '.json',
            self.out_folder
        )

    def save_to_disk(self, ):
        h5_reader = h5py.File(self._get_path(), 'r')
        data = {
            key: ''  # todo convert H5F5 dataset h5_reader.get(key)
            for key in h5_reader.keys()  # todo ask nicolas if also attrs.keys should be saved
        }
        h5_reader.close()
        file_out = self._get_output_file()
        with open(file_out, 'w') as writer:
            json.dump(data, writer)
        return file_out


class MongoH5Collection:
    """ Multiple MongoH5 """

    def __init__(self, docs, config):
        self.docs = [
            MongoH5(doc, config)
            for doc in docs
        ]

    @staticmethod
    def _get_output_file(from_folder):
        return get_output_file(
            UUIDHasher().hash_key(),
            '.tar.gz',
            from_folder
        )

    def save_to_disk(self, out_folder):
        out_file = self._get_output_file(out_folder)
        tf = tarfile.open(out_file, mode="w:gz")

        for doc in self.docs:
            file_path = doc.save_to_disk()  # save to disk
            file_name = os.path.basename(file_path)
            tf.add(file_path, arcname=file_name)  # add to tar

        tf.close()
        return out_file
