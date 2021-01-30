from mongoengine import *

connect("search-engine")


class Document(DynamicDocument):
    hash = StringField()
    text = StringField()
    words = ListField(StringField())
    meta = {
        'collection': 'documents'
    }


class Word(DynamicDocument):
    text = StringField()
    documents = ListField(ReferenceField(Document))

    meta = {
        'collection': 'words'
    }
