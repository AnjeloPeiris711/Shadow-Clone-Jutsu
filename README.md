# Shadow-Clone-Jutsu Developments 

```
  _________.__                .___              _________ .__                         
 /   _____/|  |__ _____     __| _/______  _  __ \_   ___ \|  |   ____   ____   ____   
 \_____  \ |  |  \\__  \   / __ |/  _ \ \/ \/ / /    \  \/|  |  /  _ \ /    \_/ __ \  
 /        \|   Y  \/ __ \_/ /_/ (  <_> )     /  \     \___|  |_(  <_> )   |  \  ___/  
/_______  /|___|  (____  /\____ |\____/ \/\_/    \______  /____/\____/|___|  /\___  > 
        \/      \/     \/      \/                       \/                 \/     \/  
                            ____.       __                                            
                           |    |__ ___/  |_  ________ __                             
                           |    |  |  \   __\/  ___/  |  \                            
                       /\__|    |  |  /|  |  \___ \|  |  /                            
                       \________|____/ |__| /____  >____/  分身の術 0.0.1                         
                                                 \/              
```

```
                        +----------------------+
                        |      junior.home     |
                        +----------------------+ #fake domain 

+------+   ==============1.DNS Request to ===========>  +-----------+
|  PC  |                     junior.home                | Local DNS |
+------+                                                |    Sever  |
           <=============2.DNS Answer Server =========  +-----------+ 
                            is at 10.20.0.2                   |
                                                _             ↓
                              Lord-balancer----|server1:>junior.home->10.20.0.2
                                               |server2:>junior.home->10.20.0.3       
                                           
```
<<<<<<< HEAD
### What is problems of this system?
1. I was using the fake domain i always had to use self-signed certificates for all my web services 
=======
### What is problems  of this system?

- [x] ❌ I was using the fake domain i always had to use self-signed certificates for all my web services.

### What ia trying to do ?

```
                        +----------------------+
                        |      youtube.com     |
                        +----------------------+ #clone domain 

+------+   ==============1.DNS Request to ===========>  +-----------+
|  PC  |                     youtube.com                | Local DNS |
+------+                                                |    Sever  |
           <=============2.DNS Answer Server =========  +-----------+ 
                            is at 10.20.0.2                   |
                                                _             ↓
                              Lord-balancer----|server1:>youtube.com->10.20.0.2|-------- #fake IP
                                               |server2:>youtube.com->10.20.0.3|      
                                           
```
### How browser Auto Fill
```
1. User Enter the Domin Name to access the website.
  
   User
    |
    V
2. The browser sends a POST request to the website's server with login credentials.
  
   Browser -----> Website's Server
                  Request: POST /login
                  Body: { username, password }
   
3. The website's server verifies the credentials.
  
   Browser <----- Website's Server
                  Response: 200 OK or 401 Unauthorized
  
4. If credentials are valid, the server generates a session token.
  
   Browser <----- Website's Server
                  Response: 200 OK
                  Body: { session_token }
  
5. The browser stores the session token in a secure cookie.
  
   Browser -----> Cookie
  
6. User visits the website again.
  
   User
    |
    V
   Browser
  
7. The browser sends a GET request to the website's server along with the session token.
  
   Browser -----> Website's Server
                  Request: GET /dashboard
                  Headers: Cookie: session_token
  
8. The website's server verifies the session token and user is considered logged in.
  
   Browser <----- Website's Server
                  Response: 200 OK
  
9. Browser's auto-fill feature recognizes the website and fills in the saved credentials.
  
   Browser
    |
    V
   User
  
10. User may need to manually trigger the login form submission or auto-submit might be enabled.
  
   User
    |
    V
   Browser
  
11. The browser sends the filled-in credentials to the server.
  
   Browser -----> Website's Server
                  Request: POST /login
                  Body: { username, password }
  
12. The server validates the session token and auto-fills the user's login.
  
   Browser <----- Website's Server
                  Response: 200 OK or 401 Unauthorized
                  Body: { session_token }


```

## Here's a little anecdote to clarify the process:

> When you type "youtube.com" into your browser, first your browser issues a DNS query to your primary DNS server. If installed correctly, your DNS says
```
--------------> "Yo, that server is on localhost".
```
> Then your browser is like, "word" and sends an HTTP request to localhost port 80 or Whatever. Then server slides over and says
```
--------------> "Surprise! Me again.", and proxies the HTTPS request to the destination server
```
> according to the rules you defined. "Whatever," says your browser.
>>>>>>> ff803833445e9c6c982f365f892f9875302e3525


## Chapter
[chapter_1](https://github.com/AnjeloPeiris711/Shadow-Clone-Jutsu/blob/main/chapter/chapter_1.md)
