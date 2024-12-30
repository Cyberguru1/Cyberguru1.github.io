### EasyCrackMe:)

![image](https://cyberguru1.github.io/posts/crackme/images/chall_easy_Crackme.png)

This is our first crackme in the crackme series, downloading the file and unzipping it we have:

![image](https://cyberguru1.github.io/posts/crackme/images/file_type_easycrack.png)

runnig the file with wine emulator we could see that it prompts us for a password

![image](https://cyberguru1.github.io/posts/crackme/images/easy_chall_run.png)

![image](https://cyberguru1.github.io/posts/crackme/images/trying_easy_chall.png)

let's run strings on the file and see what we got:

![image](https://cyberguru1.github.io/posts/crackme/images/east_chall_strings.png)

we could see the part that asks us for the password and also a 5 digit number, now this could possibly be the password
let's try it out,

![image](https://cyberguru1.github.io/posts/crackme/images/easy_chall_worked.png)

yeah it worked but what's really going on here ?????

let's plug it in binja and see what it decompiles to :

![image](https://cyberguru1.github.io/posts/crackme/images/binja_View.png)

we could see that the password is read from memory and loaded into `rdx` with the assembly `lea`, then the user is asked for input
which is then stored into a register, a while loop then iterates through the user input and compares it with the loaded password in memeory
which for every character if there's a mismatch it breaks and returns incorrect password.

let's plut it into IDAPro for more psuedoCode info

---

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // r8
  __int64 v4; // r8
  __int64 v5; // r8
  void **v6; // rdx
  char *v7; // rbx
  unsigned __int64 v8; // rdi
  __int64 v9; // rax
  unsigned __int8 v10; // cl
  int v11; // eax
  __int64 v12; // r8
  __int64 v13; // r8
  __int64 v14; // r8
  char *v15; // rax
  void *Block[2]; // [rsp+20h] [rbp-38h] BYREF
  __int64 v18; // [rsp+30h] [rbp-28h]
  unsigned __int64 v19; // [rsp+38h] [rbp-20h]

  *(_OWORD *)Block = 0i64;
  v18 = 0i64;
  v19 = 15i64;
  LOBYTE(Block[0]) = 0;
  sub_7FF77B8615A0(std::cout, "Welcome to EasyCrackMe!!!\n", envp);
  sub_7FF77B8615A0(std::cout, "\n", v3);
  while ( 1 )
  {
    sub_7FF77B8615A0(std::cout, "Password: ", v4);
    sub_7FF77B861770(std::cin, Block);
    v6 = Block;
    v7 = (char *)Block[0];
    v8 = v19;
    if ( v19 >= 16 )
      v6 = (void **)Block[0];
    if ( v18 == 5 )
    {
      v9 = 0i64;
      while ( 1 )
      {
        v10 = *((_BYTE *)v6 + v9++);
        if ( v10 != a12345[v9 - 1] )
          break;
        if ( v9 == 5 )
        {
          v11 = 0;
          goto LABEL_10;
        }
      }
      v11 = v10 < (unsigned __int8)a12345[v9 - 1] ? -1 : 1;
LABEL_10:
      if ( !v11 )
        break;
    }
    sub_7FF77B8615A0(std::cout, "Incorrect :(\n", v5);
    sub_7FF77B8615A0(std::cout, "\n", v12);
    sub_7FF77B8615A0(std::cout, "\n", v13);
    sub_7FF77B8615A0(std::cout, "\n", v14);
  }
  sub_7FF77B8615A0(std::cout, "Correct :)", v5);
  if ( v8 >= 0x10 )
  {
    v15 = v7;
    if ( v8 + 1 >= 0x1000 )
    {
      v7 = (char *)*((_QWORD *)v7 - 1);
      if ( (unsigned __int64)(v15 - v7 - 8) > 0x1F )
        invalid_parameter_noinfo_noreturn();
    }
    j_j_free(v7);
  }
  return 0;
}
```

---

Here is a brief explanation of its functionality:

-The program starts with the main function, which takes command-line arguments argc, argv, and environment variables envp.

-Some variables (v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, Block, v18, v19) are declared.

-The program initializes Block as an array of 2 elements and sets other variables to specific initial values.

-The program prints "Welcome to EasyCrackMe!!!" to the standard output.

-The program enters a continuous loop where it prompts the user for a password and reads the input.

-The program compares the entered password with a predefined string "a12345". If the password matches, the loop is exited; otherwise, an "Incorrect :(" message is printed, and the loop continues.

-Once the correct password is entered, the program prints "Correct :)".

-If the length of the entered password is greater than or equal to 16, the program frees memory allocated for the password string.

-The program returns 0, indicating successful execution.

Overall, this program is a simple password verification system where the user needs to enter the correct password to proceed.

what an easy challenge
that's all for now!!!!!!!!
