import numpy as np

class TimePoint:
    def __init__(self, beat, time):
        self.beat = beat
        self.time = time

    def copy(self):
        return TimePoint(self.beat, self.time)

    def __repr__(self):
        m = int(self.time // 60)
        s = int(self.time % 60)
        p = int((self.time % 1) * 100)
        return f"[{m:02d}:{s:02d}.{p:02d} {self.beat:.2f}b]"

class OffsetUnit:
    BEATS = 1
    SECONDS = 2
    def __init__(self, unit):
        if unit.endswith("b"):
            self.mode = self.BEATS
            self.val = float(unit[:-1])
        else:
            self.mode = self.SECONDS
            self.val = float(unit)

    def shift(self, time_point: TimePoint):
        if self.mode == self.SECONDS:
            self.val += time_point.time
        elif self.mode == self.BEATS:
            self.val += time_point.beat

class TempoFunction:
    CONST = 1
    LIN = 2
    POLY = 3

    def get_time(self, beat_num):
        raise NotImplementedError

    def get_beat_num(self, elapsed_time):
        raise NotImplementedError

    def get_time_point(self, offset: OffsetUnit):
        if offset.mode == offset.SECONDS:
            return TimePoint(self.get_beat_num(offset.val), offset.val)
        elif offset.mode == offset.BEATS:
            return TimePoint(offset.val, self.get_time(offset.val))

    def is_in_range(self, offset: OffsetUnit):
        if offset.mode == offset.BEATS:
            self.is_beat_in_range(offset.val)
        elif offset.mode == offset.SECONDS:
            self.is_time_in_range(offset.val)

    def is_beat_in_range(self, b):
        return self.start.beat <= b <= self.end.beat

    def is_time_in_range(self, t):
        return self.start.time <= t <= self.end.time

    def get_beats(self):
        beats = []
        b = np.ceil(self.start.beat)
        while self.is_beat_in_range(b):
            beats.append(TimePoint(b, self.get_time(b)))
            b += 1
        return beats

class ConstantFunction(TempoFunction):
    def __init__(self, start:TimePoint, bpm: float, end:OffsetUnit):
        self.type = self.CONST
        self.start = start
        self.bpm = bpm
        if end.mode == end.SECONDS:
            seconds_length = end.val - start.time
            beats_length = seconds_length * self.bpm / 60
        elif end.mode == end.BEATS:
            beats_length = end.val - start.beat
            seconds_length = beats_length * 60 / self.bpm
        else:
            raise ValueError
        self.end = TimePoint(start.beat + beats_length, start.time + seconds_length)

    def get_time(self, beat_num):
        if beat_num < self.start.beat or beat_num > self.end.beat:
            raise ValueError
        elapsed = (beat_num - self.start.beat) * 60 / self.bpm
        return self.start.time + elapsed

    def get_beat_num(self, elapsed_time):
        if (elapsed_time < self.start.time) or (elapsed_time > self.end.time):
            raise ValueError
        elapsed = (elapsed_time - self.start.time) * self.bpm / 60
        return self.start.beat + elapsed

    def __repr__(self):
        return f"C:{self.start}--{self.bpm}--{self.end}"

class LinearFunction(TempoFunction):
    def __init__(self, start:TimePoint, start_bpm: float, end_bpm:float, power:float, end:OffsetUnit):
        self.type = self.LIN
        self.start = start
        self.start_bpm = start_bpm
        self.end_bpm = end_bpm
        if end.mode == end.SECONDS:
            seconds_length = end.val - start.time
            average_bpm = (self.start_bpm + self.end_bpm) / 2
            beats_length = seconds_length * average_bpm / 60
        elif end.mode == end.BEATS:
            raise NotImplementedError("This would require a lot of algebra and I don't wanna do it right now") # [its ok this is cool af - firepal]
        else:
            raise ValueError
        self.end = TimePoint(start.beat + beats_length, start.time + seconds_length)


    def get_time(self, beat_num):
        if beat_num == self.start.beat:
            return self.start.time
        if beat_num == self.end.beat:
            return self.end.time
        slope = (self.end_bpm / 60  - self.start_bpm / 60) / (self.end.time - self.start.time)
        y_int = self.start_bpm / 60

        # terms for polynomial (integral of line)
        a = slope / 2
        b = y_int
        c = -(beat_num - self.start.beat)
        p1 = np.polynomial.Polynomial([c,b,a])
        roots = p1.roots()
        for r in roots:
            if 0 < r < self.end.time - self.start.time:
                return r + self.start.time
        raise ValueError

    def get_beat_num(self, elapsed_time):
        if (elapsed_time < self.start.time) or (elapsed_time > self.end.time):
            raise ValueError
        # lerp
        amt_elapsed = (elapsed_time - self.start.time) / (self.end.time - self.start.time)
        current_bpm = (self.end_bpm - self.start_bpm) * amt_elapsed + self.start_bpm

        # area under curve
        avg_bpm = current_bpm + self.start_bpm / 2
        elapsed_beats = elapsed_time * avg_bpm / 60

        return self.start.beat + elapsed_beats

    def __repr__(self):
        return f"L:{self.start}--{self.start_bpm}->{self.end_bpm}--{self.end} "
