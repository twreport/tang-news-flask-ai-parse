# from pyhanlp import *
import jieba
import jieba.analyse
from api.service.topic import TopicService
from api.model.keywords import PushKeywords
from api.model.keywords import PushKeywordsSchema
import time

class KeywordsService:
    file_name = '/var/www/html/flask_servers/ai_parse/src/api/utils/dict.txt'
    stop_name = '/var/www/html/flask_servers/ai_parse/src/api/utils/stop_words.txt'
    stop = None

    def __init__(self):
        jieba.load_userdict(self.file_name)
        # 加载停用词表
        self.stop = [line.strip() for line in open(self.stop_name).readlines()]

    # 关键词提取
    def extractKeyword(self, document, keyword_num=5):
        # result = HanLP.extractKeyword(document, keyword_num)
        # result = HanLP.segment(document)
        # result = jieba.analyse.textrank(document, topK=keyword_num, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
        result = jieba.analyse.textrank(document, topK=keyword_num, withWeight=False, allowPOS=('ns', 'n', 'vn'))
        result = self.del_stop(result)
        return result

    def del_stop(self, words_list):
        result_list = []
        for word in words_list:
            if word not in self.stop:
                result_list.append(word)
        return result_list

    def select_list_from_all_data_by_keyword(self, title, data_list):
        result_list = []
        title_keywords = self.extractKeyword(title, 5)
        print(title_keywords)
        for title_keyword in title_keywords:
            for data in data_list:
                if title_keyword in data['title'] and data not in result_list:
                    result_list.append(data)
        return result_list
    
    def choose_keywords(self):
        topic = TopicService()
        all_articles = topic.select_all_data()
        all_title_keywords = []
        for data in all_articles:
            title_keywords = self.extractKeyword(data['title'], 5)
            for word in title_keywords:
                all_title_keywords.append(word)
        list_ordered = self.order_list(all_title_keywords)
        now_time = int(time.time())
        for word_item in list_ordered[:20]:
            kw = PushKeywords(word_item[0], word_item[1], now_time, 0, 1)
            kw.create()
        return True
    
    def order_list(self, words_list):
        result = dict()
        for a in set(words_list):
            result[a] = words_list.count(a)
        print(result)
        sorted_dict = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return sorted_dict

    def update_dict(self, data):
        file_url = '/var/www/html/flask_servers/ai_parse/src/api/utils/dict.txt'
        with open(file_url, mode='a', encoding='utf8') as tf3:
            data = '\n' + data
            tf3.write(data)
        return True

    def update_stop(self, data):
        file_url = '/var/www/html/flask_servers/ai_parse/src/api/utils/stop_words.txt'
        with open(file_url, mode='a', encoding='utf8') as tf3:
            data = '\n' + data
            tf3.write(data)
        return True


