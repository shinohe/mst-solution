#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import numpy as np
from flask_httpauth import HTTPDigestAuth
import os
import json
import sqlite3
import math
import logs
from operator import itemgetter
from dist import dist

import sys  
sys.path.append('SOME_PATH\python\Lib\encodings');  

import codecs  
import encodings.utf_8

codecs.register(lambda encoding: utf_8.getregentry()) 

currentDir = os.path.dirname(os.path.abspath(__file__))
dbpath = currentDir + os.sep + 'db' + os.sep
dbname = 'database.db'
tablename = 'unit'

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.register_blueprint(dist.app)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
	"jdragon1": "jdragon1"
}

# おまじない
def round(x,d=0):
    p=10**d
    return (x*p*2+1)//2/p

class InvalidUsage(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload
		
	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv

class PageList:
	list = []
	pageSize = 8
	page = 1
	maxSize = 0
	def __init__(self,list, pageSize, maxSize, page):
		self.list = list
		self.pageSize = pageSize
		self.maxSize = maxSize
		self.page = page
	def serialize(self):
		return {
		'list':ViewerImageJSONEncoder().encode(self.list),
		'pageSize':self.pageSize,
		'maxSize':self.maxSize,
		'page':self.page
		}

class Thumbnail:
	id = ''
	name = ''
	displayFlag = 1
	shusshin = ''
	nenrei = -1
	seibetsu = ''
	rare = ''
	zokusei = ''
	seichouType = ''
	buki = ''
	bukiShubetsu = ''
	doujiKougekiSuu = 0
	kougekiDansuu = 0
	shokiHp = 0
	saidaiHp = 0
	kakuseiHp = 0
	idousokudo = 0
	reach = 0
	shokiKougeki = 0
	saidaiKougeki = 0
	kakuseiKougeki = 0
	kougekiKankaku = 0
	toughness = 0
	zokuseiHonoo = 0
	zokuseiMizu = 0
	zokuseiKaze = 0
	zokuseiHikari = 0
	updateDate = ''
	createDate = ''
	tantaiDps = 0
	saidaiDps=0
	dps=0
	
	def __init__( self, id, name=None, shusshin=None, nenrei=None, seibetsu=None, rare=None, zokusei=None, seichouType=None, buki=None, bukiShubetsu=None, doujiKougekiSuu=None, kougekiDansuu=None, shokiHp=None, saidaiHp=None, kakuseiHp=None, idousokudo=None, reach=None, shokiKougeki=None, saidaiKougeki=None, kakuseiKougeki=None, kougekiKankaku=None, toughness=None, zokuseiHonoo=None, zokuseiMizu=None, zokuseiKaze=None, zokuseiHikari=None, zokuseiYami=None, updateDate=None, createDate=None, displayFlag=1, tantaiDps=None, saidaiDps=None, dps=None):
		
		self.id = id
		self.name = name
		self.shusshin = shusshin
		self.nenrei = nenrei
		self.seibetsu = seibetsu
		self.rare = rare
		self.zokusei = zokusei
		self.seichouType = seichouType
		self.buki = buki
		self.bukiShubetsu = bukiShubetsu
		self.doujiKougekiSuu = doujiKougekiSuu
		self.kougekiDansuu = kougekiDansuu
		self.shokiHp = shokiHp
		self.saidaiHp = saidaiHp
		self.kakuseiHp = kakuseiHp
		self.idousokudo = idousokudo
		self.reach = reach
		self.shokiKougeki = shokiKougeki
		self.saidaiKougeki = saidaiKougeki
		self.kakuseiKougeki = kakuseiKougeki
		self.kougekiKankaku = kougekiKankaku
		self.toughness = toughness
		self.zokuseiHonoo = zokuseiHonoo
		self.zokuseiMizu = zokuseiMizu
		self.zokuseiKaze = zokuseiKaze
		self.zokuseiHikari = zokuseiHikari
		self.updateDate = updateDate
		self.createDate = createDate
		self.zokuseiYami = zokuseiYami
		self.displayFlag = displayFlag
		self.tantaiDps = tantaiDps
		self.saidaiDps = saidaiDps
		self.dps = dps
		
	def serialize(self):
		return {
			'id' : self.id,
			'name' : self.name,
			'shusshin' : self.shusshin,
			'nenrei' : self.nenrei,
			'seibetsu' : self.seibetsu,
			'rare' : self.rare,
			'zokusei' : self.zokusei,
			'seichouType' : self.seichouType,
			'buki' : self.buki,
			'bukiShubetsu' : self.bukiShubetsu,
			'doujiKougekiSuu' : self.doujiKougekiSuu,
			'kougekiDansuu' : self.kougekiDansuu,
			'shokiHp' : self.shokiHp,
			'saidaiHp' : self.saidaiHp,
			'kakuseiHp' : self.kakuseiHp,
			'idousokudo' : self.idousokudo,
			'reach' : self.reach,
			'shokiKougeki' : self.shokiKougeki,
			'saidaiKougeki' : self.saidaiKougeki,
			'kakuseiKougeki' : self.kakuseiKougeki,
			'kougekiKankaku' : self.kougekiKankaku,
			'toughness' : self.toughness,
			'zokuseiHonoo' : self.zokuseiHonoo,
			'zokuseiMizu' : self.zokuseiMizu,
			'zokuseiKaze' : self.zokuseiKaze,
			'zokuseiHikari' : self.zokuseiHikari,
			'updateDate' : self.updateDate,
			'createDate' : self.createDate,
			'zokuseiYami' : self.zokuseiYami,
			'displayFlag' : self.displayFlag,
			'tantaiDps' : self.tantaiDps,
			'saidaiDps' : self.saidaiDps,
			'dps' : self.dps
		}

class UnitListParam:
	kunrenjo = 30;
	zangekiShisetsu = 12;
	totsugekiShisetsu = 12;
	dagekiShisetsu = 12;
	yumiShisetsu = 12;
	mahouShisetsu = 12;
	juuShisetsu = 12;
	kaihukuShisetsu = 12;
	soulKougeki = 35000;
	breakKougeki = 35000;
	atackRune = 33;
	quickRune = 33;
	exantRune = 33;
	honooRune = 33;
	mizuRune = 33;
	kazeRune = 33;
	yamiRune = 33;
	hikariRune = 33;


class ViewerImageJSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, PageList):
			return o.serialize()
		if isinstance(o, Thumbnail):
			return o.serialize()
		return super(ViewerImageJSONEncoder, self).default(o)
		
