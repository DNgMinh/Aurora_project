import requests
from bs4 import BeautifulSoup

def schedule_retrieve(term, course_list):
    schedule_list = []
    # id = input("Enter id:")
    # pin = input("Enter pin:")
    id = "008005501"
    pin = "Cei@072023"
    sessid = login(id, pin)
    for course in course_list:
        subj, crse = list(course.items())[0]
        cookies = {
            'TESTID': 'set',
            'SESSID': sessid,
            'BIGipServer~INB_SSB_Flex~Banner_Self_Service_BANPROD_pool': '336723978.64288.0000',
            '_gcl_au': '1.1.1976295298.1708504805',
            '_tt_enable_cookie': '1',
            '_ttp': 'M8LOJTJwcr-V4u31oIoPweCS_g9',
            '_fbp': 'fb.1.1708504805446.430921143',
            'accessibility': 'false',
            '_gid': 'GA1.2.1525560649.1708677043',
            'TS01c6c21c': '010e8404412caae9eed6af3ae840c1b3ca974cd44ef167ec5ea43689175a83b23a2f4c88e8930d02daabe7b9a56e969489fee24649',
            'jcoPageCount': '21',
            '_ga': 'GA1.2.1269208878.1708504805',
            '_ga_5KL2MD48DQ': 'GS1.1.1708713725.3.1.1708713895.60.0.0',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://aurora.umanitoba.ca',
            'Referer': 'https://aurora.umanitoba.ca/ssb/bwskfcls.P_GetCrse',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        data = {
            'term_in': term,
            'sel_subj': [
                'dummy',
                subj,
            ],
            'SEL_CRSE': crse,
            'SEL_TITLE': '',
            'BEGIN_HH': '0',
            'BEGIN_MI': '0',
            'BEGIN_AP': 'a',
            'SEL_DAY': 'dummy',
            'SEL_PTRM': 'dummy',
            'END_HH': '0',
            'END_MI': '0',
            'END_AP': 'a',
            'SEL_CAMP': 'dummy',
            'SEL_SCHD': 'dummy',
            'SEL_SESS': 'dummy',
            'SEL_INSTR': [
                'dummy',
                '%',
            ],
            'SEL_ATTR': [
                'dummy',
                '%',
            ],
            'SEL_LEVL': [
                'dummy',
                '%',
            ],
            'SEL_INSM': 'dummy',
            'sel_dunt_code': '',
            'sel_dunt_unit': '',
            'call_value_in': '',
            'rsts': 'dummy',
            'crn': 'dummy',
            'path': '1',
            'SUB_BTN': 'View Sections',
        }
        s6 = requests.Session()
        response6 = s6.post('https://aurora.umanitoba.ca/ssb/bwskfcls.P_GetCrse', cookies=cookies, headers=headers, data=data)
        #print(response6.text)
        sessid = response6.cookies.get('SESSID')
        scheduleA = {} 
        scheduleB = {}
        soup = BeautifulSoup(response6.text, 'html.parser')
        table = soup.find(class_='datadisplaytable', recursive=True)
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td', recursive=False)
            if len(columns) >= 10:
                course = columns[2].text + columns[3].text + columns[4].text
                day = columns[8].text
                time = columns[9].text
                if columns[4].text[0] == 'A':
                    scheduleA[course] = [time, day]
                elif columns[4].text[0] == 'B':
                    scheduleB[course] = [time, day]

        if len(scheduleA) != 0:
            schedule_list.append(scheduleA)
        if len(scheduleB) != 0:
            schedule_list.append(scheduleB)
    return schedule_list

def login(id, pin):
    cookies = {
        'TESTID': 'set',
        'BIGipServer~INB_SSB_Flex~Banner_Self_Service_BANPROD_pool': '336723978.64288.0000',
        '_gcl_au': '1.1.1976295298.1708504805',
        '_tt_enable_cookie': '1',
        '_ttp': 'M8LOJTJwcr-V4u31oIoPweCS_g9',
        '_fbp': 'fb.1.1708504805446.430921143',
        'accessibility': 'false',
        'TS01c6c21c': '010e840441326cab8ab4473cb05907b9c0dee7fa50f31afdc15e8681820abb4874da67c8d79fb2a6bcfcfb5a5faad1a464e07b5cce',
        '_gid': 'GA1.2.1525560649.1708677043',
        'jcoPageCount': '20',
        '_ga': 'GA1.1.1269208878.1708504805',
        '_ga_5KL2MD48DQ': 'GS1.1.1708677042.2.1.1708677161.5.0.0',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://aurora.umanitoba.ca',
        'Referer': 'https://aurora.umanitoba.ca/ssb/twbkwbis.P_WWWLogin',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'sid': id,
        'PIN': pin,
    }
    s = requests.Session() 
    response = s.post('https://aurora.umanitoba.ca/ssb/twbkwbis.P_ValLogin', cookies=cookies, headers=headers, data=data)
    sessid = response.cookies.get('SESSID') 
    return sessid
    
# list = schedule_retrieve('202410', [{'COMP' : '1020'}, {'MATH' : '1240'}])
# print(list)