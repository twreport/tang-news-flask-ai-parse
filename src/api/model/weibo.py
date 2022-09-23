import mongoengine as me

class Logs(me.EmbeddedDocument):
    update_time = me.IntField(required=True)
    hot_num = me.IntField(required=True)

class Weibo(me.Document):
    _id = me.StringField(required=True, max_length=200)
    title = me.StringField(required=True)
    text = me.StringField(required=True)
    add_time = me.IntField(required=True)
    hot_num = me.IntField(required=True)
    is_local = me.IntField(required=False)
    history = me.ListField(me.EmbeddedDocumentField(Logs), required=False)
    status = me.IntField(required=False)

