#!/usr/bin/env python
import osmnx
import yaml

osmnx.settings.use_cache = True


def main():
    with open("data.yaml") as f:
        data = yaml.safe_load(f)

    names = [registrar_dict["osm_name"] for registrar_dict in data]
    gdf = osmnx.gdf_from_places(names)
    print(gdf)
    osmnx.plot_shape(gdf)


if __name__ == "__main__":
    main()
