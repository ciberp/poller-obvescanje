# Nastavitve pollerja

# Nastavitve za influxDB
INFLUXDB_TIMEOUT = 2 # timeout per send metric
INFLUXDB = [
#{'host':'localhost', 'port':8086, 'username':'username', 'password':'password', 'database':'k4_measurements'}
]

# Nastavitve za Graphite
GRAPHITE_TIMEOUT = 2 # timeout per send metric
GRAPHITE = [
{'host':'localhost','port':2003}
]
# Nastavitve za json poller
JSON_POLLER_TIMEOUT = 60
JSON_POLLER = [
{'name':'ogrevanje','url':'http://ogrevanje.k4/json', 'send2influx': False, 'send2graphite': False},
{'name':'rekuperator','url':'http://rekuperator.k4/json', 'send2influx': False, 'send2graphite': False},
{'name':'rastlinjak','url':'http://rastlinjak.k4/json', 'send2influx': False, 'send2graphite': False},
{'name':'rpi2','url':'http://rpi2.k4/check.php', 'send2influx': True, 'send2graphite': True},
{'name':'camera_vhod','url':'http://cam-vhod.k4:8080/check.php', 'send2influx': True, 'send2graphite': True},
{'name':'vrata','url':'http://vrata.k4/json', 'send2influx': True, 'send2graphite': True}
]   

# Nastavitve za XML poller
XML_POLLER_TIMEOUT = 30
XML_POLLER = [
{'dev': 'arso', 'url': 'http://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observationAms_LJUBL-ANA_BEZIGRAD_latest.xml', 'send2influx': True, 'send2graphite': True,
 'vars': [
     {'name': 'temp', 'multiplier': '1', 'path': '/data/metData/t'},
     {'name': 'temp_g_5cm', 'multiplier': '1', 'path': '/data/metData/tg_5_cm'},
     {'name': 'temp_g_10cm', 'multiplier': '1', 'path': '/data/metData/temp_g_10cm'},
     {'name': 'temp_g_30cm', 'multiplier': '1', 'path': '/data/metData/temp_g_30cm'},
     {'name': 'padavine', 'multiplier': '1', 'path': '/data/metData/rr_val'},
     {'name': 'vlaga', 'multiplier': '1', 'path': '/data/metData/rh'},
     {'name': 'veter_kno', 'multiplier': '1.943', 'path': '/data/metData/ff_val'},
     {'name': 'veter_sunki_kno', 'multiplier': '1.943', 'path': '/data/metData/ffmax_val'},
     {'name': 'tlak', 'multiplier': '1', 'path': '/data/metData/p'},
     {'name': 'radiation', 'multiplier': '1', 'path': '/data/metData/gSunRad'},
     {'name': 'radiation_avg', 'multiplier': '1', 'path': '/data/metData/gSunRadavg'}
     ]
 },
{'dev': 'arso', 'url': 'http://www.arso.gov.si/xml/zrak/ones_zrak_dnevni_podatki_zadnji.xml', 'send2influx': True, 'send2graphite': True,
 'vars': [
     {'name': 'pm10', 'multiplier': '1', 'path': '/arsopodatki/postaja[@sifra="E21"]/pm10_dnevna'},
     {'name': 'so2_dnevna', 'multiplier': '1', 'path': '/arsopodatki/postaja[@sifra="E21"]/so2_dnevna'},
     {'name': 'so2_max_urna', 'multiplier': '1', 'path': '/arsopodatki/postaja[@sifra="E21"]/so2_max_urna'},
     {'name': 'co_max_8urna', 'multiplier': '1', 'path': '/arsopodatki/postaja[@sifra="E21"]/co_max_8urna'},
     {'name': 'o3_max_urna', 'multiplier': '1', 'path': '/arsopodatki/postaja[@sifra="E21"]/o3_max_urna'},
     {'name': 'o3_max_8urna', 'multiplier': '1', 'path': '/arsopodatki/postaja[@sifra="E21"]/o3_max_8urna'},
     {'name': 'no2_max_urna', 'multiplier': '1', 'path': '/arsopodatki/postaja[@sifra="E21"]/no2_max_urna'}
     ]
 }
 ]


