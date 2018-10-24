import uuid

import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database


class Item:
    def __init__(self, name, price, url, store, _id=None):
        self.name = name
        self.url = url
        self.store = store  # Store contains the price and query information
        tag_name = store.tag_name
        query = store.query
        #self.price = self.load_item(tag_name, query)
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_item(self, tag_name, query_path):
        """
        To return the price of item
        :param tag_name: from website, like "span"
        :param query_path: from website, like "id", "class"
        :return:
        """
        # Amazon.ca <span id="priceblock_ourprice" class="a-size-medium a-color-price">CDN$ 374.87</span>

        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(tag_name,query_path)
        string_price = element.text.strip()

        # Use RegEx to extract the numeric from `string_price`
        pattern = re.compile("(\d+.\d)")  # re.compile()函数为正则表达式创建模式对象
        match = pattern.search(string_price)

        # return an item which is price ready

        return match.group()

    def save_to_mongo(self):
        """
        To insert json to db
        :return:
        """
        Database.insert(collection=ItemConstants.COLLECTION, data=self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "price": self.price
        }