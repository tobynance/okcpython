import sys

print """|RESPONSE|ship locations|0 9 H|0 8 H|0 7 H|0 6 H|0 5 H|END|
|RESPONSE|shots|0 0|1 0|0 1|1 1|2 1|END|
|RESPONSE|shots|0 2|1 2|2 2|0 3|1 3|END|
|RESPONSE|shots|2 3|3 3|0 4|1 4|2 4|END|
|RESPONSE|shots|3 4|4 4|END|
"""
sys.stdout.flush()

while raw_input().strip() != "|INFO|end game|END|":
    pass
