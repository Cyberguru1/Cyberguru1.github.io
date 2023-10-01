### G0l4ng_1s_C00l

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_desc.png)

This challenge is based on Golang compiled binaries, so today we are going to reverse a Golang (Mr. memory safe ;) ) executable file, as usual a zip file was given, unzipping the file we have an executable called hey.exe 

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_file.png)

using wine to run the executable file we were asked to enter a username and a password

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_run.png)

once a wrong password is entered the program simply exits

let's try running the Linux command `strings` on the file and see if we could get the password:

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_strings.png)

we were greeted with large chunks of text and blobs of data nothing interesting to use

let's try decompiling the executable in ghidra::

after ghidra successfully decompiled it we saw lots and lots of functions the program used, why is this ?

![](https://imgflip.com/gif/7n3e0g)

We did a little googling, and I was able to find out that the reason that a compiled program in Go may appear to have multiple functions due is to compiler optimizations, runtime support, standard library functions, and compiler-generated code are all packed into the
executable it'self (hmm... reason why the file size was about 2.7mb in size)

we did a little search on the main function and some little analysis on the decompiled code in Ghidra, but we didn't get anything promising, i went on to try and search for strings that we saw when we execute the program but to no avail; this is due to the fact that Golang does not use a null byte to terminate strings unlike C/C++; so everything is clamped up together and Ghidra wasn't able to find our target search string.

i went back to IDA, after loading and performing analysis on the executable file we got something interesting, IDA was able to decode the function call's properly and name the entry point, doing some googling again we saw that in most cases of golang decompiled binaries, the entry point is always a function called `main_main` these were our main program is stored.

```

text:0000000000E9BC80 ; =============== S U B R O U T I N E =======================================
.text:0000000000E9BC80
.text:0000000000E9BC80 ; Attributes: noreturn
.text:0000000000E9BC80
.text:0000000000E9BC80 ; void __cdecl main_main()
.text:0000000000E9BC80                 public main_main
.text:0000000000E9BC80 main_main       proc near               ; CODE XREF: runtime_main+1FC↑p
.text:0000000000E9BC80                                         ; .text:0000000000E9BF80↓j
.text:0000000000E9BC80                                         ; DATA XREF: ...
.text:0000000000E9BC80
.text:0000000000E9BC80 var_A0          = qword ptr -0A0h
.text:0000000000E9BC80 var_98          = qword ptr -98h
.text:0000000000E9BC80 var_90          = qword ptr -90h
.text:0000000000E9BC80 var_88          = xmmword ptr -88h
.text:0000000000E9BC80 var_78          = xmmword ptr -78h
.text:0000000000E9BC80 var_68          = xmmword ptr -68h
.text:0000000000E9BC80 var_58          = xmmword ptr -58h
.text:0000000000E9BC80 var_48          = xmmword ptr -48h
.text:0000000000E9BC80 var_38          = xmmword ptr -38h
.text:0000000000E9BC80 var_28          = xmmword ptr -28h
.text:0000000000E9BC80 var_18          = xmmword ptr -18h
.text:0000000000E9BC80 var_8           = qword ptr -8
.text:0000000000E9BC80
.text:0000000000E9BC80                 lea     r12, [rsp+var_48]
.text:0000000000E9BC85                 cmp     r12, [r14+10h]
.text:0000000000E9BC89                 jbe     loc_E9BF78
.text:0000000000E9BC8F                 sub     rsp, 0C8h
.text:0000000000E9BC96                 mov     [rsp+0C8h+var_8], rbp
.text:0000000000E9BC9E                 lea     rbp, [rsp+0C8h+var_8]
.text:0000000000E9BCA6                 lea     rax, unk_EA4300
.text:0000000000E9BCAD                 call    runtime_newobject
.text:0000000000E9BCB2                 mov     [rsp+0C8h+var_A0], rax
.text:0000000000E9BCB7                 mov     qword ptr [rax], 0
.text:0000000000E9BCBE                 movups  [rsp+0C8h+var_18], xmm15
.text:0000000000E9BCC7                 lea     rcx, unk_EA4300
.text:0000000000E9BCCE                 mov     qword ptr [rsp+0C8h+var_18], rcx
.text:0000000000E9BCD6                 lea     rdx, off_EDBCF8 ; "Enter your username : "
.text:0000000000E9BCDD                 mov     qword ptr [rsp+0C8h+var_18+8], rdx
.text:0000000000E9BCE5                 mov     rbx, cs:os_Stdout
.text:0000000000E9BCEC                 mov     edi, 1

<-!snip>

```

i went on to search for strings we saw during runtime of the program and sure enough IDA was also able to restore strings and properly separate them, how is this done ?

Doing some more googling we found out that Golang’s strings are stored at runtime in a particular structure called StringHeader with two fields:

```	
type StringHeader struct {
        Data uintptr       // string value
        Len  int           // string size 
}

```

The string’s characters (pointed by the Data field) are stored in data sections of the executables, as a series of UTF-8 encoded characters without null-terminators.

Well that's it for the decompilation stage as everything is in place let's now go ahead to reverse engineer the program ;)

