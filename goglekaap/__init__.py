from re import sub
from flask import Flask

db = 'database' # fatcotry pattern예시용 객체

def create_app():
    print('run: create_app()')

    print(__name__)
    app = Flask(__name__)
    

    @app.route('/')
    def index():
        return "hello world!!"

    """ 3-1. Routing Practice"""
    from flask import jsonify, redirect, url_for
    # 1) String
    # 기본꺽쇠는 default로 string을 받으며, 함수의 인자로 받아야한다.
    # - type출력시, <class str>형식으로 나올 것이다. 
    # -- return str시 꺽쇠는 script로 인식되기 때문에, escape처리가 필요하다.
    # Name is hello, # escape처리 안하면 꺽쇠는 스크립트로 수행된다.
    # Name is hello, <class 'str'>
    from markupsafe import escape
    @app.route('/test/name/<name>')
    def name(name):
        return f'Name is {name}, {escape(type(name))}'

    # 2) int
    # - <int:변수명>
    # - int route에 문자열 기입시 에러남
    # Not Found The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again
    @app.route('/test/id/<int:id>')
    def id(id):
        return 'Id: %d'%id

    # 3) path
    # <path:subpath>형태로  string에서  /slash를 이용할 수 있게 된다.
    # http://localhost:5000/test/path/    sub/path
    # output : sub/path
    @app.route('/test/path/<path:subpath>')
    def path(subpath):
        return subpath


    # 4) jsonify : json으로 데이터 내려줄 때
    # - 인자로 dict형태로 넘기면 된다.
    # output:  {
    #   "hello": "world"
    # }
    @app.route('/test/json')
    def json():
        return jsonify({'hello':'world'})

    # 5) redirect
    # <path:>형 route를 받아 해당path로 or 연결된path로 넘겨준다.
    # http://localhost:5000/test/redirect/https://www.naver.com
    @app.route('/test/redirect/<path:subpath>')
    def redirect_url(subpath):
        return redirect(subpath)

    # 6) url_for
    # - route에서 redirect와 마찬가지로 <path:>형 route를 받는다.
    # **url_for( '타 route의 함수명 str', 타route함수인자명 = 받은 값)  이용해 거기로 넘겨준다.**
    # **ex> rediect( url_for( 'path', subpath=url_for_subpath )))** 
    # - static file url지정해줄 때 많이 쓴다.
    # input: http://localhost:5000/test/urlfor/a/b/c/
    # output1 - str + url_for() : /test/path/a/b/c/
    # output2 - str + escape + redirect(url_for()) :<Response 240 bytes [302 FOUND]>
    # output3 - redirect(url_for()) : http://localhost:5000/test/path/a/b/c/
    #    127.0.0.1 - - [29/Aug/2021 21:46:08] "GET /test/urlfor/a/b/c/ HTTP/1.1" 302 -
    #    127.0.0.1 - - [29/Aug/2021 21:46:08] "GET /test/path/a/b/c/ HTTP/1.1" 200 -
    @app.route('/test/urlfor/<path:url_for_subpath>')
    def urlfor(url_for_subpath):
        return redirect(url_for('path', subpath=url_for_subpath))


    return app
