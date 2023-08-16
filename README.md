# Shadow-Clone-Jutsu Test
```
                                  +-------------------------------------------+
                                  |               Junior.home                 |
                                  +-------------------------------------------+   #fake-domain

+-------+     ==================1. DNS request to Junior.home ============>      +------------------------------+
|   PC  |                                                                        |            DNS Server        |  
+-------+    <===============2. DNS Answer Junior.home at 10.20.0.02 ======      +------------------------------+            _
                                                                                          server1 - Junior.home - 10.20.0.02  |
                                                                                          server2 - Junior.home - 10.20.0.03 _|
                                                                                                                #Lord- Balancer           
```
