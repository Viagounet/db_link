import datetime
import json
import dataclasses


class Link:
    def __init__(self):
        print(self.__class__.__subclasses__())

    @property
    def encoder(self):
        class JSONEncoder(json.JSONEncoder):
            def default(self, o):
                if dataclasses.is_dataclass(o):
                    return dataclasses.asdict(o)
                if isinstance(o, datetime.datetime):
                    return o.isoformat()
                return super().default(o)

        return JSONEncoder

    def to_json_file(self, folder):
        with open(folder + self.__class__.__name__ + '.json', 'w') as f:
            json.dump(self.__dict__, f, cls=self.encoder, indent=4)

    def to_json_string(self):
        return json.dumps(self.__dict__, cls=self.encoder, indent=4)

    def to_firebase(self, db):
        json_data = json.loads(self.to_json_string())
        db.add(self.__class__.__name__, json_data)


    # This should be done on the Global DB manager
    """def load_firebase(self, db):
        path = self.__class__.__name__
        json_data = db.get(path)
        print(json_data)
        self.__dict__ = json_data
        return self"""