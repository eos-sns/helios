# -*- coding: utf-8 -*-

""" Interface to deal with .h5 files in EOS database """

import os
import shutil
import tarfile

import h5py
from astraeus.core import UUIDHasher


def create_if_necessary(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_random_folder(from_folder):
    folder_name = UUIDHasher().hash_key(None)  # random folder
    out = os.path.join(from_folder, folder_name)
    create_if_necessary(out)
    return out


def get_output_file(file_name, extension, from_folder):
    create_if_necessary(from_folder)
    return os.path.join(from_folder, file_name + extension)


class MongoH5:
    """ .h5 saved in MongoDB """

    OPTIONAL_DATASET = ['co-eval_k', 'co-eval_PS_z']

    def _get_out_folder(self):
        out_folder = self.config["folder"]  # root folder out
        return get_random_folder(out_folder)

    def __init__(self, mongo_doc, config):
        self.data = mongo_doc
        self.config = config
        self.out_folder = self._get_out_folder()

    def _get_path(self):
        return self.data['path']

    def _get_output_file(self, extension='.h5'):
        return get_output_file(
            UUIDHasher().hash_key(None),
            extension,
            self.out_folder
        )

    def save_to_disk(self, files_to_get):
        h5_file = self._get_path()
        file_out = self._get_output_file()
        shutil.copy(h5_file, file_out)

        with h5py.File(file_out, 'w') as editor:
            for key in self.OPTIONAL_DATASET:
                if key not in files_to_get:
                    try:
                        del editor[key]  # remove dataset
                    except:
                        pass

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
            UUIDHasher().hash_key(None),
            '.tar.gz',
            from_folder
        )

    def save_to_disk(self, out_folder, files_to_get):
        out_file = self._get_output_file(out_folder)
        tf = tarfile.open(out_file, mode="w:gz")

        for doc in self.docs:
            file_path = doc.save_to_disk(files_to_get)  # save to disk
            file_name = os.path.basename(file_path)
            tf.add(file_path, arcname=file_name)  # add to tar

        tf.close()
        return out_file
