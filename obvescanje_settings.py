          
OBVESCANJE = [
# ime spr    , num , gt/lt/eq, recurring/onetime, in_min
# nad = gt, pod = lt, je = eq
# PAZI imamo dva operanda za FAIL in ZA OK value!
{'dev':'ogrevanje','id':'1','c':'','s':'','var':'BojlerTemp','fail_op':'pod','fail_value':'36','ok_op':'nad','ok_value':'42','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'2','c':'','s':'','var':'AutoControl','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'3','c':'','s':'','var':'SolarZgoraj','fail_op':'nad','fail_value':'96','ok_op':'pod','ok_value':'95','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'4','c':'','s':'','var':'KurTemp','fail_op':'nad','fail_value':'40','ok_op':'pod','ok_value':'30','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'ogrevanje','id':'5','c':'','s':'','var':'DnevnaTemp','fail_op':'pod','fail_value':'19','ok_op':'nad','ok_value':'20','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'6','c':'','s':'','var':'DnevnaHum','fail_op':'nad','fail_value':'70','ok_op':'pod','ok_value':'60','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'7','c':'','s':'','var':'Online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'ogrevanje','id':'8','c':'','s':'','var':'Uptime','fail_op':'pod','fail_value':'300','ok_op':'nad','ok_value':'320','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'9','c':'','s':'','var':'PecTemp','fail_op':'nad','fail_value':'95','ok_op':'pod','ok_value':'92','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'ogrevanje','id':'10','c':'','s':'','var':'Vticnica','fail_op':'je','fail_value':'1','ok_op':'je','ok_value':'0','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
#{'dev':'rpi1','id':'11','c':'','s':'','var':'DISK_free_%','fail_op':'pod','fail_value':'5','ok_op':'nad','ok_value':'10','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'rpi2','id':'12','c':'','s':'','var':'redis','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'rpi2','id':'13','c':'','s':'','var':'DISK_free_%','fail_op':'pod','fail_value':'5','ok_op':'nad','ok_value':'10','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'rpi2','id':'14','c':'','s':'','var':'grafana','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'rpi2','id':'15','c':'','s':'','var':'influxdb','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rpi2','id':'16','c':'','s':'','var':'http','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'17','c':'','s':'','var':'kamera_vhod','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter','Teja'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'18','c':'','s':'','var':'samba','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rpi2','id':'19','c':'','s':'','var':'virtualka_http','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rpi2','id':'20','c':'','s':'','var':'ssh','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'21','c':'','s':'','var':'t2_dns_v6','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'22','c':'','s':'','var':'arnes_dns_v6','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'mikrotik','id':'30','c':'','s':'','var':'voltage','fail_op':'pod','fail_value':'132','ok_op':'nad','ok_value':'136','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'arso','id':'31','c':'','s':'','var':'veter_kno','fail_op':'nad','fail_value':'18','ok_op':'pod','ok_value':'14','rec':['Peter'],'sil_start':'20:00','sil_stop':'08:00'},
#{'dev':'arso','id':'32','c':'','s':'','var':'veter_sunki_kno','fail_op':'nad','fail_value':'20','ok_op':'pod','ok_value':'20','rec':['Peter'],'sil_start':'20:00','sil_stop':'08:00'},
#{'dev':'arso','id':'33','c':'','s':'','var':'tlak','fail_op':'pod','fail_value':'900','ok_op':'nad','ok_value':'1000','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
#{'dev':'arso','id':'34','c':'','s':'','var':'tlak','fail_op':'nad','fail_value':'1110','ok_op':'pod','ok_value':'1100','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
#{'dev':'pt3.router','id':'35','c':'','s':'','var':'cpu-load-1min','fail_op':'nad','fail_value':'90','ok_op':'pod','ok_value':'70','rec':['Peter'],'sil_start':'22:00','sil_stop':'08:00'},
{'dev':'mikrotik','id':'36','c':'','s':'','var':'cpu-load','fail_op':'nad','fail_value':'90','ok_op':'pod','ok_value':'70','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
{'dev':'rastlinjak','id':'37','c':'','s':'','var':'TempZnotraj','fail_op':'nad','fail_value':'30','ok_op':'pod','ok_value':'25','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rastlinjak','id':'38','c':'','s':'','var':'Baterija','fail_op':'pod','fail_value':'10','ok_op':'nad','ok_value':'11','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rastlinjak','id':'39','c':'','s':'','var':'Baterija','fail_op':'pod','fail_value':'7','ok_op':'nad','ok_value':'11','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
#{'dev':'rastlinjak','id':'39','c':'','s':'','var':'RastSoilHum','fail_op':'pod','fail_value':'12','ok_op':'nad','ok_value':'15','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'6:00'},
#{'dev':'rastlinjak','id':'40','c':'','s':'','var':'Online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'rastlinjak','id':'41','c':'','s':'','var':'TempTla','fail_op':'nad','fail_value':'30','ok_op':'pod','ok_value':'25','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
#{'dev':'rastlinjak','id':'42','c':'','s':'','var':'WiFi','fail_op':'nad','fail_value':'-85','ok_op':'pod','ok_value':'-83','rec':['Peter'],'sil_start':'00:00','sil_stop':'23:59'},
{'dev':'rastlinjak','id':'43','c':'','s':'','var':'Uptime','fail_op':'pod','fail_value':'300','ok_op':'nad','ok_value':'320','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'virtualka','id':'50','c':'','s':'','var':'DISK_free_%','fail_op':'pod','fail_value':'5','ok_op':'nad','ok_value':'10','rec':['Peter'],'sil_start':'23:00','sil_stop':'06:00'},
{'dev':'virtualka','id':'51','c':'','s':'','var':'carbon','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'23:00','sil_stop':'08:00'},
{'dev':'virtualka','id':'52','c':'','s':'','var':'http','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
#{'dev':'virtualka','id':'53','c':'','s':'','var':'kamera_vhod','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'virtualka','id':'54','c':'','s':'','var':'graphite','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'08:00'},
{'dev':'virtualka','id':'55','c':'','s':'','var':'ssh','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'}
]		


# Tejin account na najdi.si
SMS_GW = {
    'Provider': 'najdi',
    'Username': 'username',
    'Password': 'password'
}

SMS_USERS = {
    'Peter': '031123456',
    'Teja': '041123456'
}