app.json_encoder = ViewerImageJSONEncoder

# ユニットリストのキャッシュデータ
allUnitCache = []

# メソッド
def unitListNoKana(page, pageSize, manageList):
	return unitList(page, pageSize, None, manageList)

def unitList(page, pageSize, unitName, manageList='False', idList=None, ignoreList=None, sortKey='dps'):
	unitList = []
	params =(pageSize, page*pageSize)
	
	# FIXME LIMIT OFFSETでページネーションしてるのでチューニングは必要	
	conn = sqlite3.connect(dbpath+dbname)
	c = conn.cursor()

	count_sql = 'select count(*) from unit'
	if manageList=='True':
		select_sql = 'select * from unit order by createDate desc limit ? offset ?'
	else:
		select_sql = 'select * from unit where displayFlag=1 order by (saidaiKougeki/kougekiKankaku) desc limit ? offset ?'
	
	if idList:
		idList = [str(i) for i in idList]
		idListStr = ','.join(idList)
		count_sql = 'select count(*) from unit where id in(%s) ' % idListStr
		select_sql = 'select * from unit where id in(%s) order by createDate desc limit ? offset ?' % idListStr
		params =(pageSize, page*pageSize)
		count_params = ()
		print(select_sql)
		c.execute(count_sql, count_params)
	elif unitName:
		unitName = u"%{}%".format(unitName)
		params =(unitName,)
		count_params = (unitName,)
		
		if manageList=='True':
			count_sql = 'select count(*) from unit where ( name like ? '
			select_sql = 'select * from unit where ( name like ? '
		else:
			count_sql = 'select count(*) from unit where displayFlag=1 and ( name like ? '
			select_sql = 'select * from unit where displayFlag=1 and ( name like ? '
		unitName = u"%{}%".format(unitName)
		
		count_sql = count_sql + ' ) '
		select_sql = select_sql + ' ) '
			
		if sortKey=='dps': 
			select_sql = select_sql + 'order by (saidaiKougeki/kougekiKankaku) desc limit ? offset ?'
		else:
			select_sql = select_sql + 'order by updateDate desc limit ? offset ?'
		
		params = params + (pageSize, page*pageSize)
		
		print(count_sql)
		print(select_sql)
		c.execute(count_sql, count_params)
	else:
		c.execute(count_sql)
	maxSize = c.fetchone()
	
	for row in c.execute(select_sql, params):
		unitDisp = Thumbnail(*row)
		unitList.append(unitDisp)
	conn.close
	
	print(maxSize)
	print(unitList)
	pageList = PageList(unitList, pageSize, math.ceil(maxSize[0]/pageSize), page)
	return jsonify(pageList)

