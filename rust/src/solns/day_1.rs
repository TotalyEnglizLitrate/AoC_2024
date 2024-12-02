use crate::get_input;

use std::collections::HashMap;
use std::iter::zip;

pub fn run() {
    let input = get_input(&1);
    attempted_one_line_soln(&input);
    println!();
    normal_soln(&input);
}

fn attempted_one_line_soln(input: &str) {
    let (mut v1, mut v2) = input
        .split("\n")
        .filter(|line| !line.is_empty())
        .map(|line| {
            line.split_whitespace()
                .map(|x| x.parse::<i32>().unwrap())
                .collect::<Vec<i32>>()
        })
        .map(|v| (v[0], v[1]))
        .unzip::<i32, i32, Vec<i32>, Vec<i32>>();

    v1.sort();
    v2.sort();

    let mut count: HashMap<i32, i32> = HashMap::new();
    let _ = v1
        .iter()
        .map(|x| {
            if !count.contains_key(x) {
                count.insert(*x, v2.iter().filter(|y| x == *y).count() as i32);
                x
            } else {
                x
            }
        })
        .collect::<Vec<&i32>>();

    println!("(Almost) oneline:");
    println!(
        "Part 1 -  {}",
        zip(v1.iter(), v2.iter()).fold(0, |acc, (x, y)| acc + (x - y).abs())
    );
    println!(
        "Part 2 -  {}",
        v1.iter()
            .fold(0, |acc, x| acc + (x * count.get(x).unwrap_or(&0)))
    );
}

fn normal_soln(input: &str) {
    let mut v1: Vec<i32> = vec![];
    let mut v2: Vec<i32> = vec![];
    let mut nums: Vec<i32>;
    for line in input.split("\n") {
        if line.is_empty() {
            continue;
        }
        nums = line
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
        if nums.len() != 2 {
            println!("{} - {:?}", line, nums);
        }
        v1.push(nums[0]);
        v2.push(nums[1]);
    }

    v1.sort();
    v2.sort();

    let mut part_one_sum: i32 = 0;
    let mut part_two_count: HashMap<i32, i32> = HashMap::new();
    let mut part_two_sum: i32 = 0;

    for i in 0..v1.len() {
        part_one_sum = part_one_sum + (v1[i] - v2[i]).abs();
        if !part_two_count.contains_key(&v1[i]) {
            part_two_count.insert(v1[i], v2.iter().filter(|y| &v1[i] == *y).count() as i32);
        }
        part_two_sum = part_two_sum + (v1[i] * part_two_count.get(&v1[i]).unwrap_or(&0));
    }

    println!("Normal soln:");
    println!("Part 1 - {}", part_one_sum);
    println!("Part 2 - {}", part_two_sum);
}
