from flask import Blueprint, render_template, jsonify, current_app, redirect, url_for, session
from exts import mail, db, redis_client
from flask_mail import Message
from flask import request
import string
import random
from threading import Thread
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import redis
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))



@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                #cookie:
                #cookie中不适合存储太多的数据，只适合存储少量的数据
                #cookie一般用来存放登录授权的东西
                #fask是加密以后存储在cookie中的
                session["user_id"] = user.id
                return redirect(url_for("qa.index"))
            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


def send_captcha_store_email(auth_app, email, captcha):
    with auth_app.app_context():
        message = Message(subject="注册验证码", recipients=[email], body=f"注册验证码是：{captcha}")
        mail.send(message)
        redis_client.setex(f"captcha:{email}", 300, captcha)

        # emial_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        # db.session.add(emial_captcha)
        # db.session.commit()
@bp.route("/captcha/email", methods=['GET'])
def get_email_captcha():
    #传参
    #其他传参方法
    useremail = request.args.get("email")
    #验证码的发送
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)

    auth_app = current_app._get_current_object()
    thread = Thread(target=send_captcha_store_email, args=(auth_app, useremail, captcha))
    thread.start()
    #RESTful API
    return jsonify({"code": 200, "message": "获取验证码成功", "data": None})


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("qa.index"))



@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["liuxinhut@163.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"



@bp.route("/birth")
def birth():
    return render_template("birthday.html")