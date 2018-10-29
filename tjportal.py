import cmd
import requests
import base64
import re


class S4KTJPortal(cmd.Cmd):
    '''
    Srun4K/Tongji.Portal Command Line Tool
    '''
    
    intro = 'Srun4K/Tongji.Portal Command Line Tool.\nType help or ? to list commands.\n'
    prompt = '(TJPortal) '
    req_url = 'http://192.168.192.10/include/auth_action.php'
    cookies = None

    def do_login(self, arg):
        'Login Tongji.Portal:  LOGIN id pwd'
        id, pwd = arg.split()
        loginFormData = {
            'action': 'login',
            'username': id,
            'password': r'{B}'+base64.b64encode(pwd.encode()).decode(),
            'ac_id': 1,
            'user_ip': '',
            'nas_ip': '',
            'user_mac': '',
            'save_me': 1,
            'ajax': 1}
        r = requests.post(S4KTJPortal.req_url, data=loginFormData, timeout=5)
        if r.status_code == 200:
            if re.match('login_ok', r.text):
                self.cookies = dict(login=r.text.split(',')[2])
                print('Login Success!')
            else:
                print(r.text)
        else:
            print('HTTP ERROR CODE: ' + r.status_code)

    def do_logout(self, arg):
        'Logut Tongji.Portal:  LOGOUT'
        data = {
            'action': 'logout',
            'ajax': 1}
        r = requests.post(S4KTJPortal.req_url, data=data, cookies=self.cookies, timeout=5)
        if r.status_code == 200:
            print(r.text)
        else:
            print('HTTP ERROR CODE: ' + r.status_code)

    def do_status(self, arg):
        'Check login status:  STATUS'
        data = {
            'action': 'get_online_info',
            'ajax': 1}
        r = requests.post(S4KTJPortal.req_url, data=data, cookies=self.cookies, timeout=5)
        if r.status_code == 200:
            print(r.text)
            '''
            sum_bytes
			sum_seconds
			user_balance ￥
            user_mac
            mac_auth 0|1
			user_ip
            
            '''
        else:
            print('HTTP ERROR CODE: ' + r.status_code)

    def do_bind(self, arg):
        'Bind Mac address:  BIND'
        data = {
            'action': 'bind_mac_auth',
            'user_ip': '',
            'ajax': 1}
        r = requests.post(S4KTJPortal.req_url, data=data, cookies=self.cookies, timeout=5)
        if r.status_code == 200:
            if r.text == 'not_online':
                print('Please Login before bind.')
            elif r.text == 'bind_ok':
                print('Bind Mac Address Success.')
            elif r.text != '':
                print('This Mac Address is already bound to ' + r.text)
            else:
                print('Bind Failed!')
        else:
            print('HTTP ERROR CODE: ' + r.status_code)

    def do_quit(self, arg):
        'Close and exit'
        return True

if __name__ == '__main__':
    S4KTJPortal().cmdloop()
