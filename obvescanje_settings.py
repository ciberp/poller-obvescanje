          
OBVESCANJE = [
# ime spr    , num , gt/lt/eq, recurring/onetime, in_min
# nad = gt, pod = lt, je = eq
# PAZI imamo dva operanda za FAIL in ZA OK value!
{'dev':'ogrevanje','id':'1','c':'','s':'','var':'dhw','fail_op':'pod','fail_value':'33','ok_op':'nad','ok_value':'40','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'2','c':'','s':'','var':'AutoControl','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'3','c':'','s':'','var':'KotelError','fail_op':'je','fail_value':'1','ok_op':'je','ok_value':'0','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'4','c':'','s':'','var':'BojlerError','fail_op':'je','fail_value':'1','ok_op':'je','ok_value':'0','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'5','c':'','s':'','var':'SolarError','fail_op':'je','fail_value':'1','ok_op':'je','ok_value':'0','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'6','c':'','s':'','var':'TuljavaError','fail_op':'je','fail_value':'1','ok_op':'je','ok_value':'0','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
#{'dev':'ogrevanje','id':'7','c':'','s':'','var':'Online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'ogrevanje','id':'8','c':'','s':'','var':'Uptime','fail_op':'pod','fail_value':'300','ok_op':'nad','ok_value':'320','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'9','c':'','s':'','var':'Kotel','fail_op':'nad','fail_value':'95','ok_op':'pod','ok_value':'90','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'ogrevanje','id':'10','c':'','s':'','var':'Tuljava','fail_op':'nad','fail_value':'370','ok_op':'pod','ok_value':'350','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'11','c':'','s':'','var':'ErrRateDHT0','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'12','c':'','s':'','var':'ErrRateDS0','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'13','c':'','s':'','var':'ErrRateDS1','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'14','c':'','s':'','var':'ErrRateDS2','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'15','c':'','s':'','var':'ErrRateDS3','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'16','c':'','s':'','var':'ErrRateDS4','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'17','c':'','s':'','var':'ErrRateMAX0','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'18','c':'','s':'','var':'ErrRateMAX1','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'19','c':'','s':'','var':'ErrRateMAX2','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'ogrevanje','id':'20','c':'','s':'','var':'ErrRateMAX3','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'mikrotik','id':'36','c':'','s':'','var':'cpu-load','fail_op':'nad','fail_value':'90','ok_op':'pod','ok_value':'70','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'6:00'},
{'dev':'mikrotik','id':'30','c':'','s':'','var':'voltage','fail_op':'pod','fail_value':'12','ok_op':'nad','ok_value':'13','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'mikrotik','id':'31','c':'','s':'','var':'sfp-rx-power','fail_op':'pod','fail_value':'-22','ok_op':'nad','ok_value':'-21','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'rastlinjak','id':'37','c':'','s':'','var':'Znotraj','fail_op':'nad','fail_value':'36','ok_op':'pod','ok_value':'25','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rastlinjak','id':'38','c':'','s':'','var':'Battery','fail_op':'pod','fail_value':'10','ok_op':'nad','ok_value':'11','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rastlinjak','id':'39','c':'','s':'','var':'Battery','fail_op':'pod','fail_value':'7','ok_op':'nad','ok_value':'11','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
#{'dev':'rastlinjak','id':'40','c':'','s':'','var':'Zunaj','fail_op':'pod','fail_value':'1','ok_op':'nad','ok_value':'15','rec':['Peter','Teja'],'sil_start':'23:00','sil_stop':'00:00'},
{'dev':'rastlinjak','id':'41','c':'','s':'','var':'Tla','fail_op':'nad','fail_value':'36','ok_op':'pod','ok_value':'25','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
#{'dev':'rastlinjak','id':'42','c':'','s':'','var':'TempTla','fail_op':'pod','fail_value':'7','ok_op':'nad','ok_value':'9','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rastlinjak','id':'43','c':'','s':'','var':'Uptime','fail_op':'pod','fail_value':'300','ok_op':'nad','ok_value':'320','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
#{'dev':'virtualka','id':'50','c':'','s':'','var':'DISK_free_%','fail_op':'pod','fail_value':'5','ok_op':'nad','ok_value':'10','rec':['Peter'],'sil_start':'23:00','sil_stop':'06:00'},
#{'dev':'virtualka','id':'51','c':'','s':'','var':'carbon','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'23:00','sil_stop':'08:00'},
#{'dev':'virtualka','id':'52','c':'','s':'','var':'http','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
#{'dev':'virtualka','id':'53','c':'','s':'','var':'influxdb','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
#{'dev':'virtualka','id':'54','c':'','s':'','var':'graphite','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'08:00'},
#{'dev':'virtualka','id':'55','c':'','s':'','var':'ssh','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rekuperator','id':'60','c':'','s':'','var':'SystemTemp','fail_op':'nad','fail_value':'45','ok_op':'pod','ok_value':'40','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
#{'dev':'rekuperator','id':'61','c':'','s':'','var':'Online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'08:00'},
{'dev':'rekuperator','id':'62','c':'','s':'','var':'OutsideHot','fail_op':'nad','fail_value':'45','ok_op':'pod','ok_value':'40','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'rekuperator','id':'63','c':'','s':'','var':'OutsideCold','fail_op':'nad','fail_value':'45','ok_op':'pod','ok_value':'40','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'rekuperator','id':'64','c':'','s':'','var':'FreshIntake','fail_op':'nad','fail_value':'45','ok_op':'pod','ok_value':'40','rec':['Peter','Teja'],'sil_start':'23:59','sil_stop':'00:00'},
{'dev':'pt3.mikrotik','id':'80','c':'','s':'','var':'cpu-load','fail_op':'nad','fail_value':'80','ok_op':'pod','ok_value':'60','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
{'dev':'rpi2','id':'100','c':'','s':'','var':'redis','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'rpi2','id':'101','c':'','s':'','var':'disk_free_%','fail_op':'pod','fail_value':'5','ok_op':'nad','ok_value':'10','rec':['Peter'],'sil_start':'23:00','sil_stop':'6:00'},
{'dev':'rpi2','id':'104','c':'','s':'','var':'grafana','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'rpi2','id':'105','c':'','s':'','var':'influxdb','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rpi2','id':'106','c':'','s':'','var':'http','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
#{'dev':'rpi2','id':'107','c':'','s':'','var':'kamera_vhod','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter','Teja'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'108','c':'','s':'','var':'samba','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rpi2','id':'109','c':'','s':'','var':'udpxy','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rpi2','id':'110','c':'','s':'','var':'ssh','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'111','c':'','s':'','var':'v6','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'112','c':'','s':'','var':'disk_free_%','fail_op':'pod','fail_value':'20','ok_op':'nad','ok_value':'30','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
{'dev':'rpi2','id':'113','c':'','s':'','var':'ram_free_%','fail_op':'pod','fail_value':'2','ok_op':'nad','ok_value':'10','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
{'dev':'rpi2','id':'114','c':'','s':'','var':'cpu_load','fail_op':'nad','fail_value':'20','ok_op':'pod','ok_value':'10','rec':['Peter'],'sil_start':'22:00','sil_stop':'6:00'},
{'dev':'rpi2','id':'115','c':'','s':'','var':'mqtt','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'121','c':'','s':'','var':'t2_dns_v6','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'122','c':'','s':'','var':'arnes_dns_v6','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'123','c':'','s':'','var':'mikrotik_ssh','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'124','c':'','s':'','var':'mikrotik_http','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'125','c':'','s':'','var':'mikrotik_dns','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
#{'dev':'rpi2','id':'126','c':'','s':'','var':'mikrotik_vpn','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'127','c':'','s':'','var':'mikrotik_v6','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'128','c':'','s':'','var':'ap_ssh','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'129','c':'','s':'','var':'ap_http','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'21:00','sil_stop':'09:00'},
{'dev':'rpi2','id':'130','c':'','s':'','var':'vrata-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
{'dev':'rpi2','id':'131','c':'','s':'','var':'energy-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
{'dev':'rpi2','id':'132','c':'','s':'','var':'ogrevanje-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
{'dev':'rpi2','id':'133','c':'','s':'','var':'ap-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
{'dev':'rpi2','id':'134','c':'','s':'','var':'camera-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
{'dev':'rpi2','id':'135','c':'','s':'','var':'rastlinjak-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
{'dev':'rpi2','id':'136','c':'','s':'','var':'rekuperator-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:50','sil_stop':'08:00'},
#{'dev':'rpi2','id':'137','c':'','s':'','var':'www.fd-groblje.si_icmp-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'08:00'},
#{'dev':'rpi2','id':'138','c':'','s':'','var':'www.fd-groblje.si_http-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'08:00'},
{'dev':'rpi2','id':'139','c':'','s':'','var':'www.brinke.si_icmp-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
{'dev':'rpi2','id':'140','c':'','s':'','var':'www.brinke.si_http-online','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'07:00'},
#{'dev':'rpi2','id':'141','c':'','s':'','var':'pt3_gw','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'08:00'},
#{'dev':'rpi2','id':'142','c':'','s':'','var':'pt3_wan_vpn','fail_op':'je','fail_value':'0','ok_op':'je','ok_value':'1','rec':['Peter'],'sil_start':'22:00','sil_stop':'08:00'},
{'dev':'rpi2','id':'143','c':'','s':'','var':'next-hop-packet-loss','fail_op':'nad','fail_value':'2','ok_op':'pod','ok_value':'1','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'08:00'},
{'dev':'rpi2','id':'144','c':'','s':'','var':'next-hop-rtt-avg','fail_op':'nad','fail_value':'100','ok_op':'pod','ok_value':'5','rec':['Peter'],'sil_start':'22:00','sil_stop':'08:00'},
{'dev':'arso','id':'340','c':'','s':'','var':'so2_dnevna','fail_op':'nad','fail_value':'80','ok_op':'pod','ok_value':'40','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'arso','id':'341','c':'','s':'','var':'co_max_8urna','fail_op':'nad','fail_value':'6','ok_op':'pod','ok_value':'3','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'arso','id':'342','c':'','s':'','var':'o3_max_urna','fail_op':'nad','fail_value':'130','ok_op':'pod','ok_value':'90','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'arso','id':'343','c':'','s':'','var':'no2_max_urna','fail_op':'nad','fail_value':'150','ok_op':'pod','ok_value':'90','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'7:00'},
#{'dev':'arso','id':'344','c':'','s':'','var':'pm10','fail_op':'nad','fail_value':'40','ok_op':'pod','ok_value':'35','rec':['Peter','Teja'],'sil_start':'22:00','sil_stop':'7:00'},
{'dev':'arso','id':'345','c':'','s':'','var':'veter_kno','fail_op':'nad','fail_value':'18','ok_op':'pod','ok_value':'15','rec':['Peter'],'sil_start':'20:00','sil_stop':'08:00'},
]		


SMS_GW = {
    'Provider': 'najdi',
    'Username': 'user',
    'Password': 'password'
}

MAIL_SENDER = {
    'username': 'username',
    'password': 'password',
    'server': 'mail server',
    'port': '587',
    'mail': 'mail address',
    'subject': "subject"
}

MAIL_RECEIVERS = {
    'Peter': 'mail address',
    'Teja': 'mail address'
}

SMS_USERS = {
    'Peter': '031123456',
    'Teja': '041123456'
}
