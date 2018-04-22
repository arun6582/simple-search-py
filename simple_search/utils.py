import json
import copy


class FileJsonIO:

    def __init__(self, filename):
        self.filename = filename

    def file_to_json(self, **opts):
        with open(self.filename, 'r') as f:
            js = json.load(f, **opts)
        return js

    def json_to_file(self, d, **opts):
        with open(self.filename, 'w') as f:
            json.dump(d, f, **opts)
        return True


def deep_merge_dicts(*args, **kwargs):
    '''
    can also be called merge_dicts but don't want to confuse reader
    deep_merge_dicts {'a': {'b': 5,'v': 3}}, {'c': 3}},{'a': {'b': 4}}
    will produce {'a': {'b': 4,'v': 3}}, {'c': 3}}
    '''
    if len(args) < 2:
        raise Exception('atleast two schema needed')
    elif len(args) == 2:
        if 'modify' in kwargs and kwargs['modify']:
            d1 = args[0]
        else:
            d1 = copy.copy(args[0])
        d2 = args[1]
        for key, value in d2.items():
            if key in d1 and isinstance(
                    value, dict) and isinstance(d1[key], dict):
                d1[key] = deep_merge_dicts(d1[key], value)
            else:
                d1[key] = value
        return d1
    else:
        return deep_merge_dicts(
                deep_merge_dicts(*args[:2], **kwargs), *args[2:], **kwargs)
