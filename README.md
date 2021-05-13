# pyGG

Easily retrieve op.gg data for use in Python

## Requirements

install using

```bash
pip install -r requirements.txt
```

- requests
- bs4
- lxml
- pandas

## Example

```python
from pyGG import pyGG

opgg = pyGG('dharana')
summoner = opgg.get_summoner()
print(summoner.match_history)
```

## Classes

### pyGG

Profile page

`pyGG(summoner_name, summoner_id?)`

if not called with summoner_id, it will be fetched on instantiation

| Attribute     | Contents                    |
| ------------- | --------------------------- |
| summoner_name | plain text summoner name    |
| summoner_id   | summoner id as used by opgg |

### Summoner

Match history of summoner

`Summoner(summoner_id, gamemode='Ranked Solo')`

| Attribute     | Contents                          |
| ------------- | --------------------------------- |
| summoner_id   | summoner id as used by opgg       |
| gamemode      | gamemode filter for match history |
| match_history | header items for match history    |

| Method          | Contents                                            |
| --------------- | --------------------------------------------------- |
| get_matches()   | list of Match itmems based on match history         |
| get_champions() | Champions for summoner                              |
| load_more()     | extend match history (typically load 20 more games) |

### Match

Individual match

`Match(game_id, summoner_id, game_time)`

| Attribute   | Contents                                         |
| ----------- | ------------------------------------------------ |
| game_id     | match id as used by opgg                         |
| summoner_id | summoner id as used by opgg                      |
| game_time   | epoch timestamp of match                         |
| players     | json of all player related information for match |
| summary     | json of all team related information for match   |

### Champions

Full champion stats of summoner for a season

`Champions(summoner_id, season=17)`

| Attribute   | Contents                                   |
| ----------- | ------------------------------------------ |
| summoner_id | summoner id as used by opgg                |
| df          | DataFrame representation of champion stats |
| json        | json representation of champion stats      |

### Leaderboard

Top ranked summoners in Ranked Solo gamemode

`Leaderboard(page=1)`

| Attribute | Contents                          |
| --------- | --------------------------------- |
| json      | json represenation of leaderboard |

| Method              | Contents                                  |
| ------------------- | ----------------------------------------- |
| next_page()         | load next page of the leaderboard         |
| load_page(page:int) | load given page number of the leaderboard |
