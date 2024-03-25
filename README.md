# Tankons

## Setup

Dependencies are defined in [requirements.txt](requirements.txt)

## Running locally

To run game locally (max 2 players) `python main.py`

1. Player
   * Up/Down: `W`/`S` 
   * Rotate left/right: `E`/`R`
   * Shoot `F`
2. Player 
   * Up/Down: `Arrow Up`/`Arrow Down`
   * Rotate left/right: `Arrow Left`/`Arrow Right`
   * Shoot `/`

## Running multiplayer

Adjust the IP addresses and ports if necessary in [client.py](networking/client.py), [server.py](networking/server.py)

Controls for each client are the same as 1. player controls defined above

Server runs it's own game instance and only support 1 game instance at a time for now

### Server

Running up to four players: `python main.py server <client_count>`

Default is two players: `python main.py server` 

### Client
`python main.py client`




