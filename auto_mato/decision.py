# -*- coding: utf-8 -*-
"""
decision.py

@author: Team AutoMato





Total available number of PRBs in the network is T. It depends on the bandwidth that the operator owns. Emergency slice needs C amount of PRBs.
There might be other network slices such as eMBB or URLLC. Some PRBs might have been already given to them.

"""




T = 100  # Total PRBs of the system
import math
from typing import List
from gekko import GEKKO
#def basic_decider(prediction: float) -> None: #float degil liste olacak  iki prediction icin

ALG = 2

def basic_decider(prediction: List[float]) -> None:
    if ALG == 1:
        print('Results For ALG1')
        allocated_prb_to_slice1 = math.floor((prediction[0] / 200) * T)
        allocated_prb_to_slice2 = math.floor((prediction[1] / 200) * T)
        allocated_prb_to_es = T-(allocated_prb_to_slice1 + allocated_prb_to_slice1)
        print("\nEstimated PRB usage of Slice 1:", allocated_prb_to_slice1)
        print("\nEstimated PRB usage of Slice 2:", allocated_prb_to_slice2)
        print("\nAllocated PRB Emergency Slice:", allocated_prb_to_es)
    else:
        T1 = 40
        T2 = 60


        m = GEKKO() # Initialize gekko
        m.options.SOLVER=1  # APOPT is an MINLP solver

        # optional solver settings with APOPT
        m.solver_options = ['minlp_maximum_iterations 500', \
                    # minlp iterations with integer solution
                    'minlp_max_iter_with_int_sol 10', \
                    # treat minlp as nlp
                    'minlp_as_nlp 0', \
                    # nlp sub-problem max iterations
                    'nlp_maximum_iterations 50', \
                    # 1 = depth first, 2 = breadth first
                    'minlp_branch_method 1', \
                    # maximum deviation from whole number
                    'minlp_integer_tol 0.05', \
                    # covergence tolerance
                    'minlp_gap_tol 0.01']


        #Integer constraints 
        u1 = m.Var(value=0,lb=0,ub=T,integer=True)
        u2 = m.Var(value=0,lb=0,ub=T,integer=True)
        b1 = m.Var(value=5,lb=0,ub=T1,integer=True)
        b2 = m.Var(value=5,lb=0,ub=T2,integer=True)
        for i in range(105, 149, 1):
            # Equations
            a1=round(float(prediction[0]*T1/100))
            a2=round(float(prediction[1]*T2/100))
            print(f"Predicted value a1: {a1}")
            print(f"Predicted value a2: {a2}")
            m.Equation(a1-(T1-b1)<=u1)
            m.Equation(a2-(T2-b2)<=u2)
            m.Equation(b1+b2==20)
            #m.Obj(u1+u2) # Objective
            m.Minimize(u1+u2)
            m.solve(disp=False) # Solve
            print('Results For ALG2')
            #print('u1: ' + str(u1.value))
            #print('u2: ' + str(u2.value))
            print('Number of PRBs taken from slice 1: ' + str(b1.value))
            print('Number of PRBs taken from slice 2: : ' + str(b2.value))
            #print('Objective: ' + str(m.options.objfcnval))
        


