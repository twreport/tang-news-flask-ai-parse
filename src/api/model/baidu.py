import mongoengine as me

class Logs(me.EmbeddedDocument):
    update_time = me.IntField(required=True)
    hot_num = me.IntField(required=True)

class Baidu(me.Document):
    _id = me.StringField(required=True, max_length=200)
    appUrl = me.StringField(required=True)
    desc = me.StringField(required=True)
    hotChange = me.StringField(required=True)
    hotTag = me.StringField(required=True)
    hotScore = me.StringField(required=True)
    img = me.StringField(required=True)
    index = me.IntField(required=True)
    query = me.StringField(required=True)
    rawUrl = me.StringField(required=True)
    url = me.StringField(required=True)
    word = me.StringField(required=True)
    add_time = me.IntField(required=True)
    hot_num = me.IntField(required=True)
    is_local = me.IntField(required=False)
    history = me.ListField(me.EmbeddedDocumentField(Logs), required=False)
    status = me.IntField(required=False)

