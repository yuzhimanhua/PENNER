# PENNER: Pattern-enhanced Nested Named Entity Recognition in Biomedical Literature

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This repository contains the source code for [**PENNER: Pattern-enhanced Nested Named Entity Recognition in Biomedical Literature**](https://ieeexplore.ieee.org/document/8621485).

The general goal of this project is to extract nested entity structures/patterns from a corpus.

## Dependency
The following two packages need to be installed before running our code.

* [AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase): used to extract quality phrases from raw input data.
* [Stanford CoreNLP 3.8.0](https://stanfordnlp.github.io/CoreNLP/history.html): used to do POS tagging and select quality Noun Phrases from the previous phrase list generated by AutoPhrase. The quality Noun Phrase will be treated as the "entity".

**IMPORTANT NOTE 1: You can directly download the packages from [here](https://drive.google.com/file/d/1t5jlO1-PR734nXEBEnLKRJ7JiLOOnRfM/view?usp=sharing). Once you unzip the downloaded file, you can see two folders: ```AutoPhrase/``` and ```CoreNLP/```. Please put them under ```./src/tools/```.**

## Data Input Format
Two input files are required in ```./data/penner/``` (You can change "penner" to your dataset name).

(1) The corpus with replaced type tokens and candidate meta-patterns. You can refer to ```./data/penner/corpus.txt``` for detailed format. We show the first 3 lines below:
```
effect of CHEMICAL on plasma proteins including components of the hemostatic mechanism .
the effect of CHEMICAL ( 1.5 g/day ) on different plasma proteins and on components of the hemostatic system was studied in PATTERN2 with either mild DISEASE or cardiosclerosis .
before treatment , the subjects were investigated weekly on five occasions .
```

(2) The mapping list of pattern id and pattern surface name. You can refer to ```./data/penner/pid2mp.txt```for detailed format. We show the first 3 lines below:
```
PATTERN1600	the ratio of GENE
PATTERN508	significantly DISEASE
PATTERN3096	severity of DISEASE
```

To start from a raw corpus, you first need a "flat" biomedical named entity tagger (e.g., [scispacy](https://allenai.github.io/scispacy/)). After entity tagging, please refer to [WW-PIE](https://ieeexplore.ieee.org/document/8621375) (code in ```./pattern.zip```) for meta-pattern discovery.

## Running
First, you need to set up CoreNLP.
```
cd ./src/tools/CoreNLP/stanford-corenlp/
./setup.sh
```

Then, open a new session (e.g., using tmux). Run the following script.
```
./run.sh
```

It contains both preprocessing steps and the main expansion algorithm. The expanded nested patterns will be in the output file ```./ExpanResult.txt```.

**IMPORTANT NOTE 2: To modify the input patterns and thresholds, please check Lines 38-46 in ```./src/SetExpan/set_expan_main.py```.**

## Citation
Our implementation is adapted from [SetExpan](https://github.com/mickeystroller/SetExpan). If you find this repository useful, please cite the following paper:
```
@inproceedings{wang2018penner,
  title={PENNER: Pattern-enhanced Nested Named Entity Recognition in Biomedical Literature},
  author={Wang, Xuan and Zhang, Yu and Li, Qi and Wu, Cathy H. and Han, Jiawei},
  booktitle={BIBM'18},
  pages={540--547},
  year={2018},
  organization={IEEE}
}
```
