from flask import Blueprint, request, render_template, g, redirect, url_for, jsonify
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required
# from ollama import AsyncClient
from ollama import chat
from ollama import ChatResponse
bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)

@bp.route("/qa/public", methods=['GET', "POST"])
@login_required
def public_question():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            #todo:跳转到问道详情页
            return redirect(url_for("qa.index"))
        else:
            print(form.errors)
            return redirect(url_for('qa.public_question'))


@bp.route('/qa/detail/<question_id>')
def qa_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question)

@bp.route("/answer/public", methods=['POST'])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", question_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", question_id=request.form.get("question_id")))


@bp.route("/search")
def search():
    #/search?q=flask
    q = request.args.get('q')
    print("q: ", q)
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template('index.html', questions=questions)



def get_ollama_response(prompt):
    response: ChatResponse = chat(model='qwen3:8b', messages=[
        {
            'role': 'user',
            'content': f'{prompt}',
        },
    ])
    return response['message']['content']

@bp.route('/llm')
def llm():
    return render_template('deepseek.html')

@bp.route('/ask', methods=['POST'])
async def ask():
    user_input = request.form['user_input']
    print("user_input: ", user_input)
    response = get_ollama_response(user_input)  # 使用异步函数获取响应
    print("user_input: ", response)
    return jsonify({'response': response})