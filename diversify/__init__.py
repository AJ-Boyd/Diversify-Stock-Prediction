"""
auth: AJ Boyd
date: 9/27/24
desc: hackathon fintech project
file: __init__.py
"""
from flask import Flask

def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hacker no hacking!"
    
    from .views import views
    # reg blueprint
    app.register_blueprint(views, url_prefix='/')
    return app