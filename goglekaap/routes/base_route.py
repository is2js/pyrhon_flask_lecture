from flask import Blueprint, render_template

NAME = 'base' # 1. url과 별개. flask routes의 endpoint_prefiex가 될 놈을 전역변수로 선언한다.

# 2. bp객체 선언(초기화)할 때 namespace명과 __name__을 받는다.
# - 3번째 인자인 url_prefix=가 없는 기초 route다.
bp = Blueprint(NAME, __name__)

@bp.route('/')
def index():
    return render_template('index.html')
