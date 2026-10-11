#10/10 11:46pm

Starting Project 1. It's three programs: a logger, an encryption program, and a driver that launches the other two and talks to them through pipes. I'm using Python with subprocess because I know Python the best and it's the most intuitive for me to write.

I went through the in-class example. cpu.py starts mem.py with Popen, sends it lines, and reads replies with readline(). mem.py flushes after every print, which I think is because output to a pipe gets buffered. Without the flush the reply would just sit in mem.py's buffer, and cpu.py would be stuck waiting on readline() forever. My driver will do the same thing but with two children. The encryption program needs stdin and stdout piped since it sends replies back, but the logger only needs stdin since it writes to a file.

This session I'm setting up git and starting encryption.py. I'll test it by hand with the spec's example(key HELLO, HELLO into OIWWC).


#10-11 12:20am

This session I'm writing encryption.py. It loops over stdin, splits each line into a command and argument, and replies with RESULT or ERROR. The key is a variable outside the loop so it stays set between commands.

For the cipher, A=0 through Z=25. Encrypting adds the key letter mod 26, decrypting subtracts it, and i % len(key) repeats the key if it's shorter than
the message. If PASS comes with no key I'll return an error instead of setting an empty key. Every print gets flush=True so the driver doesn't hang on readline() later.

I'll test it by typing commands by hand, using the spec's example (HELLO into OIWWC) and a shorter key to check the wraparound.