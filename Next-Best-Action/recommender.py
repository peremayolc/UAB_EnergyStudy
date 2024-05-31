import pandas as pd
import os
import json

# Load the CSV file
file_path = "C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/top_two_actions.csv"
top_two_actions_df = pd.read_csv(file_path, index_col=0)

# Function to clean the action strings
def clean_action(action):
    return action.split("'")[1]

# Apply the cleaning function to the DataFrame
top_two_actions_df['First Action'] = top_two_actions_df['First Action'].apply(clean_action)
top_two_actions_df['Second Action'] = top_two_actions_df['Second Action'].apply(clean_action)

# Define thresholds
AIQ_THRESHOLD = 75
TEMP_LOW_THRESHOLD = 19
TEMP_HIGH_THRESHOLD = 25

# Function to determine the current state based on sensor data
def determine_state(aiq, temp, external_temp, external_conditions, illumination):
    if aiq > AIQ_THRESHOLD:
        if external_conditions == "raining":
            return "Situació 2: Els nivells de qualitat de l'aire estan baixos dins l'aula, però plou fora (les finestres estan tancades). Quines d'aquestes mesures prendries:", "AIQ Threshold Problem"
        else:
            return "Situació 1: Els nivells de qualitat de l'aire estan baixos dins l'aula. Quines d'aquestes mesures prendries tenint en compte els avantatges i desavantatges de cada opció:\nNota: es poden tenir en compte variables com el soroll, corrent de l'aire, il·luminació, temperatura, posible aire acondicionat, posible sistema de calefacció, etc. (aplicable a la resta de preguntes)", "AIQ Threshold Problem"
    elif temp > TEMP_HIGH_THRESHOLD:
        if external_temp < temp:
            if external_conditions == "sunny":
                return "Situació 3:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda i fa sol:", "Temperature High Problem"
            else:
                return "Situació 4:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda, però no fa sol:", "Temperature High Problem"
        else:
            if external_conditions == "sunny":
                return "Situació 5:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta i fa sol:", "Temperature High Problem"
            else:
                return "Situació 6:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta, però no fa sol:", "Temperature High Problem"
    elif temp < TEMP_LOW_THRESHOLD:
        if external_temp < temp:
            if external_conditions == "sunny":
                return "Situació 8:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda i fa sol:", "Temperature Low Problem"
            else:
                return "Situació 9:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda, però no fa sol:", "Temperature Low Problem"
        else:
            if external_conditions == "sunny":
                return "Situació 10:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta i fa sol:", "Temperature Low Problem"
            else:
                return "Situació 11:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta, però no fa sol:", "Temperature Low Problem"
    elif illumination < 300:  # Assuming illumination threshold for low levels
        return "Situació 13:  Els nivells d'il·luminació de l'aula estan baixos.  Quines d'aquestes mesures prendries:", "Illumination Low Problem"
    elif illumination > 700:  # Assuming illumination threshold for high levels
        return "Situació 14:  Els nivells d'il·luminació de l'aula estan elevats.  Quines d'aquestes mesures prendries:", "Illumination High Problem"
    else:
        return None, "Comfort Thresholds"

# Function to get the top actions for the current state
def get_top_actions(state):
    if state in top_two_actions_df.index:
        return top_two_actions_df.loc[state]
    else:
        return None

# Function to save recommendations to JSON
def save_recommendations(sensor_name, problem_type, first_action, second_action):
    # Define the base directory
    base_dir = "C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/recommender_data_json"
    
    # Define subdirectory based on problem type
    if problem_type == "AIQ Threshold Problem":
        sub_dir = "AIQ_json"
    elif problem_type in ["Temperature High Problem", "Temperature Low Problem"]:
        sub_dir = "TEMP_json"
    else:
        sub_dir = "OTHER_json"  # You can add more categories if needed
    
    # Create full directory path
    full_dir_path = os.path.join(base_dir, sub_dir)
    
    # Ensure the directory exists
    os.makedirs(full_dir_path, exist_ok=True)
    
    # Define the full file path
    file_path = os.path.join(full_dir_path, f"{sensor_name}.json")
    
    # Create the data to save
    data = {
        "problem_type": problem_type,
        "recommended_actions": {
            "first_action": first_action,
            "second_action": second_action
        }
    }
    
    # Save data to JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
