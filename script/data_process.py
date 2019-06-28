import codecs
import re

def process(fin,processed_data):
    data_file = codecs.open(fin,encoding= 'utf-8')

    # data_all = np.loadtxt(data_file, skiprows=1)
    # data_file.read(1)

    ser_num = 0

    city_promise = ['华北仓', '西南仓', '华中仓', '华东仓', '东北仓', '华南仓', '西北仓']
    city_name = ['石家庄', '贵阳', '武汉', '东营', '南京', '苏州', '临沂', '沈阳', '宿迁', '重庆',
                 '郑州', '台州', '南通', '宁波', '阳江', '承德', '上海', '呼和浩特', '赣州', '徐州',
                 '杭州', '庆阳', '延吉', '廊坊', '乌兰察布', '泉州', '新乡', '太原', '南昌', '南宁',
                 '巴彦淖尔', '成都', '宜昌', '枣庄', '唐山', '长春', '济南', '青岛', '朔州', '昆明',
                 '广州', '龙岩', '常州', '北京', '镇江', '无锡', '天津', '义乌', '烟台', '宜宾', '潍坊',
                 '长沙', '扬州', '兰州', '东莞', '西安', '濮阳', '嘉兴', '淮南', '绍兴', '常熟', '金华',
                 '洛阳', '柳州', '大连', '福州', '淄博', '佛山', '连云港', '运城', '盐城', '深圳', '南阳',
                 '银川', '通辽', '南充', '忻州', '合肥', '桂林', '阜阳', '保定', '大同', '临汾', '聊城',
                 '信阳', '芜湖', '德阳', '寿光', '日照', '济宁', '商丘', '晋城', '张家口', '温州', '锦州',
                 '荆州', '牡丹江', '邯郸', '六安', '滨州', '抚顺', '安阳', '许昌', '株洲', '珠海', '哈尔滨',
                 '威海', '长治', '湖州', '泰安', '襄阳', '吉林', '茂名', '松原', '宿州', '泰州', '三河',
                 '乌鲁木齐', '沧州', '昆山', '江阴', '惠州', '河源', '厦门', '汕头', '泸州', '北海',
                 '蚌埠', '齐齐哈尔', '常德', '邹城', '平顶山', '达州', '遵义', '岳阳', '阳泉', '随州',
                 '上饶', '大庆', '丹东', '绵阳', '菏泽', '吉安', '中山', '汕尾', '恩施', '秦皇岛', '晋中',
                 '宝鸡', '清远', '盘锦']
    car_type_all = ['三厢车', 'SUV', '两厢车', 'MPV', '跨界轿车', '小型客车', '敞篷车', '跑车', '旅行车',
                    '轿跑车', '跨界SUV', '敞篷跑车', '中型客车', '掀背']
    year = ['不限年限','一年', '两年', '三年', '四年', '五年', '六年', '七年', '八年', '九年', '十年']
    stop_type = ['通风盘', '实心盘', '鼓式']
    stop_type_l = ['手刹', '电子驻车', '脚刹']
    engine = ['自然吸气', '涡轮增压', '机械增压', '双涡轮增压', '混合增压']
    transmission = ['DCT双离合', 'AT自动', 'MT手动', 'CVT无级变速', 'AMT半自动']
    all_wheel_drive = ['前驱', '后驱', '全时四驱', '适时四驱']
    chair = ['真皮', '皮质+织物', '织物', '仿皮']
    color = ['黄色', '白色', '红色', '黑色', '香槟色', '深灰色', '蓝色', '橙色', '多彩色', '棕色', '银灰色', '紫色', '咖啡色', '绿色', '其他']
    data_file.readline()

    while (ser_num < 20000):
        line = data_file.readline()
        info = line.split(',')
        if (info[0] == '\n' ):
            continue
        ser_num += 1

        # # 将汽车品牌转化为对应序号
        # brand = info[12].split(' ')[0]
        # if brand in brand_ser:
        #     brand_num = brand_ser.index(brand)
        # else:
        #     brand_ser.append(brand)
        #     brand_num = brand_ser.index(brand)

        # 获得无单位的行驶里程数
        mileage = eval(info[15][:-1])

        # 获得售后服务类型
        if (info[25] == '30天包退 6个月保修'):
            promise_rule_type = 0
        elif (info[25] == '30天包退 一年保修'):
            promise_rule_type = 1
        else:
            promise_rule_type = -1

        # 获得发货货仓
        if (info[26] in city_promise):
            city_promise_ser = city_promise.index(info[26])
        else:
            city_promise_ser = -1

        # 获得车辆所在地
        if (info[33] in city_name):
            city_name_ser = city_name.index(info[33])
        else:
            city_name_ser = -1

        # 获得车辆注册时间距今月份
        reg_time = info[34].split('-')
        # print(reg_time)
        reg_month = (2019 - int(reg_time[0])) * 12 + (7 - int(reg_time[1]))

        # 获得车身形式
        car_type = info[36].split('-')[-1]
        if car_type in car_type_all:
            car_type_ser = car_type_all.index(car_type)
        else:
            car_type_ser = -1

        # 获得整车质保（年份）
        promise_time = -1
        for i in year:
            if info[41].find(i) != -1:
                promise_time = year.index(i)
                break

        # 获得整车质保（里程）
        if info[41] == '0':
            promise_mile = -1
        elif (info[41].find('不限公里') != -1) or (info[41].find('不限里程') != -1):
            promise_mile = 0
        elif (re.findall(r"\d+\.?\d*",info[41]) != []):
            promise_mile = int(re.findall(r"\d+\.?\d*",info[41])[0])
        else:
            promise_mile = -1

        # 获得制动类型（前后）
        if info[54] in stop_type:
            stop_type_front = stop_type.index(info[54])
        else:
            stop_type_front = -1

        if info[55] in stop_type:
            stop_type_back = stop_type.index(info[54])
        else:
            stop_type_back = -1

        #获得驻车制动类型
        if info[56] in stop_type_l:
            stop_type_lw = stop_type_l.index(info[56])
        else:
            stop_type_lw = -1

        #获得发动机类型
        if info[63] in engine:
            engine_type = engine.index(info[63])
        else:
            engine_type = -1

        #获得燃油类型
        fuel_type = int(info[82][:2])

        #获得变速箱类型
        if info[83] in transmission:
            transmission_type = transmission.index(info[83])
        else:
            transmission_type = -1

        #获得驱动类型
        if info[85] in all_wheel_drive:
            all_wheel_drive_type = all_wheel_drive.index(info[85])
        else:
            all_wheel_drive_type = -1

        #获得座椅材质
        if info[153] in chair:
            chair_type = chair.index(info[153])
        else:
            chair_type = -1

        # 车辆颜色
        if info[-1][:-1] in color:
            color_type = color.index(info[-1][:-1])
        else:
            color_type = -1


        # 各类设施是否齐全，若有则为1，否则为0
        all_kinds_devices = info[95:149] + info[150:153] + info[154:173] + info[175:228] + info[229:242] + info[243:-1]
        for i in range(len(all_kinds_devices)):
            if all_kinds_devices[i] == '0':
                all_kinds_devices[i] = 0
            else:
                all_kinds_devices[i] = 1

        info_train = []
        info_train.append(eval(info[9]))            #汽车品牌
        info_train.append(eval(info[21]))           #新车价格
        info_train.append(eval(info[13]))           #身份认证
        info_train.append(promise_rule_type)        #售后类型
        info_train.append(city_promise_ser)         #发货货舱
        info_train.append(city_name_ser)            #车辆所在地
        info_train.append(mileage)                  #车辆行驶里程数
        info_train.append(reg_month)                #车辆注册时间距今月份
        info_train.append(car_type_ser)             #车身形式
        info_train.append(eval(info[42]))           #车长（mm）
        info_train.append(eval(info[43]))           #车宽（mm）
        info_train.append(eval(info[44]))           #车高（mm）
        info_train.append(eval(info[45]))           #车轴距（mm）
        info_train.append(eval(info[49]))           #车重（kg）
        info_train.append(eval(info[53]))           #油箱容积（L）
        info_train.append(promise_time)             #整车质保（年份）
        info_train.append(promise_mile)             #整车质保（里程）
        info_train.append(stop_type_front)          #制动类型（前）
        info_train.append(stop_type_back)           #制动类型（后）
        info_train.append(stop_type_lw)             #驻车制动类型
        info_train.append(engine_type)              #发动机类型
        info_train.append(eval(info[62]))           #发动机排气量(ml)
        info_train.append(eval(info[74]))           #发动机最大功率（kW）
        info_train.append(fuel_type)                #燃油类型
        info_train.append(eval(info[39]))           #油耗
        info_train.append(transmission_type)        #变速箱类型
        info_train.append(all_wheel_drive_type)     #驱动类型
        info_train.append(chair_type)               #座椅材质
        info_train.append(eval(info[90]))           #最高车速（km/h）
        info_train.append(eval(info[91]))           #官方百公里加速（s）
        info_train.append(color_type)               #车辆颜色
        info_train += all_kinds_devices             #标识各类别设施是否齐全，共255项
        info_train.append(eval(info[16]))           #二手车出价
        
        data_pro.append(info_train)                 #长度为287

if __name__ == '__main__':
    data_pro = []
    process('F:\data.csv',data_pro)
    print(data_pro)
