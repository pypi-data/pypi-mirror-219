"""
"""
from scinode.orm import DBItem
from scinode.engine.node_engine import EngineNode
from scinode.engine.send_to_queue import send_message_to_queue
from scinode.engine.config import broker_queue_name
from scinode.database.client import db_node, scinodedb
import time
from scinode.common.log import logging

logger = logging.getLogger("engine")


class EngineNodeTree(DBItem):
    """EngineNodeTree Class.
    Process the nodetree with the data from the database.
    It can be called by the scheduler or called manually.

    uuid: str
        uuid of the nodetree.

    Example:

    >>> # load nodetree data from database
    >>> query = {"uuid": "your-nodetree-uuid"}
    >>> dbdata = scinodedb["nodetree"].find_one(query)
    >>> nodetree = EngineNodeTree(uuid=dbdata["uuid"])
    >>> nodetree.process()
    """

    db_name: str = "nodetree"

    def __init__(self, uuid=None) -> None:
        """_summary_

        Args:
            uuid (_type_, optional): _description_. Defaults to None.
            dbdata (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(uuid)
        self.record = self.dbdata
        self.name = self.record["name"]

    def update_nodetree_state(self):
        """process the nodetree from database.
        1) analyze_node_state
        2) analyze_nodetree_state
        3) push message
        """
        from scinode.engine.send_to_queue import send_message_to_queue

        try:
            # skip paused nodetree
            if self.record["state"] in ["PAUSED"]:
                return
            # update nodetree state
            state, action = self.analyze_nodetree_state()
            send_message_to_queue(
                broker_queue_name, f"{self.uuid},nodetree,state:{state}"
            )
        except Exception:
            import traceback

            error = traceback.format_exc()
            print(
                "xxxxxxxxxx Failed xxxxxxxxxx\nNode {} failed due to: {}".format(
                    self.name, error
                )
            )
            self.update_db_keys({"state": "FAILED"})
            self.update_db_keys({"action": "NONE"})
            self.update_db_keys({"error": str(error)})

    def apply_nodetree_message(self, msg):
        # print("apply_nodetree_message: ", msg)
        self.write_log(msg + "\n")
        key, value = msg.split(":")
        if key == "action":
            self.apply_nodetree_action(value)
        elif key == "state":
            self.apply_nodetree_state(value)

    def apply_node_message(self, msg):
        self.write_log(msg + "\n")
        # print("apply_node_message: ", msg)
        name, key, value = msg.split(":")
        if key == "action":
            self.apply_node_action(name, value)
        elif key == "state":
            self.apply_node_state(name, value)
        elif key == "scatter":
            self.apply_node_scatter_state(name, value)

    def apply_ctrl_link_message(self, msg):
        self.write_log(msg + "\n")
        # print("apply_ctrl_link_message: ", msg)
        index, key, value = msg.split(":")
        index = int(index)
        if key == "action":
            self.apply_ctrl_link_action(index, value)
        elif key == "state":
            self.apply_ctrl_link_state(index, value)

    def apply_nodetree_state(self, state):
        """Apply state to nodetree"""
        from scinode.engine.send_to_queue import expose_outputs

        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {"state": state}}
        )
        if self.record["metadata"]["parent_node"] != "":
            ndata = scinodedb["node"].find_one(
                {"uuid": self.uuid}, {"name": 1, "metadata": 1}
            )
            if state == "FINISHED":
                print(f"  Nodetree {self.name} is finished.")
                expose_outputs(
                    ndata["metadata"]["worker_name"],
                    ndata["metadata"]["nodetree_uuid"],
                    ndata["name"],
                )
            else:
                msgs = f"{ndata['metadata']['nodetree_uuid']},node,{ndata['name']}:state:{state}"
                send_message_to_queue(broker_queue_name, msgs)

    def apply_nodetree_action(self, action):
        """Apply action to nodetree"""
        tstart = time.time()
        # print(f"Nodetree action: {action}")
        if action.upper() == "UPDATE":
            self.update_nodetree_state()
        elif action.upper() == "LAUNCH":
            self.launch_nodetree()
        elif action.upper() == "PAUSE":
            self.pause_nodetree()
        elif action.upper() == "PLAY":
            self.play_nodetree()
        elif action.upper() == "CANCEL":
            self.cancel_nodetree()
        elif action.upper() == "RESET":
            self.reset_nodetree()
        else:
            print("  Action {} is not supported.".format(action))
        logger.debug("apply_nodetree_action, time: {}".format(time.time() - tstart))

    def apply_node_state(self, name, state):
        """apply action to all nodes"""
        from scinode.database.client import scinodedb
        from scinode.utils.db import write_log

        # update database
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {f"nodes.{name}.state": state}}
        )
        # update tempereary record
        self.record["nodes"][name]["state"] = state
        # run the exit control link for this node
        if state in ["FINISHED", "FAILED", "SKIPPED"]:
            self.run_exit_ctrl_link(name)
            # update all nodes related to this node
            self.update_node_state_for_ref(name, state)
            self.update_node_state_for_scatter(name, state)
            self.check_state_for_output_nodes(name, state)
            self.update_nodetree_state()
        write_log(
            {"metadata.nodetree_uuid": self.uuid, "name": name},
            f"\nstate: {state}\n",
            "node",
        )
        # logger.debug("apply_node_, time: {}".format(time.time() - tstart))

    def apply_node_scatter_state(self, name, value):
        """apply scatter state.

        - update state of the scatter field
        - check the state of the node
        """
        from scinode.database.client import scinodedb
        from scinode.utils.db import write_log

        # update database
        key, state = value.split("#")
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {f"nodes.{name}.scatter.{key}": state}}
        )
        # update tempereary record
        self.record["nodes"][name]["scatter"][key] = state
        self.check_node_state(name)

    def run_exit_ctrl_link(self, name):
        """Run exit control link of the node"""
        print(f"  Run exit control link for node: {name}")
        outputs = self.record["connectivity"]["ctrl_output_link"][name]
        if "exit" in outputs:
            for index in outputs["exit"]:
                self.apply_ctrl_link_action(index, "ON")

    def check_state_for_output_nodes(self, name, state):
        """Find all output nodes and check their state"""
        print(f"  check_state_for_output_nodes: {name}")
        outputs = self.record["connectivity"]["output_node"][name]
        for socket, nodes in outputs.items():
            for node in nodes:
                self.check_node_state(node)

    def update_node_state_for_ref(self, name, state):
        """Find all nodes that reference this node and update their state"""
        from scinode.database.client import scinodedb

        print(f"  update node state for ref node: {name}")
        node_uuid = self.record["nodes"][name]["uuid"]
        child_nodes = scinodedb["node"].find(
            {"metadata.ref_uuid": node_uuid}, {"metadata": 1, "name": 1}
        )
        if child_nodes is not None:
            for child in child_nodes:
                print(f"    update child node: {child['name']}")
                msg = f"{child['metadata']['nodetree_uuid']},node,{child['name']}:state:{state}"
                send_message_to_queue(broker_queue_name, msg)

    def update_node_state_for_scatter(self, name, state):
        """If this node is a scatter node, update the state of the parent node."""
        print(f"  update node state for scattered node: {name}")
        record = scinodedb["node"].find_one(
            {"name": name, "metadata.nodetree_uuid": self.uuid}, {"metadata": 1}
        )
        if record["metadata"]["scattered_from"]:
            parent_node = scinodedb["node"].find_one(
                {"uuid": record["metadata"]["scattered_from"]},
                {"metadata": 1, "name": 1},
            )
            # TODO: update the state of the parent node
            msg = f"{parent_node['metadata']['nodetree_uuid']},node,{name}:scatter:{record['metadata']['scattered_label']}#{state}"
            print(f"push parent: {msg}")
            send_message_to_queue(broker_queue_name, msg)

    def apply_node_action(self, name, action):
        tstart = time.time()
        # print("apply_node_action: ", self.record["nodes"])
        # print(f"{action} {name}")
        print(f"  apply_node_action: {name}, {action}")
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {f"nodes.{name}.action": "NONE"}}
        )
        if action == "CHECK":
            self.check_node_state(name)
        elif action == "LAUNCH":
            self.launch_node(name)
        elif action == "EXPOSE_OUTPUTS":
            self.expose_outputs(name)
        elif action == "PAUSE":
            self.pause_node(name)
        elif action == "PLAY":
            self.play_node(name)
        elif action == "SKIP":
            self.skip_node(name)
        elif action == "RESET":
            self.reset_node(name)
        elif action == "RESET_LAUNCH":
            self.reset_node(name, launch=True)
        elif action == "FINISH":
            # TODO
            # self.record[name]["state"] = "FINISHED"
            pass
        # print("apply_node_action: ", self.record["nodes"])
        logger.debug("apply_node_action, time: {}".format(time.time() - tstart))

    def apply_ctrl_link_action(self, index, action):
        """Apply action to the control link.

        Args:
            index (int): index of the link
            action (str): action on the link
        """
        # tstart = time.time()
        # print("apply_ctrl_link_action: ", self.record["ctrl_links"])
        # print(f"{action} {index}")
        print(f"  apply_ctrl_link_action: {index}, {action}")
        if action == "ON":
            self.switch_on_ctrl_link(index)
        elif action == "OFF":
            self.switch_off_ctrl_link(index)
        else:
            raise ValueError(f"Unknown action: {action}")
        # print("apply_node_action: ", self.record["nodes"])
        # logger.debug("apply_ctrl_link_action, time: {}".format(time.time() - tstart))

    def launch_nodetree(self):
        """Launch nodetree.
        Check all nodes and launch them if they are ready.
        """
        print(f"  Launch nodetree: {self.uuid}")
        # send_message_to_queue(broker_queue_name, f"{self.uuid},nodetree,state:RUNNING")
        self.update_nodetree_state()
        for name in self.record["nodes"]:
            self.check_node_state(name)

    def pause_nodetree(self):
        """Pause nodetree."""
        print(f"  Pause nodetree: {self.uuid}")
        send_message_to_queue(broker_queue_name, f"{self.uuid},nodetree,state:PAUSED")

    def play_nodetree(self):
        """Play nodetree."""
        print(f"Play nodetree: {self.uuid}")
        # send_message_to_queue(broker_queue_name, f"{self.uuid},nodetree,state:RUNNING")
        # check state of all nodes
        for name in self.record["nodes"]:
            self.check_node_state(name)

    def reset_nodetree(self):
        """Reset node and all its child nodes.

        Args:
            name (str): name of the node to be paused
        """
        print(f"  Reset nodetree: {self.uuid}")
        ntdata = scinodedb["nodetree"].find_one({"uuid": self.uuid}, {"nodes": 1})
        for name in ntdata["nodes"]:
            if ntdata["nodes"][name]["node_type"] == "REF":
                continue
            ntdata["nodes"][name]["state"] = "CREATED"
        # print("update_node_state: ", ntdata["nodes"])
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid},
            {"$set": {"state": "CREATED", "nodes": ntdata["nodes"]}},
        )

    def cancel_nodetree(self):
        """Cancel nodetree."""
        print(f"  Cancel nodetree: {self.uuid}")
        # print("update_node_state: ", ntdata["nodes"])
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {"state": "CANCELLED"}}
        )

    def check_node_state(self, name):
        """Check node states.

        - if all input nodes finished, launch node
        - if node is a scatter node, check if all scattered nodes finished
        """
        from scinode.engine.send_to_queue import launch_node

        if self.record["nodes"][name]["node_type"] == "REF":
            return
        if self.record["nodes"][name]["state"] in ["CREATED", "WAITING"]:
            ready = self.check_parent_state(name)
            if ready:
                print(f"    Launch node: {name}")
                self.write_log(f"Lanch node: {name}\n")
                launch_node(self.record["nodes"][name]["worker"], self.uuid, name)
        elif self.record["nodes"][name]["state"] in ["SCATTERED"]:
            state, action = self.check_scattered_state(name)
            if state == "FINISHED":
                msgs = f"{self.uuid},node,{name}:state:FINISHED"
                send_message_to_queue(broker_queue_name, msgs)
            elif state == "FAILED":
                msgs = f"{self.uuid},node,{name}:state:FINISHED"
                send_message_to_queue(broker_queue_name, msgs)

    def launch_node_with_no_input_node(self):
        """launch node with no input node"""
        from scinode.engine.send_to_queue import launch_node

        for name, ndata in self.record["nodes"].items():
            if ndata["node_type"] == "REF":
                continue
            inputs = self.record["connectivity"]["input_node"][name]
            if len(inputs) == 0:
                self.write_log(f"Lanch node: {name}\n")
                launch_node(self.record["nodes"][name]["worker"], self.uuid, name)

    def analyze_nodetree_state(self):
        """analyze nodetree state.

        Args:
            node_states (_type_): _description_
        """
        # "FINISHED",  "CANCELLED",  "FAILED",  "RUNNING",  "PAUSED",  "CREATED",  "WAITING",  "SKIPPED",  "UNKNOWN"
        # fake state: "HANGING"
        node_states = {}
        for name, dbdata in self.record["nodes"].items():
            node_states[name] = dbdata["state"]
        # if one node fails, is cancelled or is paused, change all its children nodes to hanging.
        for name, ndata in self.record["nodes"].items():
            if ndata["state"] in ["FAILED", "CANCELLED"]:
                children = self.record["connectivity"]["child_node"][name]
                for c in children:
                    node_states[c] = "HANGING"
        # print(f"analyze_node_state, push: {msgs}")
        # logger.debug("analyze_node_state, time: {}".format(time.time() - tstart))
        states = list(node_states.values())
        state_list = [
            "CREATED",
            "READY",
            "FINISHED",
            "FAILED",
            "PAUSED",
            "SKIPPED",
            "RUNNING",
            "WAITING",
            "SCATTERED",
            "CANCELLED",
        ]

        counts = {x: states.count(x) for x in state_list}
        s = ""
        # s += "    Created: {}, Ready: {}, FINISHED: {}, Failed: {}, Paused: {}, Skipped: {}, Running: {}, Waiting: {}, Scattered: {}, Cancelled: {}\n".format(
        s += "{:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d}\n".format(
            counts["CREATED"],
            counts["READY"],
            counts["RUNNING"],
            counts["FINISHED"],
            counts["FAILED"],
            counts["PAUSED"],
            counts["SKIPPED"],
            counts["WAITING"],
            counts["SCATTERED"],
            counts["CANCELLED"],
        )
        # get nodetree state
        if (
            counts["CREATED"] == 0
            and counts["READY"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] == 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FINISHED"
            action = "NONE"
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] != 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FAILED"
            action = "NEED_HELP"
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["PAUSED"] == 0
            and counts["CANCELLED"] != 0
        ):
            state = "CANCELLED"
            action = "NEED_HELP"
        else:
            state = "RUNNING"
            action = "UPDATE"
        # logger.debug("analyze_nodetree_state, time: {}".format(time.time() - tstart))
        return state, action

    @property
    def dbdata_nodes(self):
        """Fetch node data from database
        1) node belong to this nodetree
        2) reference node used in this nodetree

        Returns:
            dict: node data from database
        """
        query = {"metadata.nodetree_uuid": self.dbdata["uuid"]}
        project = {"_id": 0, "uuid": 1, "name": 1, "state": 1, "action": 1}
        datas = list(db_node.find(query, project))
        dbdata_nodes = {data["name"]: data for data in datas}
        # find the ref nodes
        ref_nodes = [
            node["name"]
            for node in self.record["nodes"].values()
            if node["node_type"] == "REF"
        ]
        # populate the ref nodes
        for name in ref_nodes:
            query = {"uuid": self.record["nodes"][name]["uuid"]}
            data = db_node.find_one(query, project)
            dbdata_nodes[name] = data

        return dbdata_nodes

    def cancel(self):
        dbdata_nodes = self.dbdata_nodes
        for name, dbdata in dbdata_nodes.items():
            node = EngineNode(dbdata)
            node.update_db_keys({"action": "CANCEL"})
        self.action = "NONE"

    def check_parent_state(self, name):
        """Check parent states

        Args:
            name (str): name of node to be check

        Returns:
            ready (bool): ready to launch or not
        """
        print(f"  check_parent_state: {name}")
        ready = True
        # check the control links first
        input_links = self.record["connectivity"]["ctrl_input_link"][name]
        if input_links.get("entry", {}):
            states = [
                self.record["ctrl_links"][i]["state"] for i in input_links["entry"]
            ]
            if True not in states:
                ready = False
                return ready
        # control node needs special treatment.
        # update node will ingore the "Update" socket for the first run
        inputs = self.record["connectivity"]["input_node"][name]
        # print("node_type: ", self.record["nodes"][name]["node_type"])
        if self.record["nodes"][name]["node_type"] == "Update":
            counter = self.record["nodes"][name]["counter"]
            print(f"  counter: {counter}")
            if counter == 0:
                inputs.pop("update", None)
        # scatter node will always ingore the "Stop" socket
        elif self.record["nodes"][name]["node_type"] == "Scatter":
            inputs.pop("stop", None)
        #
        for socke_name, input_nodes in inputs.items():
            for input_node_name in input_nodes:
                if self.record["nodes"][input_node_name]["node_type"] == "REF":
                    # find ref_uuid
                    uuid = self.record["nodes"][input_node_name]["uuid"]
                    data = scinodedb["node"].find_one({"uuid": uuid}, {"metadata": 1})
                    ref_uuid = data["metadata"]["ref_uuid"]
                    # find ref date
                    data = scinodedb["node"].find_one({"uuid": ref_uuid}, {"name": 1})
                    ref_name = data["name"]
                    data = scinodedb["nodetree"].find_one(
                        {f"nodes.{ref_name}.uuid": ref_uuid},
                        {f"nodes.{ref_name}.state": 1},
                    )
                    # print(f"input_node_name: {input_node_name}, ref_uuid: {ref_uuid}, state: {data['state']}")
                    self.record["nodes"][input_node_name]["state"] = data["nodes"][
                        ref_name
                    ]["state"]
                # If a node is skipped, I consider it as finished
                if self.record["nodes"][input_node_name]["state"] not in [
                    "FINISHED",
                    "SKIPPED",
                ]:
                    print(
                        f"      input_node_name: {input_node_name}, state: {self.record['nodes'][input_node_name]['state']}"
                    )
                    ready = False
                    return ready
        return ready

    def check_scattered_state(self, name):
        """Check scattered states

        Args:
            name (str): name of node to be check
            dbdata_nodes (dict): data of all nodes

        Returns:
            ready (bool): ready to launch or not
        """
        state = "SCATTERED"
        action = "GATHER"
        node_states = self.record["nodes"][name]["scatter"]
        s = ""
        states = list(node_states.values())
        state_list = [
            "CREATED",
            "READY",
            "FINISHED",
            "FAILED",
            "PAUSED",
            "SKIPPED",
            "RUNNING",
            "WAITING",
            "SCATTERED",
            "CANCELLED",
        ]

        counts = {x: states.count(x) for x in state_list}
        s = ""
        s += "    Created: {}, Ready: {}, FINISHED: {}, Failed: {}, Paused: {}, Skipped: {}, Running: {}, Waiting: {}, Scattered: {}, Cancelled: {}\n".format(
            counts["CREATED"],
            counts["READY"],
            counts["FINISHED"],
            counts["FAILED"],
            counts["PAUSED"],
            counts["SKIPPED"],
            counts["RUNNING"],
            counts["WAITING"],
            counts["SCATTERED"],
            counts["CANCELLED"],
        )
        if (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] == 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FINISHED"
            action = "NONE"
            print(
                f"    \nCheck scattered node: {name}, state: {state}, action: {action}"
            )
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] != 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FAILED"
            action = "NEED_HELP"
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["PAUSED"] == 0
            and counts["CANCELLED"] != 0
        ):
            state = "CANCELLED"
            action = "NEED_HELP"

        return state, action

    def load_nodes(self):
        dbdata_nodes = self.dbdata_nodes
        nodes = {}
        for name, dbdata in dbdata_nodes.items():
            node = EngineNode(uuid=dbdata["uuid"])  # , self.worker_name)
            nodes[node.name] = node
        self.nodes = nodes

    def pause_node(self, name):
        """Pause node.

        Args:
            name (str): name of the node to be paused
        """
        logger.debug("pause node, name: {}".format(name))
        if self.record["nodes"][name]["node_type"] == "GROUP":
            send_message_to_queue(
                broker_queue_name,
                f"{self.record['nodes'][name]['uuid']},nodetree,action:PAUSED",
            )
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {f"nodes.{name}.state": "PAUSED"}}
        )

    def play_node(self, name):
        """Play node.

        Args:
            name (str): name of the node to be played
        """
        logger.debug("play node, name: {}".format(name))
        if self.record["nodes"][name]["node_type"] == "GROUP":
            send_message_to_queue(
                broker_queue_name,
                f"{self.record['nodes'][name]['uuid']},nodetree,action:PAUSED",
            )
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {f"nodes.{name}.state": "CREATED"}}
        )
        self.check_node_state(name)

    def skip_node(self, name):
        """Skip node.

        Args:
            name (str): name of the node to be skiped
        """
        # print("skip node, name: {}".format(name))
        nodes_to_skip = [name]
        child_nodes = self.record["connectivity"]["child_node"][name]
        nodes_to_skip.extend(child_nodes)
        logger.debug("reset node, name: {}".format(name))
        items = {}
        for name in nodes_to_skip:
            items[f"nodes.{name}.state"] = "SKIPPED"
        scinodedb["nodetree"].update_one({"uuid": self.uuid}, {"$set": items})

    def reset_node(self, name, all=False):
        """Reset node and all its child nodes.
        If this node belong to a node group, we need to reset the node group.

        Args:
            name (str): name of the node to be paused
        """
        nodes_to_reset = [name]
        child_nodes = self.record["connectivity"]["child_node"][name]
        nodes_to_reset.extend(child_nodes)
        logger.debug("reset node, name: {}".format(name))
        items = {}
        for name in nodes_to_reset:
            items[f"nodes.{name}.state"] = "CREATED"
            if all:
                items[f"nodes.{name}.counter"] = 0
            self.record["nodes"][name]["state"] = "CREATED"
        # If the nodetree is FINISHED, we change it state to CREATED.
        if self.record["state"] in ["FINISHED"]:
            items["state"] = "CREATED"
        scinodedb["nodetree"].update_one({"uuid": self.uuid}, {"$set": items})
        # reset the parent_node
        if self.record["metadata"]["parent_node"]:
            item = scinodedb["node"].find_one(
                {"uuid": self.record["metadata"]["parent_node"]},
                {"_id": 0, "name": 1, "metadata": 1},
            )
            msg = (
                f"{item['metadata']['nodetree_uuid']},node,{item['name']}:action:RESET"
            )
            send_message_to_queue(broker_queue_name, msg)
        # node group node

    def cancel_node(self, name):
        """Cancel node"""
        from scinode.engine.config import broker_queue_name
        from scinode.engine.send_to_queue import send_message_to_queue

        uuid = self.record["nodes"][name]["uuid"]
        future = self.futures.get(uuid)
        if future is not None:
            log = "Node is running: {}.\n".format(future.running())
            was_calcelled = future.cancel()
            if was_calcelled:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
                )
                log += "Node is cancelled: {}".format(was_calcelled)
                # self.update_db_keys({"outputs": {}})
            else:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
                )
                log += "Can not cancel node.".format()
        else:
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
            )
            log = "Future is None. Node {} is not running. Can not cancel.".format(
                self.dbdata["name"]
            )

    def switch_on_ctrl_link(self, index):
        """Run ctrl link.

        - set the state of the link to True
        - reset the node that the link is connected to, launch the node if it is ready.

        Args:
            index (int): index of the link to be switch on
        """
        print(f"  Switch on ctrl link, index: {index}")
        ctrl_links = self.record["ctrl_links"]
        ctrl_links[index]["state"] = True
        link = ctrl_links[index]
        if link["to_socket"] in ["entry", "iter"]:
            # print(f"    {link['to_socket']}")
            self.reset_node(link["to_node"])
            # try to launch the node, if it is will not be launched if its parent node is not finished
            self.check_node_state(link["to_node"])
        scinodedb["nodetree"].update_many(
            {"uuid": self.uuid},
            {"$set": {"ctrl_links": ctrl_links}},
        )

    def switch_off_ctrl_link(self, index):
        """Run ctrl link.

        - set the state of the link to False
        - skip the node that the link is connected to

        Args:
            index (int): index of the link to be switch off
        """
        logger.debug("Switch off ctrl link, index: {}".format(index))
        ctrl_links = self.record["ctrl_links"]
        ctrl_links[index]["state"] = False
        link = ctrl_links[index]
        scinodedb["nodetree"].update_many(
            {"uuid": self.uuid},
            {"$set": {"ctrl_links": ctrl_links}},
        )
        if link["to_socket"] == "entry":
            self.skip_link(index)

    def skip_link(self, index):
        """Skip node.

        Args:
            index (str): index of the link to be skiped
        """
        print(f"  Skip ctrl link, index: {index}")
        link = self.record["ctrl_links"][index]
        nodes_to_skip = self.record["connectivity"]["control_node"][link["from_node"]][
            link["from_socket"]
        ]
        items = {}
        for name in nodes_to_skip:
            items[f"nodes.{name}.state"] = "SKIPPED"
        scinodedb["nodetree"].update_one({"uuid": self.uuid}, {"$set": items})

    def write_log(self, log, worker=False, database=True):
        from scinode.utils.db import write_log

        if worker:
            print(log)
        if database:
            write_log({"uuid": self.uuid}, log, "nodetree")
