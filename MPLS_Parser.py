#-*- coding: UTF-8 -*-

'MPLS Data Parser'

__author__ = 'persephonearthur'

# ------------------------------

import os
import re
import xlwt
import urllib2
import fileinput
from time import clock
from sgmllib import SGMLParser

# ---------- Config Begin ----------

LIMIT = 70
dirpath = 'C:/Users/Administrator/Desktop/2016 Mar/'

# ---------- Config End ----------

start = clock()

website = []
filepath = 'file:///' + dirpath

for element in os.walk(dirpath):
	pass

for item in element[2]:
	website.append(os.path.join(filepath + item))

store = [] # 38 of 0 - 1784
time = [] # 76 - 1780
input = [] # 77 - 1781
output = [] # 79 - 1783

class MPLS_Parser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_td = ""
        self.name = []
    def start_td(self, attrs):
        self.is_td = 1
    def end_td(self):
        self.is_td = ""
    def handle_data(self, text):
        if self.is_td == 1:
            self.name.append(text)

for count, url in enumerate(website):
	content = urllib2.urlopen(url).read()
	mpls = MPLS_Parser()
	mpls.feed(content)

	# print len(mpls.name[76::6])
	# print len(mpls.name[77::6])
	# print len(mpls.name[79::6])

	for index, element in enumerate(mpls.name):
		if (index >= 77) & (index % 6 == 5):
			try:
				if float(element) > LIMIT:
					store.append(mpls.name[38])
					time.append(mpls.name[index-1])
					input.append(element)
					output.append(mpls.name[index+2])
					# print mpls.name[38]
					# print mpls.name[index-1]
					# print element
					# print mpls.name[index+2]
					# print "--------------------"
			except:
				print "---------- Input Error ----------"
				print index
				print element
				print "---------- Input Error ----------"

	for index, element in enumerate(mpls.name):
		if (index >= 79) & (index % 6 == 1):
			try:
				if float(element) > LIMIT:
					store.append(mpls.name[38])
					time.append(mpls.name[index-3])
					input.append(mpls.name[index-2])
					output.append(element)
					# print mpls.name[38]
					# print mpls.name[index-3]
					# print mpls.name[index-2]
					# print element
					# print "--------------------"
			except:
				print "---------- Output Error ----------"
				print index
				print element
				print "---------- Output Error ----------"

	# print len(store)
	# print len(time)
	# print len(input)
	# print len(output)
	# print "--------------------"

	print "---------- Finish Parsing Data " + str(count + 1) + " in " + url + " ----------"

for index, element in enumerate(time):
	print store[index]
	print time[index]
	print input[index]
	print output[index]

w = xlwt.Workbook()
ws = w.add_sheet('MPLS_Parser')

style = xlwt.easyxf('align: wrap on, vert centre, horiz centre;')

ws.write(0, 0, u'2016.03.14 - 2016.03.20', style)
ws.write(0, 7, u'주간 사용 Top 5', style)
ws.write(1, 0, u'횟수', style)
ws.write(1, 1, u'점포명', style)
ws.write(1, 2, u'날짜', style)
ws.write(1, 3, u'시간', style)
ws.write(1, 4, u'입력 사용량', style)
ws.write(1, 5, u'출력 사용량', style)
ws.write(1, 7, u'횟수', style)
ws.write(1, 8, u'점포명', style)

print "---------- Print Result 1/4 Begin ----------"

def multiple_replace(text,adict):  
    rx = re.compile('|'.join(map(re.escape,adict)))  
    def one_xlat(match):  
        return adict[match.group(0)]  
    return rx.sub(one_xlat,text)

