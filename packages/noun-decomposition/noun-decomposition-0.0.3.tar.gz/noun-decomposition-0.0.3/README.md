# SECOS
This repo is a modular python implementation of the SECOS algorithm for decomposing composite nouns.

Based on the SECOS algorithm:

[original implementation](https://github.com/riedlma/SECOS)

[original paper](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2016-riedletal-naacl.pdf)

# Installation

## From Github
`pip install git+https://github.com/mhaugestad/noun-decomposition.git -U`

## From Source
```
git clone
cd noun-decomposition
pip install -e . -U
```

## From Pip
```
pip install noun-decomposition
```

## Installing models:
The module relies on pretrained models to be passed in. These can be downloaded from command line as follows:

`python -m Secos download --model de`

Or from a python script or notebook like this:

```
from secos import Decomposition

Decomposition.download_model('de')
```

Available models and their names are:

| Language  | Model |
| ------------- | ------------- |
| Danish | da |
| German | de |
| English | en |
| Spanish | es |
| Estonian | et |
| Finnish | fi |
| Hungarian | hu |
| Latin | la |
| Latvian | lv |
| Netherland | nl |
| Norway | no |
| Swedish | sv |

# Basic Usage
```
from secos import Decomposition

model = Decomposition.load_model('de')

secos = Decomposition(model)

secos.decompose("Bundesfinanzministerium")

['bundes', 'finanz', 'ministerium']
```

# Evaluation
The evaluation folder includes code for the evaluation of the pretrained models.