import mongoengine as me

class Logs(me.EmbeddedDocument):
    update_time = me.IntField(required=True)
    hot_num = me.IntField(required=True)

class Urls(me.EmbeddedDocument):
    url = me.StringField(required=False)

class Images(me.EmbeddedDocument):
    uri = me.StringField(required=False)
    url = me.StringField(required=False)
    height = me.IntField(required=False)
    width = me.IntField(required=False)
    image_type = me.IntField(required=False)
    url_list = me.ListField(me.EmbeddedDocumentField(Urls), required=False)

class Toutiao(me.Document):
    _id = me.StringField(required=True, max_length=200)
    ClusterId = me.StringField(required=True)
    Title = me.StringField(required=True)
    Label = me.StringField(required=True)
    Url = me.StringField(required=True)
    ClusterIdStr = me.StringField(required=True)
    ClusterType = me.IntField(required=True)
    Image = me.EmbeddedDocumentField(Images)
    add_time = me.IntField(required=True)
    HotValue = me.IntField(required=True)
    is_local = me.IntField(required=False)
    history = me.ListField(me.EmbeddedDocumentField(Logs), required=False)
    status = me.IntField(required=False)