# Nastavitve za SNMP poller
SNMP_POLLER_TIMEOUT = 30
SNMP_POLLER = [
{'dev':'mikrotik','community':'community','host':'mikrotik_rb2011', 'send2influx': True, 'send2graphite': True,
  'vars': {
    '1.3.6.1.4.1.14988.1.1.3.8.0': 'voltage',
    '1.3.6.1.4.1.14988.1.1.19.1.1.6.1': 'sfp-temperature',
    '1.3.6.1.4.1.14988.1.1.19.1.1.7.1': 'sfp-voltage',
    '1.3.6.1.4.1.14988.1.1.19.1.1.8.1': 'sfp-current',
    '1.3.6.1.4.1.14988.1.1.19.1.1.9.1': 'sfp-tx-power',
    '1.3.6.1.4.1.14988.1.1.19.1.1.10.1': 'sfp-rx-power',
    '1.3.6.1.2.1.1.3.0':'uptime',
    '1.3.6.1.2.1.25.3.3.1.2.1': 'cpu-load',
    '1.3.6.1.2.1.25.2.3.1.5.65536': 'total-memory', 
    '1.3.6.1.2.1.25.2.3.1.6.65536': 'used-memory',
    '1.3.6.1.4.1.14988.1.1.3.10.0': 'temp',
    '1.3.6.1.2.1.31.1.1.1.6.1': 'wan-in-bytes',
    '1.3.6.1.2.1.31.1.1.1.10.1': 'wan-out-bytes',
    '1.3.6.1.2.1.2.2.1.14.1': 'wan-in-errors',
    '1.3.6.1.2.1.2.2.1.20.1': 'wan-out-errors',
    '1.3.6.1.2.1.2.2.1.13.1': 'wan-in-discards',
    '1.3.6.1.2.1.2.2.1.19.1': 'wan-out-discards',
    '1.3.6.1.4.1.14988.1.1.1.3.1.6.12': 'wifi-client-count',
    '1.3.6.1.4.1.14988.1.1.1.3.1.9.12': 'wifi-noise-floor',
    '1.3.6.1.4.1.14988.1.1.1.3.1.10.12': 'wifi-overall-ccq',
    '1.3.6.1.2.1.31.1.1.1.6.2': 'ether1-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.2': 'ether1-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.2': 'ether1-dis-in',
    '1.3.6.1.2.1.2.2.1.19.2': 'ether1-dis-out',
    '1.3.6.1.2.1.2.2.1.14.2': 'ether1-err-in',
    '1.3.6.1.2.1.2.2.1.20.2': 'ether1-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.3': 'ether2-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.3': 'ether2-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.3': 'ether2-dis-in',
    '1.3.6.1.2.1.2.2.1.19.3': 'ether2-dis-out',
    '1.3.6.1.2.1.2.2.1.14.3': 'ether2-err-in',
    '1.3.6.1.2.1.2.2.1.20.3': 'ether2-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.4': 'ether3-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.4': 'ether3-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.4': 'ether3-dis-in',
    '1.3.6.1.2.1.2.2.1.19.4': 'ether3-dis-out',
    '1.3.6.1.2.1.2.2.1.14.4': 'ether3-err-in',
    '1.3.6.1.2.1.2.2.1.20.4': 'ether3-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.5': 'ether4-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.5': 'ether4-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.5': 'ether4-dis-in',
    '1.3.6.1.2.1.2.2.1.19.5': 'ether4-dis-out',
    '1.3.6.1.2.1.2.2.1.14.5': 'ether4-err-in',
    '1.3.6.1.2.1.2.2.1.20.5': 'ether4-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.6': 'ether5-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.6': 'ether5-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.6': 'ether5-dis-in',
    '1.3.6.1.2.1.2.2.1.19.6': 'ether5-dis-out',
    '1.3.6.1.2.1.2.2.1.14.6': 'ether5-err-in',
    '1.3.6.1.2.1.2.2.1.20.6': 'ether5-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.7': 'ether6-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.7': 'ether6-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.7': 'ether6-dis-in',
    '1.3.6.1.2.1.2.2.1.19.7': 'ether6-dis-out',
    '1.3.6.1.2.1.2.2.1.14.7': 'ether6-err-in',
    '1.3.6.1.2.1.2.2.1.20.7': 'ether6-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.8': 'ether7-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.8': 'ether7-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.8': 'ether7-dis-in',
    '1.3.6.1.2.1.2.2.1.19.8': 'ether7-dis-out',
    '1.3.6.1.2.1.2.2.1.14.8': 'ether7-err-in',
    '1.3.6.1.2.1.2.2.1.20.8': 'ether7-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.9': 'ether8-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.9': 'ether8-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.9': 'ether8-dis-in',
    '1.3.6.1.2.1.2.2.1.19.9': 'ether8-dis-out',
    '1.3.6.1.2.1.2.2.1.14.9': 'ether8-err-in',
    '1.3.6.1.2.1.2.2.1.20.9': 'ether8-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.10': 'ether9-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.10': 'ether9-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.10': 'ether9-dis-in',
    '1.3.6.1.2.1.2.2.1.19.10': 'ether9-dis-out',
    '1.3.6.1.2.1.2.2.1.14.10': 'ether9-err-in',
    '1.3.6.1.2.1.2.2.1.20.10': 'ether9-err-out',
    '1.3.6.1.2.1.31.1.1.1.6.11': 'ether10-bytes-in',
    '1.3.6.1.2.1.31.1.1.1.10.11': 'ether10-bytes-out',
    '1.3.6.1.2.1.2.2.1.13.11': 'ether10-dis-in',
    '1.3.6.1.2.1.2.2.1.19.11': 'ether10-dis-out',
    '1.3.6.1.2.1.2.2.1.14.11': 'ether10-err-in',
    '1.3.6.1.2.1.2.2.1.20.11': 'ether10-err-out'
  },
  'multiplier': {
      'uptime': 0.01,
      'voltage': 0.1,
      'temp': 0.1,
      'sfp-tx-power': 0.001,
      'sfp-rx-power': 0.001,
      'sfp-voltage': 0.001
  }}
]
