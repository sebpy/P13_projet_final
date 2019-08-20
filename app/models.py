from flask_sqlalchemy import SQLAlchemy
import logging as lg
import datetime

from app.views import app
# Create database connection object
db = SQLAlchemy(app)


class Rigs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_rig = db.Column(db.String(20))
    id_rig = db.Column(db.String(8))
    nb_gpu = db.Column(db.Integer)
    gpu_type = db.Column(db.String(3))
    total_hash = db.Column(db.String(8))
    total_pw = db.Column(db.String(8))
    uptime = db.Column(db.String(30))
    mine_time = db.Column(db.String(30))
    hash_unit = db.Column(db.String(10))
    online = db.Column(db.Enum('0', '1'), nullable=False)

    def __init__(self, nom_rig, id_rig, nb_gpu, gpu_type, total_hash, total_pw, uptime, mine_time, hash_unit, online):
        self.nom_rig = nom_rig
        self.id_rig = id_rig
        self.nb_gpu = nb_gpu
        self.gpu_type = gpu_type
        self.total_hash = total_hash
        self.total_pw = total_pw
        self.uptime = uptime
        self.mine_time = mine_time
        self.hash_unit = hash_unit
        self.online = online


class StatsRigs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_rig = db.Column(db.String(8))
    id_gpu = db.Column(db.String(2))
    model_gpu = db.Column(db.String(200))
    temp_gpu = db.Column(db.String(8))
    fan_gpu = db.Column(db.String(8))
    hash_gpu = db.Column(db.DECIMAL(5, 2))
    hash_unit = db.Column(db.String(10))
    pw_gpu = db.Column(db.DECIMAL(5, 2))
    oc_mem = db.Column(db.String(5))
    oc_core = db.Column(db.String(5))
    vddc = db.Column(db.String(5))
    mem_freq = db.Column(db.String(5))
    core_freq = db.Column(db.String(5))
    online = db.Column(db.Enum('0', '1'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_time = db.Column(db.Integer, nullable=False)

    def __init__(self, id_rig, id_gpu, model_gpu, temp_gpu, fan_gpu, hash_gpu, hash_unit, pw_gpu, oc_mem,
                 oc_core, vddc, mem_freq, core_freq, online, created_date, date_time):
        self.id_rig = id_rig
        self.id_gpu = id_gpu
        self.model_gpu = model_gpu
        self.temp_gpu = temp_gpu
        self.fan_gpu = fan_gpu
        self.hash_gpu = hash_gpu
        self.hash_unit = hash_unit
        self.pw_gpu = pw_gpu
        self.oc_mem = oc_mem
        self.oc_core = oc_core
        self.vddc = vddc
        self.mem_freq = mem_freq
        self.core_freq = core_freq
        self.online = online
        self.created_date = created_date
        self.date_time = date_time


class ConfBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_nb_gpu = db.Column(db.Enum('0', '1'), nullable=False)
    show_total_hash = db.Column(db.Enum('0', '1'), nullable=False)
    show_total_pw = db.Column(db.Enum('0', '1'), nullable=False)
    show_uptime = db.Column(db.Enum('0', '1'), nullable=False)
    show_mine_time = db.Column(db.Enum('0', '1'), nullable=False)
    emos_api_key = db.Column(db.String(100), nullable=False)
    show_type = db.Column(db.Enum('0', '1'), nullable=False)
    show_range = db.Column(db.String(6), nullable=False)

    first = db.Column(db.Enum('0', '1'), nullable=False)

    def __init__(self, show_nb_gpu, show_total_hash, show_total_pw,
                 show_uptime, show_mine_time, emos_api_key, show_type, show_range, first):
        self.show_nb_gpu = show_nb_gpu
        self.show_total_hash = show_total_hash
        self.show_total_pw = show_total_pw
        self.show_uptime = show_uptime
        self.show_mine_time = show_mine_time
        self.emos_api_key = emos_api_key
        self.show_type = show_type
        self.show_range = show_range

        self.first = first  # First connexion => Config page


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_rig = db.Column(db.String(20))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, nom_rig, create_at):
        self.nom_rig = nom_rig
        self.create_at = create_at


def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(ConfBlock('1', '1', '1', '1', '0', "", '0', '10080', '0'))
    #db.session.add(Rigs("EM-1060", "xxxxxxxx", "6", "NV", "123.2", "688", "6j22h30m", "6j22h30m"))
    db.session.commit()
    lg.warning('Database initialized!')


if __name__ == '__main__':
    db.create_all()
    init_db()
