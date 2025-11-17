#!/usr/bin/env python3

def main():
    name = input("Enter your name: ").strip()
    if not name:
        name = "World"
    print(f"Hello, {name}")

if __name__ == "__main__":
    main()
