import requests
from bs4 import BeautifulSoup
cookies = {
    'TESTID': 'set',
    'SESSID': 'M05JUEk3ODM4NTcy',
    'BIGipServer~INB_SSB_Flex~Banner_Self_Service_BANPROD_pool': '336723978.64288.0000',
    '_gcl_au': '1.1.1976295298.1708504805',
    '_tt_enable_cookie': '1',
    '_ttp': 'M8LOJTJwcr-V4u31oIoPweCS_g9',
    '_fbp': 'fb.1.1708504805446.430921143',
    'accessibility': 'false',
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
    'Referer': 'https://aurora.umanitoba.ca/ssb/bwskfcls.p_sel_crse_search',
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
    'p_calling_proc': 'P_CrseSearch',
    'p_term': '202390',
}

response = requests.post('https://aurora.umanitoba.ca/ssb/bwckgens.p_proc_term_date', cookies=cookies, headers=headers, data=data)

soup = BeautifulSoup(response.text, 'html.parser')
