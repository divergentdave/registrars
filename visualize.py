#!/usr/bin/env python
import geopandas
import matplotlib.pyplot as plt
import osmnx
import yaml

osmnx.settings.use_cache = True


def main():
    with open("data.yaml") as f:
        data = yaml.safe_load(f)

    names = [registrar_dict["osm_name"] for registrar_dict in data]
    gdf = osmnx.gdf_from_places(names)
    print(gdf)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    # downloaded from TIGER
    states = geopandas.read_file("tiger_files/tl_2019_us_state.shp")
    states.plot(ax=ax, color="white", edgecolor="gray")

    gdf.plot(ax=ax)

    plt.show()


if __name__ == "__main__":
    main()
