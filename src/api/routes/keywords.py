from flask import Blueprint, request, jsonify
from api.controller.keywords import KeywordsController
from api.utils.responses import response_with
from api.utils import responses as resp

keywords_routes = Blueprint("keywords_routes", __name__)


@keywords_routes.route('/parse', methods=['GET'])
def choose_keywords():
    keywords = KeywordsController()
    result = keywords.choose_keywords()
    return response_with(resp.SUCCESS_200, value={"result": result})

@keywords_routes.route('/dict', methods=['POST'])
def update_dict():
    if request.method == 'POST':
        word = request.form['data']
        keywords = KeywordsController()
        result = keywords.update_dict(word)
        return response_with(resp.SUCCESS_200, value={"result": result})

@keywords_routes.route('/stop', methods=['POST'])
def update_stop():
    if request.method == 'POST':
        word = request.form['data']
        keywords = KeywordsController()
        result = keywords.update_stop(word)
        return response_with(resp.SUCCESS_200, value={"result": result})
