import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

class PlottingUtils:
    def __init__(self):
        pass

    def plot_time_series(self, df: pd.DataFrame, x: str, y: str, title: str = '', xlabel: str = '', ylabel: str = '', grid: bool = True):
        """
        Plots a time series graph from a pandas DataFrame.
        
        Parameters:
        - df: pd.DataFrame - The data frame containing the data to plot.
        - x: str - The column name for the x-axis (usually the date/time).
        - y: str - The column name for the y-axis.
        - title: str - The title of the plot.
        - xlabel: str - The label for the x-axis.
        - ylabel: str - The label for the y-axis.
        - grid: bool - Whether to display a grid (default is True).
        """
        plt.figure(figsize=(10, 6))
        plt.plot(df[x], df[y])
        plt.title(title)
        plt.xlabel(xlabel if xlabel else x)
        plt.ylabel(ylabel if ylabel else y)
        plt.grid(grid)
        plt.show()

    def plot_geodata(self, gdf: gpd.GeoDataFrame, column: str = None, cmap: str = 'viridis', title: str = '', legend: bool = True):
        """
        Plots a GeoDataFrame.
        
        Parameters:
        - gdf: gpd.GeoDataFrame - The geodata frame to plot.
        - column: str - The column to color by (optional).
        - cmap: str - The colormap to use.
        - title: str - The title of the plot.
        - legend: bool - Whether to display the legend (default is True).
        """
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        gdf.plot(column=column, cmap=cmap, legend=legend, ax=ax)
        plt.title(title)
        plt.show()

# Usage example:
# plotting_utils = PlottingUtils()
# plotting_utils.plot_time_series(df, x='date', y='value', title='Time Series Plot', xlabel='Date', ylabel='Value')
# plotting_utils.plot_geodata(gdf, column='population', title='Geospatial Plot', legend=True)
