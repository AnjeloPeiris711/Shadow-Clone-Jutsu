# Shadow-Clone-Jutsu

## DNS Step 1
``` python
import socket

def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))

    print(f"Server started on {host}:{port}")

    while True:
        # Accept a connection from a client
        data,addr = server_socket.recvfrom(512)
        print(data)
# Usage
start_server('localhost', 53)

```
### Usage
```
C:\Users\asus>dig howcode.org @127.0.0.1

```

```
Shadow-Clone-Jutsu>Python ./index.py
Server started on localhost:53
b'\xa2\x90\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xb4!\xdb\x01 -7\xa7'
b'\xa2\x90\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xb4!\xdb\x01 -7\xa7'
b'\xa2\x90\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xb4!\xdb\x01 -7\xa7'
```
### Header section format

The header contains the following fields:
```
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
where:
|               |                                                            |
|  ---          | ---                                                        |
| ID            | A 16 bit identifier assigned by the program that generates any kind of query.  This identifier is copied the corresponding reply and can be used by the requester to match up replies to outstanding queries. |

| QR             | A one bit field that specifies whether this message is a
                query (0), or a response (1). |

| OPCODE          | A four bit field that specifies kind of query in this
                message.  This value is set by the originator of a query
                and copied into the response.  The values are:

                0               a standard query (QUERY)

                1               an inverse query (IQUERY)

                2               a server status request (STATUS)

                3-15            reserved for future use |

| AA              | Authoritative Answer - this bit is valid in responses,
                and specifies that the responding name server is an
                authority for the domain name in question section.

                Note that the contents of the answer section may have
                multiple owner names because of aliases.  The AA bit |



Mockapetris                                                  
| RFC 1035        | Domain Implementation and Specification    November 1987


                corresponds to the name which matches the query name, or
                the first owner name in the answer section. |

| TC              | TrunCation - specifies that this message was truncated
                due to length greater than that permitted on the
                transmission channel. |

| RD              | Recursion Desired - this bit may be set in a query and
                is copied into the response.  If RD is set, it directs
                the name server to pursue the query recursively.
                Recursive query support is optional. |

| RA             | Recursion Available - this be is set or cleared in a
                response, and denotes whether recursive query support is
                available in the name server. |

 | Z              | Reserved for future use.  Must be zero in all queries
                and responses. |

| RCODE          | Response code - this 4 bit field is set as part of
                responses.  The values have the following
                interpretation: 

                0               No error condition

                1               Format error - The name server was
                                unable to interpret the query.

                2               Server failure - The name server was
                                unable to process this query due to a
                                problem with the name server.

                3               Name Error - Meaningful only for
                                responses from an authoritative name
                                server, this code signifies that the
                                domain name referenced in the query does
                                not exist.

                4               Not Implemented - The name server does
                                not support the requested kind of query.

                5               Refused - The name server refuses to
                                perform the specified operation for
                                policy reasons.  For example, a name
                                server may not wish to provide the
                                information to the particular requester,
                                or a name server may not wish to perform
                                a particular operation (e.g., zone) |
