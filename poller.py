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
import xmltodict
import redis

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

__version__ = '2.0'
__author__ = 'Peter Ciber'
__date__ = '30.12.2016'

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
                        #print snmp['dev'], oid.prettyPrint(), value.prettyPrint()
                        debug = '  ' + snmp['vars'][oid.prettyPrint()] + ' ' + oid.prettyPrint() + ' ' +  value.prettyPrint()
                        AddEntryToSyslog(debug)
                        Debug(debug)
                        mytmpdict[snmp['vars'][oid.prettyPrint()]] = 0
                    else:
                        mytmpdict[snmp['vars'][oid.prettyPrint()]] = value.prettyPrint()
                        debug = '  ' + snmp['vars'][oid.prettyPrint()] + ', ' + oid.prettyPrint() + ', ' + value.prettyPrint()
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
    XMLdata = {}
    try:
        response = urllib2.urlopen(url, timeout = poller_settings.XML_POLLER_TIMEOUT);
        htmlpage = response.read()
        XMLdata = xmltodict.parse(htmlpage)
        debug = ' Getting XML data from: %s' % (url)
        Debug(debug)
    except:
        # device je offline ali gre za napacen url
        debug = ' Error getting XML data from: %s' % url
        AddEntryToSyslog(debug)
        Debug(debug)
    return XMLdata

def XMLPoller():
    mydict = {}
    for xml in poller_settings.XML_POLLER:
        xml_data = XMLGetValues(xml['url'])
        mytmpdict = {}
        for var_name, var_path in xml['vars'].iteritems():
            multiplier = var_path[0] # preberem mnozilnik
            del var_path[0] # pobrisem mnozilnik
            xml_data_parcial = xml_data
            for k in var_path:
                if k in xml_data_parcial:
                    xml_data_parcial = xml_data_parcial[k]
            if xml_data_parcial is not None:
                var_num =  float(multiplier) * float(xml_data_parcial)
                mytmpdict[var_name] = str(round(var_num, 2))
            debug = '  %s, %s' % (var_name,var_num)
            Debug(debug)
    mydict[xml['dev']] = mytmpdict
    return mydict

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
        mydict = ReadJSON(SCRIPT_DIR + '/' + 'poller.json')
        debug = 'Reading from redis failed, reading poller.json!'
        AddEntryToSyslog(debug)
        Debug(debug)
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

def check_carbon_and_send_metrics(obj):
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
                debug = ' Working on metrics for dev %s' % device
                Debug(debug)
                # ogrevanje !!! posebna obravnava zaradi PCF
                if device == 'ogrevanje':
                    obj.update(UpdateObjOgrevanjeSpecial(obj,device))
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

def DecToBit(decimal, bit):
    if decimal>>bit & 1 == 0:
        return 100
    else:
        return 0

def UpdateObjOgrevanjeSpecial(obj,device):
    mydict = {}
    for var in obj[device]:
        # ce se arduino restarta dobim cudne vrednosti... zato pocakam 2min, da se podatki stabilizirajo!
        #if long(re.sub(r"\s+", "", obj[device]['Uptime'])) > 180: 
        #send_metric(device + '.' + var,float(re.sub(r"\s+", "", obj[device][var])))
        if var == 'PCF8574':
            debug = ' Ogrevanje special PCF8574 int: %s' % obj[device][var]
            Debug(debug)
            pcfnumber = int(re.sub(r"\s+", "", obj[device][var]))
            mytmpdict = obj['ogrevanje'] # v tmp dict zapisem temparature, da potem dodam PCF data!
            mytmpdict['PumpOgrevanje'] = DecToBit(pcfnumber,0)
            mytmpdict['PumpBojler'] = DecToBit(pcfnumber,1)
            mytmpdict['PumpSolar'] = DecToBit(pcfnumber,2)
            mytmpdict['Emergency'] = DecToBit(pcfnumber,3)
            mytmpdict['Vticnica'] = DecToBit(pcfnumber,4)
            mytmpdict['Relay6'] = DecToBit(pcfnumber,5)
            mytmpdict['Relay7'] = DecToBit(pcfnumber,6)
            mytmpdict['Vrata'] = DecToBit(pcfnumber,7)
            mydict[device] = mytmpdict
            break
    return mydict

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
        
def Main():
    obj = DICT_MERGE() 
    if obj: 
        check_carbon_and_send_metrics(obj)
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
