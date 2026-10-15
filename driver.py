import sys
import os
from subprocess import Popen, PIPE

# accepting a single command line argument (name of the log file)
if len(sys.argv) < 2:
    print("Usage: python driver.py <logfile>")
    sys.exit(1)

logfile = sys.argv[1]

# so it finds the other files even if i run it from a different folder
here = os.path.dirname(os.path.abspath(__file__))

# creates two new processes, encryption and logger
logger = Popen([sys.executable, os.path.join(here, "logger.py"), logfile],
               stdin=PIPE, encoding="utf8")

crypto = Popen([sys.executable, os.path.join(here, "encryption.py")],
               stdin=PIPE, stdout=PIPE, encoding="utf8")

history = []


# pipes to connect standard input and output
def log(action, msg):
    logger.stdin.write(action + " " + msg + "\n")
    logger.stdin.flush()


def send(cmd):
    crypto.stdin.write(cmd + "\n")
    crypto.stdin.flush()

    reply = crypto.stdout.readline().strip()
    parts = reply.split(" ", 1)

    if len(parts) == 1:
        return parts[0], ""

    return parts[0], parts[1]


def show_history():
    num = 1
    for item in history:
        print("  " + str(num) + ". " + item)
        num += 1


def get_input(prompt):
    # if there's history, let them pick from it
    if history:
        ans = input("Want to use something from history? (y/n): ")
        ans = ans.strip().lower()

        if ans == "y":
            show_history()
            print("  0. Type a new one instead")

            pick = input("Pick a number: ").strip()

            if pick.isdigit():
                pick = int(pick)
                if pick >= 1 and pick <= len(history):
                    return history[pick - 1], False

            # 0 or anything else just falls through to typing a new one

    s = input(prompt).strip()

    if not s.isalpha() or not s.isascii():
        return None, True

    return s.upper(), True


# provide the user with the option of using a string in the history or entering a new string
def password():
    log("CMD", "password")

    pw, new = get_input("Enter a password: ")

    if pw is None:
        print("Passwords can only have letters, try again.")
        log("ERROR", "Password had non-letter characters")
        return

    kind, rest = send("PASS " + pw)

    if kind == "RESULT":
        print("Password set.")
        log("RESULT", "Password set")  # don't log the actual password
    else:
        print("Something went wrong: " + rest)
        log("ERROR", rest)


# prompt the user for a string, record it in the history, and send an encrypt or decrypt command
def crypt(cmd):
    log("CMD", cmd.lower())

    text, new = get_input("Enter text to " + cmd.lower() + ": ")

    if text is None:
        print("Only letters are allowed, try again.")
        log("ERROR", "Input had non-letter characters")
        return

    if new:
        history.append(text)

    kind, rest = send(cmd + " " + text)

    if kind == "RESULT":
        print(cmd.capitalize() + "ed: " + rest)
        history.append(rest)
        log("RESULT", rest)
    else:
        print("Couldn't " + cmd.lower() + ": " + rest)
        log("ERROR", rest)


log("START", "Driver started")

try:
    # print a menu of commands and prompt the user for commands
    while True:
        print()
        print("What do you want to do? (password, encrypt, decrypt, history, quit)")
        choice = input("> ").strip().lower()

        if choice == "password":
            password()

        elif choice == "encrypt":
            crypt("ENCRYPT")

        elif choice == "decrypt":
            crypt("DECRYPT")

        elif choice == "history":
            log("CMD", "history")

            if not history:
                print("Nothing in history yet.")
            else:
                show_history()

            log("RESULT", "Showed " + str(len(history)) + " history entries")

        elif choice == "quit":
            log("CMD", "quit")
            break

        else:
            print("Not a command, try one from the list.")

except EOFError:
    # ctrl+d, just quit normally so the other two still close
    print()


# log exit first, logger stops listening after QUIT
log("EXIT", "Driver exited")

crypto.stdin.write("QUIT\n")
crypto.stdin.flush()

logger.stdin.write("QUIT\n")
logger.stdin.flush()

crypto.wait()
logger.wait()

print("Bye!")