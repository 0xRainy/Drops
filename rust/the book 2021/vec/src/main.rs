fn main() {
    // let v: Vec<i32> = Vec::new();
    // let v = vec![1, 2, 3];
    let mut v = Vec::new();

    v.push(1);
    v.push(2);
    v.push(3);
    v.push(4);

    let third: &i32 = &v[2];
    println!("The third element is {}", third);

    match v.get(2) {
        Some(third) => println!("The third element is {}", third),
        None => println!("There is no third element."),
    }
}
