from search import apis
import mock


class TestIndex(object):

    def test_index(self):
        cls = apis.Index()
        cls.index(data={'id': '34r35', 'f1': 'a quick brown'})


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
