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
    def save(cls, document, data, node=None):
        if node:
            return requests.post(
                node + "/meta/",
                json={
                    'document': document, 'data': data
                }
            ).json()['success']
        return utils.FileJsonIO(cls.get_path(document)).json_to_file(data)

    @classmethod
    def get_or_create(cls, document, data, node=None):
        try:
            cls.retrieve(document, node)
        except IOError:
            return cls.save(document, data, node=node)

    @classmethod
    def create_or_update(cls, document, data, node=None):
        try:
            saved = cls.retrieve(document, node=node)
        except IOError:
            return cls.save(document, data, node=node)
        else:
            saved.update(data)
            return cls.save(document, saved, node=node)

    @classmethod
    def retrieve(cls, query, node=None):
        if node:
            response = requests.get(
                "%s/meta/?document=%s" % (node, query)
            ).json()
            if response['success']:
                return response['document']
            else:
                return {}
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
                response = requests.get("%s?document=meta$" % url)
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
