import json


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
