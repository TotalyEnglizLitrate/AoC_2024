mod solns;
use std::fs::File;
use std::io::Read;
use std::path::PathBuf;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        println!("Please provide a day number as an argument.");
        return;
    }
    let day_number: i32 = args[1].parse().unwrap();
    run_day(day_number);
}

pub fn get_input(day: &u8) -> String {
    let mut input_dir_path = PathBuf::from(file!())
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .to_path_buf();
    input_dir_path.push("inputs");

    let mut input_file = File::open(format!(
        "{}/input_{}.txt",
        input_dir_path.to_string_lossy(),
        day
    ))
    .unwrap();
    let mut input = String::new();
    let _ = input_file.read_to_string(&mut input).unwrap();

    input
}

fn run_day(day_number: i32) {
    match day_number {
        1 => solns::day_1::run(),
        _ => println!("No such day exists yet!"),
    }
}
