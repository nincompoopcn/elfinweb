import json
from datetime import datetime, date

# common function
def get_date():
    today = date.today()
    return today

def json_default(obj):  
    if isinstance(obj, datetime):  
        return obj.strftime('%Y-%m-%d %H:%M:%S')  
    elif isinstance(obj, date):  
        return obj.strftime("%Y-%m-%d")

def get_json(obj):
    json_str = json.dumps(obj, ensure_ascii=False, default=json_default);
    return json_str

def get_dict(json_str):
    dict_obj = json.loads(json_str);
    return dict_obj

# template function
def get_date_delta(date_a, date_b):
    delta = (date_a - date_b).days
    return delta

def get_team_member(json_str, day=None):
    if not json_str:
        return 0

    if day == None:
        day = get_date()
    delta = day.isocalendar()
    year = str(delta[0])
    week = str(delta[1])

    year_dict = get_dict(json_str)

    years = sorted(year_dict.items(), key=lambda k:k[0], reverse=True)
    for y, l in years:
        if int(y) == int(year):
            weeks = sorted(l.items(), key=lambda k:k[0], reverse=True)
            for w, n in weeks:
                if int(w) <= int(week):
                    return n
        elif int(y) < int(year):
            weeks = sorted(l.items(), key=lambda k:k[0], reverse=True)
            for w, n in weeks:
                return n

    return 0

