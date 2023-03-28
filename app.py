from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.xxnpzo1.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


import requests

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

@app.route('/')
def home():
    return render_template('index.html')

# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route("/valid", methods=["GET"])
def valid_user():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.
    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': payload})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
    
@app.route('/signup')
def signuppage():
    # msg = request.args.get("msg")
    return render_template('signup.html')

@app.route('/signin')
def signinpage():
    # msg = request.args.get("msg")
    return render_template('signin.html')

@app.route('/signup', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give'] 
    print(id_receive , pw_receive)
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash})

    return jsonify({'result': 'success'})


@app.route('/signin', methods=['POST'])
def signin():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    print(pw_hash)
    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,

            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)

        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/profile')
def registerpage():
    # msg = request.args.get("msg")
    return render_template('register.html')

# 프로필 등록
# @app.route("/profile/<string:userId>", methods=['POST'])
@app.route("/profile", methods=["POST"])
def profile_post():
    userid_receive = request.form['userid_give']
    name_receive = request.form['name_give']
    field_receive = request.form['field_give']
    github_receive = request.form['github_give']
    blog_receive = request.form['blog_give']
    email_receive = request.form['email_give']
    mbti_receive = request.form['MBTI_give']
    image_receive = request.form['image_give']

    doc = {
        'userid':userid_receive,
        'name':name_receive,
        'field':field_receive,
        'github':github_receive,
        'blog':blog_receive,
        'email':email_receive,
        'mbti':mbti_receive,
        'image':image_receive
    }
    db.profile.insert_one(doc)
    
    return jsonify({'msg':'프로필이 등록되었습니다.'})

@app.route("/profile/all", methods=["GET"])
def profile_get():
    profile_data = list(db.profile.find({},{'_id':False}))
    return jsonify({'result':profile_data})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)