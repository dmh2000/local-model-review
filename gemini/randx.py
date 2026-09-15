import random
import math
import sys

class StdRandom:
    seed = None

    @classmethod
    def setSeed(cls, s):
        cls.seed = s
        random.seed(s)

    @classmethod
    def getSeed(cls):
        return cls.seed

    @classmethod
    def uniformDouble(cls, lo=0.0, hi=1.0):
        if not (lo <= hi):
            raise ValueError(f"invalid range: [{lo}, {hi})")
        return lo + (hi - lo) * random.random()

    @classmethod
    def uniformInt(cls, n):
        if n <= 0:
            raise ValueError("argument must be positive: " + str(n))
        return random.randint(0, n - 1)

    @classmethod
    def uniformLong(cls, n):
        if n <= 0:
            raise ValueError("argument must be positive: " + str(n))
        return random.randint(0, n - 1)

    @classmethod
    def bernoulli(cls, p=0.5):
        if p < 0.0 or p > 1.0:
            raise ValueError("probability p must be between 0.0 and 1.0: " + str(p))
        return random.random() < p

    @classmethod
    def gaussian(cls, mu=0.0, sigma=1.0):
        return mu + sigma * cls._gaussianStandard()

    @classmethod
    def _gaussianStandard(cls):
        r = 1.0
        while r >= 1.0 or r == 0.0:
            x = cls.uniformDouble(-1.0, 1.0)
            y = cls.uniformDouble(-1.0, 1.0)
            r = x * x + y * y
        return x * math.sqrt(-2 * math.log(r) / r)

    @classmethod
    def geometric(cls, p):
        if p <= 0.0 or p > 1.0:
            raise ValueError("probability p must be between 0.0 and 1.0: " + str(p))
        if p == 1.0:
            return 1
        return math.ceil(math.log(1.0 - random.random()) / math.log(1.0 - p))

    @classmethod
    def poisson(cls, lambda_val):
        if lambda_val <= 0.0:
            raise ValueError("lambda must be positive: " + str(lambda_val))
        if lambda_val == float('inf') or math.isinf(lambda_val):
            raise ValueError("lambda must not be infinite: " + str(lambda_val))
        if math.isnan(lambda_val):
            raise ValueError("lambda must not be NaN: " + str(lambda_val))
        if lambda_val < 700.0:
            k = 0
            p = 1.0
            expLambda = math.exp(-lambda_val)
            while p >= expLambda:
                k += 1
                p *= random.random()
            return k - 1
        else:
            # Gaussian approximation for large lambda
            val = int(round(cls.gaussian(lambda_val, math.sqrt(lambda_val))))
            return max(0, val)

    @classmethod
    def discrete(cls, a):
        if a is None:
            raise ValueError("argument array must not be null")
        if len(a) == 0:
            raise ValueError("argument array must not be empty")

        if any(isinstance(x, float) for x in a):
            return cls._discreteProbabilities(a)
        else:
            return cls.discreteFrequencies(a)

    @classmethod
    def _discreteProbabilities(cls, probabilities):
        eps = 1e-14
        total = 0.0
        for i in range(len(probabilities)):
            if probabilities[i] < 0:
                raise ValueError("array entry " + str(i) + " must be non-negative: " + str(probabilities[i]))
            total += probabilities[i]
        if total > 1.0 + eps or total < 1.0 - eps:
            raise ValueError("sum of array entries does not approximately equal 1.0: " + str(total))
        while True:
            r = random.random()
            total = 0.0
            for i in range(len(probabilities)):
                total += probabilities[i]
                if total > r:
                    return i

    @classmethod
    def discreteFrequencies(cls, frequencies):
        if frequencies is None:
            raise ValueError("argument array must not be null")
        if len(frequencies) == 0:
            raise ValueError("argument array must not be empty")
        sum_freq = 0
        for i in range(len(frequencies)):
            if frequencies[i] < 0:
                raise ValueError("array entry " + str(i) + " must be non-negative: " + str(frequencies[i]))
            sum_freq += frequencies[i]
        if sum_freq == 0:
            raise ValueError("at least one array entry must be positive")
        if sum_freq >= sys.maxsize:
            raise ValueError("sum of frequencies overflows an int")
        r = random.randint(0, sum_freq - 1)
        sum_freq = 0
        for i in range(len(frequencies)):
            sum_freq += frequencies[i]
            if sum_freq > r:
                return i

    @classmethod
    def exponential(cls, lambda_val):
        if lambda_val <= 0.0:
            raise ValueError("lambda must be positive: " + str(lambda_val))
        return -math.log(1.0 - random.random()) / lambda_val

    @classmethod
    def shuffle(cls, a, lo=None, hi=None):
        if a is None:
            raise ValueError("argument array must not be null")
        if lo is None and hi is None:
            random.shuffle(a)
            return
        if lo is None:
            lo = 0
        if hi is None:
            hi = len(a)
        if lo < 0 or hi > len(a) or lo > hi:
            raise ValueError(f"invalid sublist indices: lo={lo}, hi={hi}, len={len(a)}")
        # In-place sublist shuffle using Fisher-Yates algorithm
        for i in range(lo, hi):
            r = random.randint(i, hi - 1)
            a[i], a[r] = a[r], a[i]

class StdOut:
    @staticmethod
    def println(obj=""):
        print(obj)

    @staticmethod
    def print(obj=""):
        print(obj, end='')

    @staticmethod
    def printf(format_str, *args):
        print(format_str % args, end='')

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Usage: python script.py <n> [seed]")
        sys.exit(1)
    n = int(args[1])
    if len(args) == 3:
        seed = int(args[2])
        StdRandom.setSeed(seed)
    probabilities = [0.5, 0.3, 0.1, 0.1]
    frequencies = [5, 3, 1, 1]
    a = "A B C D E F G".split(" ")

    print(f"seed = {StdRandom.getSeed()}")
    for _ in range(n):
        print(f"{StdRandom.uniformInt(100):2d}", end='')
        print(f" {StdRandom.uniformDouble(10.0, 99.0):8.5f}", end='')
        print(f" {StdRandom.bernoulli(0.5)}", end='')
        print(f" {StdRandom.gaussian(9.0, 0.2):7.5f}", end='')
        print(f" {StdRandom.discrete(probabilities)}", end='')
        print(f" {StdRandom.discrete(frequencies)}", end='')
        print(f" {StdRandom.uniformLong(100000000000)}", end='')
        StdRandom.shuffle(a)
        for s in a:
            print(s, end='')
        print()
