# Lab: Unprotected admin functionality

This lab has an unprotected admin panel.

Solve the lab by deleting the user `carlos`.

Accessing the challenge link we saw our usual shopping website, the challenge told us that there is a hidden login admin panel, see this we head over to robots.txt to see all disallow route

![1694842313742.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694842313742.png)

we could see the admin route in the disallow route, now lets access it:
![1694842373083.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694842373083.png)

now we could solve the challenge by deleting the user carlos

![1694842423886.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694842423886.png)



# Lab: Unprotected admin functionality with unpredictable URL

This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application.

Solve the lab by accessing the admin panel, and using it to delete the user `carlos`.

we head over to the challenge link and try searching for the hidden admin panel route and we found it in 👍

![1694842611316.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694842611316.png)

we add the route to the url and it becomes:

```http
https://0a7a00b60386a2e081d97fe80064008a.web-security-academy.net/admin-ugi44f
```

accessing it and deleting user carlos we solved the lab:

![1694842693453.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694842693453.png)



# Lab: User role controlled by request parameter

This lab has an admin panel at `/admin`, which identifies administrators using a forgeable cookie.

Solve the lab by accessing the admin panel and using it to delete the user `carlos`

You can log in to your own account using the following credentials: `wiener:peter`

As the lab description says, we could edit the cookie while making request; this a case of access control where the admin panel is displayed only when the admin=true key value is present in the cookie; so we intercepted each and every request and put change the false to true this is an example of vertical access priviledge escalation

![1694843029389.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694843029389.png)

![1694843046191.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694843046191.png)

we delete the required use and solved the lab

![1694843101597.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694843101597.png)



# Lab: User role can be modified in user profile

This lab has an admin panel at `/admin`. It's only accessible to logged-in users with a `roleid` of 2.

Solve the lab by accessing the admin panel and using it to delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

we access the lab link and try modifying the user details, we added an extra field in the json payload of `roleid: 2` to have admin privilleges we submit this payload below:
![1694843972459.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694843972459.png)

we enter the admin route and delete the user carlos

![1694844020189.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694844020189.png)



# Lab: User ID controlled by request parameter

This lab has a horizontal privilege escalation vulnerability on the user account page.

To solve the lab, obtain the API key for the user `carlos` and submit it as the solution.

You can log in to your own account using the following credentials: `wiener:peter`

We login to the accournt and try intercepting the request and modify the id parameter to carlos:

![1694844403651.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694844403651.png)

after sending the request we got this:

![1694844367629.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694844367629.png)

we sumbit the api key and solved the lab

![1694844446302.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694844446302.png)



# Lab: User ID controlled by request parameter, with unpredictable user IDs

This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs.

To solve the lab, find the GUID for `carlos`, then submit his API key as the solution.

You can log in to your own account using the following credentials: `wiener:peter`

To find the GUID of carlos we need to find a user on the site with that name; so we search through several blog post and found him we note down his uuid as

```http
userId=0b1f98ab-20a8-48de-b847-f7c61982469a
```

we then go to the account section with the already logged in user as wiener, we intercepted this request in burp and changed the GUID with that of carlos

![1694845472010.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694845472010.png)

and we got the api key below after submiting this request:

![1694845493766.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694845493766.png)

we submit the key and we solved the lab:
![1694845544119.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694845544119.png)



# Lab: User ID controlled by request parameter with data leakage in redirect

