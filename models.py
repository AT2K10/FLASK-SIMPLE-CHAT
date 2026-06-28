import database
class User(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key = True)
    login = database.db.Column(database.db.String(20))
    password = database.db.Column(database.db.String(20))
class Room(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key = True)
    name = database.db.Column(database.db.String(20))
class Room_user(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key = True)
    role = database.db.Column(database.db.String(10))
    user_login = database.db.Column(database.db.String(20))
    room_id = database.db.Column(database.db.Integer)
class Message(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key = True)
    user_sender = database.db.Column(database.db.String(20))
    room_id = database.db.Column(database.db.Integer)
    text = database.db.Column(database.db.Text)
    image = database.db.Column(database.db.String(20), default = None)
class Invite(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key = True)
    user_login = database.db.Column(database.db.String(20))
    room_id = database.db.Column(database.db.Integer)