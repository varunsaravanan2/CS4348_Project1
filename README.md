# CS4348 Project 1

For this project, I made three programs in Python that talk to each other through pipes.

- `driver.py` - the main one. It starts the other two and runs the menu.
- `encryption.py` - does the encrypting and decrypting with a Vigenère cipher.
- `logger.py` - writes everything to a log file with the date and time.

The driver starts the other two using Popen. The encryption program needs stdin and stdout piped because the driver has to read what it sends back. The logger just needs stdin since it only writes to the file.

My notes from each session are in `devlog.md`.

## Running it

It's Python so there's nothing to compile, you just need Python 3. Make sure all three .py files are in the same folder, then run this from the command line:

```
python driver.py log.txt
```

You can name the log file whatever you want. If it doesn't exist yet the logger makes it, and if it does it just adds to the end.

## Commands

- `password` - sets the password (type a new one or pick from history)
- `encrypt` - encrypts a string (type a new one or pick from history)
- `decrypt` - decrypts a string (type a new one or pick from history)
- `history` - shows everything you've entered or gotten back this run
- `quit` - closes the other two programs and exits

You can only use letters for password, encrypt, and decrypt, so something like "Hello World!" won't work. Uppercase or lowercase doesn't matter because I change everything to uppercase before sending it. The password isn't saved in the history and doesn't get logged.

## Example

```
> password
Enter a password: hello
Password set.

> encrypt
Want to use something from history? (y/n): n
Enter text to encrypt: hello
Encrypted: OIWWC

> quit
Bye!
```

Here's what the log looked like after:

```
2026-10-15 15:19 [START] Driver started
2026-10-15 15:19 [CMD] password
2026-10-15 15:19 [RESULT] Password set
2026-10-15 15:20 [CMD] encrypt
2026-10-15 15:20 [RESULT] OIWWC
2026-10-15 15:26 [CMD] quit
2026-10-15 15:26 [EXIT] Driver exited
```

## Testing them separately

I tested the encryption program and logger by themselves before writing the driver. You can do the same by running them and typing into them.

```
python encryption.py
PASS HELLO
ENCRYPT HELLO
QUIT
```

This should print `RESULT` and then `RESULT OIWWC`.

```
python logger.py test.log
START testing
QUIT
```

Then run `cat test.log` to check what got written.