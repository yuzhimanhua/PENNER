import json
from collections import Counter
import sys

def main(corpusName):
	data = corpusName
	intputFile = '../../data/'+data+'/sentences.json.raw'
	outputEntityListFile = '../../data/'+data+'/entitylist.txt'
	outputTypeListFile = '../../data/'+data+'/typelist.txt'

	mentionList = []
	typeList = []

	with open(intputFile,"r") as fin:
		cnt = 0
		for line in fin:
			if cnt % 100000 == 0 and cnt != 0:
				print("Processed %d lines" % cnt)

			line = line.strip()
			sentence = json.loads(line)

			for mention in sentence["entityMentions"]:
				mentionList.append(mention["text"])
				## TODO: deal with multiple types for each mention later
				typeList.append(mention["type"])
			cnt += 1

	mentionCounter = Counter(mentionList)
	typeCounter = Counter(typeList)

	with open(outputEntityListFile, "w") as fout:
		for ele in sorted(mentionCounter.items(), key = lambda x:(x[0],-x[1])):
			fout.write(ele[0]+"\t"+str(ele[1])+"\n")

	with open(outputTypeListFile, "w") as fout:
		for ele in sorted(typeCounter.items(), key = lambda x:(x[0],-x[1])):
			fout.write(ele[0]+"\t"+str(ele[1])+"\n")

if __name__ == '__main__':
	corpusName = sys.argv[1]
	main(corpusName)