# ユニットの詳細検索
def detailUnitList(page, pageSize, unitName, zokusei=None, idList=None, rare=None, bukiShubetsu=None, doujiKougekiSuu=None, ignoreList=None, sortKey='dps'):
	unitList = []
	params =(pageSize, page*pageSize)
	count_sql = 'select count(*) from unit where displayFlag=1'
	select_sql = 'select * from unit where displayFlag=1'
	
	if idList:
		idList = [str(i) for i in idList]
		idListStr = ','.join(idList)
		count_sql = count_sql + ' and id in(%s) ' % idListStr
		select_sql = select_sql + ' and id in(%s) ' % idListStr
	
	if zokusei:
		zokusei = u'"{}"'.format(zokusei)
		count_sql = count_sql + ' and zokusei=%s ' % zokusei
		select_sql = select_sql + ' and zokusei=%s ' % zokusei
		
	if rare:
		rare = u'"{}"'.format(rare)
		count_sql = count_sql + ' and rare=%s ' % rare
		select_sql = select_sql + ' and rare=%s ' % rare
		
	if bukiShubetsu:
		bukiShubetsu = u'"{}"'.format(bukiShubetsu)
		count_sql = count_sql + ' and bukiShubetsu=%s ' % bukiShubetsu
		select_sql = select_sql + ' and bukiShubetsu=%s ' % bukiShubetsu
	
	if not doujiKougekiSuu:
		doujiKougekiSuu = 1
	
	if sortKey=='dps':
		dpsCalcStr = '(saidaiKougeki/kougekiKankaku)'
		select_sql = select_sql + ' order by %s desc' % (dpsCalcStr,)
	else:
		select_sql = select_sql + ' order by createDate desc'
	
	select_sql = select_sql + ' limit ? offset ?'

	print(count_sql)
	print(select_sql)
	
	conn = sqlite3.connect(dbpath+dbname)
	c = conn.cursor()
	c.execute(count_sql)
	maxSize = c.fetchone()
	for row in c.execute(select_sql, params):
		unitDisp = Thumbnail(*row)
		unitList.append(unitDisp)
	conn.close
	pageList = PageList(unitList, pageSize, math.ceil(maxSize[0]/pageSize), page)
	
	return pageList
	

# Digest認証
@auth.get_password
def get_pw(username):
	if username in users:
		return users.get(username)
	return None


# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
	title = u"トップページ"
	page = 1
	# index.html をレンダリングする
	return render_template('index.html', title=title, page=page, isMenu=True)

@app.route('/assist')
def assist():
	title = u"アシスト最適計算"
	page = 1
	# index.html をレンダリングする
	return render_template('assist.html', title=title, page=page, isMenu=True)

