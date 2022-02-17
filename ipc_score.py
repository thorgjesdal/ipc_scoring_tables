import math
import matplotlib.pyplot as plt
import numpy as np

track_events = ("100", "200", "400", "800", "1500", "5000", "10000" )
field_events = ("SP", "DT", "JT", "OT", "HJ", "LJ", "TJ" )

coefficients = { "100" : { "M" : { "T11" : ( 1200, 11.068111, 140.2461) } } }

def ipc_score(event, gender, cat, performance, youth = None):
    p = performance 

    a = coefficients[event][gender][cat][0]
    b = coefficients[event][gender][cat][1]
    c = coefficients[event][gender][cat][2]

    #print( a,b,c )
    if event in track_events:
        score = a*math.exp( -math.exp(b-c/p) )
        print (score)
    elif event in field_events:
        score = a*math.exp( -math.exp(b-c*p) )
    else:
        score = -1

    score = math.floor(score)
    return score

watimes = [10.43, 10.98, 11.51, 12.12, 13.00, 13.89, 15.99 ]
wa = [1063, 892, 742, 586, 394, 238, 25]

times = np.linspace(10.0,16.0, 101)
ipc = []

for time in times:
    ipc.append(ipc_score("100", "M", "T11", time ) )
    print ( time, ipc_score("100", "M", "T11", time ) )
    



fig, ax = plt.subplots()
plt.plot(times, ipc, label="ipc T41")
plt.plot(watimes, wa, 'x', label="wa")
plt.legend()
plt.show()



"""
# code example convert hh:mm:ss format to secs
ts = '1:23:45'
secs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(ts.split(':'))))
print(secs)
"""
