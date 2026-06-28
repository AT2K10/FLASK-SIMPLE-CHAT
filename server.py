from flask import session, Flask, url_for, request, redirect, render_template, send_from_directory
from flask_socketio import SocketIO
from config import Config
import db
import uuid
import api
import threading
import database

login2sid = {}

app = Flask('main')
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
database.db.init_app(app)
with app.app_context():
    database.db.create_all()
socket = SocketIO(app)

def handle_text(text, msg_id, room_id):
    res = api.mistral_api(f'Содержит ли текст негативные слова? Ответь только YES=да или NO=нет и ничего больше: {text}')
    print(res)
    if res == 'YES':
        print('ok', list( db.get_users_by_rid(room_id)))
        for nickname in db.get_users_by_rid(room_id):
            print('nick')
            if login2sid.get(nickname, []) != []:
                for k in login2sid[nickname]:
                    print('sent')
                    socket.emit('neg_msg', [room_id, msg_id], to=k)


@socket.event
def connect():
    login = session['login']
    if login not in login2sid:
        login2sid[login] = [request.sid]
    else:
        login2sid[login].append(request.sid) 
@socket.event
def disconnect():
    login = session['login']
    if login in login2sid:
        login2sid[login].remove(request.sid)
@app.route('/reg', methods = ["POST", "GET"])
def reg():
    if request.method == "GET":
        return render_template('reg.html')
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('check_password')
        res = db.check_log(login)
        if len(login) < 1 or len(password) < 1:
            return render_template('reg.html', error = "login or password is empty")
        if res == True:
            return render_template('reg.html', error = "login is already taken")
        else: 
            if password == password2:
                session['active'] = True
                session['login'] = login
                db.new_user(login, password)
                return redirect(url_for('main'))
            else:
                return render_template('reg.html', error = "passwords not the same")
            
@socket.event
def remove_msg(msg_id, room_id): #c=index
    db.remove_msg(msg_id)
    print(login2sid)
    for nickname in db.get_users_by_rid(room_id):
        print('nick')
        if login2sid.get(nickname, []) != []:
            for k in login2sid[nickname]:
                print('sent')
                socket.emit('remove_msg', [room_id, msg_id], to=k)

@app.route('/logout', methods = ["GET"])
def logout():
    session.clear()
    return redirect(url_for('reg'))

@app.route('/main', methods = ["GET"])
def main():
    if 'active' not in session:
        return redirect(url_for('reg'))
    nickname = session['login']
    res = db.lists(nickname)
    cur_invites = db.get_invites(nickname)
    return render_template('main.html', invites = cur_invites, result = res)

@app.route('/create', methods = ['POST'])
def create():
    button = request.form.get('create_room')
    input = request.form.get('name_room')
    nickname = session['login']
    if button != None:
        print('ok')
        db.create_room(input, nickname)
        return redirect(url_for('main'))

@app.route('/log', methods = ['POST', 'GET'])
def log():
    if request.method == 'POST':
        login = request.form.get("login")
        password = request.form.get('password')
        res = db.check_log(login)
        if res == True:
            result = db.check_ui(login, password)
            if result == True:
                session['active'] = True
                session['login'] = login
                return redirect(url_for('main'))
            else:
                return render_template('log.html', error = 'log or password incorrect')
        else:
            return render_template('log.html', error = 'log or password incorrect')
    if request.method == 'GET':
        return render_template('log.html')

error = None

@app.route('/room/<int:room_id>', methods = ['GET', 'POST'])
def room(room_id):
    global error
    if 'login' not in session:
        return redirect(url_for('log'))
    login = session['login']
    res = db.check_r_user(login, room_id)
    if res == False:
        return redirect(url_for('main'))
    session['room_id'] = room_id
    msgs = db.get_msg(room_id)
    for msg in msgs:
        if msg['login_sender'] == login:
            msg['tresh'] = True
    if error != None:
        html = render_template('room.html', msgs = msgs, error = error, room_id = room_id)
        error = None
        return html
    if request.method == 'GET':
        return render_template('room.html', msgs = msgs, room_id = room_id)
    act = request.form.get('leave')
    print(act, 'ts')
    if act == '1':
        return redirect(url_for('main'))
    elif act == '2':
        print('ok')
        db.leave_r_user(room_id, login)
        return redirect(url_for('main'))

    
    
def not_msg(login, room_id, text, image_name = None):
    for nickname in db.get_users_by_rid(room_id):
            if login2sid.get(nickname, []) != []:
                for k in login2sid[nickname]:
                    socket.emit('new msg', [text, image_name, login], to=k)


@app.route('/send', methods = ['POST'])
def send():
    global error
    act = request.form.get('send')
    image = request.files.get('file')
    text = request.form.get('message')
    login = session['login']
    room_id = session['room_id']
    if text == None and image == None:
        return redirect(url_for('room', room_id = room_id))
    if image != None and image.filename != '' and image.filename[-4:] not in ('.png', 'jpeg', '.jpg', 'webp'):
        error = 'file is not an image'
        return redirect(url_for('room', room_id = room_id))
    if image != None and image.filename[-4:] in ('.png', 'jpeg', '.jpg', 'webp'):
        print('2')
        name, msg_id, room_id = db.send_image_msg(login, room_id, image, text)
        thread = threading.Thread(target=handle_text, args=[text, msg_id, room_id], daemon=True)
        thread.start()
        not_msg(login, room_id, text, name)
        return redirect(url_for('room', room_id = room_id))
    if act != None:
        print('3')
        msg_id, room_id = db.send_msg(login, room_id, text)
        thread = threading.Thread(target=handle_text, args=[text, msg_id, room_id], daemon=True)
        thread.start()
        not_msg(login, room_id, text)
        return redirect(url_for('room', room_id = room_id))

@app.route('/invite', methods = ['POST'])
def invite():
    global error
    login = request.form.get('login')
    room_id = session['room_id']
    login_sender = session['login']
    res = db.check_log(login)
    if res == False:
        error = 'User is not exist' 
        return redirect(url_for('room', room_id = room_id))
    if res == True:
        error = db.new_invite(login, room_id, login_sender)
        if error != None:
            return redirect(url_for('room', room_id = room_id))
        else:
            if login in login2sid:
                for i in login2sid[login]:
                    socket.emit('note', [login_sender, room_id], to=i)

            return redirect(url_for('room', room_id = room_id))
    

@app.route('/not_panel/<int:room_id>/<int:invites_id>', methods = ['POST'])
def panel(room_id, invites_id):
    ok = request.form.get('ok')
    if ok is not None:
        login = session['login']
        # Добавляем пользователя в комнату
        db.join_room(login, room_id)
        # Удаляем приглашение
        db.delete_invite(invites_id)
        # Перенаправляем в комнату
        return redirect(url_for('room', room_id=room_id))
    else:
        # Если отклонили, просто удаляем приглашение
        db.delete_invite(invites_id)
        return redirect(url_for('main'))

@app.route('/image/<string:image>', methods = ['GET'])
def img(image):
    return send_from_directory('images', image)

@app.errorhandler(404)
def eror_fzf(error):
    return render_template('404.html')

if __name__ == "__main__":
    socket.run(app, port = 5000, debug=True)



        