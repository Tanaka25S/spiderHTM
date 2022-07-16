import pickle
import json
import requests


def reqItem(code):
	a = requests.get(f"https://ltn.hitomi.la/galleries/{code}.js")

	# CONVERT TO DICT
	txt = a.text
	idx = txt.find("=")
	while True:
		idx+=1
		if txt[idx] != " ":
			break
	txt = txt[idx:]

	maDic = json.loads(txt)

	return maDic


def getPage(maDic):
	return len(maDic["files"])


def getCoverHash(maDic):
	try:
		data = maDic["files"][0]["hash"]
	except:
		print("! cover_hash file {maDic['id']}")
		data = False
	return data


def getStringData(maDic):
	dataStr = ['title', 'japanese_title', 'date', 'id', 'type', 'language']
	data = {}
	for x in dataStr:
		data[x] = maDic[x]
	return data


def getUrlTag(maDic):
	dataTag      = ['parodys', 'groups', 'characters', 'artists']
	dataTagStart = [8, 7, 11, 8]
	dataHeadVal  = ['parody', 'group', 'character', 'artist']

	dataFinal = {}
	for num, tag in enumerate(dataTag):
		data = maDic[tag]
		readTag = {}
		if data:
			for x in maDic[tag]:
				val = x[dataHeadVal[num]]
				url = x["url"]
				url = url[dataTagStart[num]:-9]
				readTag[url] = val

		dataFinal[tag] = readTag

	return dataFinal


def getTags(maDIc):
	readTag = {}
	for item in maDic["tags"]:
		url = item["url"][5:-9]
		m = True if "male"   in item and item["male"]   else False
		f = True if "female" in item and item["female"] else False
		val = item["tag"]
		readTag[url] = [val, m, f]
	return readTag

def getData1(code):
	maDic = reqItem(code)
	itemData = {}

	itemData["page"]          = getPage(maDic)         # | page |
	itemData["cover_hash"]    = getCoverHash(maDic)    # | cover_hash |
	itemData.update( getStringData(maDic) )            # | title | japanese_title | date | id | type | language |
	itemData.update( getUrlTag(maDic))                 # | parodys | groups | characters | artists |
	itemData["tags"]          = getTags(maDic)         # | tags |
	itemData["scene_indexes"] = maDic["scene_indexes"] # | scene_indexes |
	itemData["related"]       = maDic["related"]       # | related |

	return itemData