```
text:0000000000E9BC80 ; =============== S U B R O U T I N E =======================================
.text:0000000000E9BC80
.text:0000000000E9BC80 ; Attributes: noreturn
.text:0000000000E9BC80
.text:0000000000E9BC80 ; void __cdecl main_main()
.text:0000000000E9BC80                 public main_main
.text:0000000000E9BC80 main_main       proc near               ; CODE XREF: runtime_main+1FC↑p
.text:0000000000E9BC80                                         ; .text:0000000000E9BF80↓j
.text:0000000000E9BC80                                         ; DATA XREF: ...
.text:0000000000E9BC80
.text:0000000000E9BC80 var_A0          = qword ptr -0A0h
.text:0000000000E9BC80 var_98          = qword ptr -98h
.text:0000000000E9BC80 var_90          = qword ptr -90h
.text:0000000000E9BC80 var_88          = xmmword ptr -88h
.text:0000000000E9BC80 var_78          = xmmword ptr -78h
.text:0000000000E9BC80 var_68          = xmmword ptr -68h
.text:0000000000E9BC80 var_58          = xmmword ptr -58h
.text:0000000000E9BC80 var_48          = xmmword ptr -48h
.text:0000000000E9BC80 var_38          = xmmword ptr -38h
.text:0000000000E9BC80 var_28          = xmmword ptr -28h
.text:0000000000E9BC80 var_18          = xmmword ptr -18h
.text:0000000000E9BC80 var_8           = qword ptr -8
.text:0000000000E9BC80
.text:0000000000E9BC80                 lea     r12, [rsp+var_48]
.text:0000000000E9BC85                 cmp     r12, [r14+10h]
.text:0000000000E9BC89                 jbe     loc_E9BF78
.text:0000000000E9BC8F                 sub     rsp, 0C8h
.text:0000000000E9BC96                 mov     [rsp+0C8h+var_8], rbp
.text:0000000000E9BC9E                 lea     rbp, [rsp+0C8h+var_8]
.text:0000000000E9BCA6                 lea     rax, unk_EA4300
.text:0000000000E9BCAD                 call    runtime_newobject
.text:0000000000E9BCB2                 mov     [rsp+0C8h+var_A0], rax
.text:0000000000E9BCB7                 mov     qword ptr [rax], 0
.text:0000000000E9BCBE                 movups  [rsp+0C8h+var_18], xmm15
.text:0000000000E9BCC7                 lea     rcx, unk_EA4300
.text:0000000000E9BCCE                 mov     qword ptr [rsp+0C8h+var_18], rcx
.text:0000000000E9BCD6                 lea     rdx, off_EDBCF8 ; "Enter your username : "
.text:0000000000E9BCDD                 mov     qword ptr [rsp+0C8h+var_18+8], rdx
.text:0000000000E9BCE5                 mov     rbx, cs:os_Stdout
.text:0000000000E9BCEC                 mov     edi, 1
.text:0000000000E9BCF1                 mov     rsi, rdi
.text:0000000000E9BCF4                 lea     rax, go_itab__os_File_io_Writer
.text:0000000000E9BCFB                 lea     rcx, [rsp+0C8h+var_18]
.text:0000000000E9BD03                 call    fmt_Fprintln
.text:0000000000E9BD08                 movups  [rsp+0C8h+var_28], xmm15
.text:0000000000E9BD11                 lea     rcx, unk_EA2500
.text:0000000000E9BD18                 mov     qword ptr [rsp+0C8h+var_28], rcx
.text:0000000000E9BD20                 mov     rdx, [rsp+0C8h+var_A0]
.text:0000000000E9BD25                 mov     qword ptr [rsp+0C8h+var_28+8], rdx
.text:0000000000E9BD2D                 mov     rbx, cs:os_Stdin
.text:0000000000E9BD34                 lea     rax, go_itab__os_File_io_Reader
.text:0000000000E9BD3B                 mov     edi, 1
.text:0000000000E9BD40                 mov     rsi, rdi
.text:0000000000E9BD43                 lea     rcx, [rsp+0C8h+var_28]
.text:0000000000E9BD4B                 call    fmt_Fscanln
.text:0000000000E9BD50                 movups  [rsp+0C8h+var_38], xmm15
.text:0000000000E9BD59                 lea     rcx, unk_EA4300
.text:0000000000E9BD60                 mov     qword ptr [rsp+0C8h+var_38], rcx
.text:0000000000E9BD68                 lea     rdx, off_EDBD08 ; "Enter your password : "
.text:0000000000E9BD6F                 mov     qword ptr [rsp+0C8h+var_38+8], rdx
.text:0000000000E9BD77                 mov     rbx, cs:os_Stdout
.text:0000000000E9BD7E                 lea     rax, go_itab__os_File_io_Writer
.text:0000000000E9BD85                 mov     edi, 1
.text:0000000000E9BD8A                 mov     rsi, rdi
.text:0000000000E9BD8D                 lea     rcx, [rsp+0C8h+var_38]
.text:0000000000E9BD95                 call    fmt_Fprintln
.text:0000000000E9BD9A                 lea     rax, unk_EA4300
.text:0000000000E9BDA1                 call    runtime_newobject
.text:0000000000E9BDA6                 mov     [rsp+0C8h+var_98], rax
.text:0000000000E9BDAB                 mov     qword ptr [rax], 0
.text:0000000000E9BDB2                 movups  [rsp+0C8h+var_48], xmm15
.text:0000000000E9BDBB                 lea     rcx, unk_EA2500
.text:0000000000E9BDC2                 mov     qword ptr [rsp+0C8h+var_48], rcx
.text:0000000000E9BDCA                 mov     qword ptr [rsp+0C8h+var_48+8], rax
.text:0000000000E9BDD2                 mov     rbx, cs:os_Stdin
.text:0000000000E9BDD9                 mov     edi, 1
.text:0000000000E9BDDE                 mov     rsi, rdi
.text:0000000000E9BDE1                 lea     rax, go_itab__os_File_io_Reader
.text:0000000000E9BDE8                 lea     rcx, [rsp+0C8h+var_48]
.text:0000000000E9BDF0                 call    fmt_Fscanln
.text:0000000000E9BDF5                 mov     rcx, [rsp+0C8h+var_A0]
.text:0000000000E9BDFA                 mov     rdx, [rcx]
.text:0000000000E9BDFD                 cmp     qword ptr [rcx+8], 5
.text:0000000000E9BE02                 jnz     short loc_E9BE7B
.text:0000000000E9BE04                 cmp     dword ptr [rdx], 'imda'
.text:0000000000E9BE0A                 jnz     short loc_E9BE7B
.text:0000000000E9BE0C                 cmp     byte ptr [rdx+4], 'n'
.text:0000000000E9BE10                 jnz     short loc_E9BE7B
.text:0000000000E9BE12                 mov     rdx, [rsp+0C8h+var_98]
.text:0000000000E9BE17                 mov     r8, [rdx]
.text:0000000000E9BE1A                 cmp     qword ptr [rdx+8], 7
.text:0000000000E9BE1F                 nop
.text:0000000000E9BE20                 jnz     short loc_E9BE7B
.text:0000000000E9BE22                 cmp     dword ptr [r8], 'akak'
.text:0000000000E9BE29                 jnz     short loc_E9BE7B
.text:0000000000E9BE2B                 cmp     word ptr [r8+4], '21'
.text:0000000000E9BE32                 jnz     short loc_E9BE7B
.text:0000000000E9BE34                 cmp     byte ptr [r8+6], '3'
.text:0000000000E9BE39                 jnz     short loc_E9BE7B
.text:0000000000E9BE3B                 movups  [rsp+0C8h+var_58], xmm15
.text:0000000000E9BE41                 lea     rdx, unk_EA4300
.text:0000000000E9BE48                 mov     qword ptr [rsp+0C8h+var_58], rdx
.text:0000000000E9BE4D                 lea     r8, off_EDBD18  ; "You are connected to the panel\n TU AS "...
.text:0000000000E9BE54                 mov     qword ptr [rsp+0C8h+var_58+8], r8
.text:0000000000E9BE59                 mov     rbx, cs:os_Stdout
.text:0000000000E9BE60                 lea     rax, go_itab__os_File_io_Writer
.text:0000000000E9BE67                 lea     rcx, [rsp+0C8h+var_58]
.text:0000000000E9BE6C                 mov     edi, 1
.text:0000000000E9BE71                 mov     rsi, rdi
.text:0000000000E9BE74                 call    fmt_Fprintln
.text:0000000000E9BE79                 jmp     short loc_E9BE85
.text:0000000000E9BE7B ; ---------------------------------------------------------------------------
.text:0000000000E9BE7B
.text:0000000000E9BE7B loc_E9BE7B:                             ; CODE XREF: main_main+182↑j
.text:0000000000E9BE7B                                         ; main_main+18A↑j ...
.text:0000000000E9BE7B                 xor     eax, eax
.text:0000000000E9BE7D                 nop     dword ptr [rax]
.text:0000000000E9BE80                 call    os_Exit
.text:0000000000E9BE85
.text:0000000000E9BE85 loc_E9BE85:                             ; CODE XREF: main_main+1F9↑j
.text:0000000000E9BE85                 lea     rax, unk_EA4300
.text:0000000000E9BE8C                 call    runtime_newobject
.text:0000000000E9BE91                 mov     [rsp+0C8h+var_90], rax
.text:0000000000E9BE96                 mov     qword ptr [rax], 0
.text:0000000000E9BE9D                 jmp     short loc_E9BEA4
.text:0000000000E9BE9F ; ---------------------------------------------------------------------------
.text:0000000000E9BE9F
.text:0000000000E9BE9F loc_E9BE9F:                             ; CODE XREF: main_main+2B0↓j
.text:0000000000E9BE9F                                         ; main_main+2F3↓j
.text:0000000000E9BE9F                 mov     rax, [rsp+0C8h+var_90]
.text:0000000000E9BEA4
.text:0000000000E9BEA4 loc_E9BEA4:                             ; CODE XREF: main_main+21D↑j
.text:0000000000E9BEA4                 movups  [rsp+0C8h+var_68], xmm15
.text:0000000000E9BEAA                 lea     rdx, unk_EA2500
.text:0000000000E9BEB1                 mov     qword ptr [rsp+0C8h+var_68], rdx
.text:0000000000E9BEB6                 mov     qword ptr [rsp+0C8h+var_68+8], rax
.text:0000000000E9BEBB                 mov     rbx, cs:os_Stdin
.text:0000000000E9BEC2                 lea     rcx, [rsp+0C8h+var_68]
.text:0000000000E9BEC7                 mov     edi, 1
.text:0000000000E9BECC                 mov     rsi, rdi
.text:0000000000E9BECF                 lea     rax, go_itab__os_File_io_Reader
.text:0000000000E9BED6                 call    fmt_Fscanln
.text:0000000000E9BEDB                 mov     rdx, [rsp+0C8h+var_90]
.text:0000000000E9BEE0                 mov     r8, [rdx]
.text:0000000000E9BEE3                 cmp     qword ptr [rdx+8], 2
.text:0000000000E9BEE8                 jnz     short loc_E9BF35
.text:0000000000E9BEEA                 cmp     word ptr [r8], 'sl'
.text:0000000000E9BEF0                 jnz     short loc_E9BF35
.text:0000000000E9BEF2                 movups  [rsp+0C8h+var_78], xmm15
.text:0000000000E9BEF8                 lea     rdx, unk_EA4300
.text:0000000000E9BEFF                 mov     qword ptr [rsp+0C8h+var_78], rdx
.text:0000000000E9BF04                 lea     r8, off_EDBD28  ; "102108971031238349109112108101951034810"...
.text:0000000000E9BF0B                 mov     qword ptr [rsp+0C8h+var_78+8], r8
.text:0000000000E9BF10                 mov     rbx, cs:os_Stdout
.text:0000000000E9BF17                 lea     rax, go_itab__os_File_io_Writer
.text:0000000000E9BF1E                 lea     rcx, [rsp+0C8h+var_78]
.text:0000000000E9BF23                 mov     edi, 1
.text:0000000000E9BF28                 mov     rsi, rdi
.text:0000000000E9BF2B                 call    fmt_Fprintln
.text:0000000000E9BF30                 jmp     loc_E9BE9F
.text:0000000000E9BF35 ; ---------------------------------------------------------------------------
.text:0000000000E9BF35
.text:0000000000E9BF35 loc_E9BF35:                             ; CODE XREF: main_main+268↑j
.text:0000000000E9BF35                                         ; main_main+270↑j
.text:0000000000E9BF35                 movups  [rsp+0C8h+var_88], xmm15
.text:0000000000E9BF3B                 lea     rdx, unk_EA4300
.text:0000000000E9BF42                 mov     qword ptr [rsp+0C8h+var_88], rdx
.text:0000000000E9BF47                 lea     r8, off_EDBD38  ; "Command not found"
.text:0000000000E9BF4E                 mov     qword ptr [rsp+0C8h+var_88+8], r8
.text:0000000000E9BF53                 mov     rbx, cs:os_Stdout
.text:0000000000E9BF5A                 lea     rax, go_itab__os_File_io_Writer
.text:0000000000E9BF61                 lea     rcx, [rsp+0C8h+var_88]
.text:0000000000E9BF66                 mov     edi, 1
.text:0000000000E9BF6B                 mov     rsi, rdi
.text:0000000000E9BF6E                 call    fmt_Fprintln
.text:0000000000E9BF73                 jmp     loc_E9BE9F
.text:0000000000E9BF78 ; ---------------------------------------------------------------------------
.text:0000000000E9BF78
.text:0000000000E9BF78 loc_E9BF78:                             ; CODE XREF: main_main+9↑j
.text:0000000000E9BF78                 call    runtime_morestack_noctxt_abi0
.text:0000000000E9BF78 main_main       endp
.text:0000000000E9BF78

```

