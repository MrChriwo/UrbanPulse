import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
import pandas as pd
import matplotlib.colors as mcolors

class RealTimeGeoPlotter:
    def __init__(self, longitude, latitude, availability):
        data = {
            'Longitude': longitude,
            'Latitude': latitude,
            'Availability': availability
        }
        self.gdf = gpd.GeoDataFrame(data, geometry=[Point(xy) for xy in zip(longitude, latitude)])
        self.gdf.set_crs(epsg=4326, inplace=True)
        self.gdf = self.gdf.to_crs(epsg=3857)  # Convert to Web Mercator
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.colormap = plt.get_cmap('coolwarm')  # Choose a colormap that fits your needs
        self.norm = mcolors.Normalize(vmin=0, vmax=1000.0)
        smappable = plt.cm.ScalarMappable(norm=self.norm, cmap=self.colormap)
        self.cbar = self.fig.colorbar(smappable, ax=self.ax)

        minx, miny, maxx, maxy = self.gdf.total_bounds
        self.ax.set_xlim(minx - 1000, maxx + 1000)
        self.ax.set_ylim(miny - 1000, maxy + 1000)
        self.ax.set_axis_off()

        ctx.add_basemap(self.ax, source=ctx.providers.OpenStreetMap.Mapnik)


        self.update_plot()

    def update_plot(self):
        self.ax.cla()
        self.gdf.plot(ax=self.ax, marker='o', column='Availability', cmap=self.colormap, markersize=20)
        plt.draw()

    def add_data(self, longitude, latitude, availability):
        new_point = Point(longitude, latitude)
        mask = self.gdf['geometry'].apply(lambda x: x.equals(new_point))
        if mask.any():
            self.gdf.loc[mask, 'Availability'] = availability
        else:
            new_data = gpd.GeoDataFrame({
                'Longitude': [longitude],
                'Latitude': [latitude],
                'Availability': [availability],
                'geometry': [new_point]
            }, crs='EPSG:4326').to_crs(epsg=3857)
            self.gdf = pd.concat([self.gdf, new_data], ignore_index=True)
        self.norm = mcolors.Normalize(vmin=self.gdf['Availability'].min(), vmax=self.gdf['Availability'].max())  # Update normalization
        self.update_plot()

    def show_plot(self):
        plt.show()
