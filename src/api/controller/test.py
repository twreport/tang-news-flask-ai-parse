import hanlp
from api.service.keywords import KeywordsService

class TestController:
    def get_test_list(self):
        print('in hanlp')
        # sentence = "异地贷款需要具备哪些条件"
        # # 返回一个列表，可以获取分词和它的词性
        # words = HanLP.segment(sentence)
        # for term in words:
        #     print(term.word, term.nature)
        hanlp.pretrained.sts.ALL  # 语种见名称最后一个字段或相应语料库
        sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)
        res = sts([
            ('看图猜一电影名', '看图猜电影'),
            ('赵立坚点赞贵州乡村篮球赛', '贵州乡村篮球赛被外交天团点赞'),
            ('被外交天团接连点赞的贵州美景', '“外交天团”接连点赞的贵州这处美景，不允许你还没看过'),
            ('赵立坚点赞贵州乡村篮球赛','台江县教育和科技局关于暑期校外培训告知书')
        ])
        print(res)
        query = 'test func'
        return query

    def choose_keywords(self):
        kw = KeywordsService()
        result = kw.choose_keywords()
        return result

    def check_status(self):
        return 'Flask Service AI_parse is OK!'


