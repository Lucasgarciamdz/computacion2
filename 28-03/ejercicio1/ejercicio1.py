import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num", help="enter a positive integer", type=int)
    args = parser.parse_args()
    if args.num > 0:
        print([i for i in range(1, args.num*2, 2)])
    else:
        print("enter a positive integer")


if __name__ == "__main__":
    main()
