import csv
from collections import defaultdict
import geopandas as gpd
import matplotlib.pyplot as plt
import folium


area = "city"
transit_score = "walk_score"
zip_results_file = f'zip_results_{area}_{transit_score}.txt'
zips_by_label = defaultdict(list)

with open(zip_results_file, newline='') as f:
    headers = f.readline().strip().split('\t')
    for line in f:
        parts = line.strip().split('\t')
        for label, zipc in zip(headers, parts):
            if zipc:          
                zips_by_label[label].append(zipc)

# headers are all of categories names. zips_by_label[label]contains all ZIP in the column
# Zip to label
label_by_zip = {}
for label, zips in zips_by_label.items():
    for z in zips:
        label_by_zip[z] = label

SHAPEFILE_PATH = "./tl_2020_us_zcta520/tl_2020_us_zcta520.shp"
ZIP_FIELD = "ZCTA5CE20"

zcta_gdf = gpd.read_file(SHAPEFILE_PATH)
# only keep zcta that is in our header's category
county_gdf = zcta_gdf[zcta_gdf[ZIP_FIELD].isin(label_by_zip)].copy()
county_gdf["category"] = county_gdf[ZIP_FIELD].map(label_by_zip).fillna("unknown")

unique_labels = list(headers) + ["unknown"]
category_numeric = {lab: i for i, lab in enumerate(unique_labels)}
county_gdf["category_num"] = county_gdf["category"].map(category_numeric)

# remember to make sure each label has a cooresponidng color
color_map = {
    **{lab: col for lab, col in zip(headers, ["green","orange","red","purple","blue"][:len(headers)])},
    "unknown": "lightgrey"
}

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
county_gdf.plot(
    column="category",
    categorical=True,
    legend=True,
    color=county_gdf["category"].map(color_map),
    edgecolor="black",
    linewidth=0.5,
    ax=ax
)

for idx, row in county_gdf.iterrows():
    centroid = row["geometry"].centroid
    zip_code = row[ZIP_FIELD]
    ax.text(
        centroid.x,
        centroid.y,
        zip_code,
        fontsize=8,
        ha="center",
        va="center",
        color="black",
        bbox=dict(facecolor='none', edgecolor='none', alpha=0.5, boxstyle='round,pad=0.2')
    )

ax.set_title(f"St. Louis {area} ZCTAs by {transit_score} Category")
ax.set_axis_off()
plt.tight_layout()
plt.show()

def style_function(feature):
    lab = feature["properties"]["category"]
    return {
        'fillColor': color_map.get(lab, "lightgrey"),
        'color': "black",
        'weight': 0.5,
        'fillOpacity': 0.7
    }

m = folium.Map(location=[38.63, -90.42], zoom_start=10, tiles="cartodbpositron")
folium.GeoJson(
    county_gdf.__geo_interface__,
    name="Transit Category",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=[ZIP_FIELD, "category"])
).add_to(m)
folium.LayerControl().add_to(m)
m.save(f"stl_{area}_{transit_score}_map.html")
print("Interactive map saved to stl_county_transit_map.html")
