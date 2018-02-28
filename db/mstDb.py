# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
from logging import getLogger
logger = getLogger(__name__)

dbname = 'database.db'

def setLocale(locale):
	global dbname
	dbname = locale

def findUnit(id):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()

	select_sql = 'select * from unit where id = ?'
	unitParam = (int(id),)
	c.execute(select_sql, unitParam)
	unit = None
	for row in c:
		unit = row
		break;
	
	conn.close()
	return unit

def findUnitByName(name):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()

	select_sql = 'select name from unit where name = ?'
	bookParam = (name,)
	c.execute(select_sql, bookParam)
	unit = None
	for row in c:
		unit = row
		break;
	
	conn.close()
	return unit

def insertUnit(name, shusshin, nenrei, seibetsu, rare, zokusei, seichouType, buki, bukiShubetsu, doujiKougekiSuu, kougekiDansuu, shokiHp, saidaiHp, kakuseiHp, idousokudo, reach, shokiKougeki, saidaiKougeki, kakuseiKougeki, kougekiKankaku, toughness, zokuseiHonoo, zokuseiMizu, zokuseiKaze, zokuseiHikari, zokuseiYami):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()
	
	select_sql = 'select name from unit where name = ?'
	c.execute(select_sql, (name,))
	for row in c:
		logger.debug('duplicate name:'+name)
		return

	insId = 0
	select_sql = 'select max(id) from unit'
	c.execute(select_sql)
	for row in c:
		if row[0] == None:
			insId = 1
		else:
			print(row[0])
			insId = int(row[0]) + 1

	# データの挿入増えたら足してく
	insert_sql = 'insert into unit(id, name, shusshin, nenrei, seibetsu, rare, zokusei, seichouType, buki, bukiShubetsu, doujikougekiSuu, kougekiDansuu, shokiHp, saidaiHp, kakuseiHp, idousokudo, reach, shokiKougeki, saidaiKougeki, kakuseiKougeki, kougekiKankaku, toughness, zokuseiHonoo, zokuseiMizu, zokuseiKaze, zokuseiHikari, zokuseiYami, updateDate, createDate, displayFlag) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
	unit = [
	    (insId, str(name), str(shusshin), int(nenrei), str(seibetsu), str(rare), str(zokusei), str(seichouType), str(buki), str(bukiShubetsu), int(doujiKougekiSuu), int(kougekiDansuu), int(shokiHp), int(saidaiHp), int(kakuseiHp), int(idousokudo), int(reach), int(shokiKougeki), int(saidaiKougeki), int(kakuseiKougeki), float(kougekiKankaku), int(toughness), int(zokuseiHonoo), int(zokuseiMizu), int(zokuseiKaze), int(zokuseiHikari), int(zokuseiYami), datetime.now().strftime("%Y/%m/%d %H:%M:%S"), datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 1)
	]
	c.executemany(insert_sql, unit)
	conn.commit()
	conn.close()

def updateBook(id, bookName=None, bookNameKana=None, thumbnailPath=None, path=None, category=None, displayFlag=None):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()
	updateDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S");

	# idなかったらそもそも問題
	if not id:
		conn.close()
		raise Exception("id is not found")

	# データの挿入増えたら足してく
	# 空たぷる生成
	param = ()
	update_sql = 'update unit set '
	param = param + (updateDate,)
	update_sql = update_sql + ' updateDate=?'
	
	if bookName:
		param = param + (bookName,)
		update_sql = update_sql + ', bookName=?'
		
	param = param + (id,)
	update_sql = update_sql + ' where id=?'
	print(update_sql)
	print(param)
	
	c.execute(update_sql, param)
	conn.commit()
	conn.close()

def deleteBook(id):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()

	# 削除
	delete_sql = 'delete from unit where id = ?'
	bookParam = (id,)
	c.execute(delete_sql, bookParam)
	conn.commit()
	conn.close()
