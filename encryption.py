import sys

def vigenere(text, key, direction):
    """direction is 1 to encrypt, -1 to decrypt. Assumes uppercase letters."""
    result = []
    for i, ch in enumerate(text):
        t = ord(ch) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')
        result.append(chr((t + direction * k) % 26 + ord('A')))
    return "".join(result)

def reply(kind, message=""):
    # flush so the driver's readline() gets the reply right away
    if message:
        print(f"{kind} {message}", flush=True)
    else:
        print(kind, flush=True)

def main():
    key = None
 
    for line in sys.stdin:
        line = line.rstrip("\n")
        command, _, arg = line.partition(" ")
        command = command.upper()
        arg = arg.strip()
 
        if command == "QUIT":
            break
 
        elif command == "PASS":
            if not arg:
                reply("ERROR", "No password given")
            else:
                key = arg.upper()
                reply("RESULT")
 
        elif command in ("ENCRYPT", "DECRYPT"):
            if key is None:
                reply("ERROR", "Password not set")
            else:
                direction = 1 if command == "ENCRYPT" else -1
                reply("RESULT", vigenere(arg.upper(), key, direction))
 
        else:
            reply("ERROR", f"Unknown command: {command}")
 
 
if __name__ == "__main__":
    main()