class AggSum():
    def __init__(self):
        self.total = 0

    def handle(self, value):
        try:
            num = float(value)
        except ValueError:
            return
        self.total += num

    def result(self):
        return self.total

class AggCount():
    def __init__(self):
        self.total = 0

    def handle(self, value):
        self.total += 1

    def result(self):
        return self.total

class AggDistinctCount():
    def __init__(self):
        self.values = set()

    def handle(self, value):
        self.values.add(value)

    def result(self):
        return len(self.values)

class AggAvg():
    def __init__(self):
        self.total = 0
        self.count = 0

    def handle(self, value):
        try:
            num = float(value)
        except ValueError:
            return
        self.total += num
        self.count += 1

    def result(self):
        if self.count == 0:
            return None
        return self.total / self.count

class AggValues():
    def __init__(self):
        self.all_values = []

    def handle(self, value):
        self.all_values.append(value)

    def result(self):
        return self.all_values

class AggUniqueValues():
    def __init__(self):
        self.all_values = set()

    def handle(self, value):
        self.all_values.add(value)

    def result(self):
        return list(self.all_values)

class AggFirst():
    def __init__(self):
        self.first_value = None
        self.done = False

    def handle(self, value):
        if not done:
            self.first_value = value

    def result(self):
        return self.first_value

class AggLast():
    def __init__(self):
        self.last_value = None

    def handle(self, value):
        self.last_value = value

    def result(self):
        return self.last_value

class AggMin():
    def __init__(self):
        self.min_value = None

    def handle(self, value):
        try:
            num = float(value)
        except ValueError:
            return
        if self.min_value is None or num < self.min_value:
            self.min_value = num

    def result(self):
        return self.min_value

class AggMax():
    def __init__(self):
        self.max_value = None

    def handle(self, value):
        try:
            num = float(value)
        except ValueError:
            return
        if self.max_value is None or num > self.max_value:
            self.max_value = num

    def result(self):
        return self.max_value

AGG_FUNCTIONS = {
    'sum': AggSum,
    'count': AggCount,
    'unique_values': AggDistinctCount,
    'dc': AggDistinctCount,
    'avg': AggAvg,
    'values': AggValues,
    'unique_values': AggUniqueValues,
    'unique': AggDistinctCount,
    'first': AggFirst,
    'last': AggLast,
    'min': AggMin,
    'max': AggMax,
}