@app.route('/Search/list', methods=['POST'])
def searchList():
	page = 0
	pageSize = 5
	unitName = ''
	zokusei = None
	bukiShubetsu = None
	if request.data:
		content_body_dict = json.loads(request.data)
	
		if 'page' in content_body_dict:
			page = request.json.get('page')
			page = int(page) - 1
			if page < 0:
				page = 0
			
		if 'manageList' in content_body_dict:
			manageList = request.json.get('manageList')
		else:
			manageList = False

		if 'pageSize' in content_body_dict:
			pageSize = request.json.get('pageSize')
			
		if 'unitName' in content_body_dict:
			unitName = request.json.get('unitName')
			
		if 'zokusei' in content_body_dict:
			zokusei = request.json.get('zokusei')
			if zokusei == '属性':
				zokusei = None
			
		if 'rare' in content_body_dict:
			rare = request.json.get('rare')
			if rare == '星':
				rare = None
			
		if 'bukiShubetsu' in content_body_dict:
			bukiShubetsu = request.json.get('bukiShubetsu')
			if bukiShubetsu == '武器':
				bukiShubetsu = None
			
		idList = None
		if 'idList' in content_body_dict:
			idList = request.json.get('idList')

	return jsonify(detailUnitList(page, pageSize, unitName, zokusei,idList=idList, rare=rare, bukiShubetsu=bukiShubetsu))

def getAsistNenreiGroup(nenrei):
	if nenrei == -1:
		return -1
	if nenrei==1:
		return 0
	
	if nenrei<=14:
		return 1
	
	if nenrei<=16:
		return 2
	
	if nenrei<=18:
		return 3
	
	if nenrei<=22:
		return 4
	
	return 5

def equalNenreiGroup(nenrei1, nenrei2):
	nenreiGroup1 = getAsistNenreiGroup(nenrei1)
	nenreiGroup2 = getAsistNenreiGroup(nenrei2)
	if nenreiGroup1==0 or nenreiGroup2==0:
		return True
	
	if nenreiGroup1== nenreiGroup2:
		return True
	
	return False
	
def getAsistReachGroup(reach):
	if reach<=50:
		return 1
	if reach<=150:
		return 2
	return 3
	
def equalReach(reach1, reach2):
	if getAsistReachGroup(reach1) == getAsistReachGroup(reach2):
		return True
	return False

def getLevel(rare):
	if rare == '★5':
		return 145
	if rare == '★4':
		return 135
	if rare == '★3':
		return 125
	if rare == '★2':
		return 115
	if rare == '★1':
		return 105
	return 0

def asistOptimize(unit, mindType=None, ignoreList=None):
	assistList = []
	lastMatchCount = 0
	for assist in allUnitCache:
		if unit.id == assist.id:
			continue
		
		if mindType:
			if mindType == assist.shusshin:

				continue
				

		matchCount = 1
		if unit.zokusei == assist.zokusei:
			matchCount = matchCount + 1

		if unit.bukiShubetsu == assist.bukiShubetsu:
			matchCount = matchCount + 1

		if unit.shusshin == assist.shusshin:
			matchCount = matchCount + 1

		if unit.seichouType == assist.seichouType:
			matchCount = matchCount + 0.5

		if equalNenreiGroup(unit.nenrei, assist.nenrei):
			matchCount = matchCount + 0.5

		if int(unit.doujiKougekiSuu) == int(assist.doujiKougekiSuu):
			matchCount = matchCount + 0.5

		if equalReach(unit.reach, assist.reach):
			matchCount = matchCount + 0.5

		if matchCount > 4.9:
			print(assist.name+" : "+str(matchCount)+" : "+str(matchCount*getLevel(assist.rare)/100))
			print(round(matchCount*getLevel(assist.rare)/100,5))
		matchCount = matchCount*getLevel(assist.rare)/100
		matchCount = round(matchCount,5)
			
		# 1番から順次比較
		# TODO
		
		assistList.append({'unit':assist,'match':matchCount})
		assistList = sorted(assistList, key=itemgetter('match'), reverse=True)
		if len(assistList) > 3:
			assistList.pop(len(assistList) - 1)

			
	return assistList
			


