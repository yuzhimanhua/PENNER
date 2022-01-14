#!/bin/bash
data=penner
path=$(pwd)

### Following are the parameters used in auto_phrase.sh
RAW_TRAIN=${RAW_TRAIN:- ../../../data/$data/corpus.txt}
MIN_SUP=${MIN_SUP:- 15}

### Following are the parameters used in phrasal_segmentation.sh
HIGHLIGHT_MULTI=${HIGHLIGHT_MULTI:- 0.7}
HIGHLIGHT_SINGLE=${HIGHLIGHT_SINGLE:- 0.99999} # no need for unigram

green=`tput setaf 2`
reset=`tput sgr0`

echo ${green}==='Corpus Name:' $data===${reset}
echo ${green}==='Current Path:' $path===${reset}


echo ${green}===Running AutoPhrase===${reset}
cd ../tools/AutoPhrase
make
./auto_phrase.sh $RAW_TRAIN $MIN_SUP
./phrasal_segmentation.sh $RAW_TRAIN $HIGHLIGHT_MULTI $HIGHLIGHT_SINGLE
cp ./models/DBLP/segmentation.txt ../../../data/$data/segmentation.txt
cd $path

echo ${green}===Running Stanford CoreNLP Tool===${reset}
## Download stanford coreNLP toolkit to specified folder if it doesn't exist
if [ ! -d ../tools/CoreNLP/stanford-corenlp ]; then
	wget -O ../tools/CoreNLP/stanford-corenlp.zip http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip
	unzip ../tools/CoreNLP/stanford-corenlp.zip -d ../tools/CoreNLP/
	mv ../tools/CoreNLP/stanford-corenlp-full-2017-06-09/ ../tools/CoreNLP/stanford-corenlp/
	rm -f ../tools/CoreNLP/stanford-corenlp.zip
fi
python3 parseAutoPhraseOutput.py $data 1

python3 generateSentencesJSONAndEntity2Id.py $data

python3 nerProc.py $data