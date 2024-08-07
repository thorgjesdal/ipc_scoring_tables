"""
Function to calculate points according to the IPC scoring tables (Raza scores)
Reference: https://www.paralympic.org/athletics/technical-information

TODO:
"""
import math
import re

track_events = ("100", "200", "400", "800", "1500", "5000", "10000" )
field_events = ("SP", "DT", "JT", "OT", "HJ", "LJ", "TJ" )


#===== ( parameters block  )=====
# Parameters for ipc scoring tables
# This block generated by
#   ipc_read_parameters.py '2023 - 2024 World Para Athletics Point Scores Calculator Track Events.xlsx' '2023 - 2024 World Para Athletics Point Scores Calculator Field Events.xlsx' 
# Do not edit this block, re-run script instead...

coefficients = {   '100': {   'F': {   'T11': (1200, 9.099032, 128.1699),
                        'T12': (1200, 9.099032, 127.3569),
                        'T13': (1200, 9.099032, 127.3462),
                        'T33': (1200, 8.9427, 209.3413),
                        'T34': (1200, 8.9427, 182.2832),
                        'T35': (1200, 9.099032, 153.7799),
                        'T36': (1200, 9.099032, 151.8185),
                        'T37': (1200, 9.099032, 143.8613),
                        'T38': (1200, 9.099032, 137.3275),
                        'T42': (1200, 9.099032, 158.6593),
                        'T43': (1200, 9.099032, 133.5111),
                        'T44': (1200, 9.099032, 136.7319),
                        'T45': (1200, 9.099032, 131.709),
                        'T46': (1200, 9.099032, 131.709),
                        'T47': (1200, 9.099032, 131.709),
                        'T51': (1200, 8.9427, 271.4804),
                        'T52': (1200, 8.9427, 195.7223),
                        'T53': (1200, 8.9427, 171.0271),
                        'T54': (1200, 8.9427, 170.3062),
                        'T61': (1200, 9.099032, 158.6593),
                        'T62': (1200, 9.099032, 133.5111),
                        'T63': (1200, 9.099032, 158.6593),
                        'T64': (1200, 9.099032, 136.7319)},
               'M': {   'T11': (1200, 10.896562, 137.9354),
                        'T12': (1200, 10.896562, 135.3659),
                        'T13': (1200, 10.896562, 134.4742),
                        'T33': (1200, 9.147912, 177.0724),
                        'T34': (1200, 9.147912, 161.8983),
                        'T35': (1200, 10.896562, 152.7867),
                        'T36': (1200, 10.896562, 149.041),
                        'T37': (1200, 10.896562, 143.623),
                        'T38': (1200, 10.896562, 138.4066),
                        'T42': (1200, 10.896562, 150.4595),
                        'T43': (1200, 10.896562, 133.999),
                        'T44': (1200, 10.896562, 137.468),
                        'T45': (1200, 10.896562, 135.3345),
                        'T46': (1200, 10.896562, 135.3345),
                        'T47': (1200, 10.896562, 135.3345),
                        'T51': (1200, 9.147912, 214.3629),
                        'T52': (1200, 9.147912, 179.7747),
                        'T53': (1200, 9.147912, 156.2475),
                        'T54': (1200, 9.147912, 149.0792),
                        'T61': (1200, 10.896562, 150.4595),
                        'T62': (1200, 10.896562, 133.999),
                        'T63': (1200, 10.896562, 150.4595),
                        'T64': (1200, 10.896562, 137.468)}},
    '10000': {   'M': {   'T11': (1200, 12.100056, 26758.1928),
                          'T12': (1200, 12.100056, 25388.4975),
                          'T13': (1200, 12.100056, 25996.1231),
                          'T20': (1200, 12.100056, 25152.21),
                          'T45': (1200, 12.100056, 26348.9847),
                          'T46': (1200, 12.100056, 26348.9847),
                          'T47': (1200, 12.100056, 26348.9847),
                          'T51': (1200, 9.006902, 21964.1753),
                          'T52': (1200, 9.006902, 16981.1636),
                          'T53': (1200, 9.006902, 12565.3126),
                          'T54': (1200, 9.006902, 12565.3126)}},
    '1500': {   'F': {   'T11': (1200, 8.382513, 2750.1674),
                         'T12': (1200, 8.382513, 2736.4016),
                         'T13': (1200, 8.382513, 2552.5041),
                         'T20': (1200, 8.382513, 2637.9459),
                         'T33': (1200, 6.672396, 2524.86),
                         'T34': (1200, 6.672396, 1817.3279),
                         'T53': (1200, 6.672396, 1589.7308),
                         'T54': (1200, 6.672396, 1589.7308)},
                'M': {   'T11': (1200, 10.422742, 2903.6451),
                         'T12': (1200, 10.422742, 2737.6817),
                         'T13': (1200, 10.422742, 2735.0023),
                         'T20': (1200, 10.422742, 2771.9829),
                         'T33': (1200, 7.215967, 2347.6413),
                         'T34': (1200, 7.215967, 1633.5639),
                         'T35': (1200, 10.422742, 3615.7945),
                         'T36': (1200, 10.422742, 3289.7321),
                         'T37': (1200, 10.422742, 2958.6169),
                         'T38': (1200, 10.422742, 2845.2051),
                         'T44': (1200, 10.422742, 3306.3109),
                         'T45': (1200, 10.422742, 2762.2923),
                         'T46': (1200, 10.422742, 2762.2923),
                         'T47': (1200, 10.422742, 2762.2923),
                         'T51': (1200, 7.215967, 2759.3469),
                         'T52': (1200, 7.215967, 1903.6858),
                         'T53': (1200, 7.215967, 1531.5005),
                         'T54': (1200, 7.215967, 1531.5005),
                         'T64': (1200, 10.422742, 3306.3109)}},
    '200': {   'F': {   'T11': (1200, 8.768913, 256.089),
                        'T12': (1200, 8.768913, 249.6571),
                        'T13': (1200, 8.768913, 256.1882),
                        'T33': (1200, 8.115445, 342.0957),
                        'T34': (1200, 8.115445, 300.5913),
                        'T35': (1200, 8.768913, 302.6947),
                        'T36': (1200, 8.768913, 307.8213),
                        'T37': (1200, 8.768913, 290.4197),
                        'T38': (1200, 8.768913, 277.3385),
                        'T42': (1200, 8.768913, 331.3547),
                        'T43': (1200, 8.768913, 268.8515),
                        'T44': (1200, 8.768913, 273.4824),
                        'T45': (1200, 8.768913, 261.3229),
                        'T46': (1200, 8.768913, 261.3229),
                        'T47': (1200, 8.768913, 261.3229),
                        'T51': (1200, 8.115445, 492.7079),
                        'T52': (1200, 8.115445, 319.8409),
                        'T53': (1200, 8.115445, 278.7572),
                        'T54': (1200, 8.115445, 280.5929),
                        'T61': (1200, 8.768913, 331.3547),
                        'T62': (1200, 8.768913, 268.8515),
                        'T63': (1200, 8.768913, 331.3547),
                        'T64': (1200, 8.768913, 273.4824)},
               'M': {   'T11': (1200, 10.300239, 267.1022),
                        'T12': (1200, 10.300239, 262.6882),
                        'T13': (1200, 10.300239, 260.8471),
                        'T33': (1200, 8.665928, 299.0305),
                        'T34': (1200, 8.665928, 274.0923),
                        'T35': (1200, 10.300239, 297.7386),
                        'T36': (1200, 10.300239, 285.1891),
                        'T37': (1200, 10.300239, 276.617),
                        'T38': (1200, 10.300239, 270.1177),
                        'T42': (1200, 10.300239, 286.6949),
                        'T43': (1200, 10.300239, 247.6128),
                        'T44': (1200, 10.300239, 264.6043),
                        'T45': (1200, 10.300239, 260.8004),
                        'T46': (1200, 10.300239, 260.8004),
                        'T47': (1200, 10.300239, 260.8004),
                        'T51': (1200, 8.665928, 376.2603),
                        'T52': (1200, 8.665928, 313.1513),
                        'T53': (1200, 8.665928, 263.1792),
                        'T54': (1200, 8.665928, 252.1763),
                        'T61': (1200, 10.300239, 286.6949),
                        'T62': (1200, 10.300239, 247.6128),
                        'T63': (1200, 10.300239, 286.6949),
                        'T64': (1200, 10.300239, 264.6043)}},
    '400': {   'F': {   'T11': (1200, 8.662912, 582.9803),
                        'T12': (1200, 8.662912, 567.4744),
                        'T13': (1200, 8.662912, 559.6729),
                        'T20': (1200, 8.662912, 587.4245),
                        'T33': (1200, 7.193309, 640.3499),
                        'T34': (1200, 7.193309, 505.8784),
                        'T35': (1200, 8.662912, 760.9468),
                        'T36': (1200, 8.662912, 716.1657),
                        'T37': (1200, 8.662912, 643.5793),
                        'T38': (1200, 8.662912, 624.0723),
                        'T43': (1200, 8.662912, 607.895),
                        'T44': (1200, 8.662912, 586.324),
                        'T45': (1200, 8.662912, 583.172),
                        'T46': (1200, 8.662912, 583.172),
                        'T47': (1200, 8.662912, 583.172),
                        'T52': (1200, 7.193309, 572.567),
                        'T53': (1200, 7.193309, 474.2046),
                        'T54': (1200, 7.193309, 467.685),
                        'T62': (1200, 8.662912, 607.895),
                        'T64': (1200, 8.662912, 586.324)},
               'M': {   'T11': (1200, 9.772637, 566.9777),
                        'T12': (1200, 9.772637, 550.5386),
                        'T13': (1200, 9.772637, 547.1738),
                        'T20': (1200, 9.772637, 546.8569),
                        'T33': (1200, 8.374964, 579.5538),
                        'T34': (1200, 8.374964, 492.3988),
                        'T35': (1200, 9.772637, 676.5108),
                        'T36': (1200, 9.772637, 609.1482),
                        'T37': (1200, 9.772637, 585.6731),
                        'T38': (1200, 9.772637, 576.3879),
                        'T42': (1200, 9.772637, 555.1883),
                        'T43': (1200, 9.772637, 518.2578),
                        'T44': (1200, 9.772637, 584.1968),
                        'T45': (1200, 9.772637, 552.1736),
                        'T46': (1200, 9.772637, 552.1736),
                        'T47': (1200, 9.772637, 552.1736),
                        'T51': (1200, 8.374964, 765.5402),
                        'T52': (1200, 8.374964, 574.87),
                        'T53': (1200, 8.374964, 477.7334),
                        'T54': (1200, 8.374964, 455.7915),
                        'T61': (1200, 9.772637, 555.1883),
                        'T62': (1200, 9.772637, 518.2578),
                        'T63': (1200, 9.772637, 555.1883),
                        'T64': (1200, 9.772637, 584.1968)}},
    '5000': {   'F': {   'T11': (1200, 10.618652, 14087.8965),
                         'T12': (1200, 10.618652, 13301.7839),
                         'T13': (1200, 10.618652, 13314.4736),
                         'T20': (1200, 10.618652, 12721.9597),
                         'T53': (1200, 9.620434, 7321.8723),
                         'T54': (1200, 9.620434, 7321.8723)},
                'M': {   'T11': (1200, 10.279372, 10811.9086),
                         'T12': (1200, 10.279372, 10219.0479),
                         'T13': (1200, 10.279372, 10292.2694),
                         'T20': (1200, 10.279372, 10345.2722),
                         'T34': (1200, 8.157716, 6480.4159),
                         'T37': (1200, 10.279372, 10631.9123),
                         'T38': (1200, 10.279372, 10325.6189),
                         'T45': (1200, 10.279372, 10154.5859),
                         'T46': (1200, 10.279372, 10154.5859),
                         'T47': (1200, 10.279372, 10154.5859),
                         'T51': (1200, 8.157716, 10364.6454),
                         'T52': (1200, 8.157716, 7241.4068),
                         'T53': (1200, 8.157716, 5680.5855),
                         'T54': (1200, 8.157716, 5680.5855)}},
    '800': {   'F': {   'T11': (1200, 8.067102, 1318.6897),
                        'T12': (1200, 8.067102, 1305.9325),
                        'T13': (1200, 8.067102, 1352.261),
                        'T20': (1200, 8.067102, 1313.4743),
                        'T33': (1200, 6.645036, 1216.2248),
                        'T34': (1200, 6.645036, 944.0037),
                        'T35': (1200, 8.067102, 2077.3616),
                        'T36': (1200, 8.067102, 1812.7115),
                        'T37': (1200, 8.067102, 1581.261),
                        'T38': (1200, 8.067102, 1523.6742),
                        'T45': (1200, 8.067102, 1343.0059),
                        'T46': (1200, 8.067102, 1343.0059),
                        'T47': (1200, 8.067102, 1343.0059),
                        'T52': (1200, 6.645036, 1058.6206),
                        'T53': (1200, 6.645036, 840.8595),
                        'T54': (1200, 6.645036, 847.5742)},
               'M': {   'T11': (1200, 10.600322, 1450.8274),
                        'T12': (1200, 10.600322, 1400.5677),
                        'T13': (1200, 10.600322, 1366.0026),
                        'T20': (1200, 10.600322, 1386.7733),
                        'T33': (1200, 7.677374, 1099.2183),
                        'T34': (1200, 7.677374, 889.5612),
                        'T35': (1200, 10.600322, 1712.6638),
                        'T36': (1200, 10.600322, 1533.0871),
                        'T37': (1200, 10.600322, 1466.1153),
                        'T38': (1200, 10.600322, 1434.3111),
                        'T44': (1200, 10.600322, 1602.6259),
                        'T45': (1200, 10.600322, 1386.5961),
                        'T46': (1200, 10.600322, 1386.5961),
                        'T47': (1200, 10.600322, 1386.5961),
                        'T51': (1200, 7.677374, 1540.1551),
                        'T52': (1200, 7.677374, 1053.9999),
                        'T53': (1200, 7.677374, 874.0824),
                        'T54': (1200, 7.677374, 838.6512),
                        'T64': (1200, 10.600322, 1602.6259)}},
    'DT': {   'F': {   'F11': (1200, 2.789979, 0.108822),
                       'F12': (1200, 2.789979, 0.101661),
                       'F13': (1200, 2.789979, 0.14403),
                       'F32': (1200, 2.520235, 0.334859),
                       'F33': (1200, 2.520235, 0.268455),
                       'F34': (1200, 2.520235, 0.180737),
                       'F35': (1200, 2.789979, 0.148584),
                       'F36': (1200, 2.789979, 0.164245),
                       'F37': (1200, 2.789979, 0.13023),
                       'F38': (1200, 2.789979, 0.124167),
                       'F40': (1200, 2.789979, 0.186051),
                       'F41': (1200, 2.789979, 0.135076),
                       'F42': (1200, 2.789979, 0.141948),
                       'F43': (1200, 2.789979, 0.111359),
                       'F44': (1200, 2.789979, 0.111359),
                       'F46': (1200, 2.789979, 0.120476),
                       'F51': (1200, 2.520235, 0.273653),
                       'F52': (1200, 2.520235, 0.269887),
                       'F53': (1200, 2.520235, 0.31603),
                       'F54': (1200, 2.520235, 0.225527),
                       'F55': (1200, 2.520235, 0.164896),
                       'F56': (1200, 2.520235, 0.176232),
                       'F57': (1200, 2.520235, 0.128307),
                       'F61': (1200, 2.789979, 0.141948),
                       'F62': (1200, 2.789979, 0.111359),
                       'F63': (1200, 2.789979, 0.141948),
                       'F64': (1200, 2.789979, 0.111359)},
              'M': {   'F11': (1200, 3.184645, 0.114962),
                       'F12': (1200, 3.184645, 0.100385),
                       'F13': (1200, 3.184645, 0.11288),
                       'F32': (1200, 2.563306, 0.193835),
                       'F33': (1200, 2.563306, 0.129567),
                       'F34': (1200, 2.563306, 0.108878),
                       'F35': (1200, 3.184645, 0.102935),
                       'F36': (1200, 3.184645, 0.115334),
                       'F37': (1200, 3.184645, 0.091331),
                       'F38': (1200, 3.184645, 0.104984),
                       'F40': (1200, 3.184645, 0.182583),
                       'F41': (1200, 3.184645, 0.118496),
                       'F42': (1200, 3.184645, 0.104589),
                       'F43': (1200, 3.184645, 0.080433),
                       'F44': (1200, 3.184645, 0.080433),
                       'F46': (1200, 3.184645, 0.096802),
                       'F51': (1200, 2.563306, 0.348628),
                       'F52': (1200, 2.563306, 0.183726),
                       'F53': (1200, 2.563306, 0.163415),
                       'F54': (1200, 2.563306, 0.138871),
                       'F55': (1200, 2.563306, 0.112711),
                       'F56': (1200, 2.563306, 0.094936),
                       'F57': (1200, 2.563306, 0.087506),
                       'F61': (1200, 3.184645, 0.104589),
                       'F62': (1200, 3.184645, 0.080433),
                       'F63': (1200, 3.184645, 0.104589),
                       'F64': (1200, 3.184645, 0.080433)}},
    'HJ': {   'F': {   'T43': (1200, 6.848669, 6.071675),
                       'T44': (1200, 6.848669, 6.071675),
                       'T62': (1200, 6.848669, 6.071675),
                       'T64': (1200, 6.848669, 6.071675)},
              'M': {   'T11': (1200, 8.002133, 6.258664),
                       'T12': (1200, 8.002133, 4.908225),
                       'T13': (1200, 8.002133, 4.673512),
                       'T42': (1200, 8.002133, 5.021741),
                       'T43': (1200, 8.002133, 4.347138),
                       'T44': (1200, 8.002133, 4.347138),
                       'T45': (1200, 8.002133, 4.66292),
                       'T46': (1200, 8.002133, 4.66292),
                       'T47': (1200, 8.002133, 4.66292),
                       'T61': (1200, 8.002133, 5.021741),
                       'T62': (1200, 8.002133, 4.347138),
                       'T63': (1200, 8.002133, 5.021741),
                       'T64': (1200, 8.002133, 4.347138)}},
    'JT': {   'F': {   'F11': (1200, 2.359204, 0.149057),
                       'F12': (1200, 2.359204, 0.090873),
                       'F13': (1200, 2.359204, 0.093556),
                       'F33': (1200, 2.747436, 0.304073),
                       'F34': (1200, 2.747436, 0.209437),
                       'F35': (1200, 2.359204, 0.154005),
                       'F36': (1200, 2.359204, 0.136406),
                       'F37': (1200, 2.359204, 0.129252),
                       'F38': (1200, 2.359204, 0.128871),
                       'F40': (1200, 2.359204, 0.168379),
                       'F41': (1200, 2.359204, 0.156565),
                       'F42': (1200, 2.359204, 0.129886),
                       'F43': (1200, 2.359204, 0.101853),
                       'F44': (1200, 2.359204, 0.101853),
                       'F46': (1200, 2.359204, 0.093484),
                       'F52': (1200, 2.747436, 0.344263),
                       'F53': (1200, 2.747436, 0.363511),
                       'F54': (1200, 2.747436, 0.231351),
                       'F55': (1200, 2.747436, 0.224832),
                       'F56': (1200, 2.747436, 0.187987),
                       'F57': (1200, 2.747436, 0.182078),
                       'F61': (1200, 2.359204, 0.129886),
                       'F62': (1200, 2.359204, 0.101853),
                       'F63': (1200, 2.359204, 0.129886),
                       'F64': (1200, 2.359204, 0.101853)},
              'M': {   'F11': (1200, 2.815418, 0.090486),
                       'F12': (1200, 2.815418, 0.06912),
                       'F13': (1200, 2.815418, 0.063234),
                       'F33': (1200, 2.483643, 0.168063),
                       'F34': (1200, 2.483643, 0.115365),
                       'F35': (1200, 2.815418, 0.112773),
                       'F36': (1200, 2.815418, 0.099146),
                       'F37': (1200, 2.815418, 0.090962),
                       'F38': (1200, 2.815418, 0.080163),
                       'F40': (1200, 2.815418, 0.117342),
                       'F41': (1200, 2.815418, 0.098881),
                       'F42': (1200, 2.815418, 0.084739),
                       'F43': (1200, 2.815418, 0.072608),
                       'F44': (1200, 2.815418, 0.072608),
                       'F46': (1200, 2.815418, 0.072072),
                       'F52': (1200, 2.483643, 0.226643),
                       'F53': (1200, 2.483643, 0.188055),
                       'F54': (1200, 2.483643, 0.139535),
                       'F55': (1200, 2.483643, 0.133216),
                       'F56': (1200, 2.483643, 0.125034),
                       'F57': (1200, 2.483643, 0.090551),
                       'F61': (1200, 2.815418, 0.084739),
                       'F62': (1200, 2.815418, 0.072608),
                       'F63': (1200, 2.815418, 0.084739),
                       'F64': (1200, 2.815418, 0.072608)}},
    'LJ': {   'F': {   'T11': (1200, 5.733964, 1.449755),
                       'T12': (1200, 5.733964, 1.227256),
                       'T13': (1200, 5.733964, 1.303181),
                       'T20': (1200, 5.733964, 1.300629),
                       'T35': (1200, 5.733964, 2.162317),
                       'T36': (1200, 5.733964, 1.679033),
                       'T37': (1200, 5.733964, 1.542668),
                       'T38': (1200, 5.733964, 1.468023),
                       'T42': (1200, 5.733964, 1.569691),
                       'T43': (1200, 5.733964, 1.235944),
                       'T44': (1200, 5.733964, 1.235944),
                       'T45': (1200, 5.733964, 1.258078),
                       'T46': (1200, 5.733964, 1.258078),
                       'T47': (1200, 5.733964, 1.258078),
                       'T61': (1200, 5.733964, 1.569691),
                       'T62': (1200, 5.733964, 1.235944),
                       'T63': (1200, 5.733964, 1.569691),
                       'T64': (1200, 5.733964, 1.235944)},
              'M': {   'T11': (1200, '5.617298', '1.085856'),
                       'T12': (1200, '5.617298', '0.984418'),
                       'T13': (1200, '5.617298', '1.010187'),
                       'T20': (1200, '5.617298', '1.000531'),
                       'T35': (1200, '5.617298', '1.414294'),
                       'T36': (1200, '5.617298', '1.241787'),
                       'T37': (1200, '5.617298', '1.121570'),
                       'T38': (1200, '5.617298', '1.069403'),
                       'T42': (1200, '5.617298', '1.063034'),
                       'T43': (1200, 5.617298, 0.978067),
                       'T44': (1200, 5.617298, 0.978067),
                       'T45': (1200, 5.617298, 1.018154),
                       'T46': (1200, 5.617298, 1.018154),
                       'T47': (1200, 5.617298, 1.018154),
                       'T61': (1200, 5.617298, 1.063034),
                       'T62': (1200, 5.617298, 0.978067),
                       'T63': (1200, 5.617298, 1.063034),
                       'T64': (1200, 5.617298, 0.978067)}},
    'OT': {   'F': {   'F31': (1200, 2.759481, 0.208391),
                       'F32': (1200, 2.759481, 0.181127),
                       'F51': (1200, 2.759481, 0.173829)},
              'M': {   'F31': (1200, 2.920325, 0.129476),
                       'F32': (1200, 2.920325, 0.123116),
                       'F51': (1200, 2.920325, 0.140613)}},
    'SP': {   'F': {   'F11': (1200, 3.004326, 0.317573),
                       'F12': (1200, 3.004326, 0.338751),
                       'F13': (1200, 3.004326, 0.367791),
                       'F20': (1200, 3.004326, 0.329094),
                       'F32': (1200, 3.000108, 0.645688),
                       'F33': (1200, 3.000108, 0.662169),
                       'F34': (1200, 3.000108, 0.540628),
                       'F35': (1200, 3.004326, 0.392092),
                       'F36': (1200, 3.004326, 0.419717),
                       'F37': (1200, 3.004326, 0.386492),
                       'F38': (1200, 3.004326, 0.413529),
                       'F40': (1200, 3.004326, 0.538936),
                       'F41': (1200, 3.004326, 0.478304),
                       'F42': (1200, 3.004326, 0.457319),
                       'F43': (1200, 3.004326, 0.346917),
                       'F44': (1200, 3.004326, 0.346917),
                       'F46': (1200, 3.004326, 0.38847),
                       'F52': (1200, 3.000108, 0.85535),
                       'F53': (1200, 3.000108, 0.907876),
                       'F54': (1200, 3.000108, 0.589267),
                       'F55': (1200, 3.000108, 0.581977),
                       'F56': (1200, 3.000108, 0.546548),
                       'F57': (1200, 3.000108, 0.428584),
                       'F61': (1200, 3.004326, 0.457319),
                       'F62': (1200, 3.004326, 0.346917),
                       'F63': (1200, 3.004326, 0.457319),
                       'F64': (1200, 3.004326, 0.346917)},
              'M': {   'F11': (1200, 3.76435, 0.400521),
                       'F12': (1200, 3.76435, 0.323428),
                       'F13': (1200, 3.76435, 0.409783),
                       'F20': (1200, 3.76435, 0.320623),
                       'F32': (1200, 3.085696, 0.423952),
                       'F33': (1200, 3.085696, 0.402777),
                       'F34': (1200, 3.085696, 0.386976),
                       'F35': (1200, 3.76435, 0.331104),
                       'F36': (1200, 3.76435, 0.356697),
                       'F37': (1200, 3.76435, 0.363811),
                       'F38': (1200, 3.76435, 0.347705),
                       'F40': (1200, 3.76435, 0.466102),
                       'F41': (1200, 3.76435, 0.401361),
                       'F42': (1200, 3.76435, 0.357342),
                       'F43': (1200, 3.76435, 0.336711),
                       'F44': (1200, 3.76435, 0.336711),
                       'F46': (1200, 3.76435, 0.329574),
                       'F52': (1200, 3.085696, 0.457065),
                       'F53': (1200, 3.085696, 0.533492),
                       'F54': (1200, 3.085696, 0.470135),
                       'F55': (1200, 3.085696, 0.394391),
                       'F56': (1200, 3.085696, 0.396213),
                       'F57': (1200, 3.085696, 0.330364),
                       'F61': (1200, 3.76435, 0.357342),
                       'F62': (1200, 3.76435, 0.336711),
                       'F63': (1200, 3.76435, 0.357342),
                       'F64': (1200, 3.76435, 0.336711)}},
    'TJ': {   'F': {   'T20': (1200, 8.225305, 0.785035),
                       'T46': (1200, 8.225305, 0.952063)},
              'M': {   'T11': (1200, 10.560785, 0.940824),
                       'T12': (1200, 10.560785, 0.820422),
                       'T13': (1200, 10.560785, 0.893248),
                       'T20': (1200, 10.560785, 0.844493),
                       'T45': (1200, 10.560785, 0.845429),
                       'T46': (1200, 10.560785, 0.845429),
                       'T47': (1200, 10.560785, 0.845429)}}}
