# -*- coding: utf-8 -*-
from core.constants import FIRST_SEMESTER, SECOND_SEMESTER

__author__ = 'sungjinyoo'

# lib requirements : rsa, requests
# rsa : pip install rsa
# requests : pip install requests

import base64
import math
import random
import requests
import rsa
import json


class EZHubLoginRequiredException(Exception):
    pass


cookies = None


def do_portal_login():
    global cookies
    # get the cookies from the login page
    r = requests.get("https://portal.hanyang.ac.kr/sso/lgin.do")
    WMONID = r.cookies['WMONID']
    HYIN_JSESSIONID = r.cookies['HYIN_JSESSIONID']

    cookies = dict(
        WMONID=WMONID,
        HYIN_JSESSIONID=HYIN_JSESSIONID,
        ipSecGb=base64.b64encode('1'),
        loginUserId=base64.b64encode('2008037280'),
    )

    headers = {
        'content-type': 'application/json+sua; charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # get public key from the server
    public_tk_url = 'https://portal.hanyang.ac.kr/sso/publicTk.do'

    # generate fake keyNm
    key_nm = 'sso_00' + str(random.randint(1, 3))

    public_tk_params = dict(
        keyNm=key_nm,
        encStr='2008037280'
    )

    public_tk_payload = json.dumps(public_tk_params)

    r = requests.post(public_tk_url, cookies=cookies, headers=headers, data=public_tk_payload)

    result = json.loads(r.text)

    public_key_n_value_string = result['key'][0]['value']

    # type cast public_key_string to integer
    public_key_n_value_int = int(public_key_n_value_string, 16)
    public_key_e_value_int = int('010001', 16)

    # make public key with n, e value
    public_key = rsa.key.PublicKey(public_key_n_value_int, public_key_e_value_int)

     # clone function in hanyang page
    def fn_rsa_enc(in_data):
        base64_string = base64.b64encode(in_data)
        length = len(base64_string)

        splitcnt = int(math.ceil(float(length) / 50))

        enc_final = ""

        for i in range(splitcnt):
            pos = i * 50
            end_pos = length if i == splitcnt - 1 else pos + 50

            enc_final += (rsa.encrypt(base64_string[pos:end_pos], public_key)).encode('hex')

        return enc_final

    # encrypt id and password with custom RSA
    enc_user_id = fn_rsa_enc('2008037280')
    enc_password = fn_rsa_enc('gmrrh9915!')

    login_params = dict(
        ipSecGb=1,
        keyNm=key_nm,
        loginGb=1,
        userId=enc_user_id,
        password=enc_password,
        signeddata='',
        symm_enckey='',
        systemGb='PORTAL',
        returl='https://portal.hanyang.ac.kr/port.do'
    )

    login_url = 'https://portal.hanyang.ac.kr/sso/lgnp.do'

    headers['accept'] = 'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*'
    headers.pop('content-type')

    # do login
    r = requests.post(login_url, cookies=cookies, headers=headers, data=login_params, allow_redirects=False)


def fetch_student_time_table(student_id, year, semester):
    global cookies

    time_table_url = 'https://portal.hanyang.ac.kr/haksa/SuscAct/findSincheongGwamokSiganpyo.do?pgmId=P309390&menuId=M006449&tk=6da76b464bd9652e47cff1b95a694172dd0bc3cdc158c18888cc4d688e8fe827'
    headers = {
        'origin': 'https://portal.hanyang.ac.kr',
        'Referer': 'https://portal.hanyang.ac.kr/port.do',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip,deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'content-type': 'application/json+sua; charset=UTF-8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'
    }

    payload = dict(
        strHakbun=str(student_id),
        strSosokCd="Y0000383",
        strSuupTerm=str(semester),
        strSuupYear=str(year)
    )

    r = requests.post(time_table_url, cookies=cookies, headers=headers, data=json.dumps(payload))

    result = json.loads(r.text)

    if result.get('exception'):
        do_portal_login()

        return fetch_student_time_table(student_id, year, semester)

    return result['DS_SUUPSC10TTM01'][0]['list']


def get_current_year():
    from datetime import datetime

    return datetime.now().year


def get_current_semester():
    from datetime import datetime

    current_month = datetime.now().month - 1  # make it as 0 based month
    semester = FIRST_SEMESTER
    if 0 <= current_month < 2:  # 겨울학기 (1~2월)
        semester = 40
    elif 2 <= current_month < 6:  # 1학기 (3~6월)
        semester = FIRST_SEMESTER
    elif 6 <= current_month < 8:  # 여름학기 (7~8월)
        semester = 30
    elif 8 <= current_month < 12:
        semester = SECOND_SEMESTER

    return semester


# given input week_num returns start, end date of the week that matches week num
def get_dates_of_week(week_num):
    pass