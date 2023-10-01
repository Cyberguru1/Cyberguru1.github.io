# Lab: OS [command injection](https://portswigger.net/web-security/os-command-injection), simple case



This lab contains an [OS command injection](https://portswigger.net/web-security/os-command-injection) vulnerability in the product stock checker.

The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.

To solve the lab, execute the `whoami` command to determine the name of the current user.

We solve this lab by simply adding the `whoami` statement at the end of the request intercepted by burpsuite:

 ![1694080380146.png](./1694080380146.png)



and we get the following result:

 ![1694080715989.png](./1694080715989.png)

we could see in the above image that the user is peter-qeL7Tm



# Lab: Blind OS [command injection](https://portswigger.net/web-security/os-command-injection) with time delays



This lab contains a blind [OS command injection](https://portswigger.net/web-security/os-command-injection) vulnerability in the feedback function. The application executes a shell command containing the user-supplied details. The output from the command is not returned in

the response.

To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay.

we submit the following entry with the message entry as:

```bash
$(sleep 10)
```

we send this request and get the following result:

 ![1694081527853.png](./1694081527853.png)




# Lab: Blind OS [command injection](https://portswigger.net/web-security/os-command-injection) with output redirection



This lab contains a blind [OS command injection](https://portswigger.net/web-security/os-command-injection) vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:

`/var/www/images/`

The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the `whoami` command and retrieve the output.

We accessed the provided link and navigate to the feedback section and pass in the following entry:

 ![1694082346005.png](./1694082346005.png)

we use the `whoami`  command and send the output to /var/www/images/out.txt and sleep for 10 seconds so that we could know that our injection have been executed.

we got the following result after sending the payload:

 ![1694082459319.png](./1694082459319.png)



 ![1694082478405.png](./1694082478405.png)




# Lab: Blind OS command injection with out-of-band interaction


This lab contains a blind OS [command injection](https://portswigger.net/web-security/os-command-injection) vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the blind OS command injection vulnerability to issue a DNS lookup to Burp Collaborator.

To solve this lab, we simply do what we did in lab 3, we ping our burp collaborator dns client address with the username of the server and get the result in the burp collaborator:

supplied input to the query:

 ![1694084751784.png](./1694084751784.png)

Result of the query:

![1694084696677.png](./1694084696677.png)



# Lab: Blind OS [command injection](https://portswigger.net/web-security/os-command-injection) with out-of-band data exfiltration


This lab contains a blind [OS command injection](https://portswigger.net/web-security/os-command-injection) vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger
out-of-band interactions with an external domain.

To solve the lab, execute the `whoami` command and exfiltrate the output via a DNS query to Burp Collaborator. You will need to enter the name of the current user to complete the lab.


This lab is simillar to the previous challenge we solved it using the same approach:

we got this result from burp collaborator client:

![1694085270763.png](./1694085270763.png)


we then submit the result:

![1694085235822.png](./1694085235822.png)

 ![1694085394662.png](./1694085394662.png)
