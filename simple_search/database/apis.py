from django.conf import settings
import utils
import os
import re
import requests
import requests.exceptions as requests_exceptions


class Operation(object):

    db = settings.DB_SETTINGS['path']

    @classmethod
    def get_path(cls, filename):
        return os.path.join(cls.db, filename)

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
            os.listdir(cls.db)
        )

    @classmethod
    def live_nodes(cls):
        live = []
        for url in settings.DB_SETTINGS['othernodes']:
            try:
                # If live then meta must be present
                response = requests.get("%s?document=meta$", url)
            except requests_exceptions.ConnectionError:
                print("%s node isn't live" % url)
            else:
                response.status_code == 200
                live.append(url)
        return live


def setup_db():
    if os.path.exists(Operation.db):
        return
    os.makedirs(Operation.db)


setup_db()
