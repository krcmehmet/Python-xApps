# Python-xApps
Python codes  for RIC xApp for prediction and decision

NOTE: Please use Ubuntu (20.04 works fine). We got problems about RMR messaging with MAC OS and  have not tried with Windows. 

 Python code: xapp_prediction.py 

It implements Gaussain Process Regression (GPR) as a ML model to make prediction. Given tha data (pla.csv), which PRB utilization taken from a real network in percentage, it perfoms training and also validation. Testing performance is based on MAE. This xapp forecasts PRB utilization in near future (e.g, next 500 ms.). We train GPR with prediciton.py and save it. This xapp takes the save model and use it. 

 Python code: xapp_decision.py 

It makes a decision given the input from xapp_predicition.  It implements two different algorithms ALG1 and ALG2. In decision.py there is paramater ALG which needs to be set  to 1 if ALG1 wants to be run. After this change it needs to rebuilt  and use
```
sudo docker-compose build
```
(after any code change it needs to rebuilt). This will be the second xapp and sends back an ACK to xapp_prediction when the message is received correctly. 

## Installation

### Dependencies
- Docker is required to build the containers, follow the installation guidelines.
- docker-compose is used to orchestrate multiple xApps, follow the installation guidelines.


### Build docker images
Once the dependencies use the following command to build the containers:
```
sudo docker-compose build
```
If you are running this command the first time it can take 5 minutes. Following builds should take significantly less time.

## Usage
To run the xApps run the following command in the root folder od Auto-Mato:
```
sudo docker-compose up
```
The prediction and decision xApps will start and print out messages.

Note: Due to a bug in the underlying RMR library following runs might require a restart.

To stop containers use Ctrl+C, this will take a minute or two. Once this step is complete run
```
sudo docker-compose down -v
```

## TODO: EVERYTHING
- [] Unit tests
- [] Add decision wrapper function in decision.py
- [] Add prediction wrapper function in prediction.py
- [] Helper class/function to create and parse messages between prediction-decision xApps
- [] Add xApp for monitoring

Additionally
- [] Data retrieval from E2 or simulator
- [] A1 intent processing
