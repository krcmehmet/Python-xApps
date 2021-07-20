# Python-xApps
Python codes  for RIC xApp for prediction and decision
There are two Python codes and also data (dataset1.csv).

First Python code: xapp_prediction. It implements a Neural Network as aML model to make prediction. Given tha data, it perfoms training and also validation. 
Testing performance is basen on root mean square (RMSE). RMSE value (foating number) found after running this code is saved  to the input for the next xapp.

Second Python code: xapp_decision. It makes a decision given the input (RMSE value) from xapp_predicition. At the moment, it just makes very simple decision. IF RMSE is below a threshold it prints "RMSE is good enough, continue".
