# ITU AI Challenge: Build-a-Thon- Team AUTOMATO

# Python xApps
Python codes  for RIC xApp for prediction and decision

NOTE: Only Linux systems are supported (Ubuntu 20.04 works fine).

### Python code: xapp_prediction.py 

Implements Gaussian Process Regression (GPR) as a ML model to make prediction. Given tha data (data from Conqureors team or pla.csv), which PRB utilization taken from a real network in percentage, it perfoms training and also validation. Testing performance is based on MAE. This xapp forecasts PRB utilization in near future (e.g, next 500 ms.). We train GPR with prediction.py and save it. This xapp takes the saved model and uses it. We also parse the intent coming from Winest team to find URL of source, model and sink.

### Python code: xapp_decision.py 

It makes a decision given the input from xapp_prediction. Two different algorithms are implemented, these are defined in the code as ALG1 and ALG2. In decision.py the variable ALG should be set to specify the running algorithm. If the algorithm type is changed the docker container needs to rebuilt. To rebuild the docker container use
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
