# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 08:35:24 2021

@author: mehmet.karaca
"""




"""
Total available number of PRBs in the network is T. It depends on the bandwidth that the operator owns.

Emergency slice needs C amount of PRBs. 

There might be other network slices such as eMBB or URLLC. Some amoung of PRB might have been already given to them.

"""
import pandas as pd

T = 100
E  =  20
N = 80

total_num_PRBs = T 

Other_Slices_PRBs = N 

ES_need_PRB = E

available_slice_for_ES = T-N


if available_slice_for_ES > ES_need_PRB:
    
    """
    There is emough number of PRBs for ES. Allocate to them.
    """
    print("The current available PRB is enoıgh for ES. Static network slicing")

    
else:
    print("The current available PRB is not enoıgh for ES. Borrow PRBS form other slice. Switch to dynamic network slicing")
        
def basic_decider(self):
    if available_slice_for_ES > ES_need_PRB:
    
    