stmap = { '## Mart Gyaeyang 512K KT: 25002471-0376 ##':u'계양점','## Mart CheoungRa 512K KT: 25002471-0397 ##':u'청라점','## Mart Bupyungyuk 512K KT: 25-002471-0131 ##':u'부평역점','## Mart Kimpo 512K KT: 25-002471-0141 ##':u'김포점','## Mart Goemdan 512K KT: 25-002471-0140 ##':u'검단점','## Mart SongDo 512K KT: 25002471-0489 ##':u'송도점','## Mart SiHwa 512K KT: 25-002471-0143 ##':u'시화점','## Mart Goyang 512K KT: 25-002471-0142 ##':u'고양점','## Mart Juyeop 512K KT: 25-002472-0034 ##':u'주엽점','## Mart Yeonsu 512K KT: 25-002471-0132 ##':u'연수점','## Mart Bupyung 512K KT: 25-002471-0134 ##':u'부평점','## Mart Youngjongdo 512K KT: 25-002471-0133 ##':u'영종도점','## Mart Samsan 512K KT: 25-002471-0138 ##':u'삼산점','## Mart GweunSeoun 512K KT: 25-002471-0179 ##':u'권선점','## Mart GwangGyo 512K KT: 25002471-0614 ##':u'광교점','## Mart Osan 512K KT:25-002471-0155 ##':u'오산점','## Mart Ansung 512K KT:25-002471-0160 ##':u'안성점','## Mart PyeungTaek 512K KT: 25-002471-0171 ##':u'평택점','## Mart Uewang 512K KT: 25-002471-0156 ##':u'의왕점','## Mart Siheoung 512K KT: 25002471-0377 ##':u'시흥점','## Mart YoungTong 512K KT: 25002471-0388 ##':u'영통점','## Mart Suwon 512K DA:500054036363 ##':u'수원점','## Mart SeounBu 512K KT: 25002471-0463 ##':u'선부점','## Mart Pyeongchon 512K KT: 25002471-0349 ##':u'평촌점','## Mart Cheoncheon 512K KT: 25-002471-0157 ##':u'천천점','## Mart Suji 512K KT: 25-002471-0159 ##':u'수지점','## MART-ANSAN 512K KT: 25-002471-0178 ##':u'안산점','## Mart SangRock 512K KT: 25002471-0392 ##':u'상록점','## Mart Samyang 512K KT:25-002472-0018 ##':u'삼양점','## Mart Masuk 512K KT:25-002472-0019 ##':u'마석점','## Mart HeangDangStation 512K KT: 25-002472-0087 ##':u'행당역점','## Mart Youngdeungpo 512K KT:25-002472-0022 ##':u'영등포점','## Mart Kangbyen 512K KT:25-002472-0023 ##':u'강변점','## Mart GumCheoun 512K KT: 25002471-0361 ##':u'금천점','## Mart Kuro 512K KT: 25-002472-0025 ##':u'구로점','## Mart WorldTower 512K INPOP ##':u'월드타워점','## Mart World 512K KT: 25-002472-0017 ##':u'잠실점','## Mart DukSo 512K KT: 25-002472-0086 ##':u'덕소점','## Mart ChunChoeun 512K KT: 25-002472-0080 ##':u'춘천점','## Mart SongPa 512K KT: 25-002472-0009 ##':u'송파점','## Mart SuckSa 512K KT: 25-002472-0085 ##':u'석사점','## Mart Junggae 512K KT: 25-002472-0027 ##':u'중계점','## Mart Dobong 512K KT: 25-002472-0028 ##':u'도봉점','## Mart Seoulyuk 512K KT: 25-002472-0029 ##':u'서울역점','## Mart WonJoo 512K KT: 25000375-0004 ##':u'원주점','## Mart Dongdoocheoun 512K KT: 25-002472-0077 ##':u'동부천점','## Mart CheungRyangRiStation 512K KT: 25-002472-0011 ##':u'청량리점','## Mart Ueijungbu 512K KT: 25-002472-0031 ##':u'의정부점','## Mart Kuri 512K KT: 25-002472-0030 ##':u'구리점','## Mart Seohyun 512K KT: 25-002472-0032 ##':u'서현점','## Mart Yangju 512K KT: 25-002472-0033 ##':u'양주점','## Mart Jangam 512K KT: 25-002472-0035 ##':u'장암점','## Mart Daeduk 512K KT: 25-002471-0196 ##':u'대덕점','## Mart HongSung 512K KT:01320050-0044 ##':u'홍성점','## Mart Seosan 512K KT: 25-002471-0211 ##':u'서산점','## Lotte Mart DangJin,512K KT: 25-002471-0212 ##':u'당진점','## Mart Ahsan 512K KT: 25-002471-0210 ##':u'안산점','## Mart AsanTerminal 512K KT: 25002471-0487 ##':u'안산터미널점','## Mart SeoCheoungJoo 512K KT: 25002471-0387 ##':u'서청주점','## Mart Jaecheon 512K KT: 25-002471-0188 ##':u'제천점','## Mart Nohen 512K KT: 25-002471-0197 ##':u'노은점','## Mart Sungjeong 512K KT: 25-002471-0195 ##':u'성정점','## Mart Cheonan 512K KT: 25-002471-0192 ##':u'천안점','## Mart Seodaejeon 512K KT: 25-002471-0193 ##':u'서대전점','## Mart Chungju 512K KT: 25-002471-0194 ##':u'충주점','## Mart DongDeajeoun 512K KT: 25-002471-0202 ##':u'동대전점','## Mart Cheongju 512K KT: 25-002471-0191 ##':u'청주점','## Mart DongCheungju 512K KT: 25-002471-0203 ##':u'동청주점','## Mart KimCheoun 512K KT: 25002471-0584 ##':u'김천점','## Mart Kumi 512K KT:25-002471-0262 ##':u'구미점','## Mart Pohang 512K KT: 25-002471-0263 ##':u'포항점','## Mart DeaGu 512K KT: 25-002471-0268 ##':u'대구점','## Mart Hwasung 512K KT: 25002471-0364 ##':u'화성점','## Mart MajangExpresswayRestArea 512K KT: 25002471-0417 ##':u'마장휴게소점','## Mart PanGyo 512K KT: 25002471-0438 ##':u'판교점','## Mart Shingal 512K KT: 25002471-0585 ##':u'신갈점','## Mart Yeosu 512K KT: 25-002471-0293 ##':u'여수점','## Mart Yeocheon 512K KT: 25-002471-0292 ##':u'여천점','## Mart Suwan 512K KT: 25-002471-0289 ##':u'수완점','## Mart Najoo 512K KT:25-021224-0114 ##':u'나주점','## Mart DuckJin 512K KT: 25-002471-0301 ##':u'덕진점','## Mart Jeongup 512K KT: 25-002471-0300 ##':u'정읍점','## Mart SongCheoun 512K KT: 25-002471-0299 ##':u'송천점','## Mart Sangmu 512K KT: 25-002471-0282 ##':u'상무점','## Mart Chumdan 512K KT: 25-002471-0283 ##':u'첨단점','## Mart Mokpo 512K KT: 25-002471-0284 ##':u'목포점','## Mart Worldcup 512K KT: 25-002471-0285 ##':u'월드컵점','## Mart Iksan 512K KT:25-002471-0295 ##':u'익산점','## Mart Kunsan 512K KT:25-002471-0296 ##':u'군산점','## Mart JeunJoo 512K KT: 25-002471-0298 ##':u'전주점','## Mart Namwon 512K KT: 25002472-0103 ##':u'남원점','## Mart Jeju 512K KT:25-002471-0304 ##':u'제주점','## Mart EastBusan 512K SKB ##':u'동부산점','## Mart DongRae 512K KT: 25-002471-0225 ##':u'동래점','## Mart Kimhea 512K KT: 25002471-0451 ##':u'김해점','## Mart Kidds mart Busan 512K KT: 25002471-0055 ##':u'키즈마트부산점','## Mart GwangBok 512K KT:##':u'관복점','## Mart Geoje 512K KT: ##':u'거제점','## Mart GuemJeoung 512K KT: 25-002471-0231 ##':u'금정점','## Mart Heawoondea 512K KT: 25-002471-0232 ##':u'해운대점','## Mart Saha 512K KT: 25-002471-0215 ##':u'사하점','## Mart Hwamyung 512K KT: 25-002471-0216 ##':u'화명점','## Mart Ueongsang 512K KT: 25-002471-0217 ##':u'웅상점','## Mart Sasang 512K KT: 25-002471-0218 ##':u'사상점','## Mart Ulsan 512K KT:25-002471-0242 ##':u'울산점','## Mart Jinjang 512K KT:25-002471-0243 ##':u'진장점','## Mart YangDuk 512K KT: 25002471-0662 ##':u'양덕점','## Mart VIC_KINTEX 512K KT: 25002471-0568 ##':u'VIC킨텍스점','## Mart Hwajung 512K KT: 25-002472-0026 ##':u'화정점','## Mart KimpoSkyPark 512K SKB: 7190984571 ##':u'김포스카이파크점', }
StoreKr = []

