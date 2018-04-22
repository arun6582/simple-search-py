from django.conf import settings
import utils
import os
import re


class Operation(object):

    @classmethod
    def get_path(cls, filename):
        return os.path.join(settings.DB_SETTINGS, filename)

    @classmethod
    def save(cls, document, data):
        return utils.FileJsonIO.json_to_file(data, cls.get_path(document))

    @classmethod
    def retrieve(cls, query):
        return utils.FileJsonIO.file_to_json(cls.get_path(query))

    @classmethod
    def get_documents(cls, regex_pattern):
        return filter(
            lambda key: bool(re.compile(regex_pattern).search(key)),
            os.listdir(settings.DB_SETTINGS)
        )
