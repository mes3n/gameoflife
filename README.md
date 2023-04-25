# Game of Life
A thrown together visualisation of Game of Life, written in Python with a pyglet frontend.

## What is the Game of Life?

Game of life is a cellular automaton. It's a 0 player game and abides by a simple set of rules. Following the seeding, or manual generation, for the cells' states the whole game is played out by these rules: 

---
* A living cell dies if surrounded by less than 2 living cells
* A living cell dies if surrounded bu more than 3 living cells
* A living cell lives if surrounded by 2 or 3 living cells
* A dead cell becomes live if surrounded by precisely 3 neighbours
---

Following the start of the game the cells follow this set of rules until a stable shape has been reached, when the shape begins repeating. 

## Installation

Make sure to have Python and pip installed.

Then, install the dependencies:
```bash
pip install -r requirements.txt
```

Lastly run the program with:
```bash
python bin/main.py
```

## Keymappings

| Key | Function |
| --- | --- |
| Esc | Exit program |
| Space | Toggle pause |
