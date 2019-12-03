import os
import unittest
import request

from app import *
from app.models import db, User, ConfBlock, Rigs
from app.emos import Statistics as st

from app.models import *
from app import *

TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BasicTests(unittest.TestCase):

    ############################
    #### setup ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.db_conf = "[{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', 'cfg_total_pw': '1', 'cfg_uptime': '1', " \
                       "'cfg_mine_time': '0', 'cfg_api_key': '', 'cfg_type': '0', 'cfg_range': '4320', 'first': '0'}]"

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def login(self, login, password):
        return self.app.post(
            '/login',
            data=dict(username=login, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

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

    def events_save(self):
        event = Notifications(nom_rig='1070', id_rig='2c5c6b6', event='1', created_date=datetime.datetime.now(),
                              date_time=datetime.datetime.now().timestamp(), valid='0')
        db.session.add(event)
        db.session.commit()

    def test_error(self):
        rv = self.app.get('/error')
        self.assertEqual(rv.status, '200 OK')

    def test_about(self):
        rv = self.app.get('/about')
        self.assertEqual(rv.status, '200 OK')

    def test_account_login(self):
        response = self.login('admin', 'emoslive')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Connexion', response.data)

    def test_invalid_passwords(self):
        response = self.login('admin', 'emosliv')
        self.assertIn(b'Login ou mot de passe incorrect', response.data)

    def test_invalid_login(self):
        response = self.login('test', 'emoslive')
        self.assertIn(b'Login ou mot de passe incorrect', response.data)

    def test_read_full_conf(self):
        self.save_cfg()
        db_conf = st.read_full_conf(self)
        assert str(db_conf) == str(self.db_conf)

    def test_show_all_rigs_stats(self):
        self.insert_rig()

        list = st.show_all_rigs_stats(self, str(self.db_conf))

        real_conf = "{'stats': [{'nom_rig': '1070', 'id_rig': '2c5c6b6', 'nb_gpu': 6, 'gpu_type': 'NV', " \
                    "'total_hash': '180.4', 'total_pw': '623.2', 'uptime': '', 'mine_time': '', " \
                    "'hash_unit': 'Mh/s', 'online': '1'}], 'cfg': \"{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', " \
                    "'cfg_total_pw': '1', 'cfg_uptime': '1', 'cfg_mine_time': '0', 'cfg_api_key': '', " \
                    "'cfg_type': '0', 'cfg_range': '4320', 'first': '0'}\", 'availability': '0.0'}"

        self.app.get('/_answer')
        assert list, str(list) == str(real_conf)

    def test_events_save(self):
        self.events_save()
        rv = self.app.get('/_events')
        self.assertEqual(rv.status, '200 OK')
        self.assertIn(b'{"events_items"', rv.data)

    def test_config(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('admin', 'emoslive')
        self.assertIn(b'Connexion', response.data)
        rv = self.app.get('/config')
        self.assertEqual(rv.status, '200 OK')

    def test_events_read(self):
        self.events_save()
        event = st.events_read(self)
        real_event = "{'events_items': [{'id': 1, 'nom_rig': '1070', 'event': '1', " \
                     "'create_at': '", datetime.datetime.now(), "'}], 'total_active_event': 1}"
        rv = self.app.get('/_events')
        #assert str(event) == str(real_event)
        self.assertEqual(rv.status, '200 OK')

    def test_events_list(self):
        self.events_save()
        st.events_list(self)
        rv = self.app.get('/_events')
        self.assertEqual(rv.status, '200 OK')

    @app.route('/login', methods=['GET', 'POST'])
    def test_discharge(self):
        self.login('admin', 'emoslive')
        self.events_save()
        self.app.get('/login', follow_redirects=True)
        event = len(st.events_list(self))
        st.discharge(self)
        self.app.post('/_valid_events')
        clean_event = len(st.events_list(self))


if __name__ == "__main__":
    unittest.main()
