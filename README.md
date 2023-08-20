# Shadow-Clone-Jutsu Developments 

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
1. User initiates a login by entering username and password.
  
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
