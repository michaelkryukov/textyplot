from __future__ import print_function
import random, time, sys

wait = 0
if len(sys.argv) > 1:
    wait = float(sys.argv[1])

lower = -20000
upper = 20000

while True:
    try:
        print(random.randint(lower, upper))
        sys.stdout.flush()
        if wait:
            time.sleep(wait)
        if random.randint(0, 42) == 23:
            lower = random.randint(-20000, 0)
            upper = random.randint(0, 20000)
    except KeyboardInterrupt:
        break
