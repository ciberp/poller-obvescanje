#!/usr/bin/env python
import os
import datetime
import time
import poller_settings
import syslog
from optparse import OptionParser
import urllib2
import json
import traceback
import re
import socket
import sys
from subprocess import Popen, PIPE
from pysnmp.entity.rfc3413.oneliner import cmdgen
import obvescanje
from lxml import etree
import redis
from influxdb import InfluxDBClient

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

__version__ = '2.1'
__author__ = 'Peter Ciber'
__date__ = '06.07.2017'

def DumpJSON(data):
    with open(SCRIPT_DIR + '/' + 'poller.json', 'w') as f:
        json.dump(data, f)
    debug = ' Writing settings in json format!'
    Debug(debug)

def ReadJSON(json_file):
    data = {}
    with open(json_file, 'r') as f:
        data = json.load(f)
    debug = 'Reading json metrics: %s' % data
    Debug(debug)
    return data

def SNMPGetValue (community, host, oid):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((host, 161)),timeout = poller_settings.SNMP_POLLER_TIMEOUT, *oid.keys(),lookupMib=False, lexicographicMode=False)
    # Check for errors and print out results
    if errorIndication:
        #print(errorIndication)
        debug = "errorIndication"
        AddEntryToSyslog(debug)
        Debug(debug)
    else:
        if errorStatus:
            debug = '%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?')
            AddEntryToSyslog(debug)
            Debug(debug)
        else:
            return varBinds

def SNMPPoller():
    mydict = {}
    for snmp in poller_settings.SNMP_POLLER:
        debug = ' Polling SNMP device: %s' % snmp['dev']
        Debug(debug)
        try:
            SnmpData = SNMPGetValue(snmp['community'], snmp['host'], snmp['vars'])
            mytmpdict = {}
            for oid, value in SnmpData:
                if oid.prettyPrint() in snmp['vars']:
                    if value.prettyPrint() == 'No Such Instance currently exists at this OID':
                        debug = '  ' + snmp['vars'][oid.prettyPrint()] + ' ' + oid.prettyPrint() + ' ' +  value.prettyPrint()
                        AddEntryToSyslog(debug)
                        Debug(debug)
                        mytmpdict[snmp['vars'][oid.prettyPrint()]] = 0
                    else:
                        if snmp['vars'][oid.prettyPrint()] in snmp['multiplier']:
                            mytmpdict[snmp['vars'][oid.prettyPrint()]] = float(value.prettyPrint()) * snmp['multiplier'][snmp['vars'][oid.prettyPrint()]]
                        else:
                            mytmpdict[snmp['vars'][oid.prettyPrint()]] = value.prettyPrint()
                        debug = '  ' + snmp['vars'][oid.prettyPrint()] + ', ' + oid.prettyPrint() + ', ' + str(mytmpdict[snmp['vars'][oid.prettyPrint()]])
                        Debug(debug)
        except:
           debug = ' Error polling SNMP device: %s %s' % (traceback.format_exc(), SnmpData)
           AddEntryToSyslog(debug)
           Debug(debug)
           pass
        mydict[snmp['dev']] = mytmpdict
    return mydict

def JSONPoller():
    mydict = {}
    html = ''
    for device in poller_settings.JSON_POLLER:
        obj = {}
        try:
            response = urllib2.urlopen(device['url'], timeout = poller_settings.JSON_POLLER_TIMEOUT)
            html = response.read()
            obj = json.loads(html)
            debug = ' Polling device: %s %s' % (device['name'], device['url'])
            Debug(debug)
        except:
            # device je offline ali gre za napacen url
            debug = ' Error polling device: %s' % device
            AddEntryToSyslog(debug)
            Debug(debug)
            offline = {'Online': '0'}
            mydict[device['name']] = offline
            continue
        obj['Online'] = '1'
        if mydict.has_key(device['name']): # ce kljuc ze obstaja, dodamo dict
            for var in obj:
                mydict[device['name']][var] = str(obj[var]).strip()
                debug = '  %s, %s' % (var,str(obj[var]).strip())
                Debug(debug)
        else:  # kljuc se ne obstaja, kreiramo key in value
            mydict[device['name']] = obj
            # tole spodaj je samo za logging!!!
            if FLAGS.debug:
                for var in obj:
                    debug = '  %s, %s' % (var,obj[var])
                    AddEntryToDebug(debug)
            if FLAGS.log_file:
                for var in obj:
                    debug = '  %s, %s' % (var,obj[var])
                    AddEntryToLogFile(debug)
    return mydict    


