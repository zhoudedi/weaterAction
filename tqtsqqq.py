#!/usr/bin/python3
#coding=utf-8

import requests, json
import os

SCKEY=os.environ.get('SCKEY') ##Server酱推送KEY
SKey=os.environ.get('SKEY') #CoolPush酷推KEY
def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()  #返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = '【奇怪的知识】\n' + english + '\n' + zh_CN
    return str

def ServerPush(info): #Server酱推送
    api = "https://sctapi.ftqq.com/{}.send".format(SCKEY)
    title = u"天气推送"
    content = info.replace('\n','\n\n')
    data = {
        "text": title,
        "desp": content
    }
    print(content)
    requests.post(api, data=data)
def CoolPush(info): #CoolPush酷推
    # cpurl = 'https://push.xuthus.cc/group/'+spkey   #推送到QQ群
    # cpurl = 'https://push.xuthus.cc/send/' + SKey  # 推送到个人QQ
    api2='https://push.xuthus.cc/pgroup/{}'.format(SKey)
    #api='https://push.xuthus.cc/psend/{}'.format(SKey)
    #print(api)
    print(api2)
    print(info)
    requests.post(api2, info.encode('utf-8'))
    #requests.post(api, info.encode('utf-8'))
def main():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'             #API地址，必须配合城市代码使用
        city_code = '101280603'   #进入https://where.heweather.com/index.html查询你的城市代码
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()         #将数据以json形式返回，这个d就是返回的json数据
        if(d['status'] == 200):     #当返回状态码为200，输出天气状况
            parent = d["cityInfo"]["parent"] #省
            city = d["cityInfo"]["city"] #市
            update_time = d["time"] #更新时间
            date = d["data"]["forecast"][0]["ymd"] #日期
            week = d["data"]["forecast"][0]["week"] #星期
            weather_type = d["data"]["forecast"][0]["type"] # 天气
            wendu_high = d["data"]["forecast"][0]["high"] #最高温度
            wendu_low = d["data"]["forecast"][0]["low"] #最低温度
            shidu = d["data"]["shidu"] #湿度
            pm25 = str(d["data"]["pm25"]) #PM2.5
            pm10 = str(d["data"]["pm10"]) #PM10
            quality = d["data"]["quality"] #天气质量
            fx = d["data"]["forecast"][0]["fx"] #风向
            fl = d["data"]["forecast"][0]["fl"] #风力
            ganmao = d["data"]["ganmao"] #感冒指数
            tips = d["data"]["forecast"][0]["notice"] #温馨提示
            # 天气提示内容
            tdwt = "【今日❤️天气】\n城市： " + parent + city + \
                   "\n日期： " + date + "爱你鑫鑫😘"+\n星期: " + week + "\n天气: " + weather_type + "\n温度: " + wendu_high + " / "+ wendu_low + "\n湿度: " + \
                    shidu + "\nPM25: " + pm25 + "\nPM10: " + pm10 + "\n空气质量: " + quality + \
                   "\n风力风向: " + fx + fl + "\n感冒指数: "  + ganmao + "\n温馨提示： " + tips + "\n更新时间: " + update_time + "\n✁-----------------------------------------\n" + get_iciba_everyday()
            # print(tdwt)
            # requests.post(cpurl,tdwt.encode('utf-8'))         #把天气数据转换成UTF-8格式，不然要报错。
            # ServerPush(tdwt)
            CoolPush(tdwt)
    except Exception:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
        print(error)
        print(Exception)

if __name__ == '__main__':
    main()
