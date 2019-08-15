from flask_sqlalchemy import SQLAlchemy
import logging as lg

from app.views import app
# Create database connection object
db = SQLAlchemy(app)


class Rigs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NomRig = db.Column(db.String(20))
    idRig = db.Column(db.String(8))
    nbGpu = db.Column(db.Integer)
    gpuType = db.Column(db.String(3))
    hashTotal = db.Column(db.String(8))
    totalpw = db.Column(db.String(8))
    uptime = db.Column(db.String(30))
    mineTime = db.Column(db.String(30))

    def __init__(self, NomRig, idRig, nbGpu, gpuType, hashTotal, totalpw, uptime, mineTime):
        self.NomRig = NomRig
        self.idRig = idRig
        self.nbGpu = nbGpu
        self.gpuType = gpuType
        self.hashTotal = hashTotal
        self.totalpw = totalpw
        self.uptime = uptime
        self.mineTime = mineTime


class StatsRigs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_rig = db.Column(db.String(8))
    id_gpu = db.Column(db.String(2))
    model_gpu = db.Column(db.String(200))
    temp_gpu = db.Column(db.String(8))
    fan_gpu = db.Column(db.String(8))
    hash_gpu = db.Column(db.String(8))
    pw_gpu = db.Column(db.String(8))
    oc_mem = db.Column(db.String(5))
    oc_core = db.Column(db.String(5))
    vddc = db.Column(db.String(5))
    mem_freq = db.Column(db.String(5))
    core_freq = db.Column(db.String(5))
    date_time = db.Column(db.Integer, nullable=False)

    def __init__(self, id_rig, id_gpu, model_gpu, temp_gpu, fan_gpu, hash_gpu, pw_gpu, oc_mem,
                 oc_core, vddc, mem_freq, core_freq, date_time):
        self.id_rig = id_rig
        self.id_gpu = id_gpu
        self.model_gpu = model_gpu
        self.temp_gpu = temp_gpu
        self.fan_gpu = fan_gpu
        self.hash_gpu = hash_gpu
        self.pw_gpu = pw_gpu
        self.oc_mem = oc_mem
        self.oc_core = oc_core
        self.vddc = vddc
        self.mem_freq = mem_freq
        self.core_freq = core_freq
        self.date_time = date_time


class ConfBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_nbGpu = db.Column(db.Enum('0', '1'), nullable=False)
    show_hashTotal = db.Column(db.Enum('0', '1'), nullable=False)
    show_totalpw = db.Column(db.Enum('0', '1'), nullable=False)
    show_uptime = db.Column(db.Enum('0', '1'), nullable=False)
    show_mineTime = db.Column(db.Enum('0', '1'), nullable=False)
    emos_api_key = db.Column(db.String(100), nullable=False)
    show_type = db.Column(db.Enum('0', '1'), nullable=False)
    show_range = db.Column(db.String(6), nullable=False)

    first = db.Column(db.Enum('0', '1'), nullable=False)

    def __init__(self, show_nbGpu, show_hashTotal, show_totalpw,
                 show_uptime, show_mineTime, emos_api_key, show_type, show_range, first):
        self.show_nbGpu = show_nbGpu
        self.show_hashTotal = show_hashTotal
        self.show_totalpw = show_totalpw
        self.show_uptime = show_uptime
        self.show_mineTime = show_mineTime
        self.emos_api_key = emos_api_key
        self.show_type = show_type
        self.show_range = show_range

        self.first = first  # First connexion => Config page


def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(ConfBlock('1', '1', '1', '1', '0', "YOUR API KEY", '0', '10080', '0'))
    #db.session.add(Rigs("EM-1060", "xxxxxxxx", "6", "NV", "123.2", "688", "6j22h30m", "6j22h30m"))
    db.session.commit()
    lg.warning('Database initialized!')


if __name__ == '__main__':
    db.create_all()
    init_db()
