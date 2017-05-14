# encoding: utf-8

from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

from wxapi import Client

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


def create_app(debug=False):
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:haoguihua@127.0.0.1/fish'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = debug

    # 如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助
    app.config['SQLALCHEMY_ECHO'] = debug

    # 可以用于显式地禁用或者启用查询记录。查询记录 在调试或者测试模式下自动启用
    app.config['SQLALCHEMY_RECORD_QUERIES'] = debug

    # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）
    app.config['SQLALCHEMY_POOL_SIZE'] = 5

    # 指定数据库连接池的超时时间。默认是 10。
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10

    # 自动回收连接的秒数。这对 MySQL 是必须的，默认 情况下 MySQL 会自动移除闲置 8 小时或者以上的连接。
    # 需要注意地是如果使用 MySQL 的话， Flask-SQLAlchemy 会自动地设置这个值为 2 小时
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 7200

    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
    db.init_app(app)
    return app


api = Client(proto='https', host='api.weixin.qq.com', app_id='wx16c9d45585b6c9dd',
             app_secret='73bcfc9d8f304a4a5ac33467b921a55d')
