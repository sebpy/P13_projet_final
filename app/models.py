from flask_sqlalchemy import SQLAlchemy
import logging as lg
import enum

from app.views import app
# Create database connection object
db = SQLAlchemy(app)


#class ShowItems(enum.Enum):
#    hidden = 0
#    show = 1


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


class ConfBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_nbGpu = db.Column(db.Enum('0', '1'), nullable=False)
    show_hashTotal = db.Column(db.Enum('0', '1'), nullable=False)
    show_totalpw = db.Column(db.Enum('0', '1'), nullable=False)
    show_uptime = db.Column(db.Enum('0', '1'), nullable=False)
    show_mineTime = db.Column(db.Enum('0', '1'), nullable=False)

    def __init__(self, show_nbGpu, show_hashTotal, show_totalpw,
                 show_uptime, show_mineTime):
        self.show_nbGpu = show_nbGpu
        self.show_hashTotal = show_hashTotal
        self.show_totalpw = show_totalpw
        self.show_uptime = show_uptime
        self.show_mineTime = show_mineTime


def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(ConfBlock('1', '1', '1', '1', '0'))
    db.session.add(Rigs("EM-1060", "xxxxxxxx", "6", "NV", "123.2", "688", "6j22h30m", "6j22h30m"))
    db.session.commit()
    lg.warning('Database initialized!')


if __name__ == '__main__':
    db.create_all()
    init_db()
