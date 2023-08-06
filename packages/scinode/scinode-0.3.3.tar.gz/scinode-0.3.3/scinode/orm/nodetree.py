from mongoengine import (
    connect,
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    BooleanField,
    DateTimeField,
    ListField,
    MapField,
    EmbeddedDocumentField,
)


class Meta(EmbeddedDocument):
    worker_name = StringField(max_length=50)
    type = StringField(max_length=50)
    parent = StringField(max_length=50)
    parent_node = StringField(max_length=50)
    platform = StringField(max_length=50)
    scatter_node = StringField(max_length=50)
    scattered_label = StringField(max_length=50)
    group_properties = ListField(ListField())
    group_inputs = ListField(ListField())
    group_outputs = ListField(ListField())


class Link(EmbeddedDocument):
    from_node = StringField(max_length=50)
    from_socket = StringField(max_length=50)
    from_socket_uuid = StringField(max_length=50)
    to_node = StringField(max_length=50)
    to_socket = StringField(max_length=50)
    to_socket_uuid = StringField(max_length=50)
    state = BooleanField()


class Node(EmbeddedDocument):
    action = StringField(max_length=50)
    state = StringField(max_length=50)
    name = StringField(max_length=50)
    worker = StringField(max_length=50)
    node_type = StringField(max_length=50)
    uuid = StringField(max_length=50)
    identifier = StringField(max_length=50)
    scatter = MapField(StringField(max_length=50))
    register_path = StringField()
    counter = IntField(min_value=0)


class Connectivity(EmbeddedDocument):
    child_node = MapField(ListField())
    control_node = MapField(ListField())
    input_node = MapField(MapField(ListField()))
    output_node = MapField(MapField(ListField()))
    ctrl_input_link = MapField(MapField(ListField()))
    ctrl_input_node = MapField(MapField(ListField()))
    ctrl_output_link = MapField(MapField(ListField()))
    ctrl_output_node = MapField(MapField(ListField()))


class NodeTree(Document):
    meta = {"collection": "nodetree"}

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
    links = ListField(EmbeddedDocumentField(Link))
    ctrl_links = ListField(EmbeddedDocumentField(Link))
    metadata = EmbeddedDocumentField(Meta)
    connectivity = EmbeddedDocumentField(Connectivity)
    nodes = MapField(EmbeddedDocumentField(Node), required=True)

    def _init__(self, uuid, name):
        self.uuid = (uuid,)
        self.name = name


if __name__ == "__main__":
    from scinode.orm.nodetree import NodeTree

    connect("scinode_db", host="mongodb://localhost:27017/")
    for nt in NodeTree.objects:
        print(nt.name)
    nt = NodeTree.objects[0]
    nt.name += "test"
    nt.save()
