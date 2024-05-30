import pandas as pd

# Load the CSV file
file_path = "C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/top_two_actions.csv"
top_two_actions_df = pd.read_csv(file_path, index_col=0)

# Define thresholds
AIQ_THRESHOLD = 75
TEMP_LOW_THRESHOLD = 19
TEMP_HIGH_THRESHOLD = 25

# Function to determine the current state based on sensor data
def determine_state(aiq, temp, external_temp, external_conditions, illumination):
    if aiq > AIQ_THRESHOLD:
        if external_conditions == "raining":
            return "Situació 2: Els nivells de qualitat de l'aire estan baixos dins l'aula, però plou fora (les finestres estan tancades). Quines d'aquestes mesures prendries:"
        else:
            return "Situació 1: Els nivells de qualitat de l'aire estan baixos dins l'aula. Quines d'aquestes mesures prendries tenint en compte els avantatges i desavantatges de cada opció:\nNota: es poden tenir en compte variables com el soroll, corrent de l'aire, il·luminació, temperatura, posible aire acondicionat, posible sistema de calefacció, etc. (aplicable a la resta de preguntes)"
    elif temp > TEMP_HIGH_THRESHOLD:
        if external_temp < temp:
            if external_conditions == "sunny":
                return "Situació 3:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda i fa sol:"
            else:
                return "Situació 4:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda, però no fa sol:"
        else:
            if external_conditions == "sunny":
                return "Situació 5:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta i fa sol:"
            else:
                return "Situació 6:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta, però no fa sol:"
    elif temp < TEMP_LOW_THRESHOLD:
        if external_temp < temp:
            if external_conditions == "sunny":
                return "Situació 8:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda i fa sol:"
            else:
                return "Situació 9:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda, però no fa sol:"
        else:
            if external_conditions == "sunny":
                return "Situació 10:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta i fa sol:"
            else:
                return "Situació 11:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta, però no fa sol:"
    elif illumination < 300:  # Assuming illumination threshold for low levels
        return "Situació 13:  Els nivells d'il·luminació de l'aula estan baixos.  Quines d'aquestes mesures prendries:"
    elif illumination > 700:  # Assuming illumination threshold for high levels
        return "Situació 14:  Els nivells d'il·luminació de l'aula estan elevats.  Quines d'aquestes mesures prendries:"
    else:
        return None

# Function to get the top actions for the current state
def get_top_actions(state):
    if state in top_two_actions_df.index:
        return top_two_actions_df.loc[state]
    else:
        return None