import demjson
import pymysql
import requests
import execjs
import csv
import json


def get_cityCode():
    url = 'https://js.51jobcdn.com/in/js/2016/layer/area_array_c.js?20210425'
    req = requests.get(url)
    req.encoding = 'GBK'
    ctx = execjs.compile(
        req.text +
        '''
        function get_area() {
            return area
        }
        '''
    )
    area = ctx.call('get_area')
    area = {value: key for key, value in area.items()}
    return area


def get_cityList():
    cityList = []
    with open("../data/BaiduMap_cityCenter.txt", 'r', encoding='utf-8') as f:
        data = f.read()
        data = demjson.decode(data)
        cityList.extend(data["municipalities"])
        cityList.extend(data["other"])
        for province in data['provinces']:
            cityList.extend(province['cities'])
    return cityList


def merge_toFile(cityList, cityCode):
    get_cityCode = lambda x: cityCode[x]
    getLonAndLat = lambda x: x["g"].split("|")[0].split(",")
    getValue = lambda x : [x["n"], getLonAndLat(x)[0], getLonAndLat(x)[1], get_cityCode(x["n"])]
    data = []
    for i in cityList:
        data.append(getValue(i))
    with open('../data/cityInfo.csv', 'w',newline='') as f:
        head = ['city', 'longitude', 'latitude', 'code']
        f_csv = csv.writer(f)
        f_csv.writerow(head)
        f_csv.writerows(data)
def to_js(cityList):
    getLonAndLat = lambda x: x["g"].split("|")[0].split(",")
    getValue = lambda x : {x["n"]: [float(getLonAndLat(x)[0]), float(getLonAndLat(x)[1])]}
    data = {}
    for i in cityList:
        data.update(getValue(i))
    open('../data/cityInfo.js','w',encoding='utf-8').write('window.cityInfo = '+str(data))


if __name__ == '__main__':
    # cityCode = get_cityCode()
    cityList = get_cityList()
    # merge_toFile(cityList, cityCode)
    to_js(cityList)
