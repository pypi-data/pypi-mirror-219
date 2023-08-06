from bbat.config import Config
from bbat.db.mysql import Mysql

conf = Config()
conf.load_yaml("./setting.yaml")
dbconf = conf.get('mysql')
print(dbconf)

db = Mysql(**dbconf)
print(db)