import pandas as pd

# Load the CSV file
file_path = "C:/GitHub Repositories/UAB_EnergyStudy/Next-Best-Action/Comfort.csv"
data = pd.read_csv(file_path)

# Remove any unnamed columns that are likely empty or irrelevant
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Define the list of states with the exact column names from the data
states = [
    "Situació 1: Els nivells de qualitat de l'aire estan baixos dins l'aula. Quines d'aquestes mesures prendries tenint en compte els avantatges i desavantatges de cada opció:\nNota: es poden tenir en compte variables com el soroll, corrent de l'aire, il·luminació, temperatura, posible aire acondicionat, posible sistema de calefacció, etc. (aplicable a la resta de preguntes)",
    "Situació 2: Els nivells de qualitat de l'aire estan baixos dins l'aula, però plou fora (les finestres estan tancades). Quines d'aquestes mesures prendries:",
    "Situació 3:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda i fa sol:",
    "Situació 4:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda, però no fa sol:",
    "Situació 5:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta i fa sol:",
    "Situació 6:   La temperatura aparent de l'aula està molt elevada. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta, però no fa sol:",
    "Situació 7:   La temperatura aparent de l'aula està molt elevada, però plou fora (les finestres estan tancades). Quines d'aquestes mesures prendries:",
    "Situació 8:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda i fa sol:",
    "Situació 9:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més freda, però no fa sol:",
    "Situació 10:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta i fa sol:",
    "Situació 11:   La temperatura aparent de l'aula està molt baixa. Quines d'aquestes mesures prendries tenint en compte que la temperatura exterior és més calenta, però no fa sol:",
    "Situació 12:   La temperatura aparent de l'aula està molt baixa, però plou fora (les finestres estan tancades). Quines d'aquestes mesures prendries:",
    "Situació 13:  Els nivells d'il·luminació de l'aula estan baixos.  Quines d'aquestes mesures prendries:",
    "Situació 14:  Els nivells d'il·luminació de l'aula estan elevats.  Quines d'aquestes mesures prendries:"
]
actions = [
    "Obrir les portes", "Tancar les portes", "Obrir les finestres", "Tancar les finestres", 
    "Pujar totalment les persianes", "Abaixar parcialment les persianes", 
    "Abaixar totalment les persianes", "Cap de les anteriors mesures"
]

# Initialize a dictionary to store counts
counts = {state: {action: 0 for action in actions} for state in states}

# Process each response
for state in states:
    for response in data[state]:
        if pd.notna(response):
            selected_actions = response.split(";")
            for action in selected_actions:
                action = action.strip()
                if action in counts[state]:
                    counts[state][action] += 1

# Convert counts to a DataFrame for better visualization
counts_df = pd.DataFrame(counts).fillna(0).astype(int)
counts_df = counts_df.T  # Transpose for better readability

# Function to get top two actions for each state
def get_top_two_actions(state_counts):
    sorted_actions = sorted(state_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_actions[:2]

# Initialize a dictionary to store the top two actions for each state
top_two_actions = {state: get_top_two_actions(counts[state]) for state in counts}

# Convert to a more readable format
top_two_actions_df = pd.DataFrame.from_dict(top_two_actions, orient='index', columns=['First Action', 'Second Action'])









AIQ_THRESHOLD = 75
TEMP_LOW_THRESHOLD = 19
TEMP_HIGH_THRESHOLD = 25
# Function to determine the current state based on sensor data
def determine_state(aiq, temp, external_temp, external_conditions):
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
    else:
        return None

def get_top_actions(state):
    if state in top_two_actions_df.index:
        return top_two_actions_df.loc[state]
    else:
        return None

