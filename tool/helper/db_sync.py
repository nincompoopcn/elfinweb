#/usr/bin/python

import re
import json
from bs4 import BeautifulSoup
from requests import get, post, Response, HTTPError

JUPITER_URL = 'http://10.140.161.16:8088/mac/dcm/overview'
QUERY_URL = 'http://10.140.161.16:8088/dcm/fault-modal-modify?faultSid='
OUT_PUT_JSON = 'jupiter_issues.json'
MAINTENENCE_URL = 'http://127.0.0.1:8080/issue/'
LOCAL = True

def dump_jupiter_issues_to_json_file():
    resp = get(JUPITER_URL).text
    soup = BeautifulSoup(resp)
    faultList = soup.select_one('#faultList > tbody')
    issues = faultList.select('button')

    output_List = []
    for issue in issues:
        issue_id = re.search('\((.*)\)', issue['onclick']).group(1)
        issue_info = get(QUERY_URL+str(issue_id)).text
        issue_info = json.loads(issue_info)
        output_List.append(issue_info)

    with open(OUT_PUT_JSON, 'w') as fp:
        json.dump(output_List, fp, indent=4)

    print('dumped %d' % len(issues))

if LOCAL:
    category_map = {
        'EDA': 1,
        'LogImprovement': 2,
        'Monsho': 3,
        'Pronto': 4,
        'Pre-check': 5,
        'RCA': 6,
        'Support': 7,
        'Yokoten': 8,
    }
    release_map = {
        'DNH0.0' : 1,
        'DNH1.0' : 2,
        'DNH2.0' : 3,
        'DNH3.0' : 4,
        'DNH4.0' : 5,
        'DNH5.0' : 6,
        'DNH6.0' : 7,
        'DNH7.0' : 8,
    }
    states_map = {
        'New' : 2,
        'Ongoing' : 1,
        'Blocked' : 3,
        'Transfered' : 4,
        'Closed' : 5,
    }
    group_map = {
        'DLPHY': 1,
        'HW': 2,
        'LOM': 3,
        'UM': 4,
        'LCPLFS': 5,
        'TRS': 6,
        'MAC PS': 7,
        'UPHWAPI': 8,
        'SPEC': 9,
        'L2': 10,
        'ULPHY': 11,
        '3G DL': 12,
        'MCUHWAPI': 13,
        '3G UL': 14,
        'CCSMCU': 15,
        'MW': 16,
        'LSPLFS': 17,
    }
else:
    category_map = {
        "Pronto" : 4,
        'EDA' : 1,
        'LogImprovement' : 2,
        'Monsho' : 3,
        'Pre-check' : 5,
        'RCA' : 6,
        'Support' : 7,
        'Yokoten' : 8,
    }
    release_map = {
        'DNH0.0' : 1,
        'DNH1.0' : 2,
        'DNH2.0' : 3,
        'DNH3.0' : 4,
        'DNH4.0' : 5,
        'DNH5.0' : 6,
        'DNH6.0' : 7,
        'DNH7.0' : 8,
    }
    states_map = {
        'New' : 2,
        'Ongoing' : 1,
        'Blocked' : 3,
        'Transfered' : 4,
        'Closed' : 5,
    }
    group_map = {
        "HW" : 1,
        "ULPHY" : 2,
        "LCPLFS" : 3,
        "3G UL" : 4,
        "UPHWAPI" : 5,
        "UM" : 6,
        "CCSMCU" : 7,
        "3G DL" : 8,
        "MCUHWAPI" : 9,
        "SPEC" : 10,
        "DLPHY" : 11,
        "TRS" : 12,
        "MW" : 13,
        "L2" : 14,
        "MAC PS" : 15,
        "LSPLFS" : 16,
        "LOM" : 17,
    }
def insert_issues_to_maintenence_db():
    with open(OUT_PUT_JSON) as fp:
        issues = json.load(fp)

    for issue in issues:

        data = {
            'category': category_map[issue["category"]] if issue["category"] in category_map else category_map['Support'], # ????
            'pronto': issue["prId"] or '',
            'monsho': issue["monshoId"] or '',
            'title': issue["title"] or 'no_title',
            'person': issue["responsiblePerson"] or 'nobody',
            'release': release_map[issue["prRelease"]] if issue["prRelease"] in release_map else release_map['DNH0.0'],
            'in': issue["inDate"] or '2014-06-06',
            'out': issue["outDate"] or '',
            'state': states_map[issue["state"]] if issue["state"] in states_map else states_map['Closed'],
            'note': issue["notes"] or '',
            'team': group_map[issue["sc"]] if issue["sc"] in group_map else group_map["UPHWAPI"], # ????
            'group': group_map[issue["prGroup"]] if issue["prGroup"] in group_map else group_map["TRS"], # ????
            'area': '',
            'ongoing': issue["openDays"] or 0,
            'blocked': issue["blockedDays"] or 0,
            'rcfound': issue["rcFoundDays"] or 0,
            'knife': issue["knifeNum"] or 0,
            'rft': issue["rft2fcc"] or 0,
            'fcc': 0,
            'closed': 0
        }
        try:
            r = post(MAINTENENCE_URL, data = data)
            r.raise_for_status()
        except HTTPError as e:
            print(r.status_code)
            print(r.text, ...)
            print(e)
            print('- '*20)
            print(data)
            return

def main():
    dump_jupiter_issues_to_json_file()
    insert_issues_to_maintenence_db()


if __name__ == '__main__':
    main()
