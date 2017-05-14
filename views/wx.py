# encoding: utf-8
import hashlib
from datetime import datetime
from functools import wraps

from flask import Blueprint, abort, jsonify, request, make_response, render_template

from ext import api
from models.msg import Msg
from wxapi.hook import Text, Image, Video, Voice, Location, incoming
from models.user import User

bp = Blueprint('wx', __name__)


def csrf_skip(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst

    return wrapper_fun


@bp.route('/')
def home():
    return render_template('index.html')


@bp.route("/msg", methods=['GET'])
def check():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echo = request.args.get('echostr')
    token = "token201618"

    l = [token, timestamp, nonce]
    l.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, l)
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        return echo
    else:
        abort(403)


def authorize_msg(req):
    signature = req.args.get('signature')
    timestamp = req.args.get('timestamp')
    nonce = req.args.get('nonce')
    token = "token201618"

    l = [token, timestamp, nonce]
    l.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, l)
    hashcode = sha1.hexdigest()
    return hashcode == signature


@bp.route("/msg", methods=['POST'])
@incoming(Text, Image, Voice, Video, Location)
def message(data):
    if authorize_msg(request):
        if isinstance(data, Text):
            """
            <xml><ToUserName><![CDATA[gh_6cafe8fadb1b]]></ToUserName>
            <FromUserName><![CDATA[orrRbwKLJYHeqjKFL1EN9Hp-bppo]]></FromUserName>
            <CreateTime>1486964295</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[我的]]></Content>
            <MsgId>6386463017764215603</MsgId>
            </xml>"""
            Msg.add(**dict(
                msg_id=data.msg_id,
                msg_type=data.msg_type,
                from_user=data.from_user,
                to_user=data.to_user,
                content=data.content,
                creation_time=datetime.fromtimestamp(float(data.create_time))
            ))
        if isinstance(data, Image):
            print data, 'Image'
        if isinstance(data, Voice):
            print data, 'voice'
        if isinstance(data, Video):
            print data, 'video'
        if isinstance(data, Location):
            print data, 'location'
        return ''
    else:
        return abort(403)


@bp.route('/sync/users')
@csrf_skip
def sync_users():
    user_info = api.get_users()
    for openid in user_info.data['openid']:
        info = api.get_user_info(openid)
        info['openid'] = openid
        info['subscribe_time'] = datetime.fromtimestamp(info.subscribe_time)
        user = User.get_by_openid(openid)
        if user:
            User.update(**info)
        else:
            User.add(**info)
    return jsonify(r=True)


@bp.route('/users')
@csrf_skip
def get_users():
    users = User.get_all()
    data = []
    for u in users:
        location = []
        if u.country:
            location.append(u.country)
        if u.province:
            location.append(u.province)
        if u.city:
            location.append(u.city)
        data.append({
            'openid': u.openid,
            'head_img_url': u.head_img_url,
            'nickname': u.nickname,
            'sex': u.sex,
            'location': '-'.join(location),
            'remark': u.remark,
            'update_time': str(u.update_time),
            'creation_time': str(u.creation_time),
        })
    return jsonify(r=True, data=data)


@bp.route('/msgs')
@csrf_skip
def get_msgs():
    msgs = Msg.get_all()
    data = []
    for m in msgs:
        openid = m.from_user
        u = User.get_by_openid(openid)
        if not u:
            info = api.get_user_info(openid)
            info['openid'] = openid
            u = User.add_or_get(**info)
        data.append({
            'from_user': openid,
            'openid': m.msg_id,
            'head_img_url': u.head_img_url,
            'nickname': u.nickname,
            'sex': u.sex,
            'remark': u.remark,
            'update_time': str(m.update_time),
            'creation_time': str(m.creation_time),
            'content': m.content
        })
    return jsonify(r=True, data=data)


@bp.route('/send', methods=['POST'])
@csrf_skip
def replay_msg():
    openid = request.form.get('openid')
    content = request.form.get('content')
    if not openid or not content:
        return jsonify(r=False)
    data = api.send_msg(content, openid)
    return jsonify(r=True, data=data)


@bp.route('/materials')
@csrf_skip
def get_materials():
    materials = api.get_materials()
    print materials
    data = []
    for m in materials:
        data.append(dict(

        ))
    return jsonify(r=True, data=data)
