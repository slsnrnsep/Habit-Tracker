from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

#폴더 및 초기환경 세팅
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

#Token생성용 암호화 키
SECRET_KEY = 'SPARTA'

#MongoDB관련 설정사항
#client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017) #서버 구동시 아래줄을 사용해주세요
db = client.dbsparta_plus_week4


# <editor-fold desc="프로필 페이지 함수">

#프로필 페이지(/) 접속 시 토큰정보에 따라 로그인창으로 이동or정상진행
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('profile_page.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

#프로필 페이지 접속시마다 GET요청하여 전체 사용자의 DB를 불러옴
@app.route('/user', methods=['GET'])
def listing():
    user_feat = list(db.users.find({}, {'_id': False}))
    return jsonify({'user_feat': user_feat})

# </editor-fold>

# <editor-fold desc="로그인,회원가입 관련 함수">
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    #해시함수를 사용한 DB에서 ID,PW 찾는 과정
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8') #토큰 발행

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": nickname_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

#중복 가입 방지
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})
# </editor-fold>

# <editor-fold desc="마이페이지 관련 함수">
@app.route('/user/<username>')
def my_page(username):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('my_page.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]

        new_doc = {
            "profile_name": name_receive,
            "profile_info": about_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
# </editor-fold>

# <editor-fold desc="습관 기록 페이지 관련 함수">

#/detail 이라는 주소를 통해 'GET'하여 습관기록 페이지로의 이동
@app.route('/detail', methods=['GET'])
def habit_move():
    token_receive = request.cookies.get('mytoken')
    try:
        #토큰을 받아 암호화를 해제하여 payload형식으로 저장
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        #현재 접속중인 사용자의 DB를 가져옴
        user_info = db.users.find_one({"username": payload["id"]})

        #습관 기록 페이지로의 이동
        return render_template('habit_page.html', user_info=user_info)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="페이지 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="페이지 정보가 존재하지 않습니다."))


@app.route('/habit', methods=['POST'])
def write_habit():
    habit_receive = request.form['new_habit_give']
    username_receive = request.form['username_give']
    doc = {
        'username' : username_receive,
        'habit': habit_receive,
        'like' : 0
    }
    db.habit.insert_one(doc)

    return jsonify({'msg': '습관 저장 완료!'})

#개인 습관 기록 불러오는 함수
@app.route('/habit/list', methods=['POST'])
def show_habit():
    try:
        username = request.form['username_give']
        habits = list(db.habit.find({"username": username}, {'_id': False}).sort('like', -1))
        return jsonify({"result": "success",'all_habits': habits})
    except:
        return redirect(url_for("home"))

@app.route('/habit/like', methods=['POST'])
def like_habit():
    habit_receive = request.form['habit_give']

    target_habit = db.habit.find_one({'habit': habit_receive})
    current_like = target_habit['like']

    new_like = current_like + 1

    db.habit.update_one({'habit': habit_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '습관 달성 완료! 오늘도 목표한 일을 이루어 내셨군요! 앞으로도 화이팅'})

@app.route('/habit/hate', methods=['POST'])
def hate_habit():
    habit_receive = request.form['habit_give']

    target_habit = db.habit.find_one({'habit': habit_receive})
    current_like = target_habit['like']

    new_like = current_like - 1

    db.habit.update_one({'habit': habit_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '습관 미달성 ㅠㅠ 내일부터 더 빡세게!!'})

@app.route('/habit/delete', methods=['POST'])
def delete_habit():
    habit_receive = request.form['habit_give']
    db.habit.delete_one({'habit': habit_receive})
    return jsonify({'msg': '습관 삭제 완료!'})
# </editor-fold>

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
