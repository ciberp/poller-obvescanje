# Nastavitve pollerja

GO_TO_SLEEP_TIMEOUT = 2
GO_TO_SLEEP = [
{'name':'rastlinjak','url':'http://192.168.1.2/sleep'},
{'name':'movable1','url':'http://192.168.1.3/sleep'}
]  

# Nastavitve za Graphite
GRAPHITE_TIMEOUT = 2 # timeout per send metric
GRAPHITE = [
{'host':'localhost','port':2003}
]
# Nastavitve za json poller
JSON_POLLER_TIMEOUT = 30
JSON_POLLER = [
{'name':'ogrevanje','url':'http://192.168.1.4/get?data'},
{'name':'ogrevanje','url':'http://192.168.1.3/get?settings'},
{'name':'movable','url':'http://192.168.1.2/json'}
]   

# Nastavitve za XML poller
XML_POLLER_TIMEOUT = 30
XML_POLLER = [
{'dev': 'arso', 'url': 'http://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observationAms_LJUBL-ANA_BEZIGRAD_latest.xml',
 'vars': {
     # 'ime': ['multiplier', 'xml_globina oz. pot do variable...']
     'temp': ['1','data','metData','t'],
     'temp_g_5cm': ['1','data','metData','tg_5_cm'],
     'temp_g_10cm': ['1','data','metData','tg_10_cm'],
     'temp_g_30cm': ['1','data','metData','tg_30_cm'],
     'padavine': ['1','data','metData','rr_val'],
     'vlaga': ['1','data','metData','rh'],
     'veter_kno': ['1.944','data','metData','ff_val'],
     'veter_sunki_kno': ['1.944','data','metData','ffmax_val'],
     'tlak': ['1','data','metData','p'],
     'radiation': ['1','data','metData','gSunRad'],
     'radiation_avg': ['1','data','metData','gSunRadavg']
     }
 } 
 ]

# Nastavitve za SNMP poller
SNMP_POLLER_TIMEOUT = 30
SNMP_POLLER = [
{'dev':'pt3.mikrotik','community':'community','host':'192.168.1.1',
  'vars': {
    '1.3.6.1.2.1.1.3.0':'uptime',
  }}
]