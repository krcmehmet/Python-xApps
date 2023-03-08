#  ITU-ML5G-PS-014: Build-a-thon(PoC) - Team "AUTOMATO"
This repo contains our submission for ITU AI Challenge 2021: ITU-ML5G-PS-014- Build-a-thon(PoC) Network resource allocation for emergency management based on closed loop analysis.  

Our detailed report and demo are available in this repo.

# Python xApps
Python codes  for RIC xApp for prediction and decision. 

The main goal of this activity is to create a closed-loop that handles an emergency case (i.e., earthquake or fire) autonomously. It includes RAN resource monitoring and computing, that is realized with machine learning algorithms, and also resource allocation at RAN that turns to be an integer-optimization problem. We have achieved the goals of this activity, implemented in Python and presented the results in our report. Also, our implementation is realized as RIC xApps to be used in Open-RAN integration in future. 

NOTE: Only Linux systems are supported (Ubuntu 20.04 works fine).

### Python code: xapp_prediction.py 

For monitoring RAN resource we apply Gaussian Process Regression (GPR) as a ML model to make a time-series prediction for future traffic in the network. Given tha data (data from Conqureors team or pla.csv), which is PRB utilization, it perfoms training and also validation. Testing performance is based on MAE. With GPR we predict how much resource (PRB) will be availabe for emergence case in near future. The implementation is a RIC xapp which  forecasts PRB utilization  (e.g, at every 500 ms.). We train GPR with prediction.py. We have trained two differet ML models and saved them on a remote server, and these models can be  pulled and used dynamically.  We also parse the intent coming from Winest team to find URL of source (data), model and sink.

### Python code: xapp_decision.py 

Once the traffic prediction is done, prediction_xapp.py sends the predictions of PRB usage to decision_xapp.py that  makes resource allocation decision. Two different algorithms are implemented for the resource allocation, and these are defined in the code as ALG1 and ALG2. In decision.py the variable ALG should be set to specify the running algorithm. If the algorithm type is changed the docker container needs to rebuilt. To rebuild the docker container use
```
sudo docker-compose build
```
(after any code change it needs to rebuilt). This will be the second xapp and sends back an ACK to xapp_prediction when the message is received correctly. 

## Installation
First using "git clone", clone this repo to your local. Then, 

### Dependencies
- Docker is required to build the containers, follow the installation guidelines.
- docker-compose is used to orchestrate multiple xApps, follow the installation guidelines.
- Install docker and docker-compose to your system.

### Build docker images
On the folder where you download this repo, use the following command to build the containers:
```
sudo docker-compose build
```
If you are running this command the first time it can take 5 minutes. Following builds should take significantly less time.

## Usage
To run the xApps run the following command in the root folder of Auto-Mato:
```
sudo docker-compose up
```
The prediction and decision xApps will start and print out messages.

Note: Due to a bug in the underlying RMR library following runs might require a restart.

To stop containers use Ctrl+C, this will take a minute or two. Once this step is complete run
```
sudo docker-compose down -v
```
