from observers.observer import Observable


class GameEventObservable(Observable):
    _game_event = None

    def set_game_event(self, event):
        self._game_event = event
        self.notify()
    
    def game_event(self):
        return self._game_event