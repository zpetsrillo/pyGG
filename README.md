# pyGG

Easily retrieve op.gg data for use in Python

## Requirements

install using
```
pip install -r requirements.txt
```

- requests
- bs4
- lxml
- pandas

## Example

```python
from pyGG import pyGG

opgg = pyGG.pyGG('dharana')
summoner = opgg.summoner
print(summoner.match_history)
```