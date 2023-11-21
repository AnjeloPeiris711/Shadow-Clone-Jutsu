use rustdns::Message;
use rustdns::types::*;
use std::net::UdpSocket;
use std::time::Duration;

fn udp_example() -> std::io::Result<()> {
    // A DNS Message can be easily constructed
    let mut m = Message::default();
    m.add_question("bramp.net", Type::A, Class::Internet);
    m.add_extension(Extension {   // Optionally add a EDNS extension
        payload_size: 4096,       // which supports a larger payload size.
        ..Default::default()
    });

    // Setup a UDP socket for sending to a DNS server.
    let socket = UdpSocket::bind("0.0.0.0:0")?;
    socket.set_read_timeout(Some(Duration::new(5, 0)))?;
    socket.connect("8.8.8.8:53")?; // Google's Public DNS Servers

    // Encode the DNS Message as a Vec<u8>.
    let question = m.to_vec()?;

    // Send to the server.
    socket.send(&question)?;

    // Wait for a response from the DNS server.
    let mut resp = [0; 4096];
    let len = socket.recv(&mut resp)?;

    // Take the response bytes and turn it into another DNS Message.
    let answer = Message::from_slice(&resp[0..len])?;

    // Now do something with `answer`, in this case print it!
    println!("DNS Response:\n{}", answer);

    Ok(())
}
fn main() {
    println!("{:?}", udp_example())
}