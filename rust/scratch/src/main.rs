fn main() {
    {
    let x = String::from("POOP");
    println!("x is {}", x);
        {
        let y = &x;
        println!("y is {} and x is {}", y, x);
        } 
    }
    println!("x is {}", x);
}
