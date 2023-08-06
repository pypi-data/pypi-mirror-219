from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    FloatField,
    IntField,
    BooleanField,
    DateTimeField,
    ListField,
    MapField,
    ObjectIdField,
    BinaryField,
    EmbeddedDocumentField,
    signals,
)
from scinode.common.log import logging

logger = logging.getLogger("orm")


class Scheduler(EmbeddedDocument):
    type = StringField()
    code = StringField()
    pre_code = StringField()
    post_code = StringField()


class Meta(EmbeddedDocument):
    worker_name = StringField(max_length=50)
    computer = StringField(max_length=50)
    identifier = StringField(max_length=50)
    catalog = StringField(required=True, max_length=50)
    node_type = StringField(max_length=50)
    nodetree_worker = StringField(max_length=50)
    nodetree_uuid = StringField(max_length=50)
    ref_uuid = StringField(max_length=50)
    copy_uuid = StringField(max_length=50)
    platform = StringField(max_length=50)
    scatter_node = StringField(max_length=50)
    copied_from = StringField(max_length=50)
    scattered_from = StringField(max_length=50)
    scattered_label = StringField(max_length=50)
    counter = IntField(min_value=0)
    args = ListField()
    kwargs = ListField()
    group_properties = ListField(ListField())
    group_inputs = ListField(ListField())
    group_outputs = ListField(ListField())
    hash = StringField(max_length=100)
    register_path = StringField()


class Executor(EmbeddedDocument):
    path = StringField()
    name = StringField(max_length=50)
    type = StringField(max_length=50)
    is_pickle = BooleanField()


class Link(EmbeddedDocument):
    from_node = StringField(max_length=50)
    from_socket = StringField(max_length=50)
    from_socket_uuid = StringField(max_length=50)
    to_node = StringField(max_length=50)
    to_socket = StringField(max_length=50)
    to_socket_uuid = StringField(max_length=50)
    state = BooleanField()


class Socket(EmbeddedDocument):
    name = StringField(max_length=50)
    type = StringField(max_length=50)
    node_uuid = StringField(max_length=50)
    identifier = StringField(max_length=50)
    uuid = StringField(max_length=50)
    link_limit = IntField(min_value=0)
    serialize = EmbeddedDocumentField(Executor)
    deserialize = EmbeddedDocumentField(Executor)
    links = ListField(EmbeddedDocumentField(Link))
    in_object_store = BooleanField()


class PropertyMeta(EmbeddedDocument):
    default = FloatField(max_length=50, required=False)
    size = IntField(required=False)


class Property(EmbeddedDocument):
    name = StringField(max_length=50)
    identifier = StringField(max_length=50)
    type = StringField(max_length=50)
    value = StringField()
    serialize = EmbeddedDocumentField(Executor)
    deserialize = EmbeddedDocumentField(Executor)
    hash = StringField(max_length=100)
    metadata = EmbeddedDocumentField(PropertyMeta)


class Node(Document):
    meta = {"collection": "node"}

    uuid = StringField(required=True)
    name = StringField(required=True, max_length=50)
    state = StringField(max_length=50)
    action = StringField(max_length=50)
    version = StringField(max_length=50)
    lastUpdate = DateTimeField()
    created = DateTimeField()
    description = StringField()
    log = StringField()
    error = StringField()
    index = IntField()
    inner_id = IntField(primary_key=True)
    metadata = EmbeddedDocumentField(Meta)
    executor = EmbeddedDocumentField(Executor)
    scheduler = EmbeddedDocumentField(Scheduler, required=False)
    inputs = ListField(EmbeddedDocumentField(Socket))
    outputs = ListField(EmbeddedDocumentField(Socket))
    ctrl_inputs = ListField(EmbeddedDocumentField(Socket))
    ctrl_outputs = ListField(EmbeddedDocumentField(Socket))
    properties = MapField(EmbeddedDocumentField(Property))
    position = ListField()
    hash = StringField(max_length=100)
    node_class = BinaryField()

    def _init__(self, uuid, name):
        self.uuid = (uuid,)
        self.name = name

    @classmethod
    def pre_init(cls, sender, document, **kwargs):
        """Pre init hook.
        Generate uuid for the node.
        """
        logging.debug("Pre Init: %s" % document.name)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """Pre save hook.
        Reset the child nodes.
        """
        logging.debug("Pre Save: %s" % document.name)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        logging.debug("Post Save: %s" % document.name)
        if "created" in kwargs:
            if kwargs["created"]:
                logging.debug("Created")
            else:
                logging.debug("Updated")

    @classmethod
    def pre_bulk_insert(cls, sender, document, **kwargs):
        """Pre save hook.
        Reset the child nodes.
        """
        logging.debug("Pre Save: %s" % document.name)


signals.pre_save.connect(Node.pre_init, sender=Node)
signals.pre_save.connect(Node.pre_save, sender=Node)
signals.post_save.connect(Node.post_save, sender=Node)

if __name__ == "__main__":
    from mongoengine import connect

    connect("scinode_db", host="mongodb://localhost:27017/")
    for n in Node.objects:
        print(n.name)
    n = Node.objects[0]
    n.name += "test"
    n.save()
    print(n.name)
