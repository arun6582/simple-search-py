from search import apis

class TestIndex(object):
    
    def test_index(self):
        cls = apis.Index()
        cls.index(data={'id': 1, 'f1': 'a quick brown'})
