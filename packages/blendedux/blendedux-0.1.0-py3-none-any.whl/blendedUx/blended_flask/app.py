

from blendedUx.blended_flask.blended_hostlib.backend import FileSystemBackend
from blendedUx.blended_flask.blended_hostlib.network import Network
from blendedUx.blended_flask.blended_hostlib.controller import Controller
from flask import Flask, send_from_directory, send_file
from blendedUx.blended_flask.settings import blended_static_dir
import os

class BlendedFlask():
    """
    """
    def __init__(self,app, package_dir):
        """
        """
        self.package_dir = package_dir
        @app.route("/blended_static/<path:path>")
        def blended_static(path):
            try:
                return send_from_directory(blended_static_dir, path)
            except Exception:
                return send_file(os.path.join(blended_static_dir, path))

    def load(self, theme_name, user_slug):
        """
        """
        network = Network()
        backend = FileSystemBackend()
        controller = Controller(network, backend)
        backend.blended_dir = self.package_dir
        context = controller.context_loader(theme_name, user_slug)
        return context

    def login(self, user_slug, password):
        """
        """
        pass

