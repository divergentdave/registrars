from registrars.query import format_url, open_index, search_index


def main():
    gps_location = (-93.3, 45.0)
    index = open_index()
    for registrar_dict in search_index(gps_location, index):
        print(registrar_dict["osm_name"])
        print(format_url(registrar_dict, gps_location))


if __name__ == "__main__":
    main()
