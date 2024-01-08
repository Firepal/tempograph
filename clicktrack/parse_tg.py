
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

class TimePoint:
    def __init__(self, beat, time):
        self.beat = beat
        self.time = time

class TempoFunction:
    CONST = 1
    LIN = 2
    POLY = 3

    def __init__(self, line: str, end: OffsetUnit):
        self.end = end
        self.parse_line(line)

    def parse_line(self, line):
        raise NotImplementedError

    def getTime(self, beatNum):
        raise NotImplementedError

    def getBeatNum(self, time):
        raise NotImplementedError

class ConstantFunction(TempoFunction):
    def parse_line(self, line):
        parts = line.split()
        self.type = self.CONST
        self.bpm = float(parts[1])
        self.start_offset = OffsetUnit(parts[2])

    def getTime(self, beatNum):

class LinearFunction(TempoFunction):
    def parse_line(self, line):
        parts = line.split()
        self.type = self.LIN
        self.start_bpm = float(parts[1])
        self.end_bpm = float(parts[2])
        self.length = float(parts[3])
        self.power = float(parts[4])
        self.start_offset = OffsetUnit(parts[5])

class PolynomialFunction(TempoFunction):
    def parse_line(self, line):
        parts = line.split()
        self.type = self.POLY
        self.start_bpm = float(parts[1])
        self.end_bpm = float(parts[2])