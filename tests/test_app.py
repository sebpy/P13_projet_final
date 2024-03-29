import os
import unittest
from functools import wraps
import requests
from flask import redirect, url_for
import request
import json

from app.emos import Statistics as st
from app.save_config import SaveConfig as sc
from app.views import *
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
        self.ctx = app.app_context()
        self.ctx.push()

        db.drop_all()
        db.create_all()
        self.app = app.test_client()
        self.now = datetime.datetime.now()

        self.app.testing = True
        app.login_manager.init_app(app)

        self.db_conf = "[{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', 'cfg_total_pw': '1', 'cfg_uptime': '1', " \
                       "'cfg_mine_time': '0', 'cfg_api_key': '', 'cfg_type': '0', 'cfg_range': '4320', 'first': '0'}]"

        self.datas = {'0': {'nom_rig': 'EM-1061', 'type_gpu': 'NV', 'nb_gpu': '1', 'mac': 'ec:a8:62:c5:c6:b6',
                      'ip': '192.168.10.10', 'miner': 'Phoenix-miner (Ethash)', 'mine_time': '6j 22h 17m',
                            'hash_unit': 'Mh/s', 'uptime': '29j 08h 52m',
                            'model_gpu': {'0': 'GeForce GTX 1060 6GB  (6078 MiB, 120.00 W)'},
                            'hashrate': {'0': 22.38}, 'temperature': {'0': '65'},
                            'fans': {'0': '54'}, 'pw': {'0': 89.78}, 'oc_mem': {'0': '800'},
                            'oc_core': {'0': '0'}, 'undervolt': {'0': ''}, 'mem_freq': {'0': '4201'},
                            'core_freq': {'0': '1835'}, 'total_hash': '22.38', 'total_pw': '89.78',
                            'cpu': '0.15 0.20 0.25', 'ram': '3,7G 587M 1,3G', 'hdd': '855M 7,3G',
                            'version_emos': '1.14', 'online': '1'}}

        self.conf_full = [{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', 'cfg_total_pw': '1', 'cfg_uptime': '1',
                           'cfg_mine_time': '0', 'cfg_api_key': '10a3857b939c6b2de638236621d2476ec8cad593812e97e05ce7824ebd4ceb92',
                           'cfg_type': '1', 'cfg_range': '4320', 'first': '0'}]

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not app.config.get('LOGIN_DISABLED', False) and g.user is None:
                return redirect(url_for('accounts_app.login', next=request.url))
            return f(*args, **kwargs)

        return decorated_function

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

    def insert_user(self):
        user = User(username='admin', password=generate_password_hash('emoslive'))
        db.session.add(user)
        db.session.commit()
        return

    def save_cfg(self):
        cfg = ConfBlock(show_nb_gpu='1', show_total_hash='1', show_total_pw='1', show_uptime='1',
                        show_mine_time='0', emos_api_key='10a3857b939c6b2de638236621d2476ec8cad593812e97e05ce7824ebd4ceb92', show_type='0', show_range='4320', first='0')
        db.session.add(cfg)
        db.session.commit()
        return

    def insert_rig(self):
        rig = Rigs(nom_rig='1070', id_rig='62c5c6b6', nb_gpu='1', gpu_type='NV',
                   total_hash='180.4', total_pw='623.2', uptime='23j 07h 42m', mine_time='23j 07h 42m',
                   hash_unit='Mh/s', online='1')
        db.session.add(rig)
        db.session.commit()
        return

    def insert_Stat_rig(self):
        rig = StatsRigs(id_rig='62c5c6b6', id_gpu='0', model_gpu='GeForce GTX 1060 6GB  (6078 MiB, 120.00 W)',
                        temp_gpu='65', fan_gpu='53', hash_gpu='22.38', pw_gpu='89.77',
                        oc_mem='', oc_core='1', vddc='0', mem_freq='4201', core_freq='1835',
                        created_date=datetime.datetime.now(), date_time=datetime.datetime.now().timestamp())

        db.session.add(rig)
        db.session.commit()
        return

    def insert_availability(self):
        av = Availability(availability='10.00', created_date=datetime.datetime.now(),
                          date_time=datetime.datetime.now().timestamp())
        db.session.add(av)
        db.session.commit()
        return

    def events_save(self):
        event = Notifications(nom_rig='1070', id_rig='62c5c6b6', event='1', created_date=datetime.datetime.now(),
                              date_time=datetime.datetime.now().timestamp(), valid='0')
        db.session.add(event)
        db.session.commit()

    def test_error(self):
        rv = self.app.get('/error')
        self.assertEqual(rv.status, '200 OK')

    def test_about(self):
        rv = self.app.get('/about')
        self.assertEqual(rv.status, '200 OK')

    def test_account_login_view(self):
        response = self.login('admin', 'emoslive')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Connexion', response.data)

    def test_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_invalid_passwords(self):
        response = self.login('admin', 'emosliv')
        self.assertIn(b'Login ou mot de passe incorrect', response.data)

    def test_invalid_login(self):
        response = self.login('test', 'emoslive')
        self.assertIn(b'Login ou mot de passe incorrect', response.data)

    def test_read_full_conf(self):
        self.save_cfg()
        conf = st.read_full_conf(self)
        self.assertEqual(conf[0]['cfg_nb_gpu'], '1')

    def test_show_all_rigs_stats(self):
        self.insert_rig()

        list = st.show_all_rigs_stats(self, str(self.db_conf))

        real_conf = "{'stats': [{'nom_rig': '1070', 'id_rig': '62c5c6b6', 'nb_gpu': 1, 'gpu_type': 'NV', " \
                    "'total_hash': '180.4', 'total_pw': '623.2', 'uptime': '', 'mine_time': '', " \
                    "'hash_unit': 'Mh/s', 'online': '1'}], 'cfg': \"{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', " \
                    "'cfg_total_pw': '1', 'cfg_uptime': '1', 'cfg_mine_time': '0', 'cfg_api_key': '', " \
                    "'cfg_type': '0', 'cfg_range': '4320', 'first': '0'}\", 'availability': '0.0'}"

        self.app.get('/_answer')
        assert list, str(list) == str(real_conf)

    def test_events_save_view(self):
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

    def test_events_list(self):
        self.events_save()
        st.events_list(self)
        rv = self.app.get('/_events')
        self.assertEqual(rv.status, '200 OK')

    def test_discharge(self):
        self.events_save()
        len(st.events_list(self))

        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)

        sent = {'valid': '1'}
        resp = self.app.post('/_valid_events', data=json.dumps(sent), content_type='application/json',
                             follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_graphpw(self):
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        resp = self.app.get('/_graphpw')
        self.assertEqual(resp.status_code, 200)

    def test_graph_rig(self):
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        resp = self.app.get('/_graph/62c5c6b6')
        self.assertEqual(resp.status_code, 200)

    def test_detail_rig_get(self):
        self.insert_Stat_rig()
        self.insert_rig()
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        resp = self.app.get('/62c5c6b6')
        self.assertEqual(resp.status_code, 200)

    def test_detail_rig_view(self):
        self.insert_Stat_rig()
        self.insert_rig()
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        resp = self.app.get('/detail/62c5c6b6')
        self.assertEqual(resp.status_code, 200)

    def test_avaibility(self):
        self.insert_rig()
        self.insert_availability()
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        resp = self.app.get('/_availability')
        self.assertEqual(resp.status_code, 200)

    def test_update_account(self):
        self.insert_Stat_rig()
        self.insert_rig()
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        sent = {'username': 'admin', 'password': 'pbkdf2:sha256:150000$S0v8fxQS$eea7ce957fd67f75f31ddb076e3f8e'
                                                 '0badff8889fa15f76ee53302d0c88bf147'}
        resp = self.app.post('/_update_account', data=sent, content_type='application/json')
        #self.assertEqual(resp.status_code, 200)

    def test_account(self):
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        resp = self.app.get('/account', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_load_user(self):
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        load_user(1)

    def test_get_status(self):
        datas = [{'cfg_nb_gpu': '1', 'cfg_total_hash': '1', 'cfg_total_pw': '1', 'cfg_uptime': '1',
                  'cfg_mine_time': '0', 'cfg_api_key': '10a3857b939c6b2de638236621d2476ec8cad593812e97e05ce7824ebd4ceb92',
                  'cfg_type': '1', 'cfg_range': '4320', 'first': '0'}]
        st.get_status(self, datas)
        url = "https://rigcenter.easy-mining-os.com/api/" + datas[0]['cfg_api_key']
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_list_rig(self):

        st.list_rigs(self, self.datas)
        list = st.show_all_rigs_stats(self, str(self.db_conf))
        self.assertEqual(list['stats'][0]['nom_rig'], 'EM-1061')
        st.list_rigs(self, self.datas)

    def test_update_status(self):
        self.insert_rig()

        st.update_stats_rig(self, self.datas)
        list = st.show_all_rigs_stats(self, str(self.db_conf))
        self.assertEqual(list['stats'][0]['nom_rig'], 'EM-1061')

    def test_read_stats(self):
        self.insert_Stat_rig()
        stats = st.read_stats(self)
        for k in stats:
            id_rig = k.id_rig
            self.assertEqual(id_rig, '62c5c6b6')

    def test_availability_save(self):
        self.insert_rig()
        self.insert_Stat_rig()

        st.availability_save(self)
        total = st.availability_total()
        self.assertEqual(total[0]['availability'], '0.02')

    def test_save_conf(self):
        self.insert_user()
        self.save_cfg()
        login_successful = self.login('admin', 'emoslive')
        self.app.post('/_save_conf')
        self.assertTrue(login_successful)

    def test_events_save(self):
        datas_offline = {'0': {'nom_rig': 'EM-1061', 'type_gpu': 'NV', 'nb_gpu': '1', 'mac': 'ec:a8:62:c5:c6:b6',
                       'ip': '192.168.10.10', 'miner': 'Phoenix-miner (Ethash)', 'mine_time': '6j 22h 17m',
                       'hash_unit': 'Mh/s', 'uptime': '29j 08h 52m',
                       'model_gpu': {'0': 'GeForce GTX 1060 6GB  (6078 MiB, 120.00 W)'},
                       'hashrate': {'0': 22.38}, 'temperature': {'0': '65'},
                       'fans': {'0': '54'}, 'pw': {'0': 89.78}, 'oc_mem': {'0': '800'},
                       'oc_core': {'0': '0'}, 'undervolt': {'0': ''}, 'mem_freq': {'0': '4201'},
                       'core_freq': {'0': '1835'}, 'total_hash': '22.38', 'total_pw': '89.78',
                       'cpu': '0.15 0.20 0.25', 'ram': '3,7G 587M 1,3G', 'hdd': '855M 7,3G',
                       'version_emos': '1.14', 'online': '0'}}

        st.events_save(self, self.datas)
        list = st.events_read(self)
        self.assertEqual(list['events_items'][0]['event'], '1')

        st.events_save(self, datas_offline)
        list = st.events_read(self)
        self.assertEqual(list['events_items'][0]['event'], '0')

    def test_delete_old_stats(self):
        self.insert_Stat_rig()
        check_old = st.delete_old_stats(self)
        self.assertFalse(check_old)

    def test_account_login(self):
        self.insert_user()
        username = sc.account_login(self)
        self.assertEqual(username, 'admin')

    def test_account_save(self):
        self.insert_user()
        self.save_cfg()
        login_successful = self.login('admin', 'emoslive')
        self.assertTrue(login_successful)
        sent = {'username': 'admin1', 'password': 'pbkdf2:sha256:150000$S0v8fxQS$eea7ce957fd67f75f31ddb076e3f8e'
                                                  '0badff8889fa15f76ee53302d0c88bf147'}
        self.app.post('/_update_account', data=sent, content_type='application/json')
        resp = self.app.get('/account')
        self.assertIn(b'admin', resp.data)


if __name__ == "__main__":
    unittest.main()
