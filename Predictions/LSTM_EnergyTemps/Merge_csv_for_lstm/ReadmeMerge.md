This code only performs several tasks related to data preprocessing and merging for the LSTM. In particular, the one that seeks to predict the energy consumption incorporating weather conditions.

The folder contains different files:
1. [Consum energia](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Merge_csv_for_lstm/Consum-energia-Q-2018-2023-horari.csv), a csv file containing the energy hourly rate consumption.
2. Not in the folder: the [meteo data](https://drive.google.com/file/d/1JL9x5iS8gFPX05HtBcOe1xiJydvL2VCw/view?usp=drive_link) of the [Xarxa d’Estacions Meteorològiques Automàtiques (XEMA)](https://analisi.transparenciacatalunya.cat/Medi-Ambient/Metadades-estacions-meteorol-giques-autom-tiques/yqwd-vj5e/about_data). The extracted CSV file is so large that we couldn't upload it to the repository.
3. [MergeCSV.py](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Merge_csv_for_lstm/MergeCSV.py), the program designed for preprocessing and merging the data.
5. [group_data_temps.csv](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Merge_csv_for_lstm/group_data_temps.csv) a intermidiate csv file that groups the meteo data hourly.
6. [Merged.csv](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Merge_csv_for_lstm/Merged.csv), the final product of the program that is fed into the LSTM.



# MergeCSV.py does:
Imports and Initial Setup

    Imports: The script imports essential libraries for data manipulation (pandas, numpy), visualization (seaborn, matplotlib.pyplot), and machine learning (sklearn).
    Confirmation Message: Prints a message indicating that the imports are done.

Mapping Dictionary and Conversion Function

    Mapping Dictionary: Defines a mapping of numeric codes to descriptive variable names.
    Conversion Function: A function that converts a numeric code to its corresponding variable name using the mapping dictionary. If the code is not found, it returns np.nan.

Data Grouping Function

    Data Grouping: Converts and pivots the input dataframe by grouping data by date. It reformats the data into a more structured form and saves the result to a CSV file.

Temperature Data Preprocessing Function

    Reading and Preprocessing: Reads the temperature data from a CSV file, maps numeric codes to variable names, drops rows with missing or irrelevant data, and calls the data grouping function.

Consumption Data Preprocessing Function

    Reading and Cleaning: Reads the consumption data from a CSV file, combines date and hour columns into a single datetime column, renames specific columns, and drops rows with invalid datetime entries.

Data Merging Function

    Merging Data: Merges the preprocessed temperature and consumption data on the datetime column, saves the merged dataframe to a CSV file, and prints a confirmation message. Returns the merged dataframe.

