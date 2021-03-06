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
#   ipc_read_parameters.py '2021 World Para Athletics Point Scores Calculator Track Events.xlsx' '2021 World Para Athletics Point Scores Calculator Field Events.xlsx' 
# Do not edit this block, re-run script instead...

coefficients = {   '100': {   'F': {   'T11': (1200, '9.269555', '130.2561'),
                        'T12': (1200, '9.269555', '129.7351'),
                        'T13': (1200, '9.269555', '129.9139'),
                        'T33': (1200, '9.088369', '212.1653'),
                        'T34': (1200, '9.088369', '184.8522'),
                        'T35': (1200, '9.269555', '157.3346'),
                        'T36': (1200, '9.269555', '154.9465'),
                        'T37': (1200, '9.269555', '146.6624'),
                        'T38': (1200, '9.269555', '140.9336'),
                        'T42': (1200, '9.269555', '164.0464'),
                        'T43': (1200, '9.269555', '137.5442'),
                        'T44': (1200, '9.269555', '139.7037'),
                        'T45': (1200, '9.269555', '134.1101'),
                        'T46': (1200, '9.269555', '134.1101'),
                        'T47': (1200, '9.269555', '134.1101'),
                        'T51': (1200, '9.088369', '279.6338'),
                        'T52': (1200, '9.088369', '198.9297'),
                        'T53': (1200, '9.088369', '174.6179'),
                        'T54': (1200, '9.088369', '173.5207'),
                        'T61': (1200, '9.269555', '164.0464'),
                        'T62': (1200, '9.269555', '137.5442'),
                        'T63': (1200, '9.269555', '164.0464'),
                        'T64': (1200, '9.269555', '139.7037')},
               'M': {   'T11': (1200, '11.068111', '140.2461'),
                        'T12': (1200, '11.068111', '137.9835'),
                        'T13': (1200, '11.068111', '137.0812'),
                        'T33': (1200, '9.194202', '177.4442'),
                        'T34': (1200, '9.194202', '163.5178'),
                        'T35': (1200, '11.068111', '155.1518'),
                        'T36': (1200, '11.068111', '151.7484'),
                        'T37': (1200, '11.068111', '146.0228'),
                        'T38': (1200, '11.068111', '140.5502'),
                        'T42': (1200, '11.068111', '152.3767'),
                        'T43': (1200, '11.068111', '136.3347'),
                        'T44': (1200, '11.068111', '140.0639'),
                        'T45': (1200, '11.068111', '137.6940'),
                        'T46': (1200, '11.068111', '137.6940'),
                        'T47': (1200, '11.068111', '137.6940'),
                        'T51': (1200, '9.194202', '217.4076'),
                        'T52': (1200, '9.194202', '181.4646'),
                        'T53': (1200, '9.194202', '157.0477'),
                        'T54': (1200, '9.194202', '149.8795'),
                        'T61': (1200, '11.068111', '152.3767'),
                        'T62': (1200, '11.068111', '136.3347'),
                        'T63': (1200, '11.068111', '152.3767'),
                        'T64': (1200, '11.068111', '140.0639')}},
    '10000': {   'M': {   'T11': (1200, '12.433239', '27587.7283'),
                          'T12': (1200, '12.433239', '26000.1799'),
                          'T13': (1200, '12.433239', '26623.6722'),
                          'T20': (1200, '12.433239', '25967.8512'),
                          'T45': (1200, '12.433239', '26985.0519'),
                          'T46': (1200, '12.433239', '26985.0519'),
                          'T47': (1200, '12.433239', '26985.0519'),
                          'T51': (1200, '9.136570', '22230.1279'),
                          'T52': (1200, '9.136570', '17186.7796'),
                          'T53': (1200, '9.136570', '12717.3224'),
                          'T54': (1200, '9.136570', '12717.3224')}},
    '1500': {   'F': {   'T11': (1200, '8.782048', '2874.7060'),
                         'T12': (1200, '8.782048', '2835.1876'),
                         'T13': (1200, '8.782048', '2700.8197'),
                         'T20': (1200, '8.782048', '2740.7777'),
                         'T33': (1200, '6.582636', '2484.7836'),
                         'T34': (1200, '6.582636', '1810.5456'),
                         'T53': (1200, '6.582636', '1581.9280'),
                         'T54': (1200, '6.582636', '1581.9280')},
                'M': {   'T11': (1200, '10.669882', '2982.1262'),
                         'T12': (1200, '10.669882', '2800.3143'),
                         'T13': (1200, '10.669882', '2801.3145'),
                         'T20': (1200, '10.669882', '2836.1692'),
                         'T33': (1200, '7.325177', '2343.4720'),
                         'T34': (1200, '7.325177', '1651.2697'),
                         'T36': (1200, '10.669882', '3350.6843'),
                         'T37': (1200, '10.669882', '3028.5630'),
                         'T38': (1200, '10.669882', '2974.5117'),
                         'T44': (1200, '10.669882', '3373.7040'),
                         'T45': (1200, '10.669882', '2815.3488'),
                         'T46': (1200, '10.669882', '2815.3488'),
                         'T47': (1200, '10.669882', '2815.3488'),
                         'T51': (1200, '7.325177', '2792.5243'),
                         'T52': (1200, '7.325177', '1932.6343'),
                         'T53': (1200, '7.325177', '1556.3662'),
                         'T54': (1200, '7.325177', '1556.3662'),
                         'T64': (1200, '10.669882', '3373.7040')}},
    '200': {   'F': {   'T11': (1200, '8.778086', '256.2784'),
                        'T12': (1200, '8.778086', '250.3720'),
                        'T13': (1200, '8.778086', '255.9768'),
                        'T33': (1200, '8.182944', '340.0333'),
                        'T34': (1200, '8.182944', '302.5380'),
                        'T35': (1200, '8.778086', '305.6233'),
                        'T36': (1200, '8.778086', '309.0085'),
                        'T37': (1200, '8.778086', '292.1928'),
                        'T38': (1200, '8.778086', '278.7288'),
                        'T42': (1200, '8.778086', '337.1197'),
                        'T43': (1200, '8.778086', '268.3630'),
                        'T44': (1200, '8.778086', '276.0083'),
                        'T45': (1200, '8.778086', '262.1252'),
                        'T46': (1200, '8.778086', '262.1252'),
                        'T47': (1200, '8.778086', '262.1252'),
                        'T51': (1200, '8.182944', '496.0955'),
                        'T52': (1200, '8.182944', '322.9509'),
                        'T53': (1200, '8.182944', '281.8819'),
                        'T54': (1200, '8.182944', '283.6977'),
                        'T61': (1200, '8.778086', '337.1197'),
                        'T62': (1200, '8.778086', '268.3630'),
                        'T63': (1200, '8.778086', '337.1197'),
                        'T64': (1200, '8.778086', '276.0083')},
               'M': {   'T11': (1200, '10.499603', '272.2701'),
                        'T12': (1200, '10.499603', '267.0938'),
                        'T13': (1200, '10.499603', '265.4746'),
                        'T33': (1200, '8.724769', '298.2493'),
                        'T34': (1200, '8.724769', '276.1954'),
                        'T35': (1200, '10.499603', '301.7648'),
                        'T36': (1200, '10.499603', '290.6072'),
                        'T37': (1200, '10.499603', '282.3351'),
                        'T38': (1200, '10.499603', '274.1177'),
                        'T42': (1200, '10.499603', '292.7373'),
                        'T43': (1200, '10.499603', '251.9053'),
                        'T44': (1200, '10.499603', '270.0442'),
                        'T45': (1200, '10.499603', '265.4624'),
                        'T46': (1200, '10.499603', '265.4624'),
                        'T47': (1200, '10.499603', '265.4624'),
                        'T51': (1200, '8.724769', '382.9885'),
                        'T52': (1200, '8.724769', '315.8300'),
                        'T53': (1200, '8.724769', '265.2052'),
                        'T54': (1200, '8.724769', '253.2448'),
                        'T61': (1200, '10.499603', '292.7373'),
                        'T62': (1200, '10.499603', '251.9053'),
                        'T63': (1200, '10.499603', '292.7373'),
                        'T64': (1200, '10.499603', '270.0442')}},
    '400': {   'F': {   'T11': (1200, '8.634278', '581.7947'),
                        'T12': (1200, '8.634278', '563.7355'),
                        'T13': (1200, '8.634278', '556.8073'),
                        'T20': (1200, '8.634278', '588.4429'),
                        'T33': (1200, '7.254613', '637.5560'),
                        'T34': (1200, '7.254613', '509.0637'),
                        'T35': (1200, '8.634278', '746.7263'),
                        'T36': (1200, '8.634278', '715.2292'),
                        'T37': (1200, '8.634278', '643.2247'),
                        'T38': (1200, '8.634278', '628.6670'),
                        'T43': (1200, '8.634278', '606.2156'),
                        'T44': (1200, '8.634278', '587.5720'),
                        'T45': (1200, '8.634278', '582.6812'),
                        'T46': (1200, '8.634278', '582.6812'),
                        'T47': (1200, '8.634278', '582.6812'),
                        'T52': (1200, '7.254613', '574.8608'),
                        'T53': (1200, '7.254613', '479.1987'),
                        'T54': (1200, '7.254613', '473.3589'),
                        'T62': (1200, '8.634278', '606.2156'),
                        'T64': (1200, '8.634278', '587.5720')},
               'M': {   'T11': (1200, '9.893996', '575.9355'),
                        'T12': (1200, '9.893996', '558.3013'),
                        'T13': (1200, '9.893996', '555.1379'),
                        'T20': (1200, '9.893996', '555.5685'),
                        'T33': (1200, '8.423961', '575.5292'),
                        'T34': (1200, '8.423961', '498.6691'),
                        'T35': (1200, '9.893996', '667.2673'),
                        'T36': (1200, '9.893996', '616.5889'),
                        'T37': (1200, '9.893996', '592.9930'),
                        'T38': (1200, '9.893996', '581.8976'),
                        'T42': (1200, '9.893996', '558.6695'),
                        'T43': (1200, '9.893996', '521.7720'),
                        'T44': (1200, '9.893996', '592.1006'),
                        'T45': (1200, '9.893996', '559.6661'),
                        'T46': (1200, '9.893996', '559.6661'),
                        'T47': (1200, '9.893996', '559.6661'),
                        'T51': (1200, '8.423961', '770.1155'),
                        'T52': (1200, '8.423961', '578.7847'),
                        'T53': (1200, '8.423961', '480.5071'),
                        'T54': (1200, '8.423961', '458.5476'),
                        'T61': (1200, '9.893996', '558.6695'),
                        'T62': (1200, '9.893996', '521.7720'),
                        'T63': (1200, '9.893996', '558.6695'),
                        'T64': (1200, '9.893996', '592.1006')}},
    '5000': {   'F': {   'T11': (1200, '10.376910', '13594.0986'),
                         'T12': (1200, '10.376910', '12966.7399'),
                         'T13': (1200, '10.376910', '13041.6341'),
                         'T20': (1200, '10.376910', '12649.3856'),
                         'T53': (1200, '9.591114', '7343.5375'),
                         'T54': (1200, '9.591114', '7343.5375')},
                'M': {   'T11': (1200, '10.534841', '11102.1235'),
                         'T12': (1200, '10.534841', '10480.5540'),
                         'T13': (1200, '10.534841', '10570.5422'),
                         'T20': (1200, '10.534841', '10617.5723'),
                         'T34': (1200, '8.079747', '6399.5657'),
                         'T37': (1200, '10.534841', '10843.1200'),
                         'T38': (1200, '10.534841', '12476.5598'),
                         'T45': (1200, '10.534841', '10430.6873'),
                         'T46': (1200, '10.534841', '10430.6873'),
                         'T47': (1200, '10.534841', '10430.6873'),
                         'T51': (1200, '8.079747', '10242.3605'),
                         'T52': (1200, '8.079747', '7238.1103'),
                         'T53': (1200, '8.079747', '5638.8959'),
                         'T54': (1200, '8.079747', '5638.8959')}},
    '800': {   'F': {   'T11': (1200, '8.379287', '1364.3071'),
                        'T12': (1200, '8.379287', '1351.3075'),
                        'T13': (1200, '8.379287', '1447.2143'),
                        'T20': (1200, '8.379287', '1352.7715'),
                        'T33': (1200, '6.707592', '1201.0810'),
                        'T34': (1200, '6.707592', '948.6769'),
                        'T35': (1200, '8.379287', '2143.7466'),
                        'T38': (1200, '8.379287', '1356.9491'),
                        'T45': (1200, '8.379287', '1385.9235'),
                        'T46': (1200, '8.379287', '1385.9235'),
                        'T47': (1200, '8.379287', '1385.9235'),
                        'T52': (1200, '6.707592', '1073.5778'),
                        'T53': (1200, '6.707592', '852.6259'),
                        'T54': (1200, '6.707592', '857.5752')},
               'M': {   'T11': (1200, '11.106382', '1513.9717'),
                        'T12': (1200, '11.106382', '1454.8136'),
                        'T13': (1200, '11.106382', '1420.5377'),
                        'T20': (1200, '11.106382', '1450.0024'),
                        'T33': (1200, '7.850796', '1123.0251'),
                        'T34': (1200, '7.850796', '914.9771'),
                        'T35': (1200, '11.106382', '1841.7852'),
                        'T36': (1200, '11.106382', '1598.4396'),
                        'T37': (1200, '11.106382', '1531.1330'),
                        'T38': (1200, '11.106382', '1520.3237'),
                        'T44': (1200, '11.106382', '1704.3699'),
                        'T45': (1200, '11.106382', '1442.7682'),
                        'T46': (1200, '11.106382', '1442.7682'),
                        'T47': (1200, '11.106382', '1442.7682'),
                        'T51': (1200, '7.850796', '1577.2386'),
                        'T52': (1200, '7.850796', '1071.9223'),
                        'T53': (1200, '7.850796', '893.2916'),
                        'T54': (1200, '7.850796', '858.4314'),
                        'T64': (1200, '11.106382', '1704.3699')}},
    'DT': {   'F': {   'F11': (1200, '2.795518', '0.112238'),
                       'F12': (1200, '2.795518', '0.101687'),
                       'F13': (1200, '2.795518', '0.143526'),
                       'F32': (1200, '2.594952', '0.338648'),
                       'F33': (1200, '2.594952', '0.288623'),
                       'F34': (1200, '2.594952', '0.184031'),
                       'F35': (1200, '2.795518', '0.147826'),
                       'F36': (1200, '2.795518', '0.164182'),
                       'F37': (1200, '2.795518', '0.128238'),
                       'F38': (1200, '2.795518', '0.129773'),
                       'F40': (1200, '2.795518', '0.192034'),
                       'F41': (1200, '2.795518', '0.138870'),
                       'F42': (1200, '2.795518', '0.144148'),
                       'F43': (1200, 2.795518, 0.113179),
                       'F44': (1200, 2.795518, 0.113179),
                       'F46': (1200, 2.795518, 0.119009),
                       'F51': (1200, 2.594952, 0.300349),
                       'F52': (1200, 2.594952, 0.287157),
                       'F53': (1200, 2.594952, 0.323687),
                       'F54': (1200, 2.594952, 0.232607),
                       'F55': (1200, 2.594952, 0.174265),
                       'F56': (1200, 2.594952, 0.181243),
                       'F57': (1200, 2.594952, 0.133016),
                       'F61': (1200, 2.795518, 0.144148),
                       'F62': (1200, 2.795518, 0.113179),
                       'F63': (1200, 2.795518, 0.144148),
                       'F64': (1200, 2.795518, 0.113179)},
              'M': {   'F11': (1200, '3.214400', '0.117333'),
                       'F12': (1200, '3.214400', '0.100844'),
                       'F13': (1200, '3.214400', '0.117031'),
                       'F32': (1200, '2.575542', '0.199741'),
                       'F33': (1200, '2.575542', '0.129710'),
                       'F34': (1200, '2.575542', '0.106028'),
                       'F35': (1200, '3.214400', '0.104542'),
                       'F36': (1200, '3.214400', '0.115779'),
                       'F37': (1200, '3.214400', '0.092118'),
                       'F38': (1200, '3.214400', '0.105321'),
                       'F40': (1200, '3.214400', '0.191169'),
                       'F41': (1200, '3.214400', '0.119009'),
                       'F42': (1200, '3.214400', '0.105090'),
                       'F43': (1200, '3.214400', '0.082548'),
                       'F44': (1200, '3.214400', '0.082548'),
                       'F46': (1200, '3.214400', '0.097193'),
                       'F51': (1200, '2.575542', '0.351131'),
                       'F52': (1200, '2.575542', '0.189084'),
                       'F53': (1200, '2.575542', '0.163071'),
                       'F54': (1200, '2.575542', '0.140174'),
                       'F55': (1200, '2.575542', '0.112544'),
                       'F56': (1200, '2.575542', '0.095860'),
                       'F57': (1200, '2.575542', '0.087777'),
                       'F61': (1200, '3.214400', '0.105090'),
                       'F62': (1200, '3.214400', '0.082548'),
                       'F63': (1200, '3.214400', '0.105090'),
                       'F64': (1200, '3.214400', '0.082548')}},
    'HJ': {   'F': {   'T43': (1200, 6.848669, 6.071675),
                       'T44': (1200, 6.848669, 6.071675),
                       'T62': (1200, 6.848669, 6.071675),
                       'T64': (1200, 6.848669, 6.071675)},
              'M': {   'T11': (1200, '7.969966', '6.156595'),
                       'T12': (1200, '7.969966', '4.902126'),
                       'T13': (1200, '7.969966', '4.645444'),
                       'T42': (1200, '7.969966', '5.037708'),
                       'T43': (1200, '7.969966', '4.336886'),
                       'T44': (1200, '7.969966', '4.336886'),
                       'T45': (1200, '7.969966', '4.696753'),
                       'T46': (1200, '7.969966', '4.696753'),
                       'T47': (1200, '7.969966', '4.696753'),
                       'T61': (1200, '7.969966', '5.037708'),
                       'T62': (1200, '7.969966', '4.336886'),
                       'T63': (1200, '7.969966', '5.037708'),
                       'T64': (1200, '7.969966', '4.336886')}},
    'JT': {   'F': {   'F11': (1200, '2.370735', '0.149487'),
                       'F12': (1200, '2.370735', '0.090357'),
                       'F13': (1200, '2.370735', '0.092521'),
                       'F33': (1200, '2.799938', '0.315623'),
                       'F34': (1200, '2.799938', '0.210815'),
                       'F35': (1200, '2.370735', '0.150952'),
                       'F36': (1200, '2.370735', '0.136599'),
                       'F37': (1200, '2.370735', '0.127941'),
                       'F38': (1200, '2.370735', '0.132970'),
                       'F40': (1200, '2.370735', '0.171992'),
                       'F41': (1200, '2.370735', '0.156707'),
                       'F42': (1200, '2.370735', '0.130131'),
                       'F43': (1200, '2.370735', '0.102169'),
                       'F44': (1200, '2.370735', '0.102169'),
                       'F46': (1200, '2.370735', '0.094472'),
                       'F52': (1200, '2.799938', '0.342197'),
                       'F53': (1200, '2.799938', '0.369892'),
                       'F54': (1200, '2.799938', '0.237193'),
                       'F55': (1200, '2.799938', '0.227599'),
                       'F56': (1200, '2.799938', '0.195356'),
                       'F57': (1200, '2.799938', '0.183570'),
                       'F61': (1200, 2.370735, 0.130131),
                       'F62': (1200, 2.370735, 0.102169),
                       'F63': (1200, 2.370735, 0.130131),
                       'F64': (1200, 2.370735, 0.102169)},
              'M': {   'F11': (1200, '2.850732', '0.090920'),
                       'F12': (1200, '2.850732', '0.069477'),
                       'F13': (1200, '2.850732', '0.065660'),
                       'F33': (1200, '2.570877', '0.170348'),
                       'F34': (1200, '2.570877', '0.118437'),
                       'F35': (1200, '2.850732', '0.112493'),
                       'F36': (1200, '2.850732', '0.099929'),
                       'F37': (1200, '2.850732', '0.091298'),
                       'F38': (1200, '2.850732', '0.082154'),
                       'F40': (1200, '2.850732', '0.121894'),
                       'F41': (1200, '2.850732', '0.100213'),
                       'F42': (1200, '2.850732', '0.086120'),
                       'F43': (1200, '2.850732', '0.075036'),
                       'F44': (1200, '2.850732', '0.075036'),
                       'F46': (1200, '2.850732', '0.074932'),
                       'F52': (1200, '2.570877', '0.236144'),
                       'F53': (1200, '2.570877', '0.192203'),
                       'F54': (1200, '2.570877', '0.146067'),
                       'F55': (1200, '2.570877', '0.135299'),
                       'F56': (1200, '2.570877', '0.127423'),
                       'F57': (1200, '2.570877', '0.095340'),
                       'F61': (1200, '2.850732', '0.086120'),
                       'F62': (1200, '2.850732', '0.075036'),
                       'F63': (1200, '2.850732', '0.086120'),
                       'F64': (1200, '2.850732', '0.075036')}},
    'LJ': {   'F': {   'T11': (1200, 5.787447, 1.470529),
                       'T12': (1200, 5.787447, 1.225753),
                       'T13': (1200, 5.787447, 1.305537),
                       'T20': (1200, 5.787447, 1.319424),
                       'T35': (1200, 5.787447, 2.127188),
                       'T36': (1200, 5.787447, 1.697302),
                       'T37': (1200, 5.787447, 1.562599),
                       'T38': (1200, 5.787447, 1.481458),
                       'T42': (1200, 5.787447, 1.635018),
                       'T43': (1200, 5.787447, 1.259742),
                       'T44': (1200, 5.787447, 1.259742),
                       'T45': (1200, 5.787447, 1.273799),
                       'T46': (1200, 5.787447, 1.273799),
                       'T47': (1200, 5.787447, 1.273799),
                       'T61': (1200, 5.787447, 1.635018),
                       'T62': (1200, 5.787447, 1.259742),
                       'T63': (1200, 5.787447, 1.635018),
                       'T64': (1200, 5.787447, 1.259742)},
              'M': {   'T11': (1200, '5.660052', '1.090072'),
                       'T12': (1200, '5.660052', '0.988655'),
                       'T13': (1200, '5.660052', '1.021053'),
                       'T20': (1200, '5.660052', '1.008066'),
                       'T35': (1200, '5.660052', '1.547771'),
                       'T36': (1200, '5.660052', '1.261844'),
                       'T37': (1200, '5.660052', '1.134776'),
                       'T38': (1200, '5.660052', '1.088730'),
                       'T42': (1200, '5.660052', '1.094213'),
                       'T43': (1200, 5.660052, 0.989392),
                       'T44': (1200, 5.660052, 0.989392),
                       'T45': (1200, 5.660052, 1.028774),
                       'T46': (1200, 5.660052, 1.028774),
                       'T47': (1200, 5.660052, 1.028774),
                       'T61': (1200, 5.660052, 1.094213),
                       'T62': (1200, 5.660052, 0.989392),
                       'T63': (1200, 5.660052, 1.094213),
                       'T64': (1200, 5.660052, 0.989392)}},
    'OT': {   'F': {   'F31': (1200, 2.847729, 0.289092),
                       'F32': (1200, 2.847729, 0.190315),
                       'F51': (1200, 2.847729, 0.182964)},
              'M': {   'F31': (1200, '2.928956', '0.130944'),
                       'F32': (1200, '2.928956', '0.126283'),
                       'F51': (1200, '2.928956', '0.146364')}},
    'SP': {   'F': {   'F11': (1200, 2.986498, 0.316457),
                       'F12': (1200, 2.986498, 0.342821),
                       'F13': (1200, 2.986498, 0.363291),
                       'F20': (1200, 2.986498, 0.333756),
                       'F32': (1200, 3.071658, 0.672851),
                       'F33': (1200, 3.071658, 0.708879),
                       'F34': (1200, 3.071658, 0.553475),
                       'F35': (1200, 2.986498, 0.38413),
                       'F36': (1200, 2.986498, 0.415717),
                       'F37': (1200, 2.986498, 0.382482),
                       'F38': (1200, 2.986498, 0.411337),
                       'F40': (1200, 2.986498, 0.562954),
                       'F41': (1200, 2.986498, 0.489331),
                       'F42': (1200, 2.986498, 0.454527),
                       'F43': (1200, 2.986498, 0.346054),
                       'F44': (1200, 2.986498, 0.346054),
                       'F46': (1200, 2.986498, 0.383996),
                       'F52': (1200, 3.071658, 0.848753),
                       'F53': (1200, 3.071658, 0.925011),
                       'F54': (1200, 3.071658, 0.603221),
                       'F55': (1200, 3.071658, 0.589441),
                       'F56': (1200, 3.071658, 0.550898),
                       'F57': (1200, 3.071658, 0.440262),
                       'F61': (1200, 2.986498, 0.454527),
                       'F62': (1200, 2.986498, 0.346054),
                       'F63': (1200, 2.986498, 0.454527),
                       'F64': (1200, 2.986498, 0.346054)},
              'M': {   'F11': (1200, 3.877517, 0.416484),
                       'F12': (1200, 3.877517, 0.331111),
                       'F13': (1200, 3.877517, 0.432261),
                       'F20': (1200, 3.877517, '0.331200'),
                       'F32': (1200, 3.114028, 0.437054),
                       'F33': (1200, 3.114028, '0.407640'),
                       'F34': (1200, 3.114028, 0.387537),
                       'F35': (1200, 3.877517, '0.346270'),
                       'F36': (1200, 3.877517, 0.372512),
                       'F37': (1200, 3.877517, 0.373891),
                       'F38': (1200, 3.877517, 0.360169),
                       'F40': (1200, 3.877517, 0.496805),
                       'F41': (1200, 3.877517, 0.411921),
                       'F42': (1200, 3.877517, 0.365998),
                       'F43': (1200, 3.877517, 0.341716),
                       'F44': (1200, 3.877517, 0.341716),
                       'F46': (1200, 3.877517, 0.344046),
                       'F52': (1200, 3.114028, 0.469393),
                       'F53': (1200, 3.114028, 0.537476),
                       'F54': (1200, 3.114028, 0.474458),
                       'F55': (1200, 3.114028, 0.396368),
                       'F56': (1200, 3.114028, 0.397033),
                       'F57': (1200, 3.114028, '0.335560'),
                       'F61': (1200, 3.877517, 0.365998),
                       'F62': (1200, 3.877517, 0.341716),
                       'F63': (1200, 3.877517, 0.365998),
                       'F64': (1200, 3.877517, 0.341716)}},
    'TJ': {   'F': {'T20': (1200, 8.360791, 0.787919)},
              'M': {   'T11': (1200, 10.653824, 0.947962),
                       'T12': (1200, 10.653824, 0.826646),
                       'T13': (1200, 10.653824, 0.900026),
                       'T20': (1200, 10.653824, 0.865227),
                       'T45': (1200, 10.653824, 0.851656),
                       'T46': (1200, 10.653824, 0.851656),
                       'T47': (1200, 10.653824, 0.851656)}}}
#===== ( end parameters block  ) =====
def secs(x):
    secs = -1
    secpat = '(\d\d[,.]\d?\d)'
    minsecpat = '(\d?\d)[:.,](\d\d[,.]\d?\d)'
    x = f'{x}'
    match1 = re.match(minsecpat,x)
    match2 = re.match(secpat,x)
    if match1:
        m = match1.group(1)
        s = match1.group(2).replace(',','.')
        secs =  60.*int(m) + float(s)
    elif match2:
        secs = float( match2.group(1).replace(',','.') )
    return secs

def ipc_score(event, gender, cat, performance, youth=None, custom=None):
    p = performance 

    if custom == 'NOR':
        if event == '60':
            event = '100'
            p *= 1.667

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

    a = coefficients[event][gender][cat][0]
    b = float(coefficients[event][gender][cat][1])
    c = float(coefficients[event][gender][cat][2])


    if event in track_events:
        # convert hh:mm:ss.dd format to seconds
        #p = sum(float(x) * 60 ** i for i, x in enumerate(reversed(f'{p}'.split(':'))))
        p = secs(p)
        if youth not in (None, False):
            c *= 1.16
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