# DPS計算
def calcDps(page, pageSize, unit, zokusei=None, rare=None, bukiShubetsu=None,\
 tekiZokusei=None, doujiKougekiSuu=None, kunrenjo=None, bukiShisetsu=None,\
 soulKougeki=35000, breakKougeki=35000,\
 atackRune=33, quickRune=33, zokuseiRune=33, shokugyouRune=33,\
 icrease=None, icreaseRune=None, zokuseiShinden=5,\
 bukiTokkou1=None, bukiTokkouValue1=100, bukiTokkou2=None, bukiTokkouValue2=100):
	sortKey='dps'
	
	for unit in allUnitCache:
		# 検索条件
		if (zokusei and zokusei != unit.zokusei) or (rare and rare != unit.rare) or (bukiShubetsu and bukiShubetsu != unit.bukiShubetsu):
			continue
		
		kougeki = unit.kakuseiKougeki
		kougekiKankaku = unit.kougekiKankaku
		
		zokusei = 100
		if tekiZokusei == '炎':
			zokusei = unit.zokuseiHonoo
		elif tekiZokusei == '水':
			zokusei = unit.zokuseiMizu
		elif tekiZokusei == '風':
			zokusei = unit.zokuseiKaze
		elif tekiZokusei == '光':
			zokusei = unit.zokuseiHikari
		elif tekiZokusei == '闇':
			zokusei = unit.zokuseiYami
		
		kougeki = kougeki*(1+())
		

def calcAssist(page, pageSize, unitId, mindType, zokusei=None, idList=None, rare=None, bukiShubetsu=None, doujiKougekiSuu=None, ignoreList=None, sortKey='dps'):
	# アシスト能力によるDPS計算
	pass

# 与えられた情報からパーティ最適解を抽出する。
def calcUnitParty():
	# ユニットのシード最大時のDPSランク上位3
		
	# ユニットの単純のDPSランク上位3
	pass


def getUnit(unitId):
	for unit in allUnitCache:
		# 検索条件
		if (int(unitId) == int(unit.id)):
			return unit
	return None

@app.route('/All/list', methods=['POST'])
def all():
	unitName = ''
	zokusei = None
	bukiShubetsu = None
	if request.data:
		content_body_dict = json.loads(request.data)
		
		if 'unitName' in content_body_dict:
			unitName = request.json.get('unitName')
			
		if 'zokusei' in content_body_dict:
			zokusei = request.json.get('zokusei')
			if zokusei == '属性':
				zokusei = None
			
		if 'rare' in content_body_dict:
			rare = request.json.get('rare')
			if rare == '星':
				rare = None
			
		if 'bukiShubetsu' in content_body_dict:
			bukiShubetsu = request.json.get('bukiShubetsu')
			if bukiShubetsu == '武器':
				bukiShubetsu = None
			
		idList = None
		if 'idList' in content_body_dict:
			idList = request.json.get('idList')

	return jsonify(allUnitCache)

@app.route('/assist/list', methods=['POST'])
def assistList():
	if request.data:
		content_body_dict = json.loads(request.data)
		if 'unitId' in content_body_dict:
			unitId = request.json.get('unitId')
			print(unitId)
			unit = getUnit(unitId)
			asistDic = asistOptimize(unit)
	return jsonify(asistDic)

@app.errorhandler(InvalidUsage)
def error_handler(error):
	response = jsonify({ 'message': error.message, 'result': error.status_code })
	return response, error.status_code

if __name__ == '__main__':
	logs.init_app(app)
	allUnitCache = detailUnitList(1, -1, None).list
	app.debug = True  #デバッグモード有効化
	app.run(host='0.0.0.0', threaded=True) # どこからでもアクセス可能に