let's break down the assembly code and understand exactly what's going on 

```

.text:0000000000E9BC80                 lea     r12, [rsp+var_48]; load the address of rsp + var_48 into r12
.text:0000000000E9BC85                 cmp     r12, [r14+10h] ; compare the contents of r14+10h with r12
.text:0000000000E9BC89                 jbe     loc_E9BF78     ; jump to loc_E9BF78 if the result is below or equal 
.text:0000000000E9BC8F                 sub     rsp, 0C8h      ; subtract 0xC8 from stack pointer
.text:0000000000E9BC96                 mov     [rsp+0C8h+var_8], rbp ; move the contents of the register rbp into memory rsp+0C8h+var_8
.text:0000000000E9BC9E                 lea     rbp, [rsp+0C8h+var_8] ; load the address rsp+0C8h+var_8 into register base pointer
.text:0000000000E9BCA6                 lea     rax, unk_EA4300       ; load the address of unk_EA4300 into register rax
.text:0000000000E9BCAD                 call    runtime_newobject     ; call the runtime_newobject() memory allocation function
.text:0000000000E9BCB2                 mov     [rsp+0C8h+var_A0], rax ; move the contents of the register rax into memory rsp+0C8h+var_A0
.text:0000000000E9BCB7                 mov     qword ptr [rax], 0 ; move 0 into the memory pointer of rax
.text:0000000000E9BCBE                 movups  [rsp+0C8h+var_18], xmm15 ; move register xmm15 into memory location of rsp+0C8h+var_18
.text:0000000000E9BCC7                 lea     rcx, unk_EA4300          ; stores the effective address of unk_EA4300 and stores it in rcx register
.text:0000000000E9BCCE                 mov     qword ptr [rsp+0C8h+var_18], rcx ; move the value of rck register into memory location at rsp+0C8h+var_18
.text:0000000000E9BCD6                 lea     rdx, off_EDBCF8   ; "Enter your username : " loads the address of off_EDBCF8 into the rdx register
.text:0000000000E9BCDD                 mov     qword ptr [rsp+0C8h+var_18+8], rdx ; copies the content of rdx register into memory location at [rsp+0C8h+var_18+8]
.text:0000000000E9BCE5                 mov     rbx, cs:os_Stdout ; load the ref. of standard output into rbx
.text:0000000000E9BCEC                 mov     edi, 1  ; move 1 to edi register
.text:0000000000E9BCF1                 mov     rsi, rdi ; copies the contents of rdi register to rsi
.text:0000000000E9BCF4                 lea     rax, go_itab__os_File_io_Writer ; load ref. to interface tavle and store it in rax
.text:0000000000E9BCFB                 lea     rcx, [rsp+0C8h+var_18] ; load the effective address at [rsp+0C8h+var_18] in rcx
.text:0000000000E9BD03                 call    fmt_Fprintln  ; calls the go print format function to print out the contents of rcx


```

