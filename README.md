# UAB_EnergyStudy

Helping the UAB's energy department make informed decisions on how to spend less money and maintain a certain level of comfort in the univeristy. We want to create an app with two different functionalities. These differ in terms of scale.

The first one is to make predictions on the expenditure for energy in different buildings. We want to check not only how the expenses are going to evolve, but also study the real impact of newer and greener energy sources. This will be done on datasets representing the Expenditure [KHW] based on time, temperature and other features. Information on the subject has been extracted from:
  1. https://www.sciencedirect.com/science/article/abs/pii/S0169207020300996, paper on RNNs and time series forcasting.
  2. https://www.sciencedirect.com/science/article/abs/pii/S0925231201007020, time series forcasting using ARIMA.





## Application Overview
This application monitors and analyzes environmental conditions in various rooms using sensor data. It processes the data with Python, stores it in PostgreSQL, and visualizes it using Grafana. The backend is managed with Express.js and hosted on Microsoft Azure. The mobile app interface is developed with React Native.

<b>Main Features</b>
1. Continuous data collection from sensors.
2. Real-time processing and storage of data in PostgreSQL.
3. Visualization of data through Grafana integrated into the mobile app.

### GET API to Database
<img width="325" alt="image (1)" src="https://github.com/peremayolc/UAB_EnergyStudy/assets/80913049/ed52f0c6-2b85-44ed-a0bc-5b7034f0ebaf">
http://4.233.217.219:3000/data?room_name=Q4-1003

### Home Screen
![Simulator Screenshot - iPhone 15 Pro Max - 2024-05-30 at 22 32 48](https://github.com/peremayolc/UAB_EnergyStudy/assets/80913049/4656951b-2f33-49bc-970c-aef64eb1c152)
Displays real-time environmental data for multiple rooms.


### Recommendation System
![image](https://github.com/peremayolc/UAB_EnergyStudy/assets/80913049/068744ce-c13f-4f28-b314-0afe1b8b7199)
Offers real-time suggestions for maintaining optimal room conditions.


### Technologies Used
<b>Backend</b>

Python: Data processing and analysis.
PostgreSQL: Data storage.
Express.js: API server for data communication.
Microsoft Azure: Hosting and infrastructure.

<b>Frontend</b>

React Native: Mobile app development.
Grafana: Data visualization.


### How to Run
1. Clone the Repository:

git clone https://github.com/peremayolc/UAB_EnergyStudy.git
cd UAB_EnergyStudy

2. Backend Setup:

Set up a PostgreSQL database.
Connect Database in python file(ExtractData.py).
Run the Express.js server.

3. Frontend Setup:

Install required libraries.
pip install -r requirements.txt

Install react and Configure expo

Start
npx expo start