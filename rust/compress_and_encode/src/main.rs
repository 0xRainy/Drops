//import needed modules
use base64::{decode, encode};
use std::io;
// compress repeated characters and appened a count to each character, do not append the count if the
// character is repeated only once, then encode the string to base64
fn main() {
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");
    // remove the newline character and carriage return
    input = input.trim_end_matches("\r\n").to_string();
    let mut compressed = Vec::new();
    let mut count = 1;
    let mut prev = input.chars().next().unwrap();
    for c in input.chars().skip(1) {
        if c.eq(&prev) {
            count += 1;
        } else if count == 1 {
            compressed.push(prev);
            count = 1;
            prev = c;
        } else {
            compressed.push(prev);
            compressed.push(char::from_digit(count, 10).unwrap());
            count = 1;
            prev = c;
        }
    }
    compressed.push(prev);
    compressed.push(char::from_digit(count, 10).unwrap());
    if compressed.last().unwrap() == &'1' {
        compressed.pop();
    }
    let encoded = compressed.into_iter().collect::<String>();
    println!("{}", &encoded);
    println!("{}", encode(encoded));
}

// For decoding the string, we need to reverse the process of encoding
// First decode the string to a vector of bytes, then split the vector into a vector of strings
// where each string is a character and a count, then reverse the process of encoding
// to get the original string
fn decode_string(input: &str) -> Vec<u8> {
    let mut decoded = Vec::new();
    let mut input = decode(input).unwrap();
    while input.len() > 0 {
        let c = input.pop().unwrap();
        let count = input.pop().unwrap();
        for _ in 0..count {
            decoded.push(c);
        }
    }
    decoded
}
