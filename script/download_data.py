import requests
from bs4 import BeautifulSoup
from script.cities import cityObjs
from script.port import Ports,L
import random
import time
import csv
import pandas as pd
import numpy as np
import os
import re
import json
import sys

headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:67.0) Gecko/20100101 Firefox/67.0',
}

def getProxy(counter):
    port = str(Ports[counter%L])
    print(port)
    proxy='www.scumall.com:'+port
    proxies={
        'http':'http://'+proxy,
        'https':'https://'+proxy
    }
    return proxies

brandUrls = ['www.xin.com/alashanmeng/aodi/', 'www.xin.com/alashanmeng/aerfaluomiou/', 'www.xin.com/alashanmeng/anchi/', 'www.xin.com/alashanmeng/asidunmading/', 'www.xin.com/alashanmeng/alpina/', 'www.xin.com/alashanmeng/acschnitzer/', 'www.xin.com/alashanmeng/ankai/', 'www.xin.com/alashanmeng/bentian/', 'www.xin.com/alashanmeng/benchi/', 'www.xin.com/alashanmeng/bieke/', 'www.xin.com/alashanmeng/baoma/', 'www.xin.com/alashanmeng/baojun/', 'www.xin.com/alashanmeng/biaozhi/', 'www.xin.com/alashanmeng/biyadi/', 'www.xin.com/alashanmeng/baoshijie/', 'www.xin.com/alashanmeng/benteng/', 'www.xin.com/alashanmeng/beiqishenbao/', 'www.xin.com/alashanmeng/beijingqiche/', 'www.xin.com/alashanmeng/beiqihuansu/', 'www.xin.com/alashanmeng/beiqiweiwang/', 'www.xin.com/alashanmeng/bisuqiche/', 'www.xin.com/alashanmeng/baowo/', 'www.xin.com/alashanmeng/beiqizhizao/', 'www.xin.com/alashanmeng/babosi/', 'www.xin.com/alashanmeng/binli/', 'www.xin.com/alashanmeng/beiqixinnenyuan/', 'www.xin.com/alashanmeng/baolong/', 'www.xin.com/alashanmeng/beiqidaoda/', 'www.xin.com/alashanmeng/baoqiqiche/', 'www.xin.com/alashanmeng/bujiadi/', 'www.xin.com/alashanmeng/changan/', 'www.xin.com/alashanmeng/changcheng/', 'www.xin.com/alashanmeng/changanoushang/', 'www.xin.com/alashanmeng/changhe/', 'www.xin.com/alashanmeng/changanqingxingche/', 'www.xin.com/alashanmeng/chenggong/', 'www.xin.com/alashanmeng/dazhong/', 'www.xin.com/alashanmeng/dongfengfengxing/', 'www.xin.com/alashanmeng/dongnan/', 'www.xin.com/alashanmeng/dongfengfengshen/', 'www.xin.com/alashanmeng/dongfengfengguang/', 'www.xin.com/alashanmeng/daoqi/', 'www.xin.com/alashanmeng/ds/', 'www.xin.com/alashanmeng/dongfeng/', 'www.xin.com/alashanmeng/dongfengxiaokang/', 'www.xin.com/alashanmeng/dongfengfengdu/', 'www.xin.com/alashanmeng/dadi/', 'www.xin.com/alashanmeng/duoshixing/', 'www.xin.com/alashanmeng/dayu/', 'www.xin.com/alashanmeng/dianka/', 'www.xin.com/alashanmeng/dongfengruitaite/', 'www.xin.com/alashanmeng/dachengqiche/', 'www.xin.com/alashanmeng/dafa/', 'www.xin.com/alashanmeng/fengtian/', 'www.xin.com/alashanmeng/fute/', 'www.xin.com/alashanmeng/feiyate/', 'www.xin.com/alashanmeng/futian/', 'www.xin.com/alashanmeng/futianchengyongche/', 'www.xin.com/alashanmeng/fudi/', 'www.xin.com/alashanmeng/falali/', 'www.xin.com/alashanmeng/fuqiqiteng/', 'www.xin.com/alashanmeng/fisker/', 'www.xin.com/alashanmeng/guangqichuanqi/', 'www.xin.com/alashanmeng/guanzhi/', 'www.xin.com/alashanmeng/guangqijiao/', 'www.xin.com/alashanmeng/gmc/', 'www.xin.com/alashanmeng/guangqijituan/', 'www.xin.com/alashanmeng/guanggang/', 'www.xin.com/alashanmeng/guojinqiche/', 'www.xin.com/alashanmeng/guangqixinnenyuan/', 'www.xin.com/alashanmeng/hafu/', 'www.xin.com/alashanmeng/haima/', 'www.xin.com/alashanmeng/hongqi/', 'www.xin.com/alashanmeng/huatai/', 'www.xin.com/alashanmeng/hanteng/', 'www.xin.com/alashanmeng/huasong/', 'www.xin.com/alashanmeng/huanghai/', 'www.xin.com/alashanmeng/hafei/', 'www.xin.com/alashanmeng/hanma/', 'www.xin.com/alashanmeng/huataixinnenyuan/', 'www.xin.com/alashanmeng/huaqi/', 'www.xin.com/alashanmeng/heibao/', 'www.xin.com/alashanmeng/hongxingqiche/', 'www.xin.com/alashanmeng/huaxiang/', 'www.xin.com/alashanmeng/huabei/', 'www.xin.com/alashanmeng/huizhong/', 'www.xin.com/alashanmeng/huapu/', 'www.xin.com/alashanmeng/huayang/', 'www.xin.com/alashanmeng/hengtian/', 'www.xin.com/alashanmeng/hangtian/', 'www.xin.com/alashanmeng/haige/', 'www.xin.com/alashanmeng/huakai/', 'www.xin.com/alashanmeng/jiliqiche/', 'www.xin.com/alashanmeng/jeep/', 'www.xin.com/alashanmeng/jianghuai/', 'www.xin.com/alashanmeng/jiebao/', 'www.xin.com/alashanmeng/jinbei/', 'www.xin.com/alashanmeng/jiangling/', 'www.xin.com/alashanmeng/jinlong/', 'www.xin.com/alashanmeng/junmaqiche/', 'www.xin.com/alashanmeng/jietu/', 'www.xin.com/alashanmeng/jinlv/', 'www.xin.com/alashanmeng/jianglingjituanqingqi/', 'www.xin.com/alashanmeng/jiulong/', 'www.xin.com/alashanmeng/jiangnan/', 'www.xin.com/alashanmeng/jianglingjituanxinnenyuan/', 'www.xin.com/alashanmeng/jinchengqiche/', 'www.xin.com/alashanmeng/juntianqiche/', 'www.xin.com/alashanmeng/kaidilake/', 'www.xin.com/alashanmeng/kaiyi/', 'www.xin.com/alashanmeng/kairui/', 'www.xin.com/alashanmeng/kelaisile/', 'www.xin.com/alashanmeng/kasheng/', 'www.xin.com/alashanmeng/kenisaike/', 'www.xin.com/alashanmeng/kaersen/', 'www.xin.com/alashanmeng/kaibaihe/', 'www.xin.com/alashanmeng/ktm/', 'www.xin.com/alashanmeng/kawei/', 'www.xin.com/alashanmeng/kaimaqiche/', 'www.xin.com/alashanmeng/kangdiquanqiuying/', 'www.xin.com/alashanmeng/nazhijie/', 'www.xin.com/alashanmeng/nanjunqiche/', 'www.xin.com/alashanmeng/nazhaqiche/', 'www.xin.com/alashanmeng/nanqi/', 'www.xin.com/alashanmeng/nanjingjinlong/', 'www.xin.com/alashanmeng/ouge/', 'www.xin.com/alashanmeng/oubao/', 'www.xin.com/alashanmeng/oushangqiche/', 'www.xin.com/alashanmeng/oula/', 'www.xin.com/alashanmeng/polestarjixing/', 'www.xin.com/alashanmeng/pajiani/', 'www.xin.com/alashanmeng/qiya/', 'www.xin.com/alashanmeng/qirui/', 'www.xin.com/alashanmeng/qichen/', 'www.xin.com/alashanmeng/qiantu/', 'www.xin.com/alashanmeng/qingnianqiche/', 'www.xin.com/alashanmeng/qiaozhibadun/', 'www.xin.com/alashanmeng/richan/', 'www.xin.com/alashanmeng/rongwei/', 'www.xin.com/alashanmeng/ruiqi/', 'www.xin.com/alashanmeng/ruichixinnenyuan/', 'www.xin.com/alashanmeng/rongdazhizao/', 'www.xin.com/alashanmeng/ruhu/', 'www.xin.com/alashanmeng/sikeda/', 'www.xin.com/alashanmeng/smart/', 'www.xin.com/alashanmeng/sanling/', 'www.xin.com/alashanmeng/sibalu/', 'www.xin.com/alashanmeng/shangqidatong/', 'www.xin.com/alashanmeng/siming/', 'www.xin.com/alashanmeng/siweiqiche/', 'www.xin.com/alashanmeng/shuanglong/', 'www.xin.com/alashanmeng/shuanghuan/', 'www.xin.com/alashanmeng/sailin/', 'www.xin.com/alashanmeng/sidataike/', 'www.xin.com/alashanmeng/shanqitongjia/', 'www.xin.com/alashanmeng/sitech/', 'www.xin.com/alashanmeng/saibao/', 'www.xin.com/alashanmeng/shijue/', 'www.xin.com/alashanmeng/sabo/', 'www.xin.com/alashanmeng/shuixing/', 'www.xin.com/alashanmeng/spirra/', 'www.xin.com/alashanmeng/tesila/', 'www.xin.com/alashanmeng/taikate/', 'www.xin.com/alashanmeng/tianma/', 'www.xin.com/alashanmeng/tongbao/', 'www.xin.com/alashanmeng/tangjunqiche/', 'www.xin.com/alashanmeng/tianjiqiche/', 'www.xin.com/alashanmeng/tongtian/', 'www.xin.com/alashanmeng/tengshi/', 'www.xin.com/alashanmeng/wuling/', 'www.xin.com/alashanmeng/woerwo/', 'www.xin.com/alashanmeng/wey/', 'www.xin.com/alashanmeng/weichaiyingzhi/', 'www.xin.com/alashanmeng/wushiling/', 'www.xin.com/alashanmeng/weilin/', 'www.xin.com/alashanmeng/weilai/', 'www.xin.com/alashanmeng/weimaqiche/', 'www.xin.com/alashanmeng/weiziman/', 'www.xin.com/alashanmeng/wanfeng/', 'www.xin.com/alashanmeng/xiandai/', 'www.xin.com/alashanmeng/xuefulan/', 'www.xin.com/alashanmeng/xuetielong/', 'www.xin.com/alashanmeng/xiyate/', 'www.xin.com/alashanmeng/xinkai/', 'www.xin.com/alashanmeng/xiaopengqiche/', 'www.xin.com/alashanmeng/xinyuan/', 'www.xin.com/alashanmeng/xingtu/', 'www.xin.com/alashanmeng/xindadi/', 'www.xin.com/alashanmeng/yingfeinidi/', 'www.xin.com/alashanmeng/yiqi/', 'www.xin.com/alashanmeng/yusheng/', 'www.xin.com/alashanmeng/yiweike/', 'www.xin.com/alashanmeng/yemaqiche/', 'www.xin.com/alashanmeng/yongyuan/', 'www.xin.com/alashanmeng/yundu/', 'www.xin.com/alashanmeng/yujie/', 'www.xin.com/alashanmeng/yunbao/', 'www.xin.com/alashanmeng/yulu/', 'www.xin.com/alashanmeng/yutongkeche/', 'www.xin.com/alashanmeng/yaxing/', 'www.xin.com/alashanmeng/yunque/', 'www.xin.com/alashanmeng/zhongtai/', 'www.xin.com/alashanmeng/zhonghua/', 'www.xin.com/alashanmeng/zhongxing/', 'www.xin.com/alashanmeng/zhongyu/', 'www.xin.com/alashanmeng/zhinuo/', 'www.xin.com/alashanmeng/zhongshun/', 'www.xin.com/alashanmeng/zhongou/', 'www.xin.com/alashanmeng/zhidou/']

