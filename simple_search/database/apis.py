from django.conf import settings
import utils
import os
import re


def setup_db():
    if os.path.exists(settings.DB_SETTINGS['path']):
        return
    os.makedirs(settings.DB_SETTINGS['path'])


setup_db()


class Operation(object):

    @classmethod
    def get_path(cls, filename):
        return os.path.join(settings.DB_SETTINGS['path'], filename)

    @classmethod
    def save(cls, document, data):
        return utils.FileJsonIO(cls.get_path(document)).json_to_file(data)

    @classmethod
    def get_or_create(cls, document, data):
        try:
            cls.retrieve(document)
        except IOError:
            return cls.save(document, data)

    @classmethod
    def create_or_update(cls, document, data):
        try:
            saved = cls.retrieve(document)
        except IOError:
            return cls.save(document, data)
        else:
            merged = utils.deep_merge_dicts(saved, data)
            return cls.save(document, merged)

    @classmethod
    def retrieve(cls, query):
        return utils.FileJsonIO(cls.get_path(query)).file_to_json()

    @classmethod
    def get_documents(cls, regex_pattern):
        return filter(
            lambda key: bool(re.compile(regex_pattern).search(key)),
            os.listdir(settings.DB_SETTINGS['path'])
        )
