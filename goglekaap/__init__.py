from re import sub
from flask import Flask

db = 'database' # fatcotry pattern예시용 객체

def create_app():
    print('run: create_app()')

    print(__name__)
    app = Flask(__name__)
    

    @app.route('/')
    def index():
        # Requests hook test
        app.logger.info("RUN HelloWorld")
        return "hello world!!"

    """ 3-1. Routing Practice"""
    from flask import jsonify, redirect, url_for
    # 1) String
    # 기본꺽쇠<>는 default로 string을 받으며, 함수의 인자로 받아야한다.
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


    """4. Request Hook"""
    # 6. app context와 같이 실습
    # - 생명주기가 1개 request로 동일하다고 했으니 같이 사용한다. 좀 더 늦게 끝난다.
    from flask import g, current_app


    #3. before_first_rquest
    # - 매 요청마다 요청전에 호출이 아니라, 처음만 요청전에 해주고 다음 요청시부터는 X
    @app.before_first_request
    def before_first_request():
        app.logger.info("BEFORE_FIRST_REQUEST")

    #1. before_request
    # - app객체에서 제공하는 logger.info로 한번 찍어본다.
    #2. 실제 처음 running이 되는 부분이 route 중 index route므로
    # - 거기서도 찍어보고 flask run > localhost:5000접속 - route접속 > 찍힌 로그를 보자.
    @app.before_request
    def before_request():
        # 6-1. g에 데이터 주입후 나중에 확인할 예정
        app.logger.info("BEFORE_REQUEST")
        g.test=True



    #4. after_request
    # - 반드시, request끝나고난 뒤 넘어노느 reponse를 인자로 받아서 return까지 해줘야한다..
    # - 인자 1개 반드시 받고, return도 반드시 1개 해줘야한다.
    @app.after_request
    def after_request( response ):
        # 6-2. g의 데이터가 아직도 살아있는지 확인. request안꺼졌음 이놈도 안꺼졌을 뜻
        app.logger.info(f"g.test >>> {g.test}")
        app.logger.info(f"current_app.config['ENV'] >>> {current_app.config['ENV']}")

        app.logger.info("AFTER_REQUEST")
        return response

    # 5. teardown_request
    # - 인자를 1개 받는데 exception을 받는다.
    # - exception == 에러를 받는 다는 뜻
    # - return은 안해줘도 된다.
    @app.teardown_request
    def teardown_request(exception):
        app.logger.info("TEARDOWN_REQUEST")
        # 6-3 request가 종료되면 g는 초기화? -> 그래도 볼 수있다. 실제 request는 아직 안끝남.
        app.logger.info(f"g.test >>> {g.test}")

    # 7. teardown_appcontext
    # - 똑같이 exception인자로 받는다.
    # - teardown_reqeust보다 이후에 작동한다.
    # - 아직 g객체가 살아있다.(request단윈데 아직 살아있는게 특이. 그래봈짜 다음 request에선 조회안됨. by before_first_request로 테스트)
    @app.teardown_appcontext
    def teardown_appcontext(exception):
        app.logger.info("TEARDOWN_APPCONTEXT")
        app.logger.info(f"g.test >>> {g.test}")


    """5. request and Method"""
    from flask import request
    # 5-1. request에 담긴 정보를 찍어보기
    # - request. method, args, form, json
    # - 정보가 여러개일 땐, return jsonify( dict ) 형태로 데이터를 노출시키면서 찍업좌.
    # - jsonify로 return시킨 정보는 postman등으로 예쁘게 볼 수 있다.
    # 5-2. get이외의 메소드는 직접추가해줘야한다.
    @app.route('/test/method/<id>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
    def method_test(id):
        return jsonify({
            'request.method' : request.method,
            'request.args' : request.args,
            'request.form' : request.form,  
            'request.json' : request.json,
        })
 
        




    return app
