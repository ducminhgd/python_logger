from mongoengine import *

class MongoDbLog(Document):
    log_content = StringField(required=True)