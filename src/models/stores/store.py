import uuid

from src.common.database import Database
import src.models.stores.constants as store_constants
import src.models.stores.errors as StoreErrors


class Store:
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<sto {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_store_by_id(cls, id):
        return cls(**Database.find_one(store_constants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        # Database.update(store_constants.COLLECTION, {"_id": self._id}, self.json())
        Database.insert('store', self.json())

    @classmethod
    def get_store_by_name(cls, store_name):
        return cls(**Database.find_one(store_constants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_store_by_url_prefix(cls, store_prefix):
        """
        :param store_prefix:
        :return: A store object
        """
        # parse the url prefix with RegEx
        return cls(**Database.find_one(store_constants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(store_prefix)}}))

    @classmethod
    def find_store_by_url(cls, url):
        """
        To return a store from a url of an item
        :param url: item's url
        :return: a store, or StoreNotFoundError if no store matches the url
        """
        for i in range(0, len(url)+1):
            try:
                store = cls.get_store_by_url_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNotFoundError("The URL Prefix used to find the store didn't give us any results!")