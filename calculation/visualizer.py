
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium


SHAPEFILE_PATH = "./tl_2020_us_zcta520/tl_2020_us_zcta520.shp"

GOOD_ZIPS    = []  
AVERAGE_ZIPS = [
    "63101","63102","63103","63104","63105","63106","63107","63108",
    "63109","63110","63111","63112","63113","63115","63116","63117",
    "63118","63119","63120","63123","63125","63130","63133","63136",
    "63137","63139","63143","63147"
]
BAD_ZIPS     = ["63138"]

def categorize(zcta):
    if zcta in GOOD_ZIPS:    return "good"
    if zcta in AVERAGE_ZIPS: return "average"
    if zcta in BAD_ZIPS:     return "bad"
    return "unknown"


zcta_gdf = gpd.read_file(SHAPEFILE_PATH)

all_zips = GOOD_ZIPS + AVERAGE_ZIPS + BAD_ZIPS
print(zcta_gdf.columns)
city_gdf = zcta_gdf[zcta_gdf["ZCTA5CE20"].isin(all_zips)].copy()

city_gdf["category"] = city_gdf["ZCTA5CE20"].apply(categorize)


color_map = {"good": "green", "average": "orange", "bad": "red", "unknown":"lightgrey"}

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
city_gdf.plot(
    column="category",
    categorical=True,
    legend=True,
    color=city_gdf["category"].map(color_map),
    edgecolor="black",
    linewidth=0.5,
    ax=ax
)
for idx, row in city_gdf.iterrows():
    centroid = row["geometry"].centroid
    zip_code = row["ZCTA5CE20"]  
    ax.text(
        centroid.x,
        centroid.y,
        zip_code,
        fontsize=8,
        ha="center",
        va="center",
        color="black" if row["category"] != "bad" else "white",  
        bbox=dict(facecolor='none', edgecolor='none', alpha=0.5, boxstyle='round,pad=0.2')
    )

ax.set_title("St. Louis City ZCTAs by Transit-Score Category")
ax.set_axis_off()
plt.tight_layout()
plt.show()


m = folium.Map(location=[38.63, -90.23], zoom_start=11, tiles="cartodbpositron")

folium.Choropleth(
    geo_data=city_gdf.__geo_interface__,
    name="Transit Score",
    data=city_gdf,
    columns=["ZCTA5CE10", "category"],
    key_on="feature.properties.ZCTA5CE10",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Transit Category"
).add_to(m)

folium.LayerControl().add_to(m)


m.save("stl_transit_map.html")
print("Interactive map saved to stl_transit_map.html")
