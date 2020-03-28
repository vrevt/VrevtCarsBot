import requests


def get_rate(Abbreviation):
    datas = requests.get('http://www.nbrb.by/API/ExRates/Rates?Periodicity=0').json()

    rate = 0

    for data in datas:
        if data['Cur_Abbreviation'] == Abbreviation:
            rate = data['Cur_OfficialRate']

    return rate
