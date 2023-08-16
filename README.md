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
| QR            | A one bit field that specifies whether this message is a query (0), or a response (1). |
| OPCODE        | A four bit field that specifies kind of query in this message.  This value is set by the originator of a query and copied into the response.  The values are:<br>`0               a standard query (QUERY)`<br>`1               an inverse query (IQUERY)`<br>`2               a server status request (STATUS)`<br>`3-15            reserved for future use` |
| AA  | Authoritative Answer - this bit is valid in responses, and specifies that the responding name server is an authority for the domain name in question section. <br>  **Note:>** ```The contents of the answer section may have multiple owner names because of aliases. The AA bit is not working as expected in some scenarios.``` |




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


# DNS Server Code Explanation

This repository contains a basic DNS server implementation in Python. The server listens for DNS queries, looks up the requested domain in preloaded zone data, and responds with appropriate DNS answers.

## Functions

### `load_zones()`

This function loads DNS zone data from JSON files located in the "zones" directory. It reads each zone file, extracts the zone name, and stores the data in a dictionary named `zonedata`.

### `getflags(flags)`

Generates DNS header flags based on various parameters such as query/response indicators, operation code, authoritative answer, truncation, recursion desired, etc. Returns the flags as bytes.

### `getquestiondomain(data)`

Parses the received DNS query data and extracts the domain name and question type. It returns the domain name as a list of domain parts and the question type as bytes.

### `getzone(domain)`

Retrieves the zone data for the given domain from the `zonedata` dictionary. It converts the domain parts into a fully qualified domain name (FQDN) and returns the corresponding zone data.

### `getrecs(data)`

Extracts the resource records (RRs) associated with a given domain and its question type. Returns a tuple containing the list of records, the question type as a string, and the domain.

### `buildquestion(domainname, rectype)`

Constructs a DNS question based on the domain name and record type. Returns the question as bytes.

### `rectobytes(domainname, rectype, recttl, recval)`

Converts a resource record to its binary representation. This function is responsible for building the DNS response body for the answer section.

### `buildresponse(data)`

Builds a DNS response packet by combining the header, question, and answer sections. This function generates a response based on the received DNS query.

## Main Loop

The main loop continuously listens for incoming DNS queries, processes them using the above functions, and sends back the appropriate DNS responses.

Please note that while this code provides a basic DNS server implementation, it lacks many advanced features and error handling that are typically required in production-ready DNS servers.

