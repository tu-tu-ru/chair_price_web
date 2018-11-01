import datetime
import uuid
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
#import src.models.items.item as Item
from src.models.items.item import Item


class Alert:
    def __init__(self, user_email, price_limit, item_id, _id=None, last_check=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_item_by_id(item_id)
        self.last_check = datetime.datetime.utcnow() if last_check is None else last_check
        self._id = uuid.uuid4().hex if _id is None else _id

    """
    For the `last_check` attribute, when an alert is created, the time it's being checked is right now, so the `datetime` function need to be callled to record time
    For an alert which comes from the database, which means that the last_check time has already exists. So, I will load the value from the database

    """

    def __repr__(self):
        return "<Alert for {} with item {} at the price of {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            url=AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user.email,
                "subject": "Price alert for item {}".format(self.item.name),
                "text": "check this link for lowest price"
            }
        )

    @classmethod
    def find_needing_update(cls, munite_since_update=AlertConstants.ALERT_TIMEOUT):
        """
        To return a list of class object which inherit from Alert class
        :param munite_since_update:
        :return:
        """
        last_update_limit = datetime.datetime.utcnow() - datetime.timedelta(munite_since_update)
        # classmethod 不实例化就直接使用类的方法
        return [cls(**i) for i in Database.find(AlertConstants.COLLECTION,
                                                {"last_check":
                                                     {"$lte":last_update_limit}})]
        # Video 101

    def save_to_mongo(self):
        Database.insert(AlertConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()  # This step will update the price w/ the latest one
        self.last_check = datetime.datetime.utcnow()  # Save the time of latest update
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.price < self.price_limit:
            self.send()
