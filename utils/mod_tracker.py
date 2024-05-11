class ModTracker:
    def __init__(self, high_counter):
        self.high_counter = high_counter

    def player_damage(self, value):
        if self.high_counter.current_status > self.high_counter.high_thr:
            return 2 * value
        return value

    def player_speed(self, value):
        if self.high_counter.current_status > self.high_counter.high_thr:
            return 0.75 * value
        return value

    def player_jump(self, value):
        if self.high_counter.current_status < self.high_counter.lower_thr:
            return 1.25 * value
        return value

    def mob_damage(self, value):
        if self.high_counter.current_status < self.high_counter.lower_thr:
            return 2 * value
        return value

    def over_red(self) -> bool:
        if self.high_counter.current_status < 10:
            return True
        return False

    def over_blue(self) -> bool:
        if self.high_counter.current_status > 90:
            return True
        return False
