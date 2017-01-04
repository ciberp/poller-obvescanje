#!/usr/bin/env python
import os
import datetime
import time
import obvescanje_settings
import syslog
from optparse import OptionParser
import urllib2
import json
import traceback
import sys
from subprocess import Popen, PIPE
import redis

FailStates = 'StatesFail.json'
OKStates = 'StatesOk.json'
STATES_FAIL = {}
STATES_OK = {}
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

__version__ = '2.0'
__author__ = 'Peter Ciber'
__date__ = '30.12.2016'

def Debug(debug):
    if FLAGS.debug:
        AddEntryToDebug(debug)
    if FLAGS.log_file:
        AddEntryToLogFile(debug)
        
def WFAIL(data):
    FileNamePath = SCRIPT_DIR + '/' + FailStates
    try:
        SaveDataToRedis(data,'obvescanje-FailStates')
    except:
        with open(FileNamePath, 'w') as f:
            json.dump(data, f)
        debug = 'Saving data to redis failed, writing data to %s!' % FileNamePath
        AddEntryToSyslog(debug)
        Debug(debug)
  
def RFAIL():
    data = {}
    FileNamePath = SCRIPT_DIR + '/' + FailStates
    try:
        data = ReadDataFromRedis('obvescanje-FailStates')
        return data
    except:
        with open(FileNamePath, 'r') as f:
            data = json.load(f)
        debug = 'Reading data from redis failed, reading %s!' % FileNamePath
        Debug(debug)
        return data
  
def WOK(data):
    FileNamePath = SCRIPT_DIR + '/' + OKStates
    try:
        SaveDataToRedis(data,'obvescanje-OKStates')
    except:
        with open(FileNamePath, 'w') as f:
            json.dump(data, f)
        debug = 'Saving data to redis failed, writing data to %s!' % FileNamePath
        Debug(debug)
  
def ROK():
    data = {}
    FileNamePath = SCRIPT_DIR + '/' + OKStates
    try:
        data = ReadDataFromRedis('obvescanje-OKStates')
        return data
    except:
        with open(FileNamePath, 'r') as f:
            data = json.load(f)
        debug = 'Reading data from redis failed, reading %s!' % FileNamePath
        Debug(debug)
        return data

def ReadJSON(json_file):
    data = {}
    with open(json_file, 'r') as f:
        data = json.load(f)
    debug = 'Reading json metrics: %s' % data
    Debug(debug)
    return data

def WriteSettingsJSONFormat(data):
    # tole je za php skripto za prikaz stanja
    FileNamePath = SCRIPT_DIR + '/' + 'obvescanje.json'
    try:
        SaveDataToRedis(data,'obvescanje-status')
    except:
        with open(FileNamePath, 'w') as f:
            json.dump(data, f)
        debug = 'Saving data to redis failed, writing data to %s!' % FileNamePath
        Debug(debug)

def Main(*JSONMetricValue):
    global STATES_OK
    global STATES_FAIL
    SendTestSMS()
    try:
            STATES_OK = ROK()
    except:
            pass
    try:
            STATES_FAIL = RFAIL()
    except:
            pass
    for ln in obvescanje_settings.OBVESCANJE:
        try:
            FullMetricName = ln['var']
            MetricValue = JSONMetricValue[0][ln['dev']]
                #print ln['var'],ln['dev']
            if not MetricValue:
                debug = 'WARNING %s.%s non existing metric, exists only: %s' % (ln['dev'], FullMetricName, MetricValue)
                AddEntryToSyslog(debug)
                Debug(debug)
                continue
            try:
                ln['c'] = str(MetricValue[FullMetricName]).strip()
            except:
                debug = 'WARNING %s.%s non existing metric, exists only: %s' % (ln['dev'], FullMetricName, MetricValue)
                Debug(debug)
                continue
            if ln['fail_op'] == 'pod':
                if float(MetricValue[FullMetricName]) < int(ln['fail_value']):
                    PreveriPosiljanje(ln)
            if ln['ok_op'] == 'pod':
                if float(MetricValue[FullMetricName]) < int(ln['ok_value']):
                    PreveriRecovery(ln)
            if ln['fail_op'] == 'nad':
                if float(MetricValue[FullMetricName]) > int(ln['fail_value']):
                    PreveriPosiljanje(ln)
            if ln['ok_op'] == 'nad':
                if float(MetricValue[FullMetricName]) > int(ln['ok_value']):
                    PreveriRecovery(ln)
            if  ln['fail_op'] == 'je':
                if int(MetricValue[FullMetricName]) == int(ln['fail_value']):
                    PreveriPosiljanje(ln)
            if  ln['ok_op'] == 'je':
                if int(MetricValue[FullMetricName]) == int(ln['ok_value']):
                    PreveriRecovery(ln)
        except:
            err = traceback.format_exc()
            debug = ' Exception: ' + err
            AddEntryToSyslog(debug)
            Debug(debug)
    WriteSettingsJSONFormat(obvescanje_settings.OBVESCANJE)
    WOK(STATES_OK)
    WFAIL(STATES_FAIL)
  
