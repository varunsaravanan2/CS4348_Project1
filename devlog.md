#10-10 11:46pm

Starting Project 1. It's three programs: a logger, an encryption program, and a driver that launches the other two and talks to them through pipes. I'm using Python with subprocess because I know Python the best and it's the most intuitive for me to write.

I went through the in-class example. cpu.py starts mem.py with Popen, sends it lines, and reads replies with readline(). mem.py flushes after every print, which I think is because output to a pipe gets buffered. Without the flush the reply would just sit in mem.py's buffer, and cpu.py would be stuck waiting on readline() forever. My driver will do the same thing but with two children. The encryption program needs stdin and stdout piped since it sends replies back, but the logger only needs stdin since it writes to a file.

This session I'm setting up git and starting encryption.py. I'll test it by hand with the spec's example(key HELLO, HELLO into OIWWC).


#10-11 12:20am

This session I'm writing encryption.py. It loops over stdin, splits each line into a command and argument, and replies with RESULT or ERROR. The key is a variable outside the loop so it stays set between commands.

For the cipher, A=0 through Z=25. Encrypting adds the key letter mod 26, decrypting subtracts it, and i % len(key) repeats the key if it's shorter than the message. If PASS comes with no key I'll return an error instead of setting an empty key. Every print gets flush=True so the driver doesn't hang on readline() later.

I'll test it by typing commands by hand, using the spec's example (HELLO into OIWWC) and a shorter key to check the wraparound.

#10-12 5:01pm

Finished encryption.py. I mostly just followed the spec: read a line, split off the first word as the command, reply with RESULT or ERROR. Every reply flushes since the driver will be reading through a pipe. Decrypt is just encrypt backwards, so I used one function for both. Checked it with the spec's HELLO example and got OIWWC.

The thing I went back and forth on was replying ERROR to unknown commands, since the spec doesn't ask for it. I almost took it out, but then realized if the driver ever sends something and gets no reply, it'll just hang on readline() forever. So I kept it. Same reason a PASS with no key gives an error instead of crashing.

Logger next.

#10-13 2:25pm

Starting logger.py. This one should be easier since it never replies, the driver just sends it lines, so only stdin needs a pipe. The log file name comes from the command line, which is how the driver passes it in when it starts the logger as its own process.

Plan is to read lines until QUIT, split off the first word as the action, and write it out with a timestamp using strftime. I'm going with append mode so old logs don't get wiped and I'll flush after every line so nothing gets lost if the driver crashes.

One thing I'm not sure about is what happens if the driver crashes before it sends QUIT. I think the logger's stdin would just hit the end, since nothing's on the other side of the pipe anymore, so the loop would end on its own. I want to test that.

#10-13 3:22pm

Finished logger.py. It reads lines from stdin until QUIT and splits the input into the action and message. Wrote the open method using the append mode so the old logs stay rather than getting deleted.

The issue I ran into during this part was how to split the line. At first I used the split(" ") to catch the whitespace, but when I looked at the spec's wording, I realized a tab or more than one space would have left extra whitespace if I were to keep it that way. To fix this, I changed it to split at the first part of whitespace instead.

Driver next.


#10-15 1:22am

Starting driver.py. This should be the main part of the project from what I am reading. It has to start the encryption and logger programs as their own processes using Popen.The encryption program needs both stdin and stdout piped since I have to read what it sends back, but the logger only needs stdin since it never replies.

After that it just loops through a menu until the user quits. Anything the user types for password, encrypt, or decrypt has to be only letters. Also have to remember to make it uppercase before sending it. The strings for encrypt and decrypt get saved in the history. However, the password doesn't and it shouldn't show up in the log either. When the user quits, I think I need to log the exit first and then send QUIT to the logger, because once it gets QUIT it won't log anything else.