this routine is done to retrieve the address of "Enter your username: " from memory and store it in a register which is then printed by fmt_Fprintln and same time performing memory checks (Mr. memory safe ;) )


```

.text:0000000000E9BD11                 lea     rcx, unk_EA2500 ; loads address of unk_EA2500 in to the rcx register
.text:0000000000E9BD18                 mov     qword ptr [rsp+0C8h+var_28], rcx ; stores the value of rcx into the memory location at [rsp+0C8h+var_28]
.text:0000000000E9BD20                 mov     rdx, [rsp+0C8h+var_A0] ; move the content at  memory location [rsp+0C8h+var_A0] into rdx register
.text:0000000000E9BD25                 mov     qword ptr [rsp+0C8h+var_28+8], rdx ; move the content of rdx into the memory location fo [rsp+0C8h+var_28+8]
.text:0000000000E9BD2D                 mov     rbx, cs:os_Stdin ; calls the ref. to standard input and stores it in rbx
.text:0000000000E9BD34                 lea     rax, go_itab__os_File_io_Reader ; loads the address of file io reader to rax
.text:0000000000E9BD3B                 mov     edi, 1 ; move 1 to edi register
.text:0000000000E9BD40                 mov     rsi, rdi ; move the content of rdi register into rsi
.text:0000000000E9BD43                 lea     rcx, [rsp+0C8h+var_28] ; move the content at the memory loaction of [rsp+0C8h+var_28] into rcx
.text:0000000000E9BD4B                 call    fmt_Fscanln ; calls the golang scanln input function 

```

