from registrars.query import format_url, search_index


def main():
    gps_location = (-93.3, 45.0)
    for registrar_dict in search_index(gps_location):
        # TODO: check point-in-polygon
        print(registrar_dict)
        print(format_url(registrar_dict, gps_location))


if __name__ == "__main__":
    main()
