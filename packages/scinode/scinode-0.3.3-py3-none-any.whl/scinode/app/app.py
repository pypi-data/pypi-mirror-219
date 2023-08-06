from flask import Flask, render_template, request
from scinode.app.db import db
from scinode.app.blueprints.node.node import node_bp
from scinode.app.blueprints.data.data import data_bp
from scinode.app.blueprints.component.component import component_bp
from scinode.app.blueprints.nodetree.nodetree import nodetree_bp
from scinode.app.blueprints.template.template import template_bp
from scinode.app.blueprints.config.config import config_bp
from scinode.app.blueprints.scheduler.scheduler import scheduler_bp


def create_app(config=None, testing=False):
    """Create a new instance of SciNode app."""
    app = Flask(__name__)
    # blueprints
    app.register_blueprint(node_bp, url_prefix="/nodes")
    app.register_blueprint(data_bp, url_prefix="/datas")
    app.register_blueprint(component_bp, url_prefix="/components")
    app.register_blueprint(nodetree_bp, url_prefix="/nodetrees")
    app.register_blueprint(template_bp, url_prefix="/templates")
    app.register_blueprint(config_bp, url_prefix="/configs")
    app.register_blueprint(scheduler_bp, url_prefix="/scheduler")

    @app.route("/")
    def index():
        """Home page
        1) Show button for nodetree and template
        2) Show statistic data of the database.
        """
        nodetreeTotal = db["nodetree"].count_documents({})
        nodeTotal = db["node"].count_documents({})
        dataTotal = db["data"].count_documents({})
        componentTotal = db["component"].count_documents({})
        templateTotal = db["template_nodetree"].count_documents({})
        return render_template(
            "index.html",
            title="",
            nodetreeTotal=nodetreeTotal,
            nodeTotal=nodeTotal,
            dataTotal=dataTotal,
            componentTotal=componentTotal,
            templateTotal=templateTotal,
        )

    @app.route("/nodetree_editor")
    def nodetree_editor():
        """Nodetree editor.

        Initialize a editor without node.
        """
        from scinode.app.init_data import init_nodetree_data
        from scinode.app.utils import get_entry_point_filename
        from uuid import uuid1

        # we should genereate a new uuid for this nodetree
        # the uuid should not be imported, otherwise it will be the same
        # all the time.
        init_nodetree_data["uuid"] = uuid1()
        eps = get_entry_point_filename()
        return render_template(
            "nodetree_editor.html",
            title="Nodetree",
            nodetree_data=init_nodetree_data,
            components=eps["components"],
            sockets=eps["sockets"],
            controls=eps["controls"],
        )

    # ====================================
    # Others
    # ====================================

    @app.route("/api/file_upload", methods=["POST"])
    def file_upload_api():
        from flask import flash, redirect
        import json

        # check if the post request has the file part
        print(request.files)
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        data = json.loads(file.read())
        print("data: ", data)
        return {
            "success": True,
            "content": data,
        }

    return app


# =================================
# Home page
# =================================


if __name__ == "__main__":
    app = create_app()
    app.run()
