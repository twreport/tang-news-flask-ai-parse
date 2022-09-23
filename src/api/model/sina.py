import mongoengine as me

class Sina(me.Document):
    _id = me.StringField(required=True, max_length=200)
    title = me.StringField(required=True)
    url = me.StringField(required=True)
    hotValue = me.StringField(required=True)
    add_time = me.IntField(required=True)
    update_time = me.IntField(required=True)
    is_local = me.IntField(required=False)
    status = me.IntField(required=False)
    