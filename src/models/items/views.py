from flask import Blueprint

item_blueprint = Blueprint('items', __name__)


@item_blueprint.route('/item/<string:name>')
def item_page():
    pass

# remove load_an_item
@item_blueprint.route('/load')
def load_an_item():
    """

    :return:
    """
    pass