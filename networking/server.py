import sys
from threading import Thread
from enums.game_event import GameEvent
import pickle
import socket
from observers.observer import Observer
from observers.game_event_observable import GameEventObservable

ADDRESS = ('127.0.0.1', 5555)
MAX_SUPPORTED_PLAYERS = 4


class Server(Observer):
    _gc = None
    _client_addresses = {}
    _current_client_count = 0
    _client_count = 2
    _player_coords = {}

    def __init__(self, game_controller):
        GameEventObservable().attach(self)
        self._gc = game_controller
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._s.bind(ADDRESS)
        print(f'Listening on port: {ADDRESS[1]}')
        
        if len(sys.argv) > 2 and int(sys.argv[2]) > MAX_SUPPORTED_PLAYERS:
            print(f'Game only supports a maximum of {MAX_SUPPORTED_PLAYERS} players')
            exit()
        elif len(sys.argv) > 2 and int(sys.argv[2]) <= MAX_SUPPORTED_PLAYERS:
            self._client_count = int(sys.argv[2])
        
        server_thread = Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()

    def run_server(self):
        while True:
            data, addr = self._s.recvfrom(1024)

            try:
                data = pickle.loads(data)
            except pickle.UnpicklingError:
                print('Error unpickling data:', data)
                continue

            message_type: GameEvent
            (message_type, value) = data
            self.handle_response(message_type, value, addr)

    def handle_response(self, message_type: GameEvent, value, addr):
        player_index = None
        for k, v in self._client_addresses.items():
            if v == addr:
                player_index = k
                break

        match message_type:
            case GameEvent.JOIN.value:
                self._current_client_count += 1
                self._client_addresses[self._current_client_count] = addr
                self._player_coords[self._current_client_count] = (0, 0, 0)
                print(f'Joined player nr.{self._current_client_count}')

                self.unicast(addr, GameEvent.JOIN, (self._current_client_count, self._client_count))

                if self._current_client_count == self._client_count:
                    print('Game starting')
                    self._gc.set_player_count(self._client_count)
                    layout = self._gc.pick_layout()
                    self._gc.render_layout(layout)
                    coords = self._gc.spawn_coordinates()
                    self._gc.start_game(coords)

                    self.broadcast(GameEvent.START_ROUND, (layout, coords))
                    self._gc.session_started = True

                    for i, coord in enumerate(coords):
                        self._player_coords[i + 1] = coord[0], coord[1], 0

            case GameEvent.COORDS.value:
                self._player_coords[player_index] = value
                self._gc.set_player_coords({player_index: value})

                self.unicast(addr, GameEvent.COORDS, self._player_coords)

            case GameEvent.SHOT.value:
                self._gc.player_shoot(player_index)
                self.broadcast_except(addr, GameEvent.SHOT, player_index)

    def unicast(self, address, message_type: GameEvent, value=None):
        self._s.sendto(pickle.dumps((message_type.value, value)), address)

    def broadcast(self, message_type: GameEvent, value=None):
        for addr in self._client_addresses.values():
            self._s.sendto(pickle.dumps((message_type.value, value)), addr)

    def broadcast_except(self, address, message_type: GameEvent, value=None):
        for addr in self._client_addresses.values():
            if addr != address:
                self._s.sendto(pickle.dumps((message_type.value, value)), addr)

    def update(self, observable: GameEventObservable):
        event_type: GameEvent
        (event_type, event_value) = observable.game_event()

        match event_type.value:
            case GameEvent.START_ROUND.value:
                layout = self._gc.pick_layout()
                self._gc.render_layout(layout)
                coords = self._gc.spawn_coordinates()
                self._gc.start_game(coords)
                self.broadcast(GameEvent.START_ROUND, (layout, coords))
            case GameEvent.RESET_ROUND.value:
                self.broadcast(GameEvent.RESET_ROUND, event_value)
