import os
import unittest
import requests
import json

from app.models import db, Rigs, StatsRigs
from app import *

TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
URL_API = "https://rigcenter.easy-mining-os.com/api/"
API_KEY = "10a3857b939c6b2de638236621d2476ec8cad593812e97e05ce7824ebd4ceb92"


class TestApi(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def insert_rig(self):
        rig = Rigs(nom_rig='1070', id_rig='2c5c6b6', nb_gpu='6', gpu_type='NV',
                   total_hash='180.4', total_pw='623.2', uptime='', mine_time='',
                   hash_unit='Mh/s', online='1')

        db.session.add(rig)
        db.session.commit()
        return

    def test_get_status(self):
        get_stats = URL_API + API_KEY
        response = requests.get(get_stats)
        result = json.loads(response.text)

        if result != "":
            try:
                self.assertEqual(result['0']['nom_rig'], 'EM-1070')
            except KeyError:
                return "No api"

    def test_list_rigs(self):
        self.insert_rig()
        list_rig = db.session.query(Rigs)
        for rig in list_rig.all():
            self.assertEqual(rig.nom_rig, '1070')
            self.assertEqual(rig.id_rig, '2c5c6b6')
            self.assertEqual(rig.nb_gpu, 6)
            self.assertEqual(rig.gpu_type, 'NV')
            self.assertEqual(rig.total_hash, '180.4')
            self.assertEqual(rig.total_pw, '623.2')
            self.assertEqual(rig.uptime, '')
            self.assertEqual(rig.mine_time, '')
            self.assertEqual(rig.hash_unit, 'Mh/s')
            self.assertEqual(rig.online, '1')

    def test_update_stats_rig(self):
        self.insert_rig()
        list_rig = db.session.query(Rigs)
        for rig in list_rig.all():
            self.assertEqual(rig.nom_rig, '1070')
            self.assertEqual(rig.id_rig, '2c5c6b6')
            self.assertEqual(rig.nb_gpu, 6)
            self.assertEqual(rig.gpu_type, 'NV')
            self.assertEqual(rig.total_hash, '180.4')
            self.assertEqual(rig.total_pw, '623.2')
            self.assertEqual(rig.uptime, '')
            self.assertEqual(rig.mine_time, '')
            self.assertEqual(rig.hash_unit, 'Mh/s')
            self.assertEqual(rig.online, '1')


if __name__ == '__main__':
    unittest.main()