#===== ( end parameters block  )=====

def secs(x):
    print(x)
    secs = -1
    secpat = '(\d\d[,.]\d?\d)'
    minsecpat = '(\d?\d)[:.,](\d\d[,.]\d?\d)'
    x = f'{x}'
#   match1 = re.match(minsecpat,x)
    match1 = re.search(minsecpat,x)
    match2 = re.match(secpat,x)
    print(match1)
    if match1:
        m = match1.group(1)
        s = match1.group(2).replace(',','.')
        print(m,s)
        secs =  60.*int(m) + float(s)
    elif match2:
        secs = float( match2.group(1).replace(',','.') )
    return secs

def ipc_score(event, gender, cat, performance, youth=None, custom=None):
    p = performance 

    if custom == 'NOR':
        if event == '60':
            event = '100'
            p = float(p)
            p *= 1.667

        """
        if cat == 'RR1':
            if gender == 'F':
                if event == '100':
                    cat = 'T51'
                elif event == '1500':
                    cat = 'T12'
                    mm, ss = p.split(':')
                    mm = int(mm)-4
                    p = f'{mm}:{ss}'
        elif cat == 'RR2':
            if gender == 'F':
                if event == '100':
                    cat = 'T53'
                elif event == '1500':
                    cat = 'T34'
                    mm, ss = p.split(':')
                    mm = int(mm)-3
                    p = f'{mm}:{ss}'
            elif gender == 'M':
                if event == '100':
                    cat = 'T52'
                elif event == '1500':
                    cat = 'T11'
                    gender = 'F'
        elif cat == 'RR3':
            if gender == 'F':
                if event == '100':
                    cat = 'T53'
                elif event == '1500':
                    cat = 'T51'
                    gender = 'M'
        """
    a = coefficients[event][gender][cat][0]
    b = float(coefficients[event][gender][cat][1])
    c = float(coefficients[event][gender][cat][2])


    print(a,b,c)
    print(type(a),type(b),type(c))
    if event in track_events:
        # convert hh:mm:ss.dd format to seconds
        #p = sum(float(x) * 60 ** i for i, x in enumerate(reversed(f'{p}'.split(':'))))
        p = secs(p)
        if youth not in (None, False):
            c *= 1.16
        print(p)
        score = a*math.exp( -math.exp(b-c/p) )
    elif event in field_events:
        if youth not in (None, False):
            c /= 0.83
        p = float(p)
        score = a*math.exp( -math.exp(b-c*p) )
    else:
        score = -1

    score = math.floor(score)
    return score

