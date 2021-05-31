# pyGG

Easily retrieve op.gg data for use in Python

## Install

You can install as pip package with the setup.py file by using this command from the main directory.

```shell
pip install .
```

## Requirements

install using

```shell
python3 -m pip install -r requirements.txt
```

- requests
- bs4
- lxml
- pandas

## Example

```python
from pyGG import Summoner

opgg = Summoner('dharana')
match_history = opgg.get_match_history()
print(match_history.json)
```

## Classes

### Summoner

Profile page

```python
Summoner(summoner_name)
```

if not called with summoner_id, it will be fetched on instantiation

| Attribute     | Contents                                      |
| ------------- | --------------------------------------------- |
| summoner_name | plain text summoner name                      |
| json          | json representaion of summoner's profile page |

| Method              | Contents                  |
| ------------------- | ------------------------- |
| get_match_history() | MatchHistory for summoner |
| get_champions()     | Champions for summoner    |

### MatchHistory

Match history of summoner

```python
MatchHistory(summoner_id, gamemode='soloranked')
```

gamemode

- soloranked
- flexranked
- normal
- aram
- bot
- clash
- event
- total

| Attribute   | Contents                               |
| ----------- | -------------------------------------- |
| summoner_id | summoner id as used by opgg            |
| gamemode    | gamemode filter for match history      |
| json        | json of header items for match history |
| df          | df of header items for match history   |

| Method        | Contents                                            |
| ------------- | --------------------------------------------------- |
| get_matches() | list of Match itmems based on match history         |
| load_more()   | extend match history (typically load 20 more games) |

### Match

Individual match

```python
Match(game_id, summoner_id, game_time)
```

| Attribute   | Contents                          |
| ----------- | --------------------------------- |
| game_id     | match id as used by opgg          |
| summoner_id | summoner id as used by opgg       |
| game_time   | epoch timestamp of match          |
| json        | json representation of match data |

### Champions

Full champion stats of summoner for a season

```python
Champions(summoner_id, season=17)
```

| Attribute   | Contents                                   |
| ----------- | ------------------------------------------ |
| summoner_id | summoner id as used by opgg                |
| json        | json representation of champion stats      |
| df          | DataFrame representation of champion stats |

### Leaderboard

Top ranked summoners in Ranked Solo gamemode

```python
Leaderboard(page=1)
```

| Attribute | Contents                          |
| --------- | --------------------------------- |
| json      | json represenation of leaderboard |
| df        | df represenation of leaderboard   |

| Method               | Contents                                  |
| -------------------- | ----------------------------------------- |
| next_page()          | load next page of the leaderboard         |
| load_page(page: int) | load given page number of the leaderboard |

### Statistics

Playerbase statistics for all champions

```python
form = {
    'type': 'win',
    'league': 'challenger',
    'period': 'month',
    'mapId': 1,
    'queue': 'ranked'
}

Statistics(form)
```

#### Form Options

type

- win
- lose
- picked
- banned

league

- EMPTY STRING (All leagues)
- iron
- bronze
- silver
- gold
- platinum
- diamond
- master
- grandmaster
- challenger

period

- month
- week
- today

mapId

- 1 (Summoners Rift)
- 12 (Howling Abyss)

queue

- ranked
- aram

| Attribute | Contents                         |
| --------- | -------------------------------- |
| json      | json represenation of statistics |
| df        | df represenation of statistics   |
