import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
import pandas as pd

# Assuming LocalDataHandler is imported and set up correctly
from local_data.local_data_handler import LocalDataHandler

# Initialize data handler
data_handler = LocalDataHandler()

# Load node data
nodes = data_handler.get_node_ids()
longitudes = data_handler.get_longitudes()
latitudes = data_handler.get_latitudes()

print(len(nodes))

all_nodes_data = {
    'Longitude': longitudes,
    'Latitude': latitudes
}

all_nodes_gdf = gpd.GeoDataFrame(all_nodes_data, geometry=[Point(xy) for xy in zip(all_nodes_data['Longitude'], all_nodes_data['Latitude'])])
all_nodes_gdf.set_crs(epsg=4326, inplace=True)  
all_nodes_gdf = all_nodes_gdf.to_crs(epsg=3857)  

availability_df = pd.read_csv('node_count.csv')

filtered_data = {
    'Longitude': [],
    'Latitude': [],
    'Availability': []
}

for node_id, count in zip(availability_df['Node'], availability_df['Count']):
    if node_id in nodes:
        index = nodes.index(node_id)
        filtered_data['Longitude'].append(longitudes[index])
        filtered_data['Latitude'].append(latitudes[index])
        filtered_data['Availability'].append(count)

available_nodes_gdf = gpd.GeoDataFrame(filtered_data, geometry=[Point(xy) for xy in zip(filtered_data['Longitude'], filtered_data['Latitude'])])
available_nodes_gdf.set_crs(epsg=4326, inplace=True)
available_nodes_gdf = available_nodes_gdf.to_crs(epsg=3857) 

fig, axs = plt.subplots(1, 2, figsize=(10, 10))

all_nodes_gdf.plot(ax=axs[0], marker='o', color='blue', markersize=15)
axs[0].set_axis_off()
ctx.add_basemap(ax=axs[0], source=ctx.providers.OpenStreetMap.Mapnik)

axs[1].set_axis_off()
available_nodes_gdf.plot(ax=axs[1], marker='o', column='Availability', cmap='coolwarm', markersize=15, alpha=0.6, legend=True)
ctx.add_basemap(ax=axs[1], source=ctx.providers.OpenStreetMap.Mapnik)


plt.subplots_adjust(wspace=0.1)

plt.suptitle("Comparison between all nodes and available nodes")
plt.figtext(0.5, 0.01, "86% of nodes are available", wrap=True, horizontalalignment='center', fontsize=12)

axs[0].set_title("All Nodes")


axs[1].set_title("Available Nodes")

plt.figtext(0.9, 0.9, "Received pings in 30 minutes", wrap=True, horizontalalignment='center', fontsize=12)


plt.show()
