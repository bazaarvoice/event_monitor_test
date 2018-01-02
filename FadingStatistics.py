import math


class FadingStatistics(object):

    increment_threshold = 0.0001

    alpha = 0.0
    sum = 0.0
    sum2 = 0.0
    increment = 0.0

    def __init__(self, window_size, oldest_weight):
        self.alpha = pow(oldest_weight, 1.0 / window_size)

    def reset(self):
        self.sum = 0.0
        self.sum2 = 0.0
        self.increment = 0.0

    def update(self, sample):
        self.weighted_update(sample, 1.0)

    def weighted_update(self, sample, weight):
        sw = sample * weight
        self.sum = (self.alpha * self.sum) + sw
        self.sum2 = (self.alpha * self.sum2) + (sw*sw)
        self.increment = (self.alpha * self.increment) + weight

    def mean(self):
        if self.increment < self.increment_threshold:
            return 0.0
        return self.sum / self.increment

    def deviation(self):
        if self.increment < self.increment_threshold:
            return 0.0
        mean = self.mean()
        return math.sqrt(abs( (self.sum2 / self.increment) - mean*mean))