for element in store:
	StoreKr.append(multiple_replace(element,stmap))

for index, element in enumerate(StoreKr):
	ws.write(index + 2, 1, element, style)

StoreSort = []

for item in set(StoreKr):
	StoreSort.append([StoreKr.count(item), item])

for index, element in enumerate(sorted(StoreSort, key = lambda StoreSort : StoreSort[0], reverse = True)):
	ws.write(index + 2, 7, element[0], style)
	ws.write(index + 2, 8, element[1], style)

for seq, store in enumerate(StoreKr):
	for element in StoreSort:
		if store == element[1]:
			ws.write(seq + 2, 0, element[0], style)

print "---------- Print Result 1/4 End ----------"

print "---------- Print Result 2/4 Begin ----------"

for index, element in enumerate(time):
	ws.write(index + 2, 2, element.split(' ')[0], style)
	ws.write(index + 2, 3, element.split(' ')[1], style)

print "---------- Print Result 2/4 End ----------"

print "---------- Print Result 3/4 Begin ----------"

for index, element in enumerate(input):
	ws.write(index + 2, 4, element + '%', style)

print "---------- Print Result 3/4 End ----------"

print "---------- Print Result 4/4 Begin ----------"

for index, element in enumerate(output):
	ws.write(index + 2, 5, element + '%', style)

print "---------- Print Result 4/4 End ----------"

w.save('MPLS_Parser.xls')

finish = clock()

print "---------- Finsh Parsing Total " + str(count + 1) + " Data ----------"
print "---------- Finish Parsing in " + str(finish - start) + " seconds ----------"
os.system('pause')