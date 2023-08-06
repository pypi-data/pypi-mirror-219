from scinode.core.executor import Executor


class ScinodeIf(Executor):
    """ """

    def run(self):
        """ """
        print("    Run If node")
        from scinode.orm.db_nodetree import DBNodeTree
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        nodetree_uuid = self.dbdata["metadata"]["nodetree_uuid"]
        nt = DBNodeTree(uuid=nodetree_uuid)
        ctrl_links = nt.record["ctrl_links"]
        if self.kwargs["input"]:
            print("update ctrl_links")
            for index, link in enumerate(ctrl_links):
                if link["from_node"] == self.name and link["from_socket"] == "true":
                    msgs = f"{self.nodetree_uuid},ctrl_link,{index}:action:ON"
                    send_message_to_queue(broker_queue_name, msgs)
                elif link["from_node"] == self.name and link["from_socket"] == "false":
                    msgs = f"{self.nodetree_uuid},ctrl_link,{index}:action:OFF"
                    send_message_to_queue(broker_queue_name, msgs)
        else:
            for index, link in enumerate(ctrl_links):
                if link["from_node"] == self.name and link["from_socket"] == "true":
                    msgs = f"{self.nodetree_uuid},ctrl_link,{index}:action:OFF"
                    send_message_to_queue(broker_queue_name, msgs)
                elif link["from_node"] == self.name and link["from_socket"] == "false":
                    msgs = f"{self.nodetree_uuid},ctrl_link,{index}:action:ON"
                    send_message_to_queue(broker_queue_name, msgs)
        this_results = self.kwargs["input"]
        return this_results
