from api.utils.database import mysql_db
from api.utils.database import ma

class PushKeywords (mysql_db.Model):
    __tablename__ = 'push_keywords'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    word = mysql_db.Column(mysql_db.String(45))
    hot_num = mysql_db.Column(mysql_db.Integer)
    add_time = mysql_db.Column(mysql_db.Integer)
    is_cloud = mysql_db.Column(mysql_db.Integer)
    status = mysql_db.Column(mysql_db.Integer)

    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self

    def __init__(self, word, hot_num, add_time, is_cloud, status):
        self.word = word
        self.hot_num = hot_num
        self.add_time = add_time
        self.is_cloud = is_cloud
        self.status = status

    def __repr__(self):
        return '<Keywords %d>' % self.id + '|' + 'word %s' % self.word

class PushKeywordsSchema (ma.SQLAlchemySchema):
    class Meta:
        model = PushKeywords
    id = ma.auto_field()
    word = ma.auto_field()
    hot_num = ma.auto_field()
    add_time = ma.auto_field()
    is_cloud = ma.auto_field()
    status = ma.auto_field()