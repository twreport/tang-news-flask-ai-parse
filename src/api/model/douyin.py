import mongoengine as me

class Logs(me.EmbeddedDocument):
    update_time = me.IntField(required=True)
    hot_num = me.IntField(required=True)

class Douyin(me.Document):
    _id = me.StringField(required=True, max_length=200)
    word = me.StringField(required=True)
    group_id = me.StringField(required=True)
    sentence_id = me.StringField(required=True)
    add_time = me.IntField(required=True)
    event_time = me.IntField(required=True)
    sentence_tag = me.IntField(required=True)
    hot_value = me.IntField(required=True)
    position = me.IntField(required=True)
    is_local = me.IntField(required=False)
    history = me.ListField(me.EmbeddedDocumentField(Logs), required=False)
    status = me.IntField(required=False)