This lab contains an [access control](https://portswigger.net/web-security/access-control) vulnerability where sensitive information is leaked in the body of a redirect response.

To solve the lab, obtain the API key for the user `carlos` and submit it as the solution.

You can log in to your own account using the following credentials: `wiener:peter`

After loggin in we refresh the account page and intercept this request in burp, we change the id to carlos and saw the following redirect message:

![1694846404247.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846404247.png)

Despite the redirect message we could see the api key in the redirect response:

![1694846388374.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846388374.png)

we submit the solution and solved the lab:

![1694846443601.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846443601.png)



# Lab: User ID controlled by request parameter with password disclosure

This lab has user account page that contains the current user's existing password, prefilled in a masked input.

To solve the lab, retrieve the administrator's password, then use it to delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

we login using the credentials provided, then we refresh the page and intercept the request using burpsuite, we now changed the id parameter to carlos and got the following password disclosure:

![1694846723876.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846723876.png)

we checked the raw html and saw the password for carlos:

![1694846755994.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846755994.png)

we do the same for administrator and retrived the password for the admin:

![1694846949932.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846949932.png)

response of the sent request:

![1694846963616.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846963616.png)

we checked the raw html for the password:

![1694846983010.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694846983010.png)

Using the admins logins details we logged in and delete the user carlos:

![1694847044113.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694847044113.png)



# Lab: [Insecure direct object references](https://portswigger.net/web-security/access-control/idor)

This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.

Solve the lab by finding the password for the user `carlos`, and logging into their account.

we go to the live chat seciton and try downloading the chat transcript, we intercepted this request using burp and sent it to repeater, we then

changed the request from /download-transcript/2.txt to /down...../1.txt

![1694847454656.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694847454656.png)

we then send the payload and got the following response:

![1694847479357.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694847479357.png)

we use the password in the above graphic to log in and solved the lab

![1694847522871.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694847522871.png)



# Lab: URL-based [access control](https://portswigger.net/web-security/access-control) can be circumvented

This website has an unauthenticated admin panel at `/admin`, but a front-end system has been configured to block external access to that path. However, the back-end application is built on a framework that supports the `X-Original-URL` header.

To solve the lab, access the admin panel and delete the user `carlos`.

We try accessing the admin endpoint using the normal route but got access-denied, so we use the X-Orginal-URL to bypass it, so we modify our response to this:

![1694847941244.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694847941244.png)

response of the above payload:

![1694847969079.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694847969079.png)

to delete a the required user carlos we then recraft the payload to this:

![1694848396623.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694848396623.png)

and we succesfully solved the lab:
![1694848412731.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694848412731.png)



# Lab: Method-based [access control](https://portswigger.net/web-security/access-control) can be circumvented

This lab implements [access controls](https://portswigger.net/web-security/access-control) based partly on the HTTP method of requests. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.

To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed access controls to promote yourself to become an administrator.

we use the following steps to solve the lab:

* Log in using the admin credentials.
* Browse to the admin panel, promote `carlos`, and send the HTTP request to Burp Repeater.
* Open a private/incognito browser window, and log in with the non-admin credentials.
* Attempt to re-promote `carlos` with the non-admin user by copying that user's session cookie into the existing Burp Repeater request, and observe that the response says "Unauthorized".
* Change the method from `POST` to `POSTX` and observe that the response changes to "missing parameter".
* Convert the request to use the `GET` method by right-clicking and selecting "Change request method".
* Change the username parameter to your username and resend the request.

After doing all the above steps we get the following payload request and send

![1694850322060.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694850322060.png)

This lab doesn't show any output of solved; but the solution reflected in the challenge description.

# Lab: Multi-step process with no [access control](https://portswigger.net/web-security/access-control) on one step

This lab has an admin panel with a flawed multi-step process for changing a user's role. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.

To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed [access controls](https://portswigger.net/web-security/access-control) to promote yourself to become an administrator.

This lab is simillar to the previous lab, we perform the replay attack and change the session cookie to that of wiener and also the username to wiener; following this we have the request payload below:

![1694954040089.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694954040089.png)

Response of the sent payload:
![1694954059326.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694954059326.png)



# Lab: Referer-based access control


This lab controls access to certain admin functionality based on the Referer header. You can familiarize yourself with the admin panel by logging in using the credentials `administrator:admin`.

To solve the lab, log in using the credentials `wiener:peter` and exploit the flawed [access controls](https://portswigger.net/web-security/access-control) to promote yourself to become an administrator.

This lab is some what simillar to the previous lab, but in this we make a GET request instead of the ususal post request to the /admin-roles endpoint.

The main goal of this lab is about the Referer header that tells the server where the request is coming from; as before we edit the content of the replayed request to match that of wiener username inculding the cookie:

![1694954410623.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694954410623.png)

Result after sending the payload:

![1694954443399.png](https://Cyberguru1.github.io/posts/portswigger/access_control/images/1694954443399.png)
