from flask import Blueprint, render_template, request
from scinode.common.log import logging

logger = logging.getLogger("app")

scheduler_bp = Blueprint("scheduler_bp", __name__, template_folder="templates")


@scheduler_bp.route("/", methods=["POST"])
def nodetree_push_message():
    """Apply actions to the nodes of this nodetree.

    The request.json should be a dict which includes the name
    and action for each node.

    Returns:
        dict: message
    """
    from scinode.engine.send_to_queue import send_message_to_queue
    from scinode.engine.config import broker_queue_name

    msg = request.json
    logger.info(f"push message: {msg}")
    send_message_to_queue(broker_queue_name, msg)
    return {"message": True}
