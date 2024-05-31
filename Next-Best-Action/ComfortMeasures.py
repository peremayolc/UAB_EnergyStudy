from pythermalcomfort.models import at
from pythermalcomfort.utilities import v_relative

# Function to calculate apparent temperature
def calculate_apparent_temp(tdb, rh, v, met, clo):
    vr = v_relative(v, met)
    apparent_temp = at(tdb=tdb, rh=rh, v=vr)
    return apparent_temp

def normalize(value, min_val, max_val):
    """Normalize the value on a scale of 0 to 100."""
    return ((value - min_val) / (max_val - min_val)) * 100

def calculate_aiq(co2, tvoc=None, o3=None, PM10=None, PM25=None):
    """Calculate the AIQ index based on the provided sensor data."""
    # Scenario: sensors with CO2, TVOC, O3, PM10, and PM25
    if o3 is not None and PM10 is not None and PM25 is not None and tvoc is not None and co2 is not None:
        co2_index = normalize(co2, 400, 1100)
        tvoc_index = normalize(tvoc, 50, 1000)
        o3_index = normalize(o3, 0, 200)
        PM10_index = normalize(PM10, 0, 100)
        PM25_index = normalize(PM25, 0, 60)

        co2_weight = 0.2
        tvoc_weight = 0.2
        o3_weight = 0.2
        PM10_weight = 0.2
        PM25_weight = 0.2

        total_weight = co2_weight + tvoc_weight + o3_weight + PM10_weight + PM25_weight
        aiq_index = (
            (co2_index * co2_weight) +
            (tvoc_index * tvoc_weight) +
            (o3_index * o3_weight) +
            (PM10_index * PM10_weight) +
            (PM25_index * PM25_weight)
        ) / total_weight
        return aiq_index

    # Scenario: sensors with CO2 and TVOC only
    elif tvoc is not None:
        co2_index = normalize(co2, 400, 1100)
        tvoc_index = normalize(tvoc, 50, 1000)

        co2_weight = 0.6
        tvoc_weight = 0.4

        aiq_index = (co2_index * co2_weight) + (tvoc_index * tvoc_weight)
        return aiq_index

    # Scenario: sensor with CO2 only
    else:
        co2_index = normalize(co2, 400, 1100)
        return co2_index