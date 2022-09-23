from api.service.keywords import KeywordsService

class KeywordsController:
    def choose_keywords(self):
        kw = KeywordsService()
        result = kw.choose_keywords()
        return result

    def update_dict(self, data):
        kw = KeywordsService()
        result = kw.update_dict(data)
        return result

    def update_stop(self, data):
        kw = KeywordsService()
        result = kw.update_stop(data)
        return result