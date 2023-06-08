## Stack-Zero

![](https://Cyberguru1.github.io/posts/phoenix/files/st0_header.png)

This is the first challenge from the stack overflow series of phoenix previously known as protostar so let's get right into it, from the challenge site a source code was given as shown below:

###  Soucrce Code
--
```
/*
 * phoenix/stack-zero, by https://exploit.education
 *
 * The aim is to change the contents of the changeme variable.
 *
 * Scientists have recently discovered a previously unknown species of
 * kangaroos, approximately in the middle of Western Australia. These
 * kangaroos are remarkable, as their insanely powerful hind legs give them
 * the ability to jump higher than a one story house (which is approximately
 * 15 feet, or 4.5 metres), simply because houses can't can't jump.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BANNER \
  "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

char *gets(char *);

int main(int argc, char **argv) {
  struct {
    char buffer[64];
    volatile int changeme;
  } locals;

  printf("%s\n", BANNER);

  locals.changeme = 0;
  gets(locals.buffer);

  if (locals.changeme != 0) {
    puts("Well done, the 'changeme' variable has been changed!");
  } else {
    puts(
        "Uh oh, 'changeme' has not yet been changed. Would you like to try "
        "again?");
  }

  exit(0);
}

```

This code snippet represents a simple C program. Let's go through it step by step:

- The line `"Welcome to " LEVELNAME ", brought to you by https://exploit.education" `is a string literal that will be printed as part of the program's execution. `LEVELNAME` is expected to be a preprocessor macro or a variable containing a specific level name. The string is not directly used in this code snippet, but it's worth noting for context.

- The declaration` char *gets(char *)`; is a function prototype for a function named gets(). However, it's important to mention that using gets() is highly discouraged due to security vulnerabilities. It is not safe to use in modern programming and has been removed from the latest C standards. It's strongly recommended to use alternative functions like `fgets()` for reading input.

- The main() function is the entry point of the program. It takes two arguments: `argc` (the number of command-line arguments) and `argv` (an array of strings containing the command-line arguments).

- Inside the` main()` function, there is a definition of a structure with two members:` buffer`, an array of characters with a size of 64, and `changeme`, a volatile integer. The volatile keyword tells the compiler that the value of this variable can be changed by external factors, such as interrupts or other threads, and therefore, the compiler should not perform certain optimizations on it.

- The `printf()` function is used to print the contents of the `BANNER` string. However, the definition of` BANNER` is not provided in the code snippet, so it's assumed to be defined elsewhere in the program.

- `locals.changeme` is initialized to 0.

- The `gets()` function is called, passing `locals.buffer` as the argument. This function reads characters from the standard input and stores them in `locals.buffer`. However, it's important to note that using `gets()` is highly unsafe because it does not check the length of the input and can easily lead to buffer overflow vulnerabilities which is the main goal of this challenge.

- After the `gets()` function, there is a conditional statement that checks whether `locals.changeme` has been changed. If it is not equal to` 0`, the program outputs the message `"Well done, the 'changeme' variable has been changed!" `using the` puts()` function. Otherwise, if `locals.changeme` is still` 0`, the program outputs the message` "Uh oh, 'changeme' has not yet been changed. Would you like to try again?"`.

- Finally, the `exit(0)` function is called to terminate the program with a status code of 0, indicating successful execution.


The use of `gets()` and the lack of input validation is what we are going to use to perform the buffer overflow attack, so the function call `gets(local.buffer)` ask the user for input and store the input into the buffer array, one thing to note here is that there is not input validation to check the length of input and compare it against the size of the buffer array and the `gets()` function does not perform that extra step of comparison, so using this methodology we could easily overflow the `locals.buffer` array and change the value of `locals.changeme`.

Demonstrating:

we first launch the program and try giving it an input of 64 bytes of A's to see the program reaction; we could easily do this in python and pass the result using pipe `|` to the program

![](https://Cyberguru1.github.io/posts/phoenix/files/st0_s1.png)

we could see that the changeme variable hasn't been changed, overflowing the buffer by just increasing the values of A's from 64 to 65 will cause the `locals.buffer` to overflow and change the current value of the `locals.changeme`

![](https://Cyberguru1.github.io/posts/phoenix/files/st0_s2.png)

and violla!! we successfully changed the value of changeme varaible........but  what's really going on under the hood let's enter gdb and see what exactly

we opened the program in gdb and show the disassembly code:

![](https://Cyberguru1.github.io/posts/phoenix/files/st0_gdb1.png)

from the source code we could see that the address of the local struct variables of buffer array and changeme is at `rbp-50` and `rbp-0x10` respectively

![](https://Cyberguru1.github.io/posts/phoenix/files/st0_gdb5.png)

knowing these we could simply set a breakpoint at the comparision point in the assembly that is `test eax, eax` then we examine the stack

runnig the program and supplying it 65 A's we reached the breakpoint

![](https://Cyberguru1.github.io/posts/phoenix/files/st0_gdb6.png)

we could see that the buffer array of size 64 starts from `0x7fffffffe660 - 90` that's exactly `0x50` in hex if you subtract it, while the address of the changeme variable is at `0x7fffffffe6a0` (stack address grows downward) where we could see our last A after the 64 A's that have filled up the buffer went to

continuing the program gives us our well done message

![](https://Cyberguru1.github.io/posts/phoenix/files/st0_gdb4.png)
