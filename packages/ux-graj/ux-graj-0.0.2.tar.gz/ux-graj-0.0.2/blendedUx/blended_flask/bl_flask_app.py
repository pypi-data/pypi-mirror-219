
from blendedUx.blended_flask.blended_hostlib.backend import FileSystemBackend
from blendedUx.blended_flask.blended_hostlib.network import Network
from blendedUx.blended_flask.blended_hostlib.controller import Controller
from flask import Flask, send_from_directory, send_file
from blendedUx.blended_flask.settings import blended_static_dir
from blended import BlendedEnvironment
import os
import typing as t
from jinja2.loaders import FileSystemLoader
from flask.json.provider import JSONProvider, DefaultJSONProvider
from flask.blueprints import Blueprint

class Bl_Flask(Flask):
    
    def __init__(
            self,
            import_name: str,
            app: t.Optional[str] = None,
            package_dir: t.Optional[t.Union[str, os.PathLike]] = None,
            static_url_path: t.Optional[str] = None,
            static_folder: t.Optional[t.Union[str, os.PathLike]] = "static",
            static_host: t.Optional[str] = None,
            host_matching: bool = False,
            subdomain_matching: bool = False,
            template_folder: t.Optional[t.Union[str, os.PathLike]] = "templates",
            instance_path: t.Optional[str] = None,
            instance_relative_config: bool = False,
            root_path: t.Optional[str] = None,
            ):
        super().__init__(
            import_name= import_name,
            static_folder=static_folder,
            static_url_path=static_url_path,
            template_folder=template_folder,
            root_path=root_path
        )
        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError(
                "If an instance path is provided it must be absolute."
                " A relative path was given instead."
            )
        self.instance_path = instance_path
        # self.json: JSONProvider = self.json_provider_class(self)
        self.cli.name = self.name
        self.package_dir = package_dir
        # if not app and package_dir:
        #     self.package_dir = package_dir
        
            
        if app and package_dir:
            """
            """
            # self.package_dir = package_dir
            @app.route("/blended_static/<path:path>")
            def blended_static(path):
                try:
                    return send_from_directory(blended_static_dir, path)
                except Exception:
                    return send_file(os.path.join(blended_static_dir, path))
        else:
            self.media_cache_load()
            
    
        
    
    def media_cache_load(self):
        '''
        Cacheing route for media
        '''
        @self.route("/blended_static/<path:path>")
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

    def run(self, host=None, port=None, debug=None, **options):
        if host:
            os.environ["custom_host"] = host
        if port:
            os.environ["custom_port"] = str(port)
        
        super().run(host=host, port=port, debug=debug, **options)

