from api.utils.database import mysql_db
from api.utils.database import ma

class PushTopic (mysql_db.Model):
    __tablename__ = 'push_topic'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    topic_title = mysql_db.Column(mysql_db.String(200))
    topic_article_num = mysql_db.Column(mysql_db.Integer)
    topic_hot_num = mysql_db.Column(mysql_db.Integer)
    topic_items = mysql_db.Column(mysql_db.Text)
    topic_distribution = mysql_db.Column(mysql_db.String(2000))
    add_time = mysql_db.Column(mysql_db.Integer)
    is_cloud = mysql_db.Column(mysql_db.Integer)
    status = mysql_db.Column(mysql_db.Integer)
   
    def create(self):
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self

    def update_new_one_in_a_topic(self, topic_article_num, topic_hot_num, topic_items, add_time, is_cloud):
        self.topic_article_num = topic_article_num
        self.topic_hot_num = topic_hot_num
        self.topic_items = topic_items
        # 如果有新文章加入话题，则更新add_time
        self.add_time = add_time
        self.is_cloud = is_cloud
        mysql_db.session.commit()

    def __init__(self, topic_title, topic_article_num, topic_hot_num, topic_items, topic_distribution, add_time, is_cloud, status):
        self.topic_title = topic_title
        self.topic_article_num = topic_article_num
        self.topic_hot_num = topic_hot_num
        self.topic_items = topic_items
        self.topic_distribution = topic_distribution
        self.add_time = add_time
        self.is_cloud = is_cloud
        self.status = status

    def __repr__(self):
        return '<Topic %d>' % self.id + '|' + 'title %s' % self.topic_title

class PushTopicSchema (ma.SQLAlchemySchema):
    class Meta:
        model = PushTopic
    id = ma.auto_field()
    topic_title = ma.auto_field()
    topic_article_num = ma.auto_field()
    topic_hot_num = ma.auto_field()
    topic_items = ma.auto_field()
    topic_distribution = ma.auto_field()
    add_time = ma.auto_field()
    is_cloud = ma.auto_field()
    status = ma.auto_field()