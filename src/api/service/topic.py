import hanlp

from api.model.topic import PushTopic
from api.model.topic import PushTopicSchema
from api.model.weibo import Weibo
from api.model.douyin import Douyin
from api.model.baidu import Baidu
from api.model.sina import Sina
from api.model.netease import Netease
from api.model.tencent import Tencent
from api.model.toutiao import Toutiao
from api.model.push import PushWeixinArticlesPool
from api.model.topic import PushTopic
import api.utils.constants as cons
import time
import pymongo
import json


class TopicService:
    now_time = int(time.time())
    time_limit = now_time - cons.PARSE_TIME
    time_limit_7 = now_time - cons.PARSE_TIME_WEEK
    all_data = None

    def __init__(self):
        print("==== init ====")
        self.all_data = self.select_all_data()
        print("------共有下列条文章可供对比--------")
        print(len(self.all_data))
        print("--------------------------------")

    def get_topic_list(self):
        fetched = PushTopic.query.all()
        for f in fetched:
            print(f.topic_title)
            print(json.loads(f.topic_items))
        topics_schema = PushTopicSchema(many=True)
        topics = topics_schema.dump(fetched)
        return topics

    def find_top_similar(self):
        top_list = self.get_local_in_top_all()
        print('需查询对比的热搜数：')
        print(len(top_list))
        for top in top_list:
            print('parse top:')
            print(top)
            result = self.find_similar(top)
        return True

    def find_weibo_hot_similar(self):
        weibo_list = self.get_local_in_hot('weibo')
        weibos = self.choose_weibo_by_hot_num(weibo_list, cons.WEIBO_NUM_TO_PARSE_TOPIC)
        print('需查询对比的微博数：')
        print(len(weibos))
        for weibo in weibos:
            print('parse weibo:')
            print(weibo)
            result = self.find_similar(weibo)
        return True
    
    def choose_weibo_by_hot_num(self, weibo_list, limit):
        new_weibo_list = sorted(weibo_list, key=lambda x: x['hot_num'], reverse=True)
        return new_weibo_list[:limit]

    def select_all_data(self):
        top_data = self.get_local_in_top_all()
        hot_data = self.get_local_in_hot_all()
        weixin_data = self.get_local_in_weixin()
        all_data = top_data + hot_data + weixin_data
        return all_data

    def find_similar(self, data):
        now = int(time.time())
        # 先判断最新请求的data是否属于已经存在的话题
        topic_old_dict = self.is_in_topics(data)

        print("==================topic_old====================")
        print(topic_old_dict)

        # 如果话题存在, 而且新增文章没有收录到话题中，则更新数据库
        if topic_old_dict['is_similar'] is True and topic_old_dict['is_in'] is None:
            topic_old = topic_old_dict['topic']
            topic_old.topic_article_num = topic_old.topic_article_num + 1
            new_hot_num = topic_old.topic_hot_num + self.format_hot_num(data['type'], data['hot_num'])
            topic_old.topic_hot_num = new_hot_num
            topic_items_list = json.loads(topic_old.topic_items)
            topic_items_list.append(data)
            topic_old.topic_items = json.dumps(topic_items_list, ensure_ascii=False)
            topic_old.update_new_one_in_a_topic(topic_old.topic_article_num, topic_old.topic_hot_num,
            topic_old.topic_items, now, 0)

        # 如果话题不存在，则搜索数据库，看看有没有类似文章组成话题    
        elif topic_old_dict['is_similar'] is None:
            similar_list = self.count_similar_hanlp(data)
            print('相似文章数：', len(similar_list))
            # 如果有两个以上相似的文章,则新建话题!
            if len(similar_list) >= 2:
                count_res = self.count_topic_hot_num(similar_list)
                topic = {
                    'topic_title': data['title'],
                    'topic_article_num': len(similar_list),
                    'topic_hot_num': count_res['num'],
                    'topic_items': json.dumps(similar_list, ensure_ascii=False),
                    'topic_distribution': str(count_res['distribution']),
                    'add_time': now,
                    'is_cloud': 0,
                    'status': 1
                }
                print('发现话题：')
                print(topic)
                tp = PushTopic(topic['topic_title'], topic['topic_article_num'], topic['topic_hot_num'], topic['topic_items'], topic['topic_distribution'], topic['add_time'], topic['is_cloud'], topic['status'])
                tp.create()
            # 如果没有相似文章组成话题，则直接忽略
            else:
                print("No Similar Article")
                pass
        # 这种情况说明话题已经存在，而且文章已经纳入话题，无需操作！
        else:
            pass
        return True

    def get_local_in_top_all(self):
        final_data = []
        weibo_top_items = Weibo.objects(add_time__gte=self.time_limit, is_local=1)
        # 微博热搜热度值除以3
        for weibo_top_item in weibo_top_items:
            data = {
                "type": "weibo",
                "title": weibo_top_item.title,
                "text": weibo_top_item.text,
                "add_time": weibo_top_item.add_time,
                "hot_num": self.format_top_num("weibo", weibo_top_item.hot_num),
                "img": '',
                "url": ''
            }
            final_data.append(data)
        # 头条热搜热度值除以10
        toutiao_top_items = Toutiao.objects(add_time__gte=self.time_limit, is_local=1)
        for toutiao_top_item in toutiao_top_items:
            data = {
                "type": "toutiao",
                "title": toutiao_top_item.Title,
                "text": '',
                "add_time": toutiao_top_item.add_time,
                "hot_num": self.format_top_num("toutiao", toutiao_top_item.HotValue),
                "img": toutiao_top_item.Image.url,
                "url": toutiao_top_item.Url
            }
            final_data.append(data)
        # 抖音热搜热度值除以40
        douyin_top_items = Douyin.objects( add_time__gte=self.time_limit, is_local=1)
        for douyin_top_item in douyin_top_items:
            data = {
                "type": "douyin",
                "title": douyin_top_item.word,
                "text": '',
                "add_time": douyin_top_item.add_time,
                "hot_num": self.format_top_num("douyin", douyin_top_item.hot_value),
                "img": '',
                "url": ''
            }
            final_data.append(data)
        # 百度热搜热度值除以50
        baidu_top_items = Baidu.objects(add_time__gte=self.time_limit, is_local=1)
        for baidu_top_item in baidu_top_items:
            data = {
                "type": "baidu",
                "title": baidu_top_item.word,
                "text": baidu_top_item.desc,
                "add_time": baidu_top_item.add_time,
                "hot_num": self.format_top_num("baidu", baidu_top_item.hotScore),
                "img": baidu_top_item.img,
                "url": baidu_top_item.url
            }
            final_data.append(data)

        # 新浪热搜热度值除以50
        sina_top_items = Sina.objects(add_time__gte=self.time_limit, is_local=1)
        print(sina_top_items)
        for sina_top_item in sina_top_items:
            data = {
                "type": "sina",
                "title": sina_top_item.title,
                "text": '',
                "add_time": sina_top_item.add_time,
                "hot_num": self.format_top_num("sina", sina_top_item.hotValue),
                "img": '',
                "url": sina_top_item.url
            }
            final_data.append(data)

        # 网易热搜热度值除以50
        netease_top_items = Netease.objects(add_time__gte=self.time_limit, is_local=1)
        for netease_top_item in netease_top_items:
            data = {
                "type": "netease",
                "title": netease_top_item.title,
                "text": netease_top_item.text,
                "add_time": netease_top_item.add_time,
                "hot_num": self.format_top_num("netease", netease_top_item.hotScore),
                "img": netease_top_item.img,
                "url": netease_top_item.url
            }
            final_data.append(data)

        # 腾讯热搜热度值除以50
        tencent_top_items = Tencent.objects(add_time__gte=self.time_limit, is_local=1)
        for tencent_top_item in tencent_top_items:
            data = {
                "type": "tencent",
                "title": tencent_top_item.title,
                "text": tencent_top_item.text,
                "add_time": tencent_top_item.add_time,
                "hot_num": self.format_top_num("tencent", tencent_top_item.readCount),
                "img": tencent_top_item.img,
                "url": tencent_top_item.url
            }
            final_data.append(data)

        return final_data

    def get_local_in_hot_all(self):
        hot_name_list = ['weibo', 'sina', 'tianyan']
        all_data = []
        for hn in hot_name_list:
            res_list = self.get_local_in_hot(hn)
            for res in res_list:
                all_data.append(res)
        return all_data

    def get_local_in_hot(self, db_name):
        final_data = []
        client = pymongo.MongoClient(host='10.168.1.100',port=27017)
        db = client['hot']
        collections = db[db_name]
        print(self.time_limit)
        results = collections.find({'add_time': {'$gt': self.time_limit}})
        if db_name == 'weibo':
            for weibo_hot_item in results:
                data = {
                    "type": "weibo",
                    "title": weibo_hot_item['title'],
                    "text": weibo_hot_item['text'],
                    "add_time": weibo_hot_item['add_time'],
                    "hot_num": self.format_hot_num("weibo", weibo_hot_item['hot_num']),
                    "img": '',
                    "url": ''
                }
                final_data.append(data)

        if db_name == 'sina':
            for sina_hot_item in results:
                data = {
                    "type": "sina",
                    "title": sina_hot_item['title'],
                    "text": '',
                    "add_time": sina_hot_item['add_time'],
                    "hot_num": self.format_hot_num("sina", sina_hot_item['hotValue']),
                    "img": '',
                    "url": sina_hot_item['url']
                }
                final_data.append(data)

        if db_name == 'tianyan':
            for tianyan_hot_item in results:
                data = {
                    "type": "tianyan",
                    "title": tianyan_hot_item['title'],
                    "text": '',
                    "add_time": tianyan_hot_item['add_time'],
                    "hot_num": self.format_hot_num("tianyan", tianyan_hot_item['news_views']),
                    "img": tianyan_hot_item['img'],
                    "url": tianyan_hot_item['url']
                }
                final_data.append(data)
        client.close()
        return final_data

    def get_local_in_weixin(self):
        final_data = []
        results = PushWeixinArticlesPool.query.filter(PushWeixinArticlesPool.push_time > self.time_limit, PushWeixinArticlesPool.is_local == 1).all()
        for weixin_item in results:
            data = {
                "type": "weixin",
                "title": weixin_item.biz_name + ': ' + weixin_item.title,
                "text": '',
                "add_time": weixin_item.push_time,
                "hot_num": int(weixin_item.read_num),
                "img": '',
                "url": weixin_item.url
            }
            final_data.append(data)
        return final_data


    def count_similar_hanlp(self, seed_data):
        title = seed_data['title']
        final_list = []
        all_data_list = self.all_data

        hanlp.pretrained.sts.ALL  # 语种见名称最后一个字段或相应语料库
        sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)

        for data in all_data_list:
            res = sts([
                (title, data['title'])
            ])
            if res[0] > cons.HANLP_SIMILAR_LIMIT:
                data['similar'] = res[0]
                final_list.append(data)
        return final_list

    def count_topic_hot_num(self, topic_data):
        total = 0
        distribution = {}
        for data in topic_data:
            if data['type'] not in distribution:
                distribution[data['type']] = 1
            else:
                distribution[data['type']] = distribution[data['type']] + 1
            total = total + data['hot_num']
        return {'num': total, 'distribution': distribution}

    def format_top_num(self, type, hot_num):
        base = 1
        if type == "weibo":
            base = cons.WEIBO_TOP_RATE
        elif type == "toutiao":
            base = cons.TOUTIAO_TOP_RATE
        elif type == "douyin":
            base = cons.DOUYIN_TOP_RATE
        elif type == "baidu":
            base = cons.BAIDU_TOP_RATE
        elif type == "sina":
            base = cons.SINA_TOP_RATE
        elif type == "tencent":
            base = cons.TENCENT_TOP_RATE
        elif type == "netease":
            base = cons.NETEASE_TOP_RATE
        else:
            pass
        changed_hot_num = int(int(hot_num) / base)
        return changed_hot_num

    def format_hot_num(self, type, hot_num):
        base = 1
        if type == "weibo":
            base = cons.WEIBO_HOT_RATE
        elif type == "sina":
            base = cons.SINA_HOT_RATE
        elif type == "tianyan":
            base = cons.TIANYAN_HOT_RATE
        else:
            pass
        changed_hot_num = int(int(hot_num) / base)
        return changed_hot_num

    def is_in_topics(self, data):
        # 取出一周内的话题
        results = PushTopic.query.filter(PushTopic.add_time > self.time_limit_7).all()

        hanlp.pretrained.sts.ALL  # 语种见名称最后一个字段或相应语料库
        sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)

        for topic in results:
            print(topic)
            res = sts([(topic.topic_title, data['title'])])
            print(res)
            if res[0] > cons.HANLP_SIMILAR_LIMIT:
                items = json.loads(topic.topic_items)
                for item in items:
                    print(item)
                    # 如果以下几项均一致，说明文章已经被收录到专题中，无需再次添加
                    if data['title'] == item['title'] and data['type'] == item['type'] and data['url'] == item['url']:
                        return {'is_similar': True, 'is_in': True, 'topic': topic}
                # 如果文章名属于话题名，但并未收入话题，则返回当前话题
                return {'is_similar': True, 'is_in': None, 'topic': topic}
        # 如果啥事没发生，说明新增文章不属于任何一个话题，可返回进入搜索判断新增程序
        return {'is_similar': None, 'is_in': None, 'topic': None}

        

