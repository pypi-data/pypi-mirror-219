import os 
import numpy as np
import pandas as pd
# Compile list of data, each set of data is individual (using pandas)
objects = [['Jupiter', 'Magnitude of -2.7', 'Surface temp of -234°F', 'Between 4.2 and 6.2 AU from earth', '5.2 AU from sun'], 
           ['Saturn', 'Magnitude of -0.55', 'Surface temp of -288°F', '7 AU from earth', '9.5 AU from sun'],
           ['Venus', 'Magnitude of -4.6', 'Surface temp of 900°F', 'Around 0.43 AU from earth', '0.72 AU from sun'],
           ['Mars', 'Magnitude of 1.76', 'Surface temp of between 70° and -225°F', '2.23 AU from Earth', '1.5 AU from the sun'],
           ['Mercury', 'mag', 'temp', 'distearth', 'distsun'],
           ['Neptune', 'mag', 'temp', 'distearth', 'distsun'],
           ['Uranus', 'mag', 'temp', 'distearth', 'distsun']]
# Make lists into actual data frame
df = pd.DataFrame(objects, columns=["Objects", "Magnitude", 'Surface Temp','Distance from Earth', 'Distance from sun'])

# Ask for the object the user wants to find
ObjectOfChoice = str(input('What is your chosen object?'))
# Queary data frame using pandas
Search = df.query("Objects == @ObjectOfChoice")
# Output
print(Search)