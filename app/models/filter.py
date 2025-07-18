import mongoengine as me

class Filter(me.Document):
    """
    Filtro model for MongoDB.
    """
    user_id = me.StringField(required=True, unique=True)
    filters = me.DictField(field=me.ListField(me.StringField()), required=True)


    meta = {'collection': 'filters'}