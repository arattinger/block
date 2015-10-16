import argparse


DESCRIPTION = "Block: Easily generate your static site in seconds."


def parse_arguments():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--verbosity", help="increase output verbosity")
    parser.parse_args()


def main():
    args = parse_arguments()
    # print(args)

if __name__ == '__main__':
    main()
