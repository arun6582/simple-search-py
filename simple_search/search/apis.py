import re
from database import apis
import math
import collections


PREFIX = {
    'document': 'docs',
    'inverted_index': 'ii',
    'meta': 'meta'
}


def _prefix(_type):
    return PREFIX[_type]


def unique_indenfier_doc(document, node=None):
    node = node or ""
    return "%s__%s" % (node, document)


class CachedSearch(object):

    @classmethod
    def get_meta(cls, query, node=None):
        try:
            document = "%s$%s" % (_prefix('inverted_index'), query['term'])
            meta = apis.Operation.retrieve(document, node=node)
            fields = '.'.join(query['fields'])
            calcs = meta.get('calcs', {})
            for doc, _ in meta.get('ii', {}).items():
                # doc is system modified id not as fed in data during indexing
                rank = calcs.get(doc, {}).get(fields, None)
                if not rank:
                    rank = Index.calculate_rank(doc, fields, query['term'], node=node)
                    calcs[doc] = calcs.get(doc, {})
                    calcs[doc][fields] = rank
            meta['calcs'] = calcs
            cls.set_meta(document, meta, node=node)
            return {
                unique_indenfier_doc(doc, node): comps[fields] for doc, comps in calcs.items()
            }
        except IOError:
            return {}

    @classmethod
    def delete_meta(cls, word, doc, node=None):
        document = "%s$%s" % (_prefix('inverted_index'), word)
        js = apis.Operation.retrieve(document, node=node)
        js.pop('calcs', {})
        return apis.Operation.save(document, js, node=node)

    @classmethod
    def set_meta(cls, document, data, node=None):
        return apis.Operation.save(document, data, node=node)

    @classmethod
    def search(cls, query):
        fields = sorted(query['fields'])
        words = re.findall("\w+", query['terms'])
        metas = []
        """
        meta format
        {doc: rank, doc2: rank2...}
        """
        for word in words:
            metas.append(cls.get_meta({'fields': fields, 'term': word}, node=None))

        for node in apis.Operation.live_nodes():
            for word in words:
                metas.append(
                    cls.get_meta({'fields': fields, 'term': word}, node=node)
                )

        consolidated = {}
        for meta in metas:
            for doc in meta:
                consolidated[doc] = consolidated.get(doc, 0) + meta[doc]

        return sorted(consolidated.items(), key=lambda x: x[1], reverse=True)


class Index(object):

    @classmethod
    def index(cls, data):
        tokenized = {}
        for field, val in data.items():
            try:
                tokenized[field] = re.findall("\w+", val)
            except TypeError:
                pass

        document = "%s$%s" % (_prefix('document'), data['id'])
        apis.Operation.save(document, data)
        cls.update_inverted_index(document, tokenized)
        cls.update_documents_meta()

    @classmethod
    def search(cls, query):
        result = CachedSearch.search(
            {
                'fields': query.get('fields', ['_all', ]),
                'terms': query['terms']
            }
        )
        response = []
        for doc, _ in result:
            node, document = doc.split("__")
            response.append(
                apis.Operation.retrieve(document, node=node)
            )
        return response

    @classmethod
    def update_inverted_index(cls, document, tokenized_field_data):
        ii = collections.defaultdict(
            lambda: collections.defaultdict(
                int
            )
        )
        for field, array_or_words in tokenized_field_data.items():
            for word in array_or_words:
                ii[word][field] += 1
                ii[word]['_all'] += 1

        for word, metas in ii.items():
            apis.Operation.create_or_update(
                "%s$%s" % (_prefix('inverted_index'), word),
                {
                    'ii': {
                        document: metas
                    }

                }
            )
            CachedSearch.delete_meta(word, document)
        return ii

    @classmethod
    def update_documents_meta(cls):
        total = len(apis.Operation.get_documents("%s\$" % _prefix('document')))
        apis.Operation.create_or_update(
            "%s$" % _prefix('meta'), {'total_documents': total}
        )

    @classmethod
    def calculate_rank(cls, doc, fields, term, node=None):
        # term is present in doc that why we have doc
        split_fields = fields.split(".")
        ii_term_file = "%s$%s" % (_prefix('inverted_index'), term)
        ii_term = apis.Operation.retrieve(ii_term_file, node=node)

        ii_ = 0
        total_words = 1
        for field in split_fields:
            ii_ += ii_term['ii'][doc].get(field, 0)
            total_words += len(
                apis.Operation.retrieve(doc, node=node).get(field, [])
            )

        number_of_times_doc_occurence = 1
        for doc, values in ii_term['ii'].items():
            present = 1
            for field in split_fields:
                present *= bool(values.get(field, 0))
            number_of_times_doc_occurence += present

        db_meta_file = "%s$" % (_prefix('meta'), )
        total_documents = apis.Operation.retrieve(
            db_meta_file, node=node
        )['total_documents']

        for node in apis.Operation.live_nodes():
            db_meta_file = apis.Operation.retrieve(db_meta_file, node)
            total_documents += db_meta_file['total_documents']

        idf_ = math.log10(
            total_documents * 1.0 / number_of_times_doc_occurence
        )

        return (ii_ / total_words) * idf_
