# Python-xApps
Python codes  for RIC xApp for prediction and decision
There are two Python codes and also data (dataset1.csv).

First Python code: xapp_prediction.py 

It implements a Neural Network as a ML model to make prediction. Given tha data (dataset1.csv), it perfoms training and also validation. 
Testing performance is based on root mean square (RMSE). RMSE value (a floating number) found after running this code is saved  to be the input for the next xapp. As a simple PoC study, this RMSE value will be our message to be sent to next xapp, xapp_decision,  through RMR.  

Second Python code: xapp_decision.py 

It makes a decision given the input (RMSE value) from xapp_predicition. At the moment, it just makes very simple decision: If RMSE is below a threshold it prints "RMSE is good enough, continue". This will be the second xapp and sends back an ACK to xapp_prediction when the message is received correctly. 

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
