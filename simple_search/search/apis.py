import re
from database import apis


PREFIX = {
    'document': 'docs',
    'inverted_index': 'iis',
    'meta': 'meta'
}


def _prefix(_type):
    return PREFIX[_type]


class CachedSearch(object):

    @classmethod
    def get_meta(cls, query):
        try:
            document = "%s$%s" % (_prefix('inverted_index'), query['term'])
            meta = apis.Operation.retrieve(document)
            fields = '.'.join(query['fields'])
            calcs = meta.get('calcs', {})
            for doc, comps in calcs.items():
                rank = comps.get(fields, None)
                if not rank:
                    rank = Index.calculate_rank(doc, fields, query['term'])
                    calcs[doc][comps] = comps
                    calcs[doc][comps][fields] = rank

            cls.set_meta(document, meta)
        except IOError:
            return {}

    @classmethod
    def set_meta(cls, document, data):
        return apis.Operation.save(document, data)

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
    def total_documents(cls):
        pass

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

    @classmethod
    def calculate_rank(cls, doc, fields, term):
        return {}
