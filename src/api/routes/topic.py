from flask import Blueprint, request, jsonify
from api.controller.topic import TopicController
from api.utils.responses import response_with
from api.utils import responses as resp

topic_routes = Blueprint("topic_routes", __name__)

@topic_routes.route('/', methods=['GET'])
def get_topic_list():
    topic = TopicController()
    result = topic.get_topic_list()
    return response_with(resp.SUCCESS_200, value={"result": result})

@topic_routes.route('/find_similar', methods=['POST'])
def find_similar():
    if request.method == 'POST':
        print(request)
        json_data = request.json
        print(json_data)
        topic = TopicController()
        result = topic.find_similar(json_data)
        return response_with(resp.SUCCESS_200, value={"result": result})

@topic_routes.route('/weixin_similar', methods=['GET'])
def find_weixin_similar():
    topic = TopicController()
    result = topic.find_weixin_similar()
    return response_with(resp.SUCCESS_200, value={"result": result})


@topic_routes.route('/weibo_similar', methods=['GET'])
def find_weibo_hot_similar():
    topic = TopicController()
    result = topic.find_weibo_hot_similar()
    return response_with(resp.SUCCESS_200, value={"result": result})

@topic_routes.route('/top_similar', methods=['GET'])
def find_top_similar():
    topic = TopicController()
    result = topic.find_top_similar()
    return response_with(resp.SUCCESS_200, value={"result": result})
