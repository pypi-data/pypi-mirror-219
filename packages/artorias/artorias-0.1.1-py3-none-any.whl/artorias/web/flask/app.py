from __future__ import annotations

import logging
import os

from flask import Flask as BaseFlask
from flask.logging import default_handler

from artorias.web.flask.json import JSONProvider
from artorias.web.flask.utils import find_blueprints


class Flask(BaseFlask):
    json_provider_class = JSONProvider

    def __init__(
        self,
        import_name: str,
        static_url_path: str | None = None,
        static_folder: str | os.PathLike | None = "static",
        static_host: str | None = None,
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: str | os.PathLike | None = "templates",
        instance_path: str | None = None,
        instance_relative_config: bool = False,
        root_path: str | None = None,
        settings: dict | None = None,
    ):
        super().__init__(
            import_name,
            static_url_path,
            static_folder,
            static_host,
            host_matching,
            subdomain_matching,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path,
        )

        self.source_path = os.path.join(self.root_path, os.path.basename(self.root_path))

        self.load_settings(settings)
        self.init_logger()
        self.load_exts()
        self.load_blueprints()
        self.load_error_handlers()

    def load_exts(self):
        from artorias.web.flask.exts import cache, cors, db, migrate

        db.init_app(self)
        migrate.init_app(self)
        cors.init_app(self)
        cache.init_app(self)

        if self.debug:
            with self.app_context():
                db.create_all()

        @self.shell_context_processor
        def make_shell_context():
            return {"cache": cache}

    def load_settings(self, settings: dict | None):
        from artorias.web.flask.settings import DefaultSettings

        default_setttings = DefaultSettings().model_dump()
        if settings:
            default_setttings.update(**settings)
        self.config.from_mapping(default_setttings)

    def load_blueprints(self):
        blueprints_package = f"{os.path.basename(self.source_path)}.apis"
        for blueprint in find_blueprints(blueprints_package):
            self.logger.debug(f"Find blueprint '{blueprint}'")
            self.register_blueprint(blueprint)

    def init_logger(self):
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        default_handler.setFormatter(logging.Formatter(self.config["LOGGER_FORMAT_STRING"]))
        self.logger.addHandler(default_handler)

    def load_error_handlers(self):
        @self.errorhandler(Exception)
        def unknown_exception(exp: Exception):
            self.logger.exception(str(exp))
            return {"error": self.config["UNKNOWN_EXCEPTION_MESSAGE"]}, 500
