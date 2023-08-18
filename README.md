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
