from flask import Blueprint, render_template

NAME = 'auth'

bp = Blueprint(NAME, __name__, url_prefix='/auth')



from goglekaap.forms.auth_form import LoginForm, RegisterForm
    
@bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    # 1. form route는 GET-render_template의 화면 보여주기 외에
    # - POST로 form 버튼을 눌렀을 때,데이터 생성 및 수정을 해줘야한다.
    # - 화면으로 가기전에 if ~ return으로 필터링하자.
    # if request.method=="POST" 의 기능 및 validator 통과도 확인해주는 method가 form객체에서 제공함.
    if form.validate_on_submit():
        # POST로 유입 & validators들이 OK 상태
        # 0) 데이터 받아서 꺼내기(form.data는 완벽한 dict)
        user_id = form.data.get('user_id')
        password = form.data.get('password')
        # TODO: sqlalchemy로 DB연결후, POST를 처리해야할 것들
        # 1) 로그인 -> user_id로 유저조회후 존재하는 유지인지 체크
        # 2) 로그인 -> password (form vs DB)정합확인
        # 3) 로그인 -> 로그인 유지(session) 

        # QQQ) 지금은 front에 찍기만. (if안에서는 return으로 끝내야함.)
        # - 빈화면에 string만찍히도록 한다.
        return f"{user_id}, {password}"
    else:
        # 2. POST인데,  valid 를 통과못할시가 else다. error부분이므로 pass시켜놓고..나중에 에러처리하자.
        # TODO: ERROR
        pass

    return render_template(f'{NAME}/login.html', form=form)
    
#  로그아웃은 따로 form객체가 필요하지 않음.
@bp.route('/logout')
def logout():
    return f'{NAME}/logout'

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.data)
        # 0) 데이터 받아서 꺼내기(form.data는 완벽한 dict)
        user_id = form.data.get('user_id')
        user_name = form.data.get('user_name')
        password = form.data.get('password')
        repassword = form.data.get('repassword')
        # TODO: sqlalchemy로 DB연결후, POST를 처리해야할 것들
        # 1) 회원가입 -> user_id로 유저조회후 존재하는 유지인지 체크
        # 2) 회원가입 -> 없는 유저면 생성
        # 3) 회원가입 -> 로그인 유지(세션)
        return f"{user_id}, {user_name}, {password}, {repassword}"
    else:
        # 4) POST인데,(validator 통과못햇을 때!)
        # print("?", form.errors)
        print("GET일 때도 들어오나요?")
        pass

    return render_template(f'{NAME}/register.html', form=form)