def XMLGetValues(url):
    try:
        response = urllib2.urlopen(url, timeout = poller_settings.XML_POLLER_TIMEOUT);
        xml = response.read()
        debug = ' Getting XML data from: %s' % (url)
        Debug(debug)
    except:
        # device je offline ali gre za napacen url
        debug = ' Error getting XML data from: %s' % url
        AddEntryToSyslog(debug)
        Debug(debug)
    return xml

def XMLPoller():
    mydict = {}
    mytmpdict = {}
    for xml in poller_settings.XML_POLLER:
        xml_data = etree.fromstring(XMLGetValues(xml['url']))
        for var in xml['vars']:
            var_num = ''
            try:
                var_num =  float(var['multiplier']) * float(xml_data.xpath(var['path'])[0].text)
                mytmpdict[var['name']] = str(round(var_num, 2))
                debug = '  %s, %s' % (var['name'],var_num)
                Debug(debug)
            except:
                debug = '  WARNING, no data for %s' % (var['name'])
                Debug(debug)
    mydict[xml['dev']] = mytmpdict
    return mydict

# ce ni novih podatkob ohranja staro vrednost!!!
def DictUpdateFunction(Old,New):
    for dev in New.keys():
        if not dev in Old:
            Old[dev] = {}
        for metric in New[dev].keys():
            Old[dev][metric] = New[dev][metric]
    return Old
  
def DICT_MERGE():
    try:
        mydict = ReadDataFromRedis('poller-data')
    except:
        try:
            mydict = ReadJSON(SCRIPT_DIR + '/' + 'poller.json')
        except:
            debug = 'No such file or directory: poller.json!'
            AddEntryToSyslog(debug)
            Debug(debug)
            mydict = {}
            pass
        debug = 'Reading from redis failed, reading poller.json!'
        AddEntryToSyslog(debug)
        Debug(debug)
    mydict = {} # povozim stare podatke in posiljam samo nove, ce to vrstico zakomentiram bo ohranjal tudi stare (vedno poslje last)
    mydict = DictUpdateFunction(mydict,JSONPoller())
    mydict = DictUpdateFunction(mydict,SNMPPoller())
    mydict = DictUpdateFunction(mydict,XMLPoller())
    return mydict

# feeding graphite
def send_metric(name, value, host, port):
    if not FLAGS.no_graphite:
        for graphite_host in poller_settings.GRAPHITE:
            try:
                sock = socket.socket()
                sock.settimeout(poller_settings.GRAPHITE_TIMEOUT)
                sock.connect( (host, port) )
                timestamp = int(time.time())
                sock.send("%s %s %d\n" % (name, value, timestamp))
                sock.close()
                debug = '  Send metric %s, %s' % (name, value)
                Debug(debug)
            except socket.error: 
                debug = '  Error send metric to %s:%s, connection refused: %s %s' % (host, port, name, value)
                AddEntryToSyslog(debug)
                Debug(debug)

def check_carbon_and_send_metrics(obj,dev2graphite):
    for graphite_host in poller_settings.GRAPHITE:
        s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((graphite_host['host'],graphite_host['port']))
        s.close()
        if result:
            debug = 'Carbon at %s:%s is down, skipping!' % (graphite_host['host'], graphite_host['port'])
            AddEntryToSyslog(debug)
            Debug(debug)
        else:
            debug = 'Sending metrics to carbon at %s:%s!' % (graphite_host['host'], graphite_host['port'])
            Debug(debug)      
            for device in obj:
                if dev2graphite[device]:
                    debug = ' Working on metrics for dev %s' % device
                    Debug(debug)
                    for var in obj[device]:
                        try:
                            send_metric(device + '.' + var,obj[device][var], graphite_host['host'], graphite_host['port'])
                        except:
                            try:
                                send_metric(device + '.' + var,(obj[device][var]), graphite_host['host'], graphite_host['port'])
                            except:
                                debug = ' Error send metric to %s:%s, %s' % (graphite_host['host'], graphite_host['port'], traceback.format_exc())
                                AddEntryToSyslog(debug)
                                Debug(debug)


def check_influxdb_and_send_measurements(obj,dev2influx):
    for influx_host in poller_settings.INFLUXDB:
        s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((influx_host['host'],influx_host['port']))
        s.close()
        if result:
            debug = 'Influxdb at %s:%s is down, skipping!' % (influx_host['host'], influx_host['port'])
            AddEntryToSyslog(debug)
            Debug(debug)
        else:
            client = InfluxDBClient(influx_host['host'], influx_host['port'], influx_host['username'], influx_host['password'], influx_host['database'])
            debug = 'Sending measurements to influxdb at %s:%s database:%s!' % (influx_host['host'], influx_host['port'], influx_host['database'])
            Debug(debug)      
            for device in obj:
                if dev2influx[device]:
                    debug = ' Working on measurements for dev %s' % device
                    Debug(debug)
                    measurement = {}
                    measurement['fields'] = obj[device]
                    measurement['measurement'] = device # nastavim ime meritve
                    client.write_points([measurement])

