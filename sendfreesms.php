<?php

SendFreeSms($argv[1],$argv[2],$argv[3],$argv[4],$argv[5]);

//=========================================================================
//	Skripta za posiljanje sms preko Simobilove Klape / Najdi.si / Tusmobil
//	Verzija 2.50                (c) blackbfm @ slo-tech
//=========================================================================
//	Pošiljanje: 
//	SendFreeSms("ponudnik", "uporabniskoime", "geslo", "stevilka", "sporocilo")
//
//	Preverjanje stanja:
//	SendFreeSms("ponudnik", "uporabniskoime", "geslo", "stevilka", "sporocilo", False)
//
//	Namesto ponudnika vpišeš "klapa" / "najdi" / "tusmobil". Funkcija ob uspešno poslanem smsu
//	vrne število preostalih sporočil ali pa vrže error:
//	-1 splošna napaka
//	-2 prazno / predolgo sporočilo
//	-3 napačna telefonska številka
//=========================================================================
//ini_set('display_errors', 'On');
//error_reporting(E_ALL);

function SendFreeSms($SmsProvider, $SmsUser, $SmsPwd, $SmsNum, $SmsMsg, $Send = True)
{
	$ValidNetworks = array("070", "064", "031", "041", "051", "071", "030", "040");
	$KlapaMaxLen = 280;
	$NajdiMaxLen = 160;
	$TusmobilMaxLen = 140;
	
	if (((!is_numeric($SmsNum)) || (strlen($SmsNum) != 9) || (!in_array(substr($SmsNum,0,3), $ValidNetworks))) && ($Send)) {
		return -3;
	}

	$Cookies = tempnam(sys_get_temp_dir(), uniqid());
	if (! $Cookies) { 'Cookie file ERROR'; die(); }

	$ch = curl_init();
	//curl_setopt($ch, CURLOPT_PROXY, '127.0.0.1:8888');
	curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36');
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
	curl_setopt($ch, CURLOPT_COOKIEJAR, $Cookies);
	curl_setopt($ch, CURLOPT_COOKIEFILE, $Cookies);
	
	if ($SmsProvider == "klapa") {

		if (((strlen($SmsMsg) == 0) || (strlen($SmsMsg) >= $KlapaMaxLen)) && ($Send)) {
			return -2;
		}
		
		try {	
			curl_setopt($ch, CURLOPT_URL, "http://klapa.simobil.net/klapa/send.php");
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }
			
			preg_match("/id=\"__VIEWSTATE\" value=\"(.*)\" \/>/", $response, $parsed_viewstate);
			preg_match("/id=\"__EVENTVALIDATION\" value=\"(.*)\" \/>/", $response, $parsed_eventvalidation);
			 
			$PostData =    "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=" . urlencode($parsed_viewstate[1]) .
							"&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=" . urlencode($parsed_eventvalidation[1]) .
							"&ctl00%24ContentPlaceHolder%24txtUsername=" . $SmsUser .
							"&ctl00%24ContentPlaceHolder%24txtPassword=" . $SmsPwd . "&ctl00%24ContentPlaceHolder%24btnLogin=PRIJAVITE+SE";
							 
			curl_setopt($ch, CURLOPT_POST, true);
			curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);
			$lasturl = curl_getinfo($ch);
			curl_setopt($ch, CURLOPT_URL, $lasturl['url']);
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }
			preg_match("/name=\"authTicket\" value=\"(.*)\"\/>/", $response, $KlapaAuthTicket);
			if (empty($KlapaAuthTicket)) { throw new Exception(); }
			curl_setopt($ch, CURLOPT_URL, "http://klapa.simobil.net/klapa/send.php");
			$PostData = "authTicket=" . urlencode($KlapaAuthTicket[1]);
			curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }
			preg_match("/Preostalo .*?tevilo sporo.*?il: (\d+)<\/span>/u", $response, $SmsCredit);
	
			$SmsCredit = $SmsCredit[1];
			if (!$Send) { return $SmsCredit; }
			if ($SmsCredit == 0) { return 0; }
			
			curl_setopt($ch, CURLOPT_URL, "http://klapa.simobil.net/klapa/send_msg.php ");
			$PostData = "recipient=&number.1001=386" . substr($SmsNum, 1,8) . "&text=" . urlencode($SmsMsg) . "&js_enabled=true&sendit=true";
			curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }
			preg_match("/Preostalo .*?tevilo sporo.*?il: (\d+)<\/span>/u", $response, $SmsCredit);
			curl_close($ch);
			return $SmsCredit[1];
		} catch (Exception $e) {
			return -1;
		}

	}
	elseif ($SmsProvider == "najdi") {
	
		if (((strlen($SmsMsg) == 0) || (strlen($SmsMsg) >= $NajdiMaxLen)) && ($Send)) {
			return -2;
		}
		
		try {	
			curl_setopt($ch, CURLOPT_URL, "http://www.najdi.si/prijava");
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }

			preg_match("/<input value=\"([^\"]*?)\" name=\"t:formdata\"/", $response, $t_formdata);
                        //echo $response;
			curl_setopt($ch, CURLOPT_URL, "https://www.najdi.si/prijava.jsecloginform");
			curl_setopt($ch, CURLOPT_POST, true);
			curl_setopt($ch, CURLOPT_HEADER, true);
			$PostData = 't%3Aformdata=' . urlencode($t_formdata[1]) . "&jsecLogin=" . $SmsUser . "&jsecPassword=" . $SmsPwd;
			curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);
			$response = curl_exec($ch);
			//echo $PostData;
			//echo $response;
			if (curl_errno($ch) != 0) { throw new Exception(); }

			curl_setopt($ch, CURLOPT_URL, "http://www.najdi.si/najdi/sms");
			curl_setopt($ch, CURLOPT_POST, false);
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }

			preg_match("/<div class=\"smsno\">poslani SMS-i: <strong>(.*?) \/ 40</",$response,$SmsCredit);
	
			if (!$Send) { return 40 - $SmsCredit[1]; }
			if ($SmsCredit == 0) { return 0; }		

			preg_match_all("/<input value=\"([^\"]*?)\" name=\"t:formdata\"/", $response, $t_formdata);

			curl_setopt($ch, CURLOPT_URL, "http://www.najdi.si/najdi.shortcutplaceholder.freesmsshortcut.smsform");
			curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-Requested-With: XMLHttpRequest')); 
			curl_setopt($ch, CURLOPT_POST, true);
			$PostData = '';

			foreach ($t_formdata[1] as $value) {
				$PostData .= '&t%3Aformdata=' . urlencode($value);				
			}
			$PostData = ltrim($PostData, '&');
			$PostData .= '&t%3Aac=sms&t%3Asubmit=%5B%22send%22%2C%22send%22%5D&t%3Azoneid=smsZone' .
						'&areaCodeRecipient=' . substr($SmsNum, 0, 3). '&phoneNumberRecipient=' . substr($SmsNum, 3, 6) . '&text=' . urlencode($SmsMsg);
			curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);

			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }

			preg_match("/Danes lahko po.+ljete .+e <strong>(.+?)</",$response,$SmsCredit);
			curl_close($ch);
			return $SmsCredit[1];

		} catch (Exception $e) {
			return -1;
		}
	}
	elseif ($SmsProvider == "tusmobil") {
	
		if (((strlen($SmsMsg) == 0) || (strlen($SmsMsg) >= $TusmobilMaxLen)) && ($Send)) {
			return -2;
		}
	
		try {
			if (!is_dir("tusmobil_session")) { mkdir("tusmobil_session"); }
			$CookiesFile = dirname(__FILE__) . "/tusmobil_session/" . md5($SmsUser);
			curl_setopt($ch, CURLOPT_COOKIEFILE, $CookiesFile);
			curl_setopt($ch, CURLOPT_COOKIEJAR, $CookiesFile);
			
			function FBGetSignedRequest(&$ch) {
				curl_setopt($ch, CURLOPT_URL, "https://www.facebook.com/pages/Tu%C5%A1mobil-doo/183068912838?sk=app_142611112521439");
				$response = curl_exec($ch);
				preg_match("/signedRequest\":\"(.*?)\"}/", $response, $AppSignedRequest);
				if (empty($AppSignedRequest)) { return -1; }
				if (strpos($response, "login_form") !== False) { return -1; }
				$AppSignedRequest = $AppSignedRequest[1];
				return $AppSignedRequest;
			}
		
			$AppSignedRequest = FBGetSignedRequest($ch);
			
			if ($AppSignedRequest == -1) {
			
				curl_setopt($ch, CURLOPT_URL, "https://www.facebook.com");
				$response = curl_exec($ch);
				if (curl_errno($ch) != 0) { throw new Exception(); }
				curl_setopt($ch, CURLOPT_URL, "https://www.facebook.com/login.php?login_attempt=1");
				curl_setopt($ch, CURLOPT_POST, true);
				$PostData = "email=" . urlencode($SmsUser) . "&pass=" . urlencode($SmsPwd) . "&persistent=1";
				curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);
				$response = curl_exec($ch);
				if (curl_errno($ch) != 0) { throw new Exception(); }
				$AppSignedRequest = FBGetSignedRequest($ch);
			}
		
			curl_setopt($ch, CURLOPT_URL, "https://moj.tusmobil.si/fbsms/index.php");
			curl_setopt($ch, CURLOPT_POST, true);
			$PostData = "signed_request=" . $AppSignedRequest;
			curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }
			preg_match("/danes .*?e (\d+) od \d+ sporo.*?il/", $response, $SmsCredit);
			if (empty($SmsCredit)) { throw new Exception(); }
			$SmsCredit = $SmsCredit[1];
		
			if (!$Send) { return $SmsCredit; }
			if ($SmsCredit == 0) { return 0; }
			
			curl_setopt($ch, CURLOPT_URL, "https://moj.tusmobil.si/fbsms/message.php");
			curl_setopt($ch, CURLOPT_POST, true);
			$PostData = "prefix=" . substr($SmsNum, 1, 2) . "&number=" . urlencode(substr($SmsNum, 3, 3) . " " . substr($SmsNum, 6, 3)  ) .
						"&message=" . urlencode($SmsMsg). "&signed_request=" . $AppSignedRequest;
			curl_setopt($ch, CURLOPT_POSTFIELDS, $PostData);
			$response = curl_exec($ch);
			if (curl_errno($ch) != 0) { throw new Exception(); }
			preg_match("/danes .*?e (\d+) od \d+ sporo.*?il/", $response, $SmsCredit);
			$SmsCredit = $SmsCredit[1];
			return $SmsCredit;
	} catch (Exception $e) {
			return -1;
	}
	}
	curl_close($ch);
};

?>
