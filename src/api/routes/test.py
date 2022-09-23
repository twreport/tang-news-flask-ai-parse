from flask import Blueprint, request, jsonify
from api.controller.test import TestController
from api.utils.responses import response_with
from api.utils import responses as resp

test_routes = Blueprint("test_routes", __name__)

@test_routes.route('/', methods=['GET'])
def get_test_list():
    test = TestController()
    result = test.get_test_list()
    return response_with(resp.SUCCESS_200, value={"result": result})

@test_routes.route('/find_similar', methods=['POST'])
def find_similar():
    if request.method == 'POST':
        print(request)
        json_data = request.json
        print(json_data)
        test = TestController()
        result = test.find_similar(json_data)
        return response_with(resp.SUCCESS_200, value={"result": result})

@test_routes.route('/choose_keywords', methods=['GET'])
def choose_keywords():
    test = TestController()
    result = test.choose_keywords()
    return response_with(resp.SUCCESS_200, value={"result": result})



@test_routes.route('/status', methods=['GET'])
def check_status():
    test = TestController()
    result = test.check_status()
    return response_with(resp.SUCCESS_200, value={"result": result})
    
