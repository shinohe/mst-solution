# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

dbname = 'database.db'
tablename = 'unit'

conn = sqlite3.connect(dbname)
c = conn.cursor()

# 削除するなら
c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % tablename)
if c.fetchone() != None: #存在してたら初期化
	c.execute('DROP TABLE unit')

if c.fetchone() == None: #存在してないので作る
	# executeメソッドでSQL文を実行する
	
	create_table = '''create table unit (id int, name varchar(256), shusshin varchar(256), nenrei int, seibetsu varchar(32), rare varchar(32), zokusei varchar(32), seichouType varchar(256),buki varchar(64), bukiShubetsu varchar(64), doujiKougekiSuu varchar(32), kougekiDansuu varchar(32), shokiHp int, saidaiHP int, kakuseiHp int, idousokudo int, reach int, shokiKougeki int, saidaiKougeki int, kakuseiKougeki int, kougekiKankaku float, toughness int, zokuseiHonoo int, zokuseiMizu int, zokuseiKaze int, zokuseiHikari int, zokuseiYami int, updateDate datetime, createDate datetime, displayFlag int)'''
	c.execute(create_table)

#データの削除
delete_sql = 'delete from unit'
c.execute(delete_sql)
conn.commit()

# 本のデータの挿入増えたら足してく
insert_sql = 'insert into unit(id, name, shusshin, nenrei, seibetsu, rare, zokusei, seichouType, buki, bukiShubetsu, doujiKougekiSuu, kougekiDansuu, shokiHp, saidaiHP, kakuseiHp, idousokudo, reach, shokiKougeki, saidaiKougeki, kakuseiKougeki, kougekiKankaku, toughness, zokuseiHonoo, zokuseiMizu, zokuseiKaze, zokuseiHikari, zokuseiYami, updateDate, createDate, displayFlag) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
unit = [
	(1, '「砲台上の酒豪」ヴィルベル','常夏の国',23,'女','★5','炎','晩成','大砲','銃弾',5,1,2600,5460,8535,40,200,3100,6510,10185,3.50,17,100,91,110,100,100, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), datetime.now().strftime("%Y/%m/%d %H:%M:%S"),1),
]
c.executemany(insert_sql, unit)
conn.commit()

#select_sql = 'select * from unit limit ? offset ?'
select_sql = 'select * from unit'
params = (2,1)
for row in c.execute(select_sql):
	print(row)

conn.close()
