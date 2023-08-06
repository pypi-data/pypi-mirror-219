
from bbat.config import Config
import os

os.environ["APP_NAME"] = "knowledge_chat"


conf = Config()
conf.load_yaml("./setting.yaml")
print(conf.get_env("app.name"))
print(conf.get_env("app.port"))