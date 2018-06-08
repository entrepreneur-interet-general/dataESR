from airflow.plugins_manager import AirflowPlugin
from mongo_plugin.hooks.mongo_hook import MongoHook


class MongoPlugin(AirflowPlugin):
    name = "MongoPlugin"
    hooks = [MongoHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
