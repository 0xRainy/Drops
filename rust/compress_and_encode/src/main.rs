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
    input = input.replace(" ","").to_string();
//TODO: Make compressed store tuples of (char, count)
    let mut compressed = Vec::new();
    let mut count: u32 = 1;
    let mut prev = input.chars().next().unwrap();
    let mut pairs: (char, u32);
    for c in input.chars().skip(1) {
        if c.eq(&prev) {
            count += 1;
        } else if count == 1 {
            pairs = (prev, count);
            compressed.push(pairs);
            count = 1;
            prev = c;
        } else {
            pairs = (prev, count);
            compressed.push(pairs);
            count = 1;
            prev = c;
        }
    }
    pairs = (prev, count);
    compressed.push(pairs);
    if compressed.last().unwrap() == &(prev, 1) {
        compressed.pop();
    }
    let encoded = &compressed;
    let encoded_string = &compressed.iter().map(|(c, n)| format!("{}{}", c, n)).collect::<Vec<String>>().join("").replace("1","");
    println!("{:?}", &encoded);
    println!("{}", encode(encoded_string));
    println!("{}", &encoded_string);
    //println!("{}", decode_string(&encoded));
}

// For decoding the string, we need to reverse the process of encoding
// First decode the string to a vector of bytes, then split the vector into a vector of strings
// where each string is a character and a count, then reverse the process of encoding
// to get the original string
fn decode_string(input: &Vec<char>) -> String {
    let mut decoded = String::new();
    let mut input = decode(&input.into_iter().collect::<String>()).unwrap();
    for i in 0..input.len() {
        let c = input[i];
        let count = input[i + 1];
        input.remove(i);
        input.remove(i + 1);
        for _ in 0..count {
            decoded.push(c as char);
        }
    }
    decoded
}