def PreveriRecovery(ln):
    global STATES_OK
    global STATES_FAIL
    start = ln['sil_start']
    stop = ln['sil_stop']
    now = datetime.datetime.now()
    now = datetime.datetime.strptime(str(now.hour)+':'+str(now.minute), '%H:%M')
    silent_start = datetime.datetime.strptime(start, '%H:%M')
    silent_stop = datetime.datetime.strptime(stop, '%H:%M')
    #print "RECOVERY", ln['var'], ln['c']
    CurrentTimeStamp = int(round(time.time()))
    #stanje je spet OK, preverim in posljem recovery msg
    debug = 'OK %s.%s,\tcurrent:%s, fail=%s %s, ok=%s %s' % (ln['dev'], ln['var'], ln['c'], ln['fail_op'], ln['fail_value'], ln['ok_op'], ln['ok_value'])
    Debug(debug)
    if not ln['id'] in STATES_OK:
        # Ok se ni bil poslan, pobrisem FAIL in posljem OK
        debug = '%s.%s msg se ni bil poslan, pobrisem FAIL in posljem OK msg: %s' % (ln['dev'], ln['var'], ln['c'])
        Debug(debug)
        try:  
            del STATES_FAIL[ln['id']]
        except:
            pass
        #popravim text besedila v storitev OK
        debug = '%s.%s popravim text besedila v stanje OK: %s' % (ln['dev'], ln['var'], ln['c'])
        Debug(debug)
        ln['s'] = ", Status:OK"
        if now < silent_start and now > silent_stop:
            # ce gre za silent hours, potem ne posljem in ne zapisem, zato da sms ziher pride izven silent hours
            SendNow(ln)
            #zapisem, da je bil OK poslan
            debug = '%s.%s zapisem, da je bil OK msg poslan: %s' % (ln['dev'], ln['var'], ln['c'])
            Debug(debug)
            STATES_OK[ln['id']] = CurrentTimeStamp
        else:
            debug = '%s.%s silent hours, SMS is waiting in queue!' % (ln['dev'], ln['var'])
            Debug(debug)           

def PreveriPosiljanje(ln):
    global STATES_OK
    global STATES_FAIL
    start = ln['sil_start']
    stop = ln['sil_stop']
    now = datetime.datetime.now()
    now = datetime.datetime.strptime(str(now.hour)+':'+str(now.minute), '%H:%M')
    silent_start = datetime.datetime.strptime(start, '%H:%M')
    silent_stop = datetime.datetime.strptime(stop, '%H:%M')
    #print "FAIL", obvestilo['var'], obvestilo['c']
    CurrentTimeStamp = int(round(time.time()))
    #stanje je spet FAIL, preverim in posljem FAIL msg
    debug = 'FAIL %s.%s,\tcurrent:%s, fail=%s %s, ok=%s %s' % (ln['dev'], ln['var'], ln['c'], ln['fail_op'], ln['fail_value'],ln['ok_op'], ln['ok_value'])
    Debug(debug)
    if not ln['id'] in STATES_FAIL:
        # FAIL se ni bil poslan, pobrisem OK in posljem FAIL
        debug = '%s.%s FAIL msg se ni bil poslan, pobrisem OK in posljem FAIL msg: %s' % (ln['dev'], ln['var'], ln['c'])
        Debug(debug)     
        try:  
            del STATES_OK[ln['id']]
        except:
            pass
        #popravim text besedila v storitev FAIL
        debug = '%s.%s popravim text besedila v stanje FAIL: %s' % (ln['dev'], ln['var'], ln['c'])
        Debug(debug)
        ln['s'] = ", Status:FAIL"
        if now < silent_start and now > silent_stop:
                # ce gre za silent hours, potem ne posljem in ne zapisem, zato da sms ziher pride izven silent hours
                SendNow(ln)
                #zapisem, da je bil FAIL poslan
                debug = '%s.%s zapisem, da je bil FAIL msg poslan: %s' % (ln['dev'], ln['var'], ln['c'])
                Debug(debug)
                ln['s'] = ", Status:FAIL"
                STATES_FAIL[ln['id']] = CurrentTimeStamp
        else:
            debug = '%s.%s silent hours, SMS is waiting in queue!' % (ln['dev'], ln['var'])
            Debug(debug)

