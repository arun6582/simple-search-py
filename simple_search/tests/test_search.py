from search import apis
import mock
from database import apis as db_apis
import re


class TestIndex(object):

    def test_index(self):
        apis.Index.index(data={'id': '34r35', 'f1': 'a quick brown'})

    @mock.patch.object(
        db_apis.Operation, 'get_documents', classmethod(lambda y, x: [1, 2])
    )
    def test_update_documents_meta(self):
        apis.Index.update_documents_meta()
        metafile = db_apis.Operation.retrieve("%s$" % apis._prefix('meta'))
        assert metafile['total_documents'] == 2

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

    def _get_meta(self):
        result = apis.CachedSearch.get_meta(
            {'fields': ['f1', 'f2'], 'term': 'w'}
        )
        assert result == {'doc1': 2.709269960975831, 'doc2': 2.709269960975831}

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
                    classmethod(lambda y, x: retrieve(x))
                ):

            self._get_meta()
            result = cls.calculate_rank('doc1', 'f1', 'w')
            assert result == 1.2041199826559248
            result = cls.calculate_rank('doc2', 'f1', 'w')
            assert result == 1.2041199826559248
            result = cls.calculate_rank('doc1', 'f3', 'w')
            assert result == 0.0
            result = cls.calculate_rank('doc2', 'f3', 'w')
            assert result == 2.4082399653118496
            result = cls.calculate_rank('doc2', 'f3.f2', 'w')
            assert result == 5.418539921951662
            result = cls.calculate_rank('doc1', 'f3.f2', 'w')
            assert result == 3.010299956639812


class TestCachedSearch(object):

    def test_search(self):
        meta = {
            'w1': {
                'd1': 3,
                'd2': 4
            },
            'w2': {
                'd2': 10,
                'd4': 2
            }
        }

        with mock.patch.object(
                    apis.CachedSearch, 'get_meta',
                    classmethod(lambda y, x: meta[x['term']])
                ):
            result = apis.CachedSearch.search(
                {'fields': ['f1', 'f2'], 'terms': 'w1 w2'})

        assert result == [('d2', 14), ('d1', 3), ('d4', 2)]
