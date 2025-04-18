import time


class Timer:
    def __init__(self, _init_time=9000):
        self.init_time = _init_time  # 초기화 시간, 사용자 설정 시가
        self.timer_seconds = self.init_time  # 현재 남은 시간
        self.start_timer_seconds = self.timer_seconds  # 현재 남은 시작 시간
        self.is_start = False  # 시합 시작
        self.timer_running = False

    def get_time_remaining(self):
        minutes = self.timer_seconds // 6000
        seconds = (self.timer_seconds % 6000) // 100
        ms = self.timer_seconds % 100

        if minutes > 0:
            time_remaining = "{:02d}:{:02d}.{:02d}".format(minutes, seconds, ms)
        else:
            time_remaining = "{:02d}.{:02d}".format(seconds, ms)

        return time_remaining

    def get_elapsed_time(self):
        return int(
            (time.time() - self.start_time) * 100
        )  # Calculate the elapsed time in milliseconds

    def update_timer_seconds(self):
        # Update the timer seconds
        self.timer_seconds = self.start_timer_seconds - self.get_elapsed_time()

    def start(self, isStart):
        self.timer_running = isStart

        if isStart:
            self.start_time = time.time()  # Save the current time
        else:
            self.start_timer_seconds = self.timer_seconds

    def set_init_time(self, time):
        self.init_time = time
        self.timer_seconds = time
        self.start_timer_seconds = time

    def reset(self):
        self.timer_seconds = self.init_time
        self.start_timer_seconds = self.init_time
        self.timer_running = False
        self.is_start = False

    def increase_timer(self, time):
        self.timer_seconds += time
        self.start_timer_seconds = self.timer_seconds
        if not self.is_start:
            self.init_time = self.timer_seconds

    def decrease_timer(self, time):
        if (self.timer_seconds - time) > 0:
            self.timer_seconds -= time
            self.start_timer_seconds = self.timer_seconds
            if not self.is_start:
                self.init_time = self.timer_seconds
