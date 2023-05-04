import secrets
from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
from db_config import db_config
import re
import requests
import folium

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['MYSQL_HOST'] = db_config['host']
app.config['MYSQL_USER'] = db_config['user']
app.config['MYSQL_PASSWORD'] = db_config['password']
app.config['MYSQL_DB'] = db_config['database']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_UNIX_SOCKET'] = '/path/to/socket'
mysql = MySQL(app)

# 홈
@app.route('/home', methods=['GET', 'POST'])
def home():
    user = session.get('user')
    if request.method == 'POST':
        city = request.form['city']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE users SET city = %s WHERE account = %s',
            (city, user['account']))
        mysql.connection.commit()
        cursor.close()

        return render_template('home.html', message="지역이 정상적으로 등록되었습니다.")
    return render_template('home.html')

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    return render_template('setting.html')

# 첫 접속시화면
@app.route('/index', methods=['GET'])
def start():
    return render_template('./login_join/index.html')

# 로그인화면
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['action'] == '로그인':
            # 로그인
            account = request.form['account']
            password = request.form['password']
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE account = %s AND password = %s', (account, password))
            user = cursor.fetchone()
            cursor.close()
            if user is not None:
                session['user'] = user
                return redirect(url_for('home'))
            else:
                return render_template('login_join/login.html', error_message="아이디 또는 비밀번호를 잘못 입력했습니다.")
    return render_template('login_join/login.html')


# 회원가입화면
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form['name']
        account = request.form['account']
        password = request.form['password']

        # name 검사
        if not re.match(r'^[가-힣a-zA-Z]{2,}$', name):
            return render_template('login_join/join.html', error_message="이름은 두 글자 이상이어야합니다.")

        # account 검사
        if not re.match(r'^[a-zA-Z0-9]{6,}$', account):
            return render_template('login_join/join.html', error_message="계정은 여섯 글자 이상이어야 합니다.")

        # password 검사
        if not re.match(r'^[a-zA-Z0-9]{4,}$', password):
            return render_template('login_join/join.html', error_message="비밀번호가 너무 짧습니다.")

        cursor = mysql.connection.cursor()

        # 중복되는 account나 name이 있는지 검사
        cursor.execute(
            'SELECT * FROM users WHERE account = %s OR name = %s', (account, name))
        user = cursor.fetchone()
        if user is not None:
            cursor.close()
            return render_template('./login_join/join.html', error_message="이미 존재하는 아이디 또는 이름입니다.")

        # 회원가입
        cursor.execute(
            'INSERT INTO users (name, account, password) VALUES (%s, %s, %s)', (name, account, password))
        mysql.connection.commit()
        cursor.close()
        return render_template('./login_join/joinsuc.html')
        
    return render_template('login_join/join.html')


# 회원가입 완료 화면
@app.route('/joinsuc', methods=['GET'])
def joinsuc():
    return render_template('login_join/joinsuc.html')

# 맵화면 수정필요(지도에 각 지역별 날씨(서울, 부산, 경기, 충청, 전라도, 경상도 등))
@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        data = request.get_json()
        region = data['region']
        if region:
            # 기본 세팅
            apikey = "26e6bba66e0bbf92a5972deb09369a20"
            lang = "kr"
            api = f"http://api.openweathermap.org/data/2.5/weather?q={region}&appid={apikey}&lang={lang}&units=metric"

            response = requests.get(api)
            if response.status_code == 200:
                data = response.json()
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                map = folium.Map(location=[lat, lon], zoom_start=10)
                folium.Marker(location=[lat, lon],
                              icon=None, popup=region).add_to(map)
                return render_template('map.html', error_message="지역을 다시 입력해주세요.")
            else:
                return "데이터를 가져오는 중 오류가 발생했습니다."
        else:
            # 값이 None일 때 처리
            return "지역을 다시 입력해주세요."
    return render_template('map.html')


# 메인함수
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
