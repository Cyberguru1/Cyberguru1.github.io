### GDB BASICS

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basic.png)

This another challenge from crackme that tends to test your knowledge of GDB debugger,[link](https://crackmes.one/crackme/645d3d4e33c5d43938913079) to challenge.

A zip file was given in the challenge description, downloading it and unzipping we have:
![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basics_fileinfo.png)

we could see that it's a dynamically linked x86-64 executable file which is not stripped (^*__*^), when we run the file it prompts us for a password.

plugging the file in gdb we have:

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basics_run.png)

setting the disassembly flavour to intel for easy readability of the assembly and getting info on the available functions we have:

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basics_gdb.png)

from the previous photo we could see that the executable doesn't have much functions but theres a main

disassemblying the main function we have:

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basics_disass_main.png)

we could see that there's some assembly call's here and there

explaning the assembly code

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basics_asm.png)

- the first marked line shows that the decimal `2` is stored  4 bytes down the base pointer `[rbp-0x4]`
- the second shows that another decimal `2` is stored 8 bytes down the base pointer `[rbp-0x8]`
- then a comparision is made between `0x13` and `[rbp-0x8]` which then enters a *For Loop*  till `[rbp-0x8]` is equal to `0x13`
- within the loop `[rbp-0x4]` is multiplied with `[rbp-0x8]`  with the assembly `imul` which then `[rbp-0x8]` is incremented
- the first two instructions before the fourth marked instructions prompts the user for input and stores the input into the `[rbp-0xc]` register which would then be used for further comparisions
- the fourth instruction then compares the user input stored in the `[rbp-0xc]` register against the result of the for loop multiplication stored in the `[rbp-0x4]` register, if the result is positive then fifth marked instruction executes and prints out the flag, else the  sixth marked instruction executes and prints out wrong password!!

from our analysis above we could write a javascript code that proves our assertions from the assembly code

```
var prod = 2;

for(var i = 2; i < 14; i++){
    prod *= i;
}

console.log("Enter your password: ");
var user_input =  readline()
user_input = parseInt(user_input, 10)
if (user_input === prod){
    console.log("Correct, here's your FLAG");
}
else{
    console.log("WRONG, try again!!!");
}
```

but let's leave this aside for now since the challenge is base on gdb, and we should find a way to get the password using gdb, Now how do we go about that ???

WHAT DO WE KNOW TO GET THE PASSWORD ???

we know that the password is generated at runtime of the program and is stored somewhere in the program memeory which is then compared against our input, which the program then decide if it matches or not, with this idea in mind we could use the super power of GDB to debug the program and set breakpoints, but wait a minute, where is this important comparision against our password and the program password made -- well going back to the previous picture were the assembly are marked, the fourth marked instruction shows us that important point.......well good let's carry on

going back to gdb and executing the program for the first time and supplying a random password::

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basics_wp.png)

now let's set that breakpoint and examine the contents of `[rbp-0x4]` we have:

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basics_pass.png)

from the previous pic we could see that our breakpoint was hit and we saw the contents of `[rbp-0x4]` as 219283456 pheeeeee........ that was a easy one, now let's check the password in the program

![](https://blog.cyb3rguru.tech/posts/crackme/images/gdb_basic_flag.png)

and taraaaaaaaah....... we got our love message!!!!!!!