what this lines of assembly simply does is to get our response to username query input and store it into dynamically allocated memory created using runtime.newobject(); the Dynamic memory allocation variable is usually through a call to runtime.newobject(), which takes in input the description of the type to be allocated ;

this same principle is done also for the "Enter your password : " and the input to that query which is stored for further use

the next part is the comparison which is made

```
.text:0000000000E9BDFD                 cmp     qword ptr [rcx+8], 5 ; compares the length of our input stored in [rcx+8] with 5
.text:0000000000E9BE02                 jnz     short loc_E9BE7B     ; jump if not equal
.text:0000000000E9BE04                 cmp     dword ptr [rdx], 'imda' ; compares the first 4 bytes (dword) with 'imba' (x86 little endian)
.text:0000000000E9BE0A                 jnz     short loc_E9BE7B        ; jump if not equal
.text:0000000000E9BE0C                 cmp     byte ptr [rdx+4], 'n'   ; compares the next byte content at memory location [rdx+4] with 'n'
.text:0000000000E9BE10                 jnz     short loc_E9BE7B        ; jumpus if not equal to
; comparision of username done
.text:0000000000E9BE12                 mov     rdx, [rsp+0C8h+var_98]  ; move the content at memory location [rdx+0C8h+var_98] to rdx
.text:0000000000E9BE17                 mov     r8, [rdx]               ; move the memory address at location [rdx] to r8
.text:0000000000E9BE1A                 cmp     qword ptr [rdx+8], 7    ; compares the size at [rdx+8] with 7
.text:0000000000E9BE1F                 nop                             ; do nothing
.text:0000000000E9BE20                 jnz     short loc_E9BE7B        ; jump if not equal
.text:0000000000E9BE22                 cmp     dword ptr [r8], 'akak'  ; comparet the 4 bytes (dword) content at [r8] with 'akak' (little endian)
.text:0000000000E9BE29                 jnz     short loc_E9BE7B        ; jump if not equal
.text:0000000000E9BE2B                 cmp     word ptr [r8+4], '21'   ; compares the 2 bytes (word) content at [r8+4] with '21' (little endian)
.text:0000000000E9BE32                 jnz     short loc_E9BE7B        ; jump if not equal
.text:0000000000E9BE34                 cmp     byte ptr [r8+6], '3'    ; compares the next byte content at memory location [rdx+4] with '3'
.text:0000000000E9BE39                 jnz     short loc_E9BE7B        ; jump if not equal
; comparision of password done
```

the above assembly compares the input username and password with the one stored in memory; which for each case exits the program if a mismatch is found, from above we concluded that the username is `imdan` and password is `akak213` since for each check the length is compared (i.e. for username it's 5 in length and for password is 7 in length) 

A more illustrative explaination 

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang.png)

we try entering the password into the program but the program just simply exits, i thinker for a little and thought why the password isn't working, then i realize that the username is actually  `admin` and not `imda` this is because we are dealing with an x86 executable and the strings are written in little-endian ; note that when a small local string is used for comparison only, no StringHeader structure gets allocated. The string comparison is done directly by machine instructions; for example, CMP [EAX], 0x64636261 to compare with “abcd” on x86

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_pass.png)

we were greeted with a text, the text probably looks like latin so let's try translating it to english

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_trans.png)

it says we could only use the `ls` command in the panel, after writing the command a txt file with a decimal number name was printed out

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_ls.png)

we try deciphering the file name to Ascii characters in python and i got these:

![](https://blog.cyb3rguru.tech/posts/crackme/images/golang_flag.png)

And we finally got our flag to be `flag{S1mple_g0l4ng_b1n4ry}`

What a challenge, thanks for Reading


**Arigato !!!!**