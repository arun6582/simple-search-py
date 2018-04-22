from database import apis
import mock


class TestOperation(object):

    @mock.patch(
        'os.listdir',
        lambda x: ['document$1', 'document$2', 'cache$5']
    )
    def test_get_documents(self):
        result = apis.Operation.get_documents("^document\$.*")
        assert result == ['document$1', 'document$2']

    @mock.patch('django.conf.settings.DB_SETTINGS', {'othernodes': ['n1']})
    def test_live_nodes(object):
        def mm(*args, **kwargs):
            class A:
                status_code = 200
            return A

        with mock.patch('requests.get', mm):
            assert apis.Operation.live_nodes() == ['n1']