class car:
    def __init__(self):
        self._id = 0
        pass

    @property
    def id(self):
        """Unique id."""
        return self._id

class Data:
    def __init__(self):
        self._DataDic = {}
        self._currCarID = ""
        self._counter = 20

    @property
    def DataDic(self):
        return self._DataDic

    @property
    def currCarID(self):
        return self._currCarID

    def download_one_page(self,target):
        # '''
        # Aim to get url for each brand,
        # and get the cars url of each brand
        # '''
        # req = requests.get(url=target,proxies=proxies)
        # # print(req.text)
        # soup = BeautifulSoup(req.text,"lxml")
        # # soup = BeautifulSoup(req.text)
        # brandUrls = []
        #
        # '''
        # Find the tag for brand which contain five layers until url.
        # Traversal across the tag to get url for each brand.
        # The URLs of brands store in brandUrls.
        # like: www.xin.com/shanghai/dazhong/
        # '''
        # spell = ['A','B','C','D','E','F','G','H','I','J','K','L'\
        #          'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        # const = "li_spell li_spell_"
        # # list = []
        # # for chr in spell:
        # #     className = const + chr
        # #     LIs = soup.find_all('li', className)
        # #     if len(LIs) > 0: list.append(chr)
        # list = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z']
        # for chr in list:
        #     className = const + chr
        #     LIs = soup.find_all('li',className)[0].contents
        #     for li in LIs:
        #         if li == '\n': continue
        #         DDs = li.contents
        #         for dd in DDs:
        #             if dd == '\n': continue
        #             a = dd
        #             href = a.contents[1].get('href')
        #             url = href.split('/', 2)[2]
        #             brandUrls.append(url)
        # print(brandUrls)

        '''
        Get urls of cars for each brand.
        '''
        carUrls = {}
        brand_num = 0  # Used to back to last brand from error
        for brandurl in brandUrls:
            '''
            Get all the car-item urls over multi-pages
            '''
            brandname = brandurl.split('/')[len(brandurl.split('/'))-2]
            carUrls[brandname] = []
            print("Current brand is: ", brandname)
            print("Brand number is: ", brand_num)
            # if (brand_num < 20) : continue
            pageNum = 1
            while True:
                # brandurl = brandurl + "i38/" # Used to back to last page from error
                print("http://" + brandurl)
                self._counter += 5
                req = requests.get(url="http://" + brandurl,proxies=getProxy(self._counter))
                self._counter+=1
                # print(req.text)
                # soup = BeautifulSoup(req.text)
                soup = BeautifulSoup(req.text, "lxml")
                LIs = soup.find_all('li','con caritem conHeight')
                for li in LIs:
                    href = li.find('a','aimg').get('href')
                    url = href.split('/', 2)[2]
                    carUrls[brandname].append(url)
                    self._currCarID = url.split('/')[2].split('.')[0]
                    self._DataDic[self._currCarID] = {}
                    try:
                        self.download_one_car(url)
                    except :
                        print(self._currCarID," failed")
                        self._counter += 1
                    print("Finish loading car whose id is: ",self._currCarID)
                '''
                turn to next page
                '''
                pageNum += 1
                pages = soup.find_all('div',"con-page search_page_link")[0]
                pageItems = pages.contents
                if (pageItems[len(pageItems)-2].text=='下一页'):
                    print(pageItems[len(pageItems)-2])
                    brandurl = "www.xin.com" + \
                               pageItems[len(pageItems)-2].get('href')
                    print("Start to crawl page ",pageNum)
                else: break
            brand_num += 1
            if (brand_num % 5 == 0):
                with open("segment.json", "a") as f:
                    json.dump(self.DataDic, f, indent=4)
                    print("finish saving json...")

    def download_one_car(self, target):
        # target = "https://www.xin.com/yrek41mkmg/che38489791.html?cityid=2401"
        print("start: ","http://"+target)
        req = requests.get(url="http://"+target,proxies=getProxy(self._counter))
        self._counter+=1
        # print(req.text)
        # soup = BeautifulSoup(req.text)
        soup = BeautifulSoup(req.text, "lxml")

        '''
        Get basic information
        1. keyword: like '大众 速腾 2014款 1.4T 自动 豪华型 改款'
        2. price_1: discount price, like '8.21'
        3. price_2: original price, like '8.76'
        4. time: like '4年8个月'
        5. odograph: like '4.1万公里'
        6. emission: like '国4'
        7. VUP: Vehicle usage property, like '非营运'
        8. MOT: every years' check, like '2020-10-01'
        9. insurance: like '2019-10-31'
        10. manufacturer: like '一汽-大众'<-this is in Shenzheng
        11. size: like '紧凑型'
        12. color: like '白色'
        13. structure: like '轿车-三厢车'
        14. weight(整备质量): like '1380  kg '
        15. length(轴距): like '2651  mm'
        16. engine: like 'EA111'
        17. transmission: like 'DCT双离合'
        18. displacement: like '1390 mL'
        19. fuel: fuel type, like '汽油'
        20. drive: like '前驱'
        21. consumption: like '6.4 L/100km'
        22. service: like '优信金牌认证'
        '''
        line = soup.find_all('div',"cd_m_h cd_m_h_zjf")[0].find('span').\
            contents[0].split('\n')[1]
        for i in range(len(line)):
            if line[i] != " ":
                n = i
                break
        keyword = line[n:]
        # Also change '原价8.76万' into 8.76, change '￥8.21万' into 8.21
        price_1 = soup.find_all('span',"cd_m_info_jg")[0].find('b').text[1:-1]
        price_2 = soup.find_all('b',"new-noline")[0].contents[0][2:-1]
        # TODO: change '4年8个月' into xxxx, change 4.1万公里 into xxx, change '国4' into xx
        info = soup.find_all('li', "cd_m_desc_li cd_m_desc_line")
        time = info[0].contents[1].next
        odograph = info[1].contents[1].next.split('\n')[1].split(' ')[\
            len(info[1].contents[1].next.split('\n')[1].split(' '))-1]
        emission = info[2].contents[1].next

        tit = soup.find_all('span',"cd_m_i_pz_tit")
        val = soup.find_all('span',"cd_m_i_pz_val")
        VUP = val[2].next # Vehicle usage property
        MOT = val[3].next # nian jian
        insurance = val[4].next # baoxian
        # 生产厂商（例如一汽大众（深圳）、上汽（上海）。。。）
        manufacturer = val[6].contents[1].contents[0].split('\n')[1].split(' ')[\
            len(val[6].contents[1].contents[0].split('\n')[1].split(' '))-1]
        # 车辆级别（例如紧凑型）
        size = val[7].contents[1].contents[0].split('\n')[1].split(' ')[ \
            len(val[7].contents[1].contents[0].split('\n')[1].split(' '))-1]
        # 车辆颜色（例如白色）
        color = val[8].contents[1].contents[0].split('\n')[1].split(' ')[ \
            len(val[8].contents[1].contents[0].split('\n')[1].split(' '))-1]
        # 车身结构（例如4门 5座 轿车-三厢车）
        structure = val[9].contents[1].contents[0].split('\n')[1].split(' ')[ \
            len(val[9].contents[1].contents[0].split('\n')[1].split(' '))-1]
        # 整备质量 （如'1380  kg '）
        weight = val[10].contents[0]
        # 轴距（如'2651  mm')
        length = val[11].contents[0]
        # 发动机(如'EA111'）
        engine = val[12].contents[0]
        # 变速器(如'DCT双离合')
        transmission = val[13].contents[1].contents[0].split('\n')[1].split(' ')[ \
            len(val[13].contents[1].contents[0].split('\n')[1].split(' '))-1]
        # 排量（如'1390 mL'）
        text = val[14].contents[1].contents[0].split('\n')[1]
        s = 0
        for i in range(len(text) - 1):
            if (text[i] == " ") and (text[i + 1] != " "):
                if not (s): s = i + 1
            if (text[i] != " ") and (text[i + 1] == " "):
                e = i+1
        Displacement = text[s:e]
        # 燃油类型(如"汽油"）
        fuel = val[15].contents[0]
        # 驱动方式(如"前驱")
        drive = val[16].contents[0]
        # 综合油耗(如"6.4 L/100km")
        consumption = val[17].contents[0]
        # service rank, like '优信金牌认证'
        service = soup.find_all('div',"cd_m_i cd_m_yxrz")[0]
        service_rank = service.text.split('\n',7)[\
            len(service.text.split('\n',7))-2]

        '''
        Get more details.
        130 details which are in the format like:
            keys: each key like '款代'
            vals: each value like '第6代'
        Note: val = '●' means no such information
        '''
        key = soup.find_all('span', "cd_m_pop_pzcs_key")
        val = soup.find_all('span', "cd_m_pop_pzcs_val")
        keys = []
        vals = []
        for i in key:
            text = i.text
            text = text.split('\n')[len(text.split('\n')) - 2]
            for j in range(len(text) - 1, 0, -1):
                if (text[j - 1] == " ") and (text[j] != " "):
                    keys.append(text[j:])
                    break
        for i in val:
            text = i.text
            text = text.split('\n')[len(text.split('\n')) - 2]
            for j in range(len(text) - 1, 0, -1):
                if (text[j - 1] == " ") and (text[j] != " "):
                    vals.append(text[j:])
                    break

        '''
        Get report information.
        several defects pointed out by report
            items: each item like '前保险杠'
            infos: each info like '曾经喷漆'
        '''
        item = soup.find_all('span', "p-flaw-list-text")
        info = soup.find_all('span', "text-pannel")
        items = []
        infos = []
        for i in item:
            items.append(i.next)
        for i in info:
            text = i.text
            text = text.split('\n')[len(text.split('\n')) - 2]
            for j in range(len(text)-1,0,-1):
                if (text[j-1]==" ") and (text[j]!=" "):
                    infos.append(text[j:])
                    break

        '''
        Write items into datadic
        '''
        self._DataDic[self._currCarID]["BasicInfo"] = {}
        self._DataDic[self._currCarID]["BasicInfo"]["keyword"] = keyword
        self._DataDic[self._currCarID]["BasicInfo"]["price_1"] = price_1
        self._DataDic[self._currCarID]["BasicInfo"]["price_2"] = price_2
        self._DataDic[self._currCarID]["BasicInfo"]["time"] = time
        self._DataDic[self._currCarID]["BasicInfo"]["odograph"] = odograph
        self._DataDic[self._currCarID]["BasicInfo"]["emission"] = emission
        self._DataDic[self._currCarID]["BasicInfo"]["VUP"] = VUP
        self._DataDic[self._currCarID]["BasicInfo"]["MOT"] = MOT
        self._DataDic[self._currCarID]["BasicInfo"]["insurance"] = insurance
        self._DataDic[self._currCarID]["BasicInfo"]["manufacturer"] = manufacturer
        self._DataDic[self._currCarID]["BasicInfo"]["size"] = size
        self._DataDic[self._currCarID]["BasicInfo"]["color"] = color
        self._DataDic[self._currCarID]["BasicInfo"]["structure"] = structure
        self._DataDic[self._currCarID]["BasicInfo"]["weight"] = weight
        self._DataDic[self._currCarID]["BasicInfo"]["length"] = length
        self._DataDic[self._currCarID]["BasicInfo"]["engine"] = engine
        self._DataDic[self._currCarID]["BasicInfo"]["transmission"] = transmission
        self._DataDic[self._currCarID]["BasicInfo"]["Displacement"] = Displacement
        self._DataDic[self._currCarID]["BasicInfo"]["fuel"] = fuel
        self._DataDic[self._currCarID]["BasicInfo"]["drive"] = drive
        self._DataDic[self._currCarID]["BasicInfo"]["consumption"] = consumption
        self._DataDic[self._currCarID]["BasicInfo"]["service_rank"] = service_rank

        self._DataDic[self._currCarID]["Details"] = {}
        for i in range(len(keys)):
            self._DataDic[self._currCarID]["Details"][keys[i]] = vals[i]

        self._DataDic[self._currCarID]["Report"] = {}
        for i in range(len(items)):
            self._DataDic[self._currCarID]["Report"][items[i]] = infos[i]


if __name__ == '__main__':
    XinData = Data()
    '''
    Get city list
    '''
    cityList = []
    for obj in cityObjs:
        cityList.append(obj["short"].lower())

    '''
    Download data from different cities.
    '''
    startPage = 'https://www.xin.com/shanghai/dazhong/'
    for city in cityList:
        # print(city)
        # try:
        page = 'https://www.xin.com/'+city+'/dazhong/'
        XinData.download_one_page(page)
            # time.sleep(random.randint(10, 15))
        # except: pass

    with open("report.json", "w") as f:
        json.dump(XinData.DataDic, f, indent=4)
        print("Finish saving json...")



