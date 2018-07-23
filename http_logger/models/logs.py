from mongoengine import *

class Log(Document):
    content = StringField(required=True)