def PutToSleep():
    for sleep in poller_settings.GO_TO_SLEEP:
        try:
            response = urllib2.urlopen(sleep['url'], timeout = poller_settings.GO_TO_SLEEP_TIMEOUT);
            htmlpage = response.read()
            debug = ' Putting to sleep: %s' % (sleep['url'])
            Debug(debug)
        except:
            pass

def SaveDataToRedis(data, name):
    dictofarray = {}
    r = redis.StrictRedis()
    r.set(name, json.dumps(data))

def ReadDataFromRedis(name):
    r = redis.StrictRedis()
    data = r.get(name)
    return json.loads(data)
   
def Debug(debug):
    if FLAGS.debug:
        AddEntryToDebug(debug)
    if FLAGS.log_file:
        AddEntryToLogFile(debug)
        
def Dev2Influx():
    # create lookup table for device to send to influx
    dev2influx = {}
    for line in poller_settings.JSON_POLLER:
        dev2influx[line['name']] = line['send2influx']
    for line in poller_settings.XML_POLLER:
        dev2influx[line['dev']] = line['send2influx']
    for line in poller_settings.SNMP_POLLER:
        dev2influx[line['dev']] = line['send2influx']
    return dev2influx  
       
def Dev2Graphite():
    # create lookup table for device to send to carbon
    dev2graphite = {}
    for line in poller_settings.JSON_POLLER:
        dev2graphite[line['name']] = line['send2graphite']
    for line in poller_settings.XML_POLLER:
        dev2graphite[line['dev']] = line['send2graphite']
    for line in poller_settings.SNMP_POLLER:
        dev2graphite[line['dev']] = line['send2graphite']
    return dev2graphite  
        
def Main():
    dev2influx = Dev2Influx()
    dev2carbon = Dev2Graphite()
    obj = DICT_MERGE() 
    if obj:
        check_carbon_and_send_metrics(obj,dev2carbon)
        check_influxdb_and_send_measurements(obj,dev2influx) 
    else:
        debug = ' Error no data from pollers'
        AddEntryToSyslog(debug)
        Debug(debug)
    try:
        SaveDataToRedis(obj,'poller-data')        # zapisem v redis      
    except:
        DumpJSON(obj) # vse metrike zapisen v file poller.json json format
        debug = ' Saving data to redis failed, writing data to poller.json!'
        AddEntryToSyslog(debug)
        Debug(debug)
    PutToSleep()
    return obj

def LogFileCurrentTimeStamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + ' '

def AddEntryToLogFile(debug_string):
    with open(FLAGS.log_file, "a") as myfile:
        myfile.write(LogFileCurrentTimeStamp() + debug_string + '\n')

def AddEntryToDebug(debug_string):
    print LogFileCurrentTimeStamp() + debug_string
  
def AddEntryToSyslog(error_string):
    syslog.syslog(sys.argv[0] + ' ' + error_string)  
  
def WriteJSON(data,file):
    with open(SCRIPT_DIR + '/' + file, 'w') as f:
        json.dump(data, f)
    debug = ' Writing metrics to: %s' % SCRIPT_DIR + '/' + file
    Debug(debug)
    
if __name__ == '__main__':
    usage = 'usage: %prog'
    _parser = OptionParser(usage=usage, version='%prog '+__version__)
    _parser.add_option('-d', help='Debug nacin', dest='debug', action='store_true', default=False)
    _parser.add_option('-l', help='Debug, zapisovanje v Log file', dest='log_file', default=None, type='str')
    _parser.add_option('-n', help='Ne posiljaj metrik v graphite', dest='no_graphite', action='store_true', default=None)
    _parser.add_option('-j', help='Zapisi metrike v json', dest='json', default=False, type='str')
    _parser.add_option('-m', help='Pozeni, vendar ne posiljaj SMS-ov', dest='no_sms', action='store_true', default=False)
    (FLAGS, args) = _parser.parse_args()
    try:
        AllPolledData = Main()
        if FLAGS.json:
            WriteJSON(AllPolledData,FLAGS.json)
    except Exception:
        err = traceback.format_exc()
        debug = ' Exception: ' + err
        AddEntryToSyslog(debug)
        Debug(debug)
