from registrars.query import DATA, format_url


def main():
    hennepin = DATA[0]
    print(format_url(hennepin, (-93.3, 45.0)))


if __name__ == "__main__":
    main()

