from json import JSONEncoder, dumps


class RobustEncoder(JSONEncoder):
    def default(self, o):
        try:
            return super().default(o)
        except TypeError:
            return repr(o)


def json(obj):
    return dumps(obj, indent=4, ensure_ascii=False, cls=RobustEncoder)
