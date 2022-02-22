import math

track_events = ("100", "200", "400", "800", "1500", "5000", "10000" )
field_events = ("SP", "DT", "JT", "OT", "HJ", "LJ", "TJ" )

coefficients = { "100" : { "M" : { "T11" : ( 1200, 11.068111, 140.2461) } } }

def ipc_score(event, gender, cat, performance, youth = None, custom = None):
    p = performance 

    a = coefficients[event][gender][cat][0]
    b = coefficients[event][gender][cat][1]
    c = coefficients[event][gender][cat][2]

    #print( a,b,c )
    if event in track_events:
        score = a*math.exp( -math.exp(b-c/p) )
    elif event in field_events:
        score = a*math.exp( -math.exp(b-c*p) )
    else:
        score = -1

    score = math.floor(score)
    return score

times = [10.43, 10.98, 12.12, 13.89, 15.99 ]

for time in times:
    print ( time, ipc_score("100", "M", "T11", time ) )
    
"""
# code example convert hh:mm:ss format to secs
ts = '1:23:45'
secs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(ts.split(':'))))
print(secs)
"""
