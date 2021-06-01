import sys
import json

def loadMap(filename):
	map = {}
	with open(filename, 'r') as fin:
		for line in fin:
			seg = line.strip('\r\n').split('\t')
			map[seg[0]] = int(seg[1])
	return map

if __name__ == "__main__":
	data = sys.argv[1]
	eidMapFilename = '../../data/'+data+'/entity2id.txt'
	jsonFilename = '../../data/'+data+'/sentences.json.raw'
	outputfile = '../../data/'+data+'/sentences.json'
	eidMap = loadMap(eidMapFilename)
	#print(jsonFilename)
	#print(outputfile)
	with open(jsonFilename, 'r') as fin, open(outputfile, 'w') as fout:
		ct = 0
		for line in fin:
			if ct % 100000 == 0 and ct != 0:
					print("Processed %s of lines" % ct)
			ct += 1
			sentInfo = json.loads(line.strip('\r\n'))
			ems = sentInfo['entityMentions']
			ems_new = []
			for em in ems:
				if em["text"] in eidMap:
					em['entityId'] = eidMap[em["text"]]
					ems_new.append(em)
			sentInfo['entityMentions'] = ems_new
			fout.write(json.dumps(sentInfo)+'\n')
