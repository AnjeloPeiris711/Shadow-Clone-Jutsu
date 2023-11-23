1 - The DNS protocol
====================

We'll start out by investigating the DNS protocol and use our knowledge thereof
to implement a simple client.

Conventionally, DNS packets are sent using UDP transport and are limited to 512
bytes. As we'll see later, both of those rules have exceptions: DNS can be used
over TCP as well, and using a mechanism known as eDNS we can extend the packet
size. For now, we'll stick to the original specification, though.

DNS is quite convenient in the sense that queries and responses use the same
format. This means that once we've written a packet parser and a packet writer,
our protocol work is done. This differs from most Internet Protocols, which
typically use different request and response structures. On a high level, a DNS
packet looks as follows:

| Section            | Size     | Type              | Purpose                                                                                                |
| ------------------ | -------- | ----------------- | ------------------------------------------------------------------------------------------------------ |
| Header             | 12 Bytes | Header            | Information about the query/response.                                                                  |
| Question Section   | Variable | List of Questions | In practice only a single question indicating the query name (domain) and the record type of interest. |
| Answer Section     | Variable | List of Records   | The relevant records of the requested type.                                                            |
| Authority Section  | Variable | List of Records   | An list of name servers (NS records), used for resolving queries recursively.                          |
| Additional Section | Variable | List of Records   | Additional records, that might be useful. For instance, the corresponding A records for NS records.    |

Essentially, we have to support three different objects: Header, Question and
Record. Conveniently, the lists of records and questions are simply individual
instances appended in a row, with no extras. The number of records in each
section is provided by the header. The header structure looks as follows:

| RFC Name | Descriptive Name     | Length             | Description                                                                                                                                                                         |
| -------- | -------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID       | Packet Identifier    | 16 bits            | A random identifier is assigned to query packets. Response packets must reply with the same id. This is needed to differentiate responses due to the stateless nature of UDP.       |
| QR       | Query Response       | 1 bit              | 0 for queries, 1 for responses.                                                                                                                                                     |
| OPCODE   | Operation Code       | 4 bits             | Typically always 0, see RFC1035 for details.                                                                                                                                        |
| AA       | Authoritative Answer | 1 bit              | Set to 1 if the responding server is authoritative - that is, it "owns" - the domain queried.                                                                                       |
| TC       | Truncated Message    | 1 bit              | Set to 1 if the message length exceeds 512 bytes. Traditionally a hint that the query can be reissued using TCP, for which the length limitation doesn't apply.                     |
| RD       | Recursion Desired    | 1 bit              | Set by the sender of the request if the server should attempt to resolve the query recursively if it does not have an answer readily available.                                     |
| RA       | Recursion Available  | 1 bit              | Set by the server to indicate whether or not recursive queries are allowed.                                                                                                         |
| Z        | Reserved             | 3 bits             | Originally reserved for later use, but now used for DNSSEC queries.                                                                                                                 |
| RCODE    | Response Code        | 4 bits             | Set by the server to indicate the status of the response, i.e. whether or not it was successful or failed, and in the latter case providing details about the cause of the failure. |
| QDCOUNT  | Question Count       | 16 bits            | The number of entries in the Question Section                                                                                                                                       |
| ANCOUNT  | Answer Count         | 16 bits            | The number of entries in the Answer Section                                                                                                                                         |
| NSCOUNT  | Authority Count      | 16 bits            | The number of entries in the Authority Section                                                                                                                                      |
| ARCOUNT  | Additional Count     | 16 bits            | The number of entries in the Additional Section  

The question is quite a bit less scary:

| Field  | Type           | Description                                                          |
| ------ | -------------- | -------------------------------------------------------------------- |
| Name   | Label Sequence | The domain name, encoded as a sequence of labels as described below. |
| Type   | 2-byte Integer | The record type.                                                     |
| Class  | 2-byte Integer | The class, in practice always set to 1.                              |

The tricky part lies in the encoding of the domain name, which we'll return to
later.

Finally, we've got the records which are the meat of the protocol. Many record
types exists, but for now we'll only consider a few essential. All records have
the following preamble:

| Field  | Type           | Description                                                                       |
| ------ | -------------- | --------------------------------------------------------------------------------- |
| Name   | Label Sequence | The domain name, encoded as a sequence of labels as described below.              |
| Type   | 2-byte Integer | The record type.                                                                  |
| Class  | 2-byte Integer | The class, in practice always set to 1.                                           |
| TTL    | 4-byte Integer | Time-To-Live, i.e. how long a record can be cached before it should be requeried. |
| Len    | 2-byte Integer | Length of the record type specific data.                                          |

Now we are all set to look a specific record types, and we'll start with the
most essential: the A record, mapping a name to an ip.

| Field      | Type            | Description                                                                       |
| ---------- | --------------- | --------------------------------------------------------------------------------- |
| Preamble   | Record Preamble | The record preamble, as described above, with the length field set to 4.          |
| IP         | 4-byte Integer  | An IP-address encoded as a four byte integer.                                      |

Having gotten this far, let's get a feel for this in practice by performing
a lookup using the `dig` tool:

```python 
PS C:\Users\👻> dig +noedns google.com

; <<>> DiG 9.16.28 <<>> +noedns google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 16700
;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 4, ADDITIONAL: 8

;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             243     IN      A       142.251.175.101
google.com.             243     IN      A       142.251.175.100
google.com.             243     IN      A       142.251.175.102
google.com.             243     IN      A       142.251.175.113
google.com.             243     IN      A       142.251.175.138
google.com.             243     IN      A       142.251.175.139

;; AUTHORITY SECTION:
google.com.             7173    IN      NS      ns1.google.com.
google.com.             7173    IN      NS      ns4.google.com.
google.com.             7173    IN      NS      ns2.google.com.
google.com.             7173    IN      NS      ns3.google.com.

;; ADDITIONAL SECTION:
ns1.google.com.         193251  IN      A       216.239.32.10
ns1.google.com.         240797  IN      AAAA    2001:4860:4802:32::a
ns2.google.com.         193251  IN      A       216.239.34.10
ns2.google.com.         224460  IN      AAAA    2001:4860:4802:34::a
ns3.google.com.         193251  IN      A       216.239.36.10
ns3.google.com.         300300  IN      AAAA    2001:4860:4802:36::a
ns4.google.com.         193251  IN      A       216.239.38.10
ns4.google.com.         19289   IN      AAAA    2001:4860:4802:38::a

;; Query time: 11 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Thu Nov 23 08:33:22 Sri Lanka Standard Time 2023
;; MSG SIZE  rcvd: 372
```
We're using the `+noedns` flag to make sure we stick to the original format. There are a few things of note in the output above:
* We can see that dig explicitly describes the `header, question and answer sections` of the response packet.
* The header is using the `OPCODE QUERY` which corresponds to 0. The status (RESCODE) is set to `NOERROR`, which is 0 numerically. The id is `16700`, and will change randomly with repeated queries. The Query Response `(qr)`, Recursion Desired `(rd)`, Recursion Available `(ra)` flags are enabled, which are 1 numerically. If there is `ad` since it relates to DNSSEC. Finally, the header tells us that there is one question and one answer record.
* The question section shows us our question, with the `IN` indicating the class, and `A` telling us that we're performing a query for A records.
* The answer section contains the answer record, with google's IP. `243` is the `TTL`, `IN` is again the class, and `A` is the record type. Finally, we've got the google.com IP-address.
* We can ignore AUTHORITY SECTION and ADDITIONAL SECTION for now,
* The final line tells us that the total packet size was `372` bytes.
