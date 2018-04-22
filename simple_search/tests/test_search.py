from search import apis
import mock
from database import apis as db_apis
import re
import shutil


def reset_db(func):
    shutil.rmtree(db_apis.Operation.db)
    db_apis.setup_db()

    def _inner(*args, **kwargs):
        return func(*args, **kwargs)

    return _inner


class TestIndex(object):

    @mock.patch.object(
        db_apis.Operation, 'get_documents', classmethod(lambda y, x: [1, 2])
    )
    def test_update_documents_meta(self):
        apis.Index.update_documents_meta()
        metafile = db_apis.Operation.retrieve("%s$" % apis._prefix('meta'))
        assert metafile['total_documents'] == 2

    @reset_db
    def test_update_inverted_index(self):
        result = apis.Index.update_inverted_index(
            "%s$%s" % (apis._prefix('document'), '44'),
            {
                'f1': re.findall('\w+', 'a quick brown'),
                'f2': re.findall('\w+', 'jump right over the'),
                'f3': re.findall('\w+', 'over a lazy dog')
            }
        )
        assert 'f1' not in result['the']
        assert 'f1' in result['brown']
        assert result['brown']['_all'] == 1
        assert result['the']['_all'] == 1
        assert result['a']['_all'] == 2

    @reset_db
    def test_index(self):
        apis.Index.index(
            {
                'id': 34,
                'f1': 'a quick brown',
                'f2': 'jump right over the',
                'f3': 'over a lazy dog'
            }
        )
        result = apis.Index.search({'terms': 'brown'})
        assert result[0]['f1'] == 'a quick brown'

    def _get_meta(self):
        result = apis.CachedSearch.get_meta(
            {'fields': ['f1', 'f2'], 'term': 'w'}
        )
        result = map(lambda x: x[0].split("__")[1], result.items())
        assert 'doc1' in result
        assert 'doc2' in result

    @reset_db
    def test_calculate_rank(self):
        cls = apis.Index()

        ii_term_file = {
            'ii': {
                'doc1': {
                    'f1': 4,
                    'f2': 5
                },
                'doc2': {
                    'f1': 4,
                    'f2': 5,
                    'f3': 4
                }
            }
        }

        db_meta_file = {
            'total_documents': 4
        }

        def retrieve(x):
            if x == "%s$%s" % (apis._prefix('inverted_index'), 'w'):
                return ii_term_file
            else:
                return db_meta_file

        with mock.patch.object(
                    db_apis.Operation,
                    'retrieve',
                    classmethod(lambda y, x, node: retrieve(x))
                ):

            self._get_meta()
            result1 = cls.calculate_rank('doc1', 'f1', 'w')
            result2 = cls.calculate_rank('doc2', 'f1', 'w')
            assert result1 == result2
            result1 = cls.calculate_rank('doc1', 'f3', 'w')
            result2 = cls.calculate_rank('doc2', 'f3', 'w')
            assert result2 > result1
            result1 = cls.calculate_rank('doc2', 'f3.f2', 'w')
            result2 = cls.calculate_rank('doc1', 'f3.f2', 'w')
            assert result2 < result1


class TestCachedSearch(object):

    def test_search(self):
        meta = {
            'w1': {
                apis.unique_indenfier_doc('d1'): 3,
                apis.unique_indenfier_doc('d2'): 4
            },
            'w2': {
                apis.unique_indenfier_doc('d2'): 10,
                apis.unique_indenfier_doc('d4'): 2
            }
        }

        with mock.patch.object(
                    apis.CachedSearch, 'get_meta',
                    classmethod(lambda y, x, node: meta[x['term']])
                ):
            result = apis.CachedSearch.search(
                {'fields': ['f1', 'f2'], 'terms': 'w1 w2'})

            assert result == [('__d2', 14), ('__d1', 3), ('__d4', 2)]
