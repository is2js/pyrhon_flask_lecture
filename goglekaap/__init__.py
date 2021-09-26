from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect() # 1.csrf객체생성 = CSRFProtect(app) 방법도 있지만, 팩토리 패턴에서는 creat_app()안에서 초기화해준다.

def create_app():
    app = Flask(__name__)

    if app.config['DEBUG']:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

    app.config['SECRET_KEY'] = 'secretkey'

    '''Routes INIT'''
    from goglekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)


    '''CSRF INIT'''
    csrf.init_app(app)

    # routes
    # @app.route('/') -> bp의 base로 이동됨.

    @app.errorhandler(404)
    def page_404(error):
        return render_template("/404.html"), 404


    # Form용 로그인, 로그아웃, 회원가입 route정리

    return app
