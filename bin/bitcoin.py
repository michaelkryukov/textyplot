"""Parses bitcoin cost from http://bitcointicker.co/"""

from telnetlib import Telnet
import sys, re

with Telnet('ticker.bitcointicker.co', 10080) as tn:
    skip = True

    while True:
        try:
            match = re.match(r"\x1b\[10C\x1b\[.+?m(\d+?\.\d+?)\x1b\[H", str(tn.read_some(), "UTF-8"))
            if match:
                if skip:
                    skip = not skip
                    continue
                
                print(match.group(1))
                sys.stdout.flush()
        except KeyboardInterrupt:
            break
