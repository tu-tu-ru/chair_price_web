import uuid

import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database
#import src.models.stores.store as Store
from src.models.stores.store import Store


class Item:
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        corresponding_store = Store.find_store_by_url(url)
        self.tag_name = corresponding_store.tag_name
        self.query = corresponding_store.query
        #self.price = self.load_item(tag_name, query)
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    @classmethod
    def get_item_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
        # return cls(**Database.find_one(collection='items', query={"_id": item_id}))

    def load_price(self):
        """
        To return the price of item
        :return:
        """
        # Amazon.ca <span id="priceblock_ourprice" class="a-size-medium a-color-price">CDN$ 374.87</span>

        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        # Use RegEx to extract the numeric from `string_price`
        pattern = re.compile("(\d+.\d)")  # re.compile()函数为正则表达式创建模式对象
        match = pattern.search(string_price)
        self.price = float(match.group())  # `self.price` 原本是 None，每次调用 `load_price()` 都会 update 一下 price 的数值

        # return an item which is price ready

        return match.group()

    def save_to_mongo(self):
        """
        To insert json to db
        :return:
        """
        Database.update(collection=ItemConstants.COLLECTION, query={"_id": self._id}, data=self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "price": self.price,
            "_id": self._id
        }

