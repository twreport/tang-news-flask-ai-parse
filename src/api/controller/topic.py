from api.service.topic import TopicService
from api.model.push import PushWeixinArticlesPool
import api.utils.constants as cons
import time

class TopicController:
    now_time = int(time.time())
    time_limit = now_time - cons.PARSE_TIME
    def get_topic_list(self):
        topic = TopicService()
        result = topic.get_topic_list()
        return result

    def find_similar(self, data):
        topic = TopicService()
        result = topic.find_similar(data)
        return result

    def find_weixin_similar(self):
        print("Start Weixin Similar Finder!")
        weixin_num = cons.WEIXIN_NUM_TO_PARSE_TOPIC
        articles = PushWeixinArticlesPool.query.filter(PushWeixinArticlesPool.push_time > self.time_limit).order_by(PushWeixinArticlesPool.read_num.desc()).limit(weixin_num).all()
        topic = TopicService()
        for a in articles:
            data = {
                "type": "weixin",
                "title": a.title,
                "text": '',
                "add_time": a.push_time,
                "hot_num": int(a.read_num),
                "img": '',
                "url": a.url
            }
            topic.find_similar(data)
        return True

    def find_top_similar(self):
        topic = TopicService()
        result = topic.find_top_similar()
        return result
    
    def find_weibo_hot_similar(self):
        topic = TopicService()
        result = topic.find_weibo_hot_similar()
        return result