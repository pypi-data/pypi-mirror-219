from mongoengine import (
    Document,
    StringField,
    IntField,
    ListField,
    BinaryField,
    EmbeddedDocumentField,
)
from scinode.orm.node import Executor, Link


class Data(Document):
    name = StringField(max_length=50)
    index = IntField(min_value=0)
    link_limit = IntField(min_value=0)
    type = StringField(max_length=50)
    hash = StringField(max_length=50)
    node_uuid = StringField(max_length=50)
    identifier = StringField(max_length=50)
    uuid = StringField(max_length=50)
    serialize = EmbeddedDocumentField(Executor)
    deserialize = EmbeddedDocumentField(Executor)
    links = ListField(EmbeddedDocumentField(Link))
    value = BinaryField()
