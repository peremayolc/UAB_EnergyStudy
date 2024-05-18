import paho.mqtt.client as mqtt
import json
from datetime import datetime
import pytz
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import pyodbc
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pythermalcomfort.models import at
from pythermalcomfort.utilities import v_relative
import numpy as np


# Function to calculate apparent temperature
def calculate_apparent_temp(tdb, rh, v, met, clo):
    vr = v_relative(v, met)
    apparent_temp = at(tdb=tdb, rh=rh, v=vr)
    return apparent_temp

def normalize(value, min_val, max_val):
    """Normalize the value on a scale of 0 to 100."""
    return ((value - min_val) / (max_val - min_val)) * 100

def calculate_aiq(co2, tvoc, o3=None, PM10=None, PM25=None):
    """Calculate the AIQ index based on the provided sensor data."""

    if o3 is not None or PM10 is not None or PM25 is not None:
        # Normalize additional pollutants
        co2_index = normalize(co2, 400, 1100)
        tvoc_index = normalize(tvoc, 50, 1000)
        o3_index = normalize(o3, 0, 200) if o3 is not None else 0
        PM10_index = normalize(PM10, 0, 100) if PM10 is not None else 0
        PM25_index = normalize(PM25, 0, 60) if PM25 is not None else 0

        # Weights for additional pollutants
        co2_weight = 0.2
        tvoc_weight = 0.2
        o3_weight = 0.2
        PM10_weight = 0.2
        PM25_weight = 0.2

        # Calculate combined AIQ index
        total_weight = co2_weight + tvoc_weight + o3_weight + PM10_weight + PM25_weight
        aiq_index = (
            (co2_index * co2_weight) +
            (tvoc_index * tvoc_weight) +
            (o3_index * o3_weight) +
            (PM10_index * PM10_weight) +
            (PM25_index * PM25_weight)
        ) / total_weight

    #if only co2 and tvocs
    else:
        co2_index = normalize(co2, 400, 1100)
        tvoc_index = normalize(tvoc, 50, 1000)

        co2_weight = 0.6
        tvoc_weight = 0.4
        # Calculate base AIQ index using CO2 and TVOCs
        aiq_index = (co2_index * co2_weight) + (tvoc_index * tvoc_weight)

    return aiq_index



'''

# Initialize lists to store time, apparent temperatures, and CO2 levels
times = []
apparent_temps = []
co2_levels = []

# Generate artificial CO2 levels and data points
for i, point in enumerate(data_points):
    met = point["met"]
    v = point["v"]
    tdb = point["tdb"]
    rh = point["rh"]
    clo = point["clo"]

    apparent_temp = calculate_apparent_temp(tdb, rh, v, met, clo)
    co2_level = np.random.uniform(low=300, high=1000)  # Generate random CO2 level for demonstration

    times.append(i)  # Assuming each data point corresponds to a unique time step
    apparent_temps.append(apparent_temp)
    co2_levels.append(co2_level)

# Plot 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting the data points
ax.scatter(times, apparent_temps, co2_levels, c='b', marker='o')

# Labeling the axes
ax.set_xlabel('Time')
ax.set_ylabel('Apparent Temperature (°C)')
ax.set_zlabel('CO2 Levels (ppm)')

# Title
ax.set_title('Apparent Temperature and CO2 Levels over Time')

plt.show()
'''