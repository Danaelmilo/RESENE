# RESENE TEE Heat netowrk

Work realized in October 2023 by Mona Boufraïne and Milo Dreyfus.

## How to use ?

You just have to clone the repository and run the different scripts questions by question (Q1, Q2, Q3 and Q4).

## Parameters that can be changed.

All the parameters are grouped in the "constants.py" file.  
Some of them are questionable and may be changed :  
- The emission factors because the source is not reliable
- The emission factors if you want to put the biomass factor = 0 : replace line 63 by line 64
- The price of the carbon tax
You are invited to do so and see the impact on the results of the simulation.  


To take the carbon tax into account, go to "fuctions.py" and replace line 166 and 167 by line 168 and 169.  
Then re run the Q3 and Q4 scripts to see the difference.  


In "Q4.py" line 27, you can increase the precision of the simulation with the parameter n.