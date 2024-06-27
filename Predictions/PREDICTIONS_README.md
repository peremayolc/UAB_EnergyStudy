Here it will be explained what each document does inside the Predictions folder, from the datasets used to the resulting predictions.
Firstly, the only document besides this one outside of any folder exist regarding the data. Its the [DataSet](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Copy%20of%20Consum%20energia%20Q%202018-2023%20horari.csv) used along the way. This contains hourly rates on energy expenditure in the Escola d'Enginyeria faculty building.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The first folder, named [SARIMA](https://github.com/peremayolc/UAB_EnergyStudy/tree/main/Predictions/SARIMA) contains everything on how we did the predictions on the SARIMA model, as well as the results. This is separated in two parts:
1. Making predictions for the MEAN monthly consumption.
[Results 1](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/SARIMA/RESULTS%20SARIMA.png) is using one year prior as a test set.
And [Results 2](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/SARIMA/RESULTS_SARIMA_TEST2YEARS.png) is using two year prior as a test set.

  The notebook containing everything is named [Project Final Sarima](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/SARIMA/project_final_SARIMA.ipynb) where everything can be found on how we coded and constructed our SARIMA model. Further explanations on how the model works can be found on the main report. Both predictions appear in this document.

2. Making predictions for the TOTAL monthly SUM consumption.
The notebook containing everythig for this part is here => [SARIMA monthly SUM](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/SARIMA/project_final_SARIMA_SUM.ipynb) And the [results](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/SARIMA/RESULTS_SARIMA_SUM.png) are showcased in the same folder as well.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The second folder, named [Random Forest Regressor](https://github.com/peremayolc/UAB_EnergyStudy/tree/main/Predictions/Random%20Forest%20Regressor) contains everything on how we created the model for rfr. Here you can also find results and procedures followed during the process. Some plots were included to show important information we got and used along the way. It is separated between two folders, each contain the same things and the jupyter notebook for both is the same, the difference is the date used to split the training and test data. Here are both folders and the files that they contain:

1.[First Split](https://github.com/peremayolc/UAB_EnergyStudy/tree/main/Predictions/Random%20Forest%20Regressor/SPLIT1), here you can find the results after using "2021-09-09" to split the data:
  1. The [jupyter notebook](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT1/project_final_RFR.ipynb). Containing the steps on how we treated the data, trained the model and showcased the results.
  2. The [split used](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT1/test_train%20split.png).
  3. [Predictions](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT1/PREDICTIONS.png) graphically represented.
  4. A [.csv file](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT1/data.csv) containing the data so that we have the numerical comparison as well.


2.[Second Split](https://github.com/peremayolc/UAB_EnergyStudy/tree/main/Predictions/Random%20Forest%20Regressor/SPLIT2), here you can find the results after using "2023-01-01" to split the data:
  1. The [jupyter notebook](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT2/project_final_RFR_split2.ipynb). Containing the steps on how we treated the data, trained the model and showcased the results.
  2. The [split used](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT2/test_train%20split2.png).
  3. [Predictions](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT2/PREDICTIONS_split2.png) graphically represented.
  4. A [.csv file](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/Random%20Forest%20Regressor/SPLIT2/data_split2.csv) containing the data so that we have the numerical comparison as well.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The third folder, named [LSTM_EnergyTemps](https://github.com/peremayolc/UAB_EnergyStudy/tree/main/Predictions/LSTM_EnergyTemps) contains almost everything on how we created the model for the LSTM. Here you can also find results and procedures followed during the process. Some plots were included to show some information we got and used along the way. There is an additional folder, named [Merge_csv_for_lstm](https://github.com/peremayolc/UAB_EnergyStudy/tree/main/Predictions/LSTM_EnergyTemps/Merge_csv_for_lstm), containing some of the preprocessing of the data we used in the LSTM. Here is some information about all the files:

1. [Merge_csv_for_lstm](https://github.com/peremayolc/UAB_EnergyStudy/tree/main/Predictions/LSTM_EnergyTemps/Merge_csv_for_lstm), here you can find the data and program used to make the [Merged.csv](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Merge_csv_for_lstm/Merged.csv) file, which is used to train the LSTM.
2. [Merged.csv](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Merged.csv) file, it is the file containing the meteo information as well as the energy expenditure in an hourly rate.
3. [LSTM.py](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/LSTM.py). Containing the file that trains the LSTM model.
4. [Historial.png](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Historial.png), image containing some of the information about training.
5. [.keras file](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/lstm_model.keras), where we store the weights of the model to be able to reuse it.
6. [Validation plot](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Actual_Energy_Values_Validation.png). It shows the actual energy values of the validation split.
7. [Actual](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Actual_Energy_Values_Test.png) and [Predicted](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Predicted_Energy_Values_Test.png) images of the plots that show the actual and predicted values of the test split.
8. [Evaluation](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Evaluation_Energy_Values_Test.png) plot that puts on the same image the [Actual](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Actual_Energy_Values_Test.png) and [Predicted](https://github.com/peremayolc/UAB_EnergyStudy/blob/main/Predictions/LSTM_EnergyTemps/Predicted_Energy_Values_Test.png) energy values of the test split.
