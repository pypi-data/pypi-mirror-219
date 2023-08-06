from scinode.core.executor import Executor


class ScinodeFor(Executor):
    """ """

    def run(self):
        """ """
        print("    Run For node")
        from scinode.orm.db_nodetree import DBNodeTree
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        nodetree_uuid = self.dbdata["metadata"]["nodetree_uuid"]
        nt = DBNodeTree(uuid=nodetree_uuid)
        ctrl_links = nt.record["ctrl_links"]
        n = len(self.kwargs["input"])
        counter = nt.record["nodes"][self.name]["counter"]
        if counter <= n - 1:
            print("Run Loop")
            for index, link in enumerate(ctrl_links):
                if link["from_node"] == self.name and link["from_socket"] == "loop":
                    msgs = f"{self.nodetree_uuid},ctrl_link,{index}:action:ON"
                    send_message_to_queue(broker_queue_name, msgs)
            this_results = self.kwargs["input"][counter]
        else:
            print("Exit Loop")
            for index, link in enumerate(ctrl_links):
                if link["from_node"] == self.name and link["from_socket"] == "loop":
                    msgs = f"{self.nodetree_uuid},ctrl_link,{index}:action:OFF"
                    send_message_to_queue(broker_queue_name, msgs)
                if link["from_node"] == self.name and link["from_socket"] == "jump":
                    msgs = f"{self.nodetree_uuid},ctrl_link,{index}:action:ON"
                    send_message_to_queue(broker_queue_name, msgs)
            this_results = None
        self.update_counter()
        return this_results
