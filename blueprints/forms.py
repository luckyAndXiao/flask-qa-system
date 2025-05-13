import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db, redis_client
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])
    confirm_password = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    #自定义验证
    def validate_email(self, filed):
        """
        验证邮箱
        :param filed:
        :return:
        """
        email = filed.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册")
    #验证码
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_key = f"captcha:{email}"
        stored_captcha = redis_client.get(captcha_key)
        if not stored_captcha:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        #todo: 可以删除captcha_model
        else:
            if stored_captcha.decode("utf-8") == captcha:
                print("验证码通过")
                redis_client.delete(captcha_key)
            else:
                raise wtforms.ValidationError(message="验证码错误！")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=2, max=100, message="标题格式错误")])
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题ID")])
