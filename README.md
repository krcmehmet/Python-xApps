# Python-xApps
Python codes  for RIC xApp for prediction and decision
There are two Python codes and also data (dataset1.csv).

First Python code: xapp_prediction.py It implements a Neural Network as a ML model to make prediction. Given tha data (dataset1.csv), it perfoms training and also validation. 
Testing performance is based on root mean square (RMSE). RMSE value (a floating number) found after running this code is saved  to be the input for the next xapp. As a simple PoC study, this RMSE value will be our message to be sent to next xapp, xapp_decision,  through RMR.  

Second Python code: xapp_decision.py It makes a decision given the input (RMSE value) from xapp_predicition. At the moment, it just makes very simple decision: If RMSE is below a threshold it prints "RMSE is good enough, continue". This will be the second xapp and sends back an ACK to xapp_prediction when the message is received correctly. 
