//import needed modules
use base64::{decode, encode};
use std::io;
//TODO: Refactor encoding into its own function and clean up mian function
// Compress by run-length by appeneding a count to each unique character, do not append the count if the
// character is repeated only once, then encode the string to base64
fn main() {
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");
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
    compressed.pop();
    compressed.pop();
    let encoded = &compressed;
    let encoded_string = &compressed.iter().map(|(c, n)| format!("{}{}", c, n)).collect::<Vec<String>>().join("");
    println!("{:?}", &encoded);
    println!("{}", encode(encoded_string));
    //println!("{}", decode_string(encode(encoded_string)));
    println!("{:?}", decode(encode(encoded_string)));
    println!("{}", &encoded_string);
    println!("{}", decode_string(&encode(encoded_string)));
}

//Take a String and decode from base64 to a Vec<char>
//Then reverse the text compression and return the original text as a String
//TODO: fix count not working for numbers greater than 19 ?????
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
            println!("{:?}", num);
        }
        if num.len() > 0 {
            count = num.iter().map(|n| n.to_string()).collect::<String>().parse::<u8>().unwrap();
            println!("{}", count);
        }
        if count == 0 {
            decoded.push(prev);
        } else {
            for _ in 0..count-1 {
                decoded.push(prev);
                num = Vec::new();
                count = 0;
            }
        }
    }
    decoded
}