def SendNow(obvestilo):
    for name in (obvestilo['rec']):
        debug = 'Sending SMS to ' + name + ': ' + obvestilo['dev'] + ' ' + obvestilo['var'] + '(' + obvestilo['c'].strip() + ')' + ' ' + obvestilo['s']
        AddEntryToSyslog(debug)
        Debug(debug)
        if not FLAGS.no_sms:
            SendSMS([name],obvestilo['dev'] + ' ' + obvestilo['var'] + '(' + obvestilo['c'].strip() + ')' + ' ' + obvestilo['s'])

def SendSMS(name,sms_str):
    if not FLAGS.no_sms:
        provider = obvescanje_settings.SMS_GW['Provider']
        username = obvescanje_settings.SMS_GW['Username']
        password = obvescanje_settings.SMS_GW['Password']
        for user in name:
            mobilenumber = obvescanje_settings.SMS_USERS[user]
            proc = Popen(["php", SCRIPT_DIR + "/sendfreesms.php", provider, username, password, mobilenumber, sms_str], stdout=PIPE)
            debug = proc.communicate()[0]
            if debug != '':
                AddEntryToSyslog(debug)
                Debug(debug)

def LogFileCurrentTimeStamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + ' '

def RemoveMinMaxAVG(data,metric):
    debug = ''
    data_sum = 0
    data_num = 0
    items = []
    for datapoints in data:
        if datapoints[0] != None:
            items.append(str(datapoints[0]))
            data_sum = data_sum + datapoints[0]
            data_num = data_num + 1
    debug = ','.join(items)
    avg = 0
    if data_num > 0:
        avg = float(data_sum / data_num)
    debug = metric + ' avg=' + str(avg) + ' points:' + debug
    Debug(debug)
    return avg

def AddEntryToLogFile(debug_string):
    with open(FLAGS.log_file, "a") as myfile:
        myfile.write(LogFileCurrentTimeStamp() + debug_string + '\n')

def AddEntryToDebug(debug_string):
    print LogFileCurrentTimeStamp() + debug_string
  
def AddEntryToSyslog(error_string):
    syslog.syslog(sys.argv[0] + ' ' + error_string)  

def SendTestSMS():
    msg = 'To je testno SMS sporocilo!'
    if FLAGS.test_sms_user:
        if FLAGS.test_sms:
            msg = FLAGS.test_sms
        SendSMS([FLAGS.test_sms_user],msg)
        debug = ' Send test SMS to ' + str(FLAGS.test_sms_user) + ', msg:' + msg
        AddEntryToSyslog(debug)
        Debug(debug)

def SaveDataToRedis(data,name):
    dictofarray = {}
    r = redis.StrictRedis()
    r.set(name, json.dumps(data))

def ReadDataFromRedis(name):
    r = redis.StrictRedis()
    data = r.get(name)
    return json.loads(data)

if __name__ == '__main__':
    usage = 'usage: %prog'
    _parser = OptionParser(usage=usage, version='%prog '+__version__)
    _parser.add_option('-d', help='Debug nacin', dest='debug', action='store_true', default=False)
    _parser.add_option('-l', help='Debug zapis v Log file', dest='log_file', default=None, type='str')
    _parser.add_option('-m', help='Pozeni, vendar ne posiljaj SMS-ov', dest='no_sms', action='store_true', default=False)
    _parser.add_option('-u', help='Poslji testni SMS uporabniku "-u Peter"', dest='test_sms_user', default=False, type='str')
    _parser.add_option('-t', help='Nastavi besedilo testnemu SMS-ju: -t "Testno sporocilo"', dest='test_sms', default=False, type='str')
    (FLAGS, args) = _parser.parse_args()
    try:
        try:
            # poskusim prebrati iz RAM-a (redis)
            JSONMetricValue = ReadDataFromRedis('poller-data')
            Main(JSONMetricValue)
        except:
            JSONMetricValue = ReadJSON(SCRIPT_DIR + '/' + 'poller.json')
            Main(JSONMetricValue)
            debug = 'Reading from redis failed, reading poller.json!'
            AddEntryToSyslog(debug)
            Debug(debug)
    except Exception:
        err = traceback.format_exc()
        debug = ' Exception: ' + err
        AddEntryToSyslog(debug)
        Debug(debug)
