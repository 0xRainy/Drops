use std::collections::HashMap;
use rand::{Rng, seq::SliceRandom, thread_rng};

use crate::user::get_input;

pub mod user {
    use std::io;

    pub fn get_input() -> String {
        let mut input = String::new();

        io::stdin()
            .read_line(&mut input)
            .expect("Failed to read line");
        return input
    }
}


pub struct Markov {
    map: HashMap<String, Vec<String>>
}

impl Markov {
    pub fn new() -> Markov {
        Markov {
            map: HashMap::new()
        }
    }
    pub fn parse(&mut self, sentence: &str) {
        let words = sentence.split_whitespace().collect::<Vec<&str>>();
        let word_count = words.len();

        for n in 0..word_count {
            if n + 1 < word_count {
                let key = words[n];
                let value = words[n + 1];
                self.insert(key.to_string(), value.to_string())
            } else {
                break
            }
        }
    }

    fn insert(&mut self, key: String, value: String) {
        if self.map.contains_key(&key) {
            let current_value = self.map.get_mut(&key).unwrap();
            current_value.push(value);
        } else {
            self.map.insert(key, vec!(value));
        }
    }

    pub fn generate_sentence(self) -> String {
        let keys = self.map.keys().collect::<Vec<&String>>();
        let mut rng = thread_rng();

        let mut key = keys.choose(&mut rng)
            .expect("could not get random value").to_string();
        let mut sentence = key.clone();

        loop {
            match self.map.get(&key) {
                Some(values) => {
                    if values.len() >= 2 {
                        let value = &values.choose(&mut rng)
                            .expect("could not get random value");
                        sentence = format!("{} {}", sentence, value);

                        key = value.to_string();
                    } else {
                        if thread_rng().gen_range(1..3) == 1 {
                            let value = &values.choose(&mut rng)
                                .expect("could not get random value");
                            sentence = format!("{} {}", sentence, value);

                            key = value.to_string();
                        } else {
                            key = keys.choose(&mut rng)
                                .expect("could not get random value").to_string();
                        }
                    }
                }
                None => break
            }
        }
        sentence.to_string()
    }
}

fn main() {
    println!("Welcome to Markov chain bot!");
    let mut map = Markov::new();
    let input = get_input();
    map.parse(&input.to_string());
    println!("{:?}", map.generate_sentence());
}

