import json
import random
import sys
import time

SAMPLES = 20
VARIABLES = ['var1', 'var2', 'var3']


def generate_sample():
    """Generate a random sample to be used as SimpleStats input."""
    # choice a random variable
    var = random.choice(VARIABLES)

    # generate ts in the last 7 days, random hours
    now = int(time.time())
    ts_delta = random.randint(0, 7)
    ts = now - ts_delta * 3600 * 24 - random.randint(0, 3600 * 24)

    # generate a random value
    value = random.randint(0, 100)

    return (var, ts, value)


if __name__ == '__main__':
    # usage: sample_generator [number of samples to generate]
    samples = SAMPLES
    if len(sys.argv) == 2:
        try:
            samples = int(sys.argv[1])
        except ValueError:
            pass

    for i in range(samples):
        print json.dumps(generate_sample())
