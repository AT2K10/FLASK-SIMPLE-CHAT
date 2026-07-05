import uuid
import pickle  
import uuid
from database import db
import models
from werkzeug.security import generate_password_hash, check_password_hash



def check_log(login):
    user = models.User.query.filter_by(login = login).first()
    if user:
        return True
    else:
        return False
    
def new_user(login, password):
    new = models.User(login = login, password = generate_password_hash(password))
    db.session.add(new)
    db.session.commit()
    
    
def create_room(name, nickname):
    room = models.Room(name = name)
    db.session.add(room)
    db.session.commit()
    room_user = models.Room_user(user_login = nickname, room_id = room.id, role = 'admin')
    db.session.add(room_user)
    db.session.commit()

def lists(nickname):
    us_room = []
    rooms = models.Room_user.query.filter_by(user_login = nickname).all()
    for i in rooms:
        room_id = i.room_id
        name_n = models.Room.query.filter_by(id = room_id).first()
        info = {}
        info['id'] = i.room_id
        info['name'] = name_n.name
        us_room.append(info)
    return us_room

def check_ui(login, password):
    user = models.User.query.filter_by(login = login, password = generate_password_hash(password)).first()
    if user:
        return True
    else:
        return False

def send_msg(login_sender, room_id, message):
    msg = models.Message(room_id = room_id, text = message, user_sender = login_sender, image = None)
    db.session.add(msg)
    db.session.commit()
    return msg.id, room_id

def get_msg(room_id):
    msg_info = []
    msgs = models.Message.query.filter_by(room_id = room_id).all()
    for i in msgs:
        msg = {}
        msg['id'] = i.id
        msg['login_sender'] = i.user_sender
        msg['room_id'] = i.room_id
        msg['message'] = i.text
        msg['image'] = i.image
        msg_info.append(msg)
    print(msg_info)
    return msg_info

def new_invite(login, room_id, login_sender):
    invite = models.Room_user.query.filter_by(room_id = room_id, user_login = login).first()
    if invite:
        return 'user is already in room'
    invite = models.Invite(user_login = login, room_id = room_id)
    db.session.add(invite)
    db.session.commit()

def delete_invite(invites_id):
    invite = models.Invite.query.filter_by(id = invites_id).first()
    db.session.delete(invite)
    db.session.commit()

def get_invites(login):
    cur_invites = []
    invites = models.Invite.query.filter_by(user_login = login).all()
    for i in invites:
        invite = {}
        invite['login'] = i.user_login
        invite['room_id'] = i.room_id
        invite['invites_id'] = i.id
        invite['login_sender'] = i.user_login #delete this later
        cur_invites.append(invite)
    return cur_invites

def join_room(login, room_id):
    room_user = models.Room_user(user_login = login, room_id = room_id, role = 'user')
    db.session.add(room_user)
    db.session.commit()


def send_image_msg(login_sender, room_id, image, message = None):
    name = uuid.uuid4().hex
    msg = models.Message(room_id = room_id, text = message, user_sender = login_sender, image = name)
    db.session.add(msg)
    db.session.commit()
    return name, msg.id, room_id

def get_users_by_rid(room_id):
    users = models.Room_user.query.filter_by(room_id = room_id).all()
    for i in users:
        yield i.user_login

def remove_msg(msg_id): #c=index
    msg = models.Message.query.filter_by(id = msg_id).first()
    db.session.delete(msg)
    db.session.commit()

def leave_r_user(room_id, nickname):
    user = models.Room_user.query.filter_by(user_login = nickname, room_id = room_id).first()
    db.session.delete(user)
    db.session.commit()
def check_r_user(login, room_id):
    user = models.Room_user.query.filter_by(user_login = login, room_id = room_id).first()
    if user:
        return True
    else:
        return False

           

