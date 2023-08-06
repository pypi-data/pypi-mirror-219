import httpx
import random
import uuid
from time import *
import string
import secrets
import binascii
from gamerinsta.tokens import Tokens



def generateRandomString(n):
    # Generate a random string of length n
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))



class Login:
    def __init__(self):
        self.Pigionid=f'UFS-{str(uuid.uuid4())}-0'
        self.Block='4a40c892c95e48d772a51c3e512eface26cba248924e73e874956fd781bcd1f4'
        self.Deviceid=str(uuid.uuid4())
        self.FDeviceid=str(uuid.uuid4())
        self.Androidid=f'android-{generateRandomString(8).encode().hex()}'
        rnd = str(random.randint(150, 999))
        self.Useragent="Instagram 291.1.0.34.111 Android (" + ["23/6.0", "24/7.0", "25/7.1.1", "26/8.0", "27/8.1", "28/9.0"][random.randint(0, 5)] + "; " + str(random.randint(100, 1300)) + "dpi; " + str(random.randint(200, 2000)) + "x" + str(random.randint(200, 2000)) + "; " + ["SAMSUNG", "HUAWEI", "LGE/lge", "HTC", "ASUS", "ZTE", "ONEPLUS", "XIAOMI", "OPPO","VIVO", "SONY", "REALME"][random.randint(0,11)] + "; SM-T" + rnd + "; SM-T" + rnd + "; qcom; en_US; 494078218)"
        self.Waterid=str(uuid.uuid4())
        self.qpl_join_id=str(uuid.uuid4())


    def Loginv1(self,Username,Password):
        Tokens.Cooki(self)
        self.Usernamee=Username
        self.Passs=Password
        self.Mid, self.Elgn, self.Plgn, self.Insid, self.Mkrid, self.headers
        data = {
            'params': '{"client_input_params":{"contact_point":"' + self.Usernamee + '","password":"#PWD_INSTAGRAM:0:' + str(
                round(
                    time())) + ':' + self.Passs + '","fb_ig_device_id":[],"event_flow":"login_manual","openid_tokens":{},"machine_id":"' + self.Mid + '","family_device_id":"' + self.FDeviceid + '","accounts_list":[],"try_num":1,"login_attempt_count":1,"device_id":"' + self.Androidid + 'a","auth_secure_device_id":"","device_emails":[""],"secure_family_device_id":"","event_step":"home_page"},"server_params":{"is_platform_login":0,"qe_device_id":"' + self.Deviceid + '","family_device_id":"' + self.FDeviceid + '","credential_type":"password","waterfall_id":"' + self.Waterid + '","username_text_input_id":"' + self.Elgn + '","password_text_input_id":"' + self.Plgn + '","offline_experiment_group":"caa_iteration_v3_perf_ig_4","INTERNAL__latency_qpl_instance_id":' + self.Insid + ',"INTERNAL_INFRA_THEME":"default","device_id":"' + self.Androidid + '","server_login_source":"login","login_source":"Login","ar_event_source":"login_home_page","INTERNAL__latency_qpl_marker_id":' + self.Mkrid + '}}',
            'bk_client_context': '{"bloks_version":"' + self.Block + '","styles_id":"instagram"}',
            'bloks_versioning_id': self.Block,
        }
        updict = {
            "Content-Length": str(len(data)),
            'X-Pigeon-Rawclienttime': str(round(time(), 3)),

        }
        self.headers = {key: updict.get(key, self.headers[key]) for key in self.headers}
        try:
            response = httpx.post(
                'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/',
                headers=self.headers,
                data=data,
            )
            if 'two_factor_identifier' in response.text:
                value={"Response":'2FA Enabled '}
                print(value)
                self.two_factor_identifier = str(response.text.split(r'"two_factor_identifier\\\":\\\"')[1].split(r'\\\"')[0])
                self.trusted_notification_polling_nonce = str(response.text.split(r'"trusted_notification_polling_nonce\\\":\\\"')[1].split(r'\\\"')[0])
                self.ppk=str(response.text.split(r'"pk\\\":')[1].split(',')[0])
                self.unnmm = str(response.text.split(r'"username\\\":\\\"')[1].split('\\\"')[0])

                updict={'x-ig-nav-chain': f'TwoFacLoginVerifyFragment:two_fac:1:button:{round(time())}.{random.randint(111,999)}::,TwoFacLoginHelpSheetFragment:two_fac:2:button:{round(time())}.{random.randint(111,999)}::',}
                self.headers.update(updict)
                data = {
                    'signed_body': 'SIGNATURE.{"two_factor_identifier":"'+self.two_factor_identifier+'","username":"'+self.unnmm+'","guid":"'+self.Deviceid+'","device_id":"'+self.Androidid+'"}',
                }

                response = httpx.post('https://i.instagram.com/api/v1/accounts/send_two_factor_login_sms/',
                                         headers=self.headers, data=data)
                if '"status": "ok"' in response.text:
                    value={'Response':'2FA Otp Sent On Your Number'}
                    #print(value)
                    self.Otp=str(input("Enter Otp : "))
                    updict={'x-ig-nav-chain': f'TwoFacLoginVerifyFragment:two_fac:1:button:{round(time())}.{random.randint(111,999)}::,TwoFacLoginHelpSheetFragment:two_fac:2:button:{round(time())}.{random.randint(111,999)}::',}
                    self.headers = {key: updict.get(key, self.headers[key]) for key in self.headers}
                    data = {
                        'signed_body': 'SIGNATURE.{"verification_code":"'+str(self.Otp)+'","phone_id":"'+str(self.FDeviceid)+'","two_factor_identifier":"'+self.two_factor_identifier+'","username":"'+self.unnmm+'","trust_this_device":"1","guid":"'+self.Deviceid+'","device_id":"'+self.Androidid+'","waterfall_id":"'+self.Waterid+'","verification_method":"1"}',
                    }

                    response = httpx.post('https://i.instagram.com/api/v1/accounts/two_factor_login/',
                                             headers=self.headers, data=data)
                    if "logged_in_user" in response.text:
                        self.bearer=response.headers['ig-set-authorization'].split(':')[2]
                        self.UserId=response.headers['ig-set-ig-u-ds-user-id']
                        self.rur=response.headers['rur'].split(':')[1]
                        Tokens.Cooki2(self)
                        self.claim, self.shbts, self.igid, self.shbi, self.urur
                        value = {
                            'Response': 'Login Sucessful.',
                            'Username': self.unnmm,
                            'Userid': self.UserId,
                            'Ig-Bearer-Token': self.bearer,
                            'X-pigeon-session-id': self.Pigionid,
                            'X-Ig-Family-Device-Id': self.FDeviceid,
                            'X-Ig-Device-Id': self.Deviceid,
                            'X-AndroidId': self.Androidid,
                            'X-Mid': self.Mid,
                            'X-Claim': self.claim,
                            'IgId': self.igid,
                            'X-UserAgent': self.Useragent,
                            'Block-Version': self.Block,
                            'Ig-Rur': self.urur,
                            'Ig-Shbid': self.shbi,
                            'Ig-Shbts': self.shbts

                        }
                        return value
                    else:
                        print(response.text)


                else:
                    value={'Response':response.text}
                    print(value)


            if 'Incorrect Password: The password you entered is incorrect. Please try again.' in response.text:
                value = {
                    "Response": 'Incorrect Password: The password you entered is incorrect. Please try again.',
                }
            elif f"An unexpected error occurred. Please try logging in again." in response.text:

                value = {
                    "Response": f"Login Error: An unexpected error occurred. Please try logging in again.",
                }
            elif 'Please wait a few minutes before you try again.' in response.text:
                value = {
                    "Response": 'Please wait a few minutes before you try again.',
                }

            elif f". Try another phone number or email, or if you don't have an Instagram account, you can sign up." in response.text:

                value = {
                    "Response": f"We can't find an account with {self.Usernamee}. Try another phone number or email, or if you don't have an Instagram account, you can sign up.",
                }

            elif f"Login Error: An unexpected error occurred. Please try logging in again." in response.text:

                value = {
                    "Response": f"Login Error: An unexpected error occurred. Please try logging in again.",
                }
            elif 'Bearer IGT:2:' in response.text:
                self.Usernmm = response.text.split(r'username\\\\\\\":\\\\\\\"')[1].split(r'\\\\\\\"')[0]
                # print(self.Usernmm)
                self.bearer = \
                    response.text.split(r'\\\\\\\", \\\\\\\"IG-Set-Password-Encryption-Key-Id\\\\\\\": \\\\\\\"')[
                        0].split(
                        '"Bearer IGT:2:')[1]
                # self.csrf = response.text.split(r'csrftoken=')[1].split('; Domain=.instagram.com; expires=')[0]
                self.rur = \
                    response.text.split(r'\\\\\\\", \\\\\\\"Cross-Origin-Embedder-Policy-Report-Only')[0].split(
                        r'"ig-set-ig-u-rur\\\\\\\": \\\\\\\"')[1]
                self.UserId = response.text.split(r', \\\\\\\"ig-set-ig-u-rur\\\\\\\"')[0].split(
                    r'"ig-set-ig-u-ds-user-id\\\\\\\": ')[1]

                Tokens.Cooki2(self)
                self.claim,self.shbts,self.igid,self.shbi,self.urur
                value={
                    'Response': 'Login Sucessful.',
                    'Username':self.Usernmm,
                    'Userid':self.UserId,
                    'Ig-Bearer-Token': self.bearer,
                    'X-pigeon-session-id': self.Pigionid,
                    'X-Ig-Family-Device-Id': self.FDeviceid,
                    'X-Ig-Device-Id':self.Deviceid,
                    'X-AndroidId':self.Androidid,
                    'X-Mid':self.Mid,
                    'X-Claim':self.claim,
                    'IgId':self.igid,
                    'X-UserAgent':self.Useragent,
                    'Block-Version':self.Block,
                    'Ig-Rur':self.urur,
                    'Ig-Shbid':self.shbi,
                    'Ig-Shbts':self.shbts

                }
            elif 'challenge_required' in response.text:
                value = {
                    "Response": 'Challenge_Required',
                }



            elif 'checkpoint_challenge_required' in response.text:

                value = {
                    "Response": 'Checkpoint_Challenge_Required',
                }


            elif 'checkpoint_required' in response.text:
                value = {
                    "Response": 'checkpoint_required',
                }

            elif f"An unexpected error occurred. Please try logging in again." in response.text:

                value = {
                    "Response": f"Login Error: An unexpected error occurred. Please try logging in again.",
                }


            else:
                value = {
                    "Response": response.json(),
                }

            return value
        except Exception as e:
            print(e)



