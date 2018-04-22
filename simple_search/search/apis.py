import re


class Index(object):

    PREFIX = {
        'document': 'docs',
        'inverted_index': 'iis'
    }

    @classmethod
    def prepare_inverted_index_metas(cls, text):
        pass

    @classmethod
    def index(self, data):
        import pdb; pdb.set_trace()
        tokenized = {}
        for field, val in data.items():
            tokenized[field] = re.findall("\w+", val)

    @classmethod
    def get_save_prefix(cls,  _type):
        return cls.PREFIX[_type]

    @classmethod
    def search(cls, query):
        pass

    @classmethod
    def update_inverted_index(cls, index):
        pass
