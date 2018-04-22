from django.conf import settings
import utils
import os


class Operation(object):

    @classmethod
    def get_path(cls, filename):
        return os.path.join(settings.DB_SETTINGS, filename)

    @classmethod
    def save(cls, data):
        return utils.FileJsonIO.json_to_file(data, cls.get_path(data['id']))

    @classmethod
    def retrieve(cls, query):
        return utils.FileJsonIO.file_to_json(cls.get_path(query))
