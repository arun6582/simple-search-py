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
