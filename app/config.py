import os
#  取得啟動文件資料夾路徑
basedir = os.path.abspath(os.path.dirname(__file__))
def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(basedir, db_name)
SQLALCHEMY_DATABASE_URI = create_sqlite_uri('petpetdontcry.sqlite3')
SECRET_KEY = os.urandom(32)
ENV = "DEVELOPMENT"