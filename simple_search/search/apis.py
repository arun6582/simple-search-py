import re
from database import apis


PREFIX = {
    'document': 'docs',
    'inverted_index': 'iis',
    'cache': 'cache'
}


def save_prefix(_type):
    return PREFIX[_type]


class CachedSearch(object):

    @classmethod
    def get_meta(cls, query):
        pass

    @classmethod
    def set_meta(cls, query):
        pass

    @classmethod
    def search(cls, query):
        fields = sorted(query['fields'])
        words = re.findall("\w+", query['terms'])
        metas = []
        for word in words:
            metas.append(cls.get_meta({'fields': fields, 'term': word}))

        consolidated = {}
        for meta in metas:
            for doc in meta:
                consolidated[doc] = consolidated.get(doc, 0) + meta[doc]

        return sorted(consolidated.items(), key=lambda x: x[1], reverse=True)


class Index(object):

    @classmethod
    def prepare_inverted_index_metas(cls, text):
        pass

    @classmethod
    def index(self, data):
        tokenized = {}
        for field, val in data.items():
            try:
                tokenized[field] = re.findall("\w+", val)
            except TypeError:
                pass

    @classmethod
    def search(cls, query):
        pass

    @classmethod
    def update_inverted_index(cls, index):
        pass
