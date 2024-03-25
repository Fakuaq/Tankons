from enums.game_event import GameEvent
from observers.observer import Observer
from observers.game_event_observable import GameEventObservable
import socket
import pickle
from threading import Thread

ADDRESS = ('127.0.0.1', 5555)


class Client(Observer):
    _identity = None

    def __init__(self, game_controller):
        GameEventObservable().attach(self)
        self._gc = game_controller
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_thread = Thread(target=self.listen)
        server_thread.daemon = True
        server_thread.start()

    def listen(self):
        while True:
            try:
                data, _ = self._s.recvfrom(1024)
                data = pickle.loads(data)
                (message_type, value) = data

                self.handle_response(message_type, value)
            except OSError as e:
                print(e)

    def transmit(self, message_type: GameEvent, value=None):
        self._s.sendto(pickle.dumps((message_type.value, value)), ADDRESS)

    def handle_response(self, message_type: str, value):
        match message_type:
            case GameEvent.JOIN.value:
                (identity, player_count) = value
                self._gc.set_identity(identity)
                self._identity = identity
                self._gc.set_player_count(player_count)
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
                self._gc.player_shoot(value)
            case GameEvent.POWERUP.value:
                (powerup_class_name, coords) = value
                self._gc.spawn_powerup(powerup_class_name, coords)

    def update(self, observable: GameEventObservable):
        event_type: GameEvent
        (event_type, _) = observable.game_event()

        match event_type.value:
            case GameEvent.SHOT.value:
                self.transmit(GameEvent.SHOT)
