import sys
from datetime import datetime

# accepting single line command arg (name of the file)
if len(sys.argv) < 2:
    print("need a log file name")
    sys.exit(1)

filename = sys.argv[1]
f = open(filename, "a") # writing log messages to a log file, appending so old logs still stay

# accepts log messages through input until it receives "QUIT"
for line in sys.stdin:
    line = line.strip()
    if line == "QUIT":
        break
    if line == "":
        continue

    parts = line.split(maxsplit=1) # splits into action and message
    action = parts[0] 
    msg = parts[1] if len(parts) > 1 else ""

    time = datetime.now().strftime("%Y-%m-%d %H:%M") # recording time stamp
    f.write(time + " [" + action + "] " + msg + "\n")
    f.flush()

f.close()