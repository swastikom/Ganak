from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField, StringField, EmailField, IntField, DateTimeField, ObjectIdField
from bson import ObjectId

# Define the Inputs embedded document
class Inputs(EmbeddedDocument):
    input = StringField()

# Define the Outputs embedded document
class Outputs(EmbeddedDocument):
    output = StringField()

# Define the Contexts embedded document
class Contexts(EmbeddedDocument):
    inputs = EmbeddedDocumentField(Inputs)
    outputs = EmbeddedDocumentField(Outputs)

# Define the ChatData embedded document
class ChatData(EmbeddedDocument):
    id = ObjectIdField(default=ObjectId, primary_key=True)   
    digon = StringField()
    improvements = StringField()
    contexts = EmbeddedDocumentListField(Contexts)

# Define the User document
class User(Document):
    firstname = StringField()
    secondname = StringField()
    email = EmailField(required=True)
    password = StringField()
    age = IntField()
    address = StringField()
    gender = StringField()
    otp = StringField()
    createdAt = DateTimeField()
    updatedAt = DateTimeField()
    chat_data = EmbeddedDocumentListField(ChatData)
    meta = {
        'collection': 'users'
    }
