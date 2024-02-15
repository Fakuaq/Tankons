from enums.game_event import GameEvent
from observers.observer import Observer
from observers.game_event_observable import GameEventObservable
import socket
import pickle
from threading import Thread

HOST = '127.0.0.1'
PORT = 5555


class Client(Observer):
    _identity = None

    def __init__(self, game_controller):
        GameEventObservable().attach(self)
        self._gc = game_controller
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((HOST, PORT))

        server_thread = Thread(target=self.listen)
        server_thread.daemon = True
        server_thread.start()

    def listen(self):
        while True:
            data = self._s.recv(1024)
            data = pickle.loads(data)
            (message_type, value) = data

            self.handle_response(message_type, value)

    def transmit(self, message_type: GameEvent, value=None):
        self._s.sendall(pickle.dumps((message_type.value, value)))

    def handle_response(self, message_type: str, value):
        match message_type:
            case GameEvent.JOIN.value:
                self._gc.set_identity(value)
                self._identity = value
            case GameEvent.START_ROUND.value:
                self._gc.reset_game()
                self._gc.session_started = True
                (layout_index, spawn_coords) = value
                self._gc.render_layout(layout_index)
                self._gc.start_game(spawn_coords)
            case GameEvent.RESET_ROUND.value:
                self._gc.update_scoreboard(value)
            case GameEvent.COORDS.value:
                self._gc.set_player_coords(value)
            case GameEvent.SHOT.value:
                print(value)
                self._gc.player_shoot(value)
            case GameEvent.POWERUP.value:
                (powerup_class_name, coords) = value
                self._gc.spawn_powerup(powerup_class_name, coords)

    def update(self, observable: GameEventObservable):
        (event_type, event_value) = observable.game_event()

        match event_type:
            case GameEvent.SHOT.value:
                self.transmit(GameEvent.SHOT)

    def __del__(self):
        self._s.close()
