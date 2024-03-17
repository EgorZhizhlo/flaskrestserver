import datetime

from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from static.schemas import PostSchema, UserSchema
from static.models import db, POSTS, USERS, app

o_key = "CgFuhy@g9XBc-6NEqTZ2ESUUc-6Z*SppVR#Nua"


@app.route('/about/', methods=['GET'])
async def about():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify([])
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify([])
    return jsonify({
        "title": 'Добро пожаловать!',
        "text": 'Меня зовут Егор Жижло, и я являюсь начинающим Backend-разработчиком. '
                'В данный момент я являюсь студентом 1 курса факультета '
                'Прикладной математики и информатики Финансового Университета при Правительстве РФ. '
                'Этот блог я реализовал с помощью REST API с'
                " использованием фреймворка Flask с целью получения новых навыков и знаний в сфере Backend-разработки.",
        "contacts": {
            "email": 'zhizhloegor_r@mail.ru',
            "github": 'https://github.com/EgorZhizhlo'
        }
    })


@app.route('/', methods=['GET', 'POST'])
async def home():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify([])
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify([])
    return jsonify(PostSchema(many=True).dump(POSTS.query.all()))


@app.route('/aboutpost/<int:post_id>/', methods=['GET', 'POST'])
async def about_post(post_id):
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify([])
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify([])
    return jsonify(PostSchema(many=True).dump(POSTS.query.filter_by(id=post_id)))


@app.route('/createpost/', methods=['POST'])
async def create_post():
    post = request.json
    if not post or 'post' not in post or 'operation_key' not in post or 'email' not in post or \
            not check_password_hash(post['operation_key'], o_key):
        return jsonify({"data": "Неопознаный запрос!"})
    if USERS.query.filter_by(email=post['email']).first() is None:
        return jsonify({"data": f"Автор поста {post['post']['author']} не найден!"})
    db.session.add(
        POSTS(title=post['post']['title'], datetime=datetime.datetime.now().date(), author=post['post']['author'],
              text=post['post']['text']))
    db.session.commit()
    return jsonify({"data": f"Пост создан пользователем {post['post']['author']}!"})


@app.route('/login/', methods=['POST'])
async def login():
    user = request.json
    if not user or 'user' not in user or 'operation_key' not in user or \
            not check_password_hash(user['operation_key'], o_key):
        return jsonify({"data": "Неопознаный запрос!"})
    user = user['user']
    db_user = USERS.query.filter_by(email=user['email']).first()
    if db_user is None or user['password'] is None or user['email'] is None:
        return jsonify({"data": "Пользователь не найден!"})
    if not check_password_hash(db_user.password, user['password']):
        return jsonify({"data": "Некорректный ввод данных!"})
    return jsonify(
        {'data': f"Добро пожаловать, {db_user.username}!", 'email': db_user.email, 'username': db_user.username})


@app.route('/login/checkstatus/', methods=['GET', 'POST'])
async def check_status():
    user = request.json
    if user and 'user' in user and 'operation_key' in user and \
            check_password_hash(user['operation_key'], o_key):
        user = user['user']
        db_user = USERS.query.filter_by(email=user['email']).first()
        if db_user is not None:
            return jsonify({'data': db_user.admin})
    return jsonify({'data': 0})


@app.route('/registration/', methods=['POST'])
async def registration():
    req = request.json
    if not req or 'user' not in req or 'operation_key' not in req or \
            not check_password_hash(req['operation_key'], o_key):
        return jsonify({"data": "Неопознаный запрос!", "id": 0})
    new_user = req['user']
    db_user = USERS.query.filter(
        USERS.email.like(new_user['email']) | USERS.username.like(new_user['username'])).first()
    if db_user is not None:
        return jsonify({"data": "Пользователь с такими данными уже существует!", "id": 0})
    if new_user['username'] is None or new_user['password_rep'] is None or \
            new_user['password'] is None or new_user['email'] is None or \
            new_user['password_rep'] != new_user['password']:
        return jsonify({"data": "Некорректный ввод данных!", "id": 0})
    db.session.add(
        USERS(username=new_user['username'], password=generate_password_hash(new_user['password']),
              repeat_password=generate_password_hash(new_user['password_rep']), email=new_user['email']))
    db.session.commit()
    user = USERS.query.filter_by(email=new_user['email']).first()
    return jsonify({"data": f"Пользователь {new_user['username']} успешно создан!",
                    'username': user.username,
                    'email': user.email,
                    "id": 1
                    })


@app.route('/search/', methods=['GET', 'POST'])
async def search():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify([])
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify([])
    return jsonify(PostSchema(many=True).dump(
        POSTS.query.filter(POSTS.title.like(operation_key['search']) | POSTS.datetime.like(operation_key['search']) |
                           POSTS.author.like(operation_key['search']) | POSTS.text.like(operation_key['search']))))


@app.route('/adminpanel/operation/', methods=['GET', 'POST'])
async def adminpanel_operation():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key or \
            'operation' not in operation_key or 'id' not in operation_key or \
            'text' not in operation_key:
        return jsonify([])
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify([])
    if operation_key['operation'] == 'changetitle':
        post = POSTS.query.filter_by(id=operation_key['id']).first()
        post.title = operation_key['text']
        db.session.commit()
    elif operation_key['operation'] == 'changeauthor':
        post = POSTS.query.filter_by(id=operation_key['id']).first()
        post.author = operation_key['text']
        db.session.commit()
    elif operation_key['operation'] == 'changetext':
        post = POSTS.query.filter_by(id=operation_key['id']).first()
        post.text = operation_key['text']
        db.session.commit()
    elif operation_key['operation'] == 'deletepost':
        db.session.delete(POSTS.query.filter_by(id=operation_key['id']).first())
        db.session.commit()
    elif operation_key['operation'] == 'changeusername':
        user = USERS.query.filter_by(id=operation_key['id']).first()
        user.username = operation_key['text']
        db.session.commit()
    elif operation_key['operation'] == 'deleteuser':
        db.session.delete(USERS.query.filter_by(id=operation_key['id']).first())
        db.session.commit()
    return jsonify([])


@app.route('/adminpanel/users/allusernames/', methods=['GET', 'POST'])
async def adminpanel_allusernames():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify([])
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify([])
    return jsonify([user.username for user in USERS.query.all()])


@app.route('/adminpanel/users/', methods=['GET', 'POST'])
async def adminpanel_allusers():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key:
        return jsonify([])
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify([])
    return jsonify(UserSchema(many=True).dump(USERS.query.all()))


@app.route('/finduser/', methods=['GET', 'POST'])
async def finduser():
    operation_key = request.json
    if 'operation_key' not in operation_key or not operation_key or \
            'email' not in operation_key or 'username' not in operation_key:
        return jsonify({'data': 0})
    if not check_password_hash(operation_key['operation_key'], o_key):
        return jsonify({'data': 0})
    user = USERS.query.filter_by(email=operation_key['email'], username=operation_key['username']).first()
    if user is None:
        return jsonify({'data': 0})
    return jsonify({'data': 1})


if __name__ == '__main__':
    app.run(host="127.0.0.2", port=8000)
