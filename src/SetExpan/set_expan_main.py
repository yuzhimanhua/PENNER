import util
import set_expan
import time

## Setting global versions
FLAGS_USE_TYPE=True

## Loading Corpus
data = "penner"
print('dataset:%s' % data)
folder = '../../data/'+data+'/'
start = time.time()
print('loading eid and name maps')
eid2ename, ename2eid = util.loadEidToEntityMap(folder+'entity2id.txt') #entity2id.txt
print('loading eid and skipgram maps')
eid2patterns, pattern2eids = util.loadFeaturesAndEidMap(folder+'eidSkipgramCounts.txt') #eidSkipgramCount.txt
print('loading skipgram strength map')
eidAndPattern2strength = util.loadWeightByEidAndFeatureMap(folder+'eidSkipgram2TFIDFStrength.txt', idx=-1) #(eid, feature, weight) file
if (FLAGS_USE_TYPE):
	print('loading eid and type maps')
	eid2types, type2eids = util.loadFeaturesAndEidMap(folder+'eidTypeCounts.txt') #eidTypeCount.txt
	print('loading type strength map')
	eidAndType2strength = util.loadWeightByEidAndFeatureMap(folder+'eidType2TFIDFStrength.txt', idx=-1) #(eid, feature, weight) file
end = time.time()
print("Finish loading all dataset, using %s seconds" % (end-start))

pid2mp = dict()
with open(folder+'pid2mp.txt', 'r') as fin:
	for line in fin:
		seg = line.strip().split('\t')
		pid2mp[seg[0]] = seg[1]

for entType in ['GENE', 'CHEMICAL', 'DISEASE', 'SPECIES']:
	pid2mp[entType] = entType

## Seed Patterns
seedNames = dict()
seedNames['Process'] = ['PATTERN2288', 'PATTERN4076'] # Process: GENE upregulation, GENE downregulation
seedNames['Treatment'] = ['PATTERN428', 'PATTERN968'] # Treatment: CHEMICAL injection, CHEMICAL inhalation

seedNames['Gene'] = ['GENE', 'PATTERN3909'] # Gene: GENE, GENE peroxidase
seedNames['Chemical'] = ['CHEMICAL', 'PATTERN1685'] # Chemical: CHEMICAL, GENE agonist
seedNames['Disease'] = ['DISEASE', 'PATTERN3223'] # Disease: DISEASE, cellular DISEASE
seedNames['Species'] = ['SPECIES', 'PATTERN37'] # Species: SPECIES, female SPECIES

thrsCoef = {'Gene':0.2, 'Chemical':0.4, 'Disease':0.35, 'Species':0.3, 'Process':0.4, 'Treatment':0.2}

negativeSeedEids = []
for entType in seedNames:
	for ele in seedNames[entType]:
		negativeSeedEids.append(ename2eid[ele.lower()])

## Expansion
for idx in range(5):
	for entType in seedNames:
		userInput = seedNames[entType]
		seedEidsWithConfidence = [(ename2eid[ele.lower()], 0.0) for ele in userInput]

		expandedEidsWithConfidence = set_expan.setExpan(
				seedEidsWithConfidence=seedEidsWithConfidence,
				negativeSeedEids=negativeSeedEids,
				eid2patterns=eid2patterns,
				pattern2eids=pattern2eids,
				eidAndPattern2strength=eidAndPattern2strength,
				eid2types=eid2types,
				type2eids=type2eids,
				eidAndType2strength=eidAndType2strength,
				eid2ename=eid2ename,
				thrsCoef=thrsCoef[entType],
				FLAGS_VERBOSE=True,
				FLAGS_DEBUG=True
		)

		for ele in expandedEidsWithConfidence:
			negativeSeedEids.append(ele[0])

			ename = eid2ename[ele[0]].rstrip('s').rstrip('es')
			if ename.lower() in ename2eid and ename not in seedNames[entType]:
				seedNames[entType].append(ename)

## Expand Result
with open('ExpanResult.txt', 'w') as fout:
	for entType in seedNames:
		fout.write(entType + ':\n')
		for idx, entName in enumerate(seedNames[entType]):
			if idx <= 1:
				fout.write('Seed\t' + pid2mp[entName] + '\n')
			else:
				fout.write(str(idx-1) + '\t' + pid2mp[entName] + '\n')
		fout.write('\n')
