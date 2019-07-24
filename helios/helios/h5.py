# -*- coding: utf-8 -*-

""" Interface to deal with .h5 files in EOS database """
import json
import os
import tarfile

import h5py


class MongoH5:
    """ .h5 saved in MongoDB """

    @staticmethod
    def _get_out_folder():
        out = ''  # todo tmp folder where to save tmp .h5

        if not os.path.exists(out):
            os.makedirs(out)

        return out

    def __init__(self, mongo_doc):
        self.data = mongo_doc
        self.out_folder = self._get_out_folder()

    def _get_path(self):
        return self.data['path']

    def _get_output_file(self):
        file_name = self.data['_id']
        folder_name = self.out_folder
        return os.path.join(folder_name, file_name)

    def save_to_disk(self):
        h5_reader = h5py.File(self._get_path(), 'r')
        data = {
            key: h5_reader.get(key)
            for key in h5_reader.keys()  # todo ask nicolas if also attrs.keys should be saved
        }
        h5_reader.close()
        file_out = self._get_output_file()
        with open(file_out, 'w') as writer:
            json.dump(data, writer)  # todo check


class MongoH5Collection:
    """ Multiple MongoH5 """

    def __init__(self, docs):
        self.docs = [
            MongoH5(doc)
            for doc in docs
        ]
        self.out_folder = self._get_out_folder()

    @staticmethod
    def _get_out_folder():
        out = ''  # todo tmp folder where to save tmp .h5

        if not os.path.exists(out):
            os.makedirs(out)

        return out

    def _get_output_file(self):
        file_name = '.tar.gz'  # todo generate random uuid
        folder_name = self.out_folder
        return os.path.join(folder_name, file_name)

    def save_to_disk(self):
        tf = tarfile.open(self._get_output_file(), mode="w:gz")

        for doc in self.docs:
            doc.save_to_disk()  # save to disk
            tf.add(doc._get_output_file())  # add to tar

        tf.close()
        return self._get_output_file()
