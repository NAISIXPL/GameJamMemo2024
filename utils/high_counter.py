from sprites.candy import Candy


class HighCounter:
    def __init__(self):
        self.lower_thr = 45
        self.high_thr = 55
        self.current_status = 50

    def absorb_candy(self, candy: Candy):
        self.current_status += candy.points
        if self.current_status > 100:
            self.current_status = 100
        if self.current_status < 0:
            self.current_status = 0
        candy.kill()