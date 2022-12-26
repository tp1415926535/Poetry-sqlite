import sqlite3
import os
from pathlib import Path
import json
from datetime import datetime

configFile='poetryConfig.json'
dataSourceFolder=""
connection = cur = None

def init():
	global dataSourceFolder

	if os.path.exists(configFile):
		f = open(configFile,"r",encoding='utf-8')
		config = json.load(f)
		f.close()
	else:
		print("不存在配置文件，无法生成数据库！")
		input("按下回车键退出")
		sys.exit() 

	if ("dataSourceFolder" not in config)|("dbPath" not in config):
		print("未配置输入或输出路径！")
		input("按下回车键退出")
		sys.exit() 

	dataSourceFolder=os.path.realpath(config["dataSourceFolder"])
	if not os.path.exists(dataSourceFolder):
		print("未找到源数据文件夹。 请修改配置文件的 dataSourceFolder 值为 chinese-poetry 项目解压的文件夹路径！")
		input("按下回车键退出")
		sys.exit()

	databaseFile=os.path.realpath(config["dbPath"])
	if os.path.isfile(databaseFile):
		print("数据库文件已存在！\r\n1.自动删除数据库重新创建\r\n2.退出程序")
		while True:
			result = input("请输入所选编号? ")
			if result=="1":
				os.remove(databaseFile)
				break
			elif result=="2":
				sys.exit()
	createConnect(databaseFile)


def getDataToDB():
	items = [ f.path for f in os.scandir(dataSourceFolder) if f.is_file()]
	for file in items:
		if file.endswith(".csv")==False:
			continue
		print(f"正在处理“{os.path.basename(file)}”...")
		lines = []
		f = open(file,"r",encoding='utf-8')
		lines = f.readlines()
		f.close()
		data=[]
		columns= lines[0].replace('"','').strip().split(",")
		index = 0
		for line in lines:
			index = index+1
			if index <=1:
				continue
			strs=line.replace("\u3000"," ").split('","')
			if len(strs)!=len(columns):
				continue
			dic={}
			for i in range(0,len(strs)):
				dic[columns[i]]=strs[i].replace('"','').strip()
			data.append(dic)
		try:
			fillTable(Path(file).stem,data)
		except Exception as e:
			print("【错误】"+str(e))

def createConnect(dbFile):
	global connection,cur
	connection = sqlite3.connect(dbFile)
	connection.row_factory = sqlite3.Row 
	cur = connection.cursor()

def createTable(tableName,tableConstruct):
	global connection,cur
	sql=f"create table if not exists {tableName} ("
	for x in tableConstruct:
		sql= sql + f"{x} {tableConstruct[x]},"
	sql=sql[:-1]+")"
	cur.execute(sql)
	connection.commit()

def fillTable(tableName,diclist):
	global connection,cur
	tableConstruct={"id":"INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"}
	for x in list(diclist[0].keys()):
		tableConstruct[x] = "TEXT"
	createTable(tableName,tableConstruct)

	insertcolumns=",".join(diclist[0].keys())
	tuplearray= [tuple(dic.values()) for dic in diclist]
	valuesTemplate="("
	for i in diclist[0].keys():
	    valuesTemplate = valuesTemplate+"?,"
	valuesTemplate=valuesTemplate[:-1]+")"
	cur.executemany(f'INSERT INTO {tableName} ({insertcolumns}) VALUES {valuesTemplate}', tuplearray)
	connection.commit()



if __name__ == "__main__":
	try:
		init()
		timeBegin=datetime.now()
		getDataToDB()
		timeEnd = datetime.now()
		input(f"\r\n\r\n写入数据库完成，耗时{str(timeEnd-timeBegin)[:-7]}")
	except Exception as e:
		print("【错误】"+str(e))
	input("按下回车键退出")

