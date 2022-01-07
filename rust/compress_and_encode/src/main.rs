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
    let encoded_string = &compressed.iter().map(|(c, n)| format!("{}{}", c, n)).collect::<Vec<String>>().join("").replace("1","").replace("\r","");
    println!("{:?}", &encoded);
    println!("{}", encode(encoded_string));
    //println!("{}", decode_string(encode(encoded_string)));
    println!("{:?}", decode(encode(encoded_string)));
    println!("{}", &encoded_string);
    println!("{}", decode_string(&encode(encoded_string)));
}

// For decoding the string, we need to reverse the process of encoding
// First decode the string to a vector of bytes, then split the vector into a vector of strings
// where each string is a character and a count, then reverse the process of encoding
// to get the original string
fn decode_string(input: &String) -> String {
    let mut decoded = String::new();
    let decoded_input = decode(&input).unwrap().iter().map(|b| *b as char).collect::<Vec<char>>();
    let mut num: Vec<u8> = Vec::new();
    let mut count: u8 = 0;
    let mut prev: char = *decoded_input.first().unwrap();
    for c in decoded_input {
        if !c.is_numeric() {
            prev = c;
        }
        if c.is_numeric() {
            num.push(c.to_digit(10).unwrap() as u8);
        }
        if num.len() > 0 {
            count = num.iter().map(|n| n.to_string() + ",").collect::<String>().replace(",","").parse::<u8>().unwrap();
            num = Vec::new();
        }
        if count == 0 {
            decoded.push(prev);
        } else {
            for _ in 0..count-1 {
                decoded.push(prev);
            }
            count = 0;
        }
    }
    decoded
}
