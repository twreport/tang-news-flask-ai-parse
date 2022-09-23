# coding:utf-8
from main import app as application

if __name__ == "__main__":
    application.run(port=5001, host="0.0.0.0", use_reloader=False)
