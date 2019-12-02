import os
import unittest
import request

from app import *
from app.models import db, User, ConfBlock, Rigs
from app.emos import Statistics as st
from app.save_config import SaveConfig as save

TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class SaveConfig(unittest.TestCase):

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

    def login(self, username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )

    def create_admin(self):
        new_user = User(username='admin', password='emoslive')
        db.session.add(new_user)
        db.session.commit()

    def test_admin_site_valid_access(self):
        self.create_admin()
        self.app.get('/login', follow_redirects=True)
        response = self.login('admin', 'emoslive')
        self.assertIn(b'Connexion', response.data)

    def save_cfg(self):
        cfg = ConfBlock(show_nb_gpu='1', show_total_hash='1', show_total_pw='1', show_uptime='1',
                        show_mine_time='0', emos_api_key='', show_type='0', show_range='4320', first='0')
        db.session.add(cfg)
        db.session.commit()
        return

    def insert_rig(self):
        rig = Rigs(nom_rig='1070', id_rig='2c5c6b6', nb_gpu='6', gpu_type='NV',
                   total_hash='180.4', total_pw='623.2', uptime='', mine_time='',
                   hash_unit='Mh/s', online='1')
        db.session.add(rig)
        db.session.commit()
        return

    def test_read_full_conf(self):
        self.save_cfg()
        real_conf = "[{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', 'cfg_total_pw': '1', 'cfg_uptime': '1', " \
                    "'cfg_mine_time': '0', 'cfg_api_key': '', 'cfg_type': '0', 'cfg_range': '4320', 'first': '0'}]"

        db_conf = st.read_full_conf(self)
        assert str(db_conf) == str(real_conf)

    def test_show_all_rigs_stats(self):
        self.insert_rig()
        db_conf = "{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', 'cfg_total_pw': '1', 'cfg_uptime': '1', " \
                    "'cfg_mine_time': '0', 'cfg_api_key': '', 'cfg_type': '0', 'cfg_range': '4320', 'first': '0'}"

        list = st.show_all_rigs_stats(self, db_conf)

        real_conf = "{'stats': [{'nom_rig': '1070', 'id_rig': '2c5c6b6', 'nb_gpu': 6, 'gpu_type': 'NV', 'total_hash': '180.4', 'total_pw': '623.2', 'uptime': '', 'mine_time': '', 'hash_unit': 'Mh/s', 'online': '1'}], 'cfg': \"{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', 'cfg_total_pw': '1', 'cfg_uptime': '1', 'cfg_mine_time': '0', 'cfg_api_key': '', 'cfg_type': '0', 'cfg_range': '4320', 'first': '0'}\", 'availability': '0.0'}"

        assert str(list) == str(real_conf)


#    def test_nb_gpu_chk(self):
#        nbgpu_chk = save.nb_gpu_chk(self)
#        assert nbgpu_chk == '1'


if __name__ == '__main__':
    unittest.main()
