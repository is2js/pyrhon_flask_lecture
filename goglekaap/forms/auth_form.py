from flask_wtf import FlaskForm
# 1. 필드들은 wtforms에서 가져온다.
# - wtforms가 원본이고, flask에 연결만 해준 것이 flaskWTF임.
# - 문서는 wtforms를 봐야함.
# https://wtforms.readthedocs.io/en/2.3.x/fields/#field-definitions
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    # 2. 각 필드는 노출될 Label , validators를 기본으로 받음
    user_id = StringField('User Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    

# 3. 대박) 회원가입 > 로그인 필드들을 포함하니 상속받아서 + 추가로 넣어주자.
# - 작은 집합이 부모!
class RegisterForm(LoginForm):
    # 4. login의 password를 상속받지만, validators에서 추가되는 부분이 있어 재정의한다.
    # user_id는 상속
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), EqualTo(
            'repassword', # 미리 밑에 나올 repassword필드를 지정해준다.
            message='Password must match.' # 같지않은 에러일 경우 노출할 메시지
        )]
        )
    # 5. confirm하는 password필드이며,
    # - 원본 password필드의 EqualTo에 걸리게 되며, 당하는 입장에서는 validators에 기입안해도 된다.
    repassword = PasswordField(
        'Confirm Password',
        validators=[ DataRequired()]
    )

    # 6. username
    # - user_id(상속) pass, repass, username까지 다 필수다.
    user_name = StringField('User Name', validators=[DataRequired()])

