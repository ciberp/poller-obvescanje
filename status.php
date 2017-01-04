<html >
  <head>
    <meta charset="UTF-8">
    <title>STANJE @K4</title>
        <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <html lang="en">
<head>
	<meta charset="utf-8" />
	<meta http-equiv="refresh" content="5; url=">
	<title>Table Style</title>
	<meta name="viewport" content="initial-scale=1.0; maximum-scale=1.0; width=device-width;">
</head>
<body>
<div class="table-title">
<h3>STANJE @K4</h3>
</div>
<table class="table-fill">
<thead>
<tr>
<th class="text-left">METRIKA</th>
<th class="text-left">VREDNOST</th>
<th class="text-left">OK</th>
<th class="text-left">NAPAKA</th>
<th class="text-left">ČAS</th>
</tr>
</thead>
<tbody class="table-hover">

<?php

function secondsToTime($seconds) {
    $dtF = new \DateTime('@0');
    $dtT = new \DateTime("@$seconds");
    return $dtF->diff($dtT)->format('%ad %hh %im %ss');
}

#$Settings = file_get_contents("/home/pi/scripts/poller_obve/obvescanje.json");
#$json_settings = json_decode($Settings, true);
#var_dump( $json_settings);

//Connecting to Redis server on localhost
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
#echo "Server is running: ".$redis->ping();
$json_settings = json_decode($redis -> get('obvescanje-status'), true);

#$StatesFail = file_get_contents("/home/pi/scripts/poller_obve/StatesFail.json");
#$json_states = json_decode($StatesFail, true);
$json_states = json_decode($redis -> get('obvescanje-FailStates'), true);

foreach ($json_states as $id => $timestamp) {
    echo '<tr>';

        foreach ($json_settings as $line) {
	    #echo var_dump($line);
	    foreach ($line as $skey => $sval) {
		if (($skey == 'id') and ($sval == $id)) {
		    echo "<td class=\"text-left\">$line[dev].$line[var]</td>";
		    echo "<td class=\"text-left\">$line[c]</td>";
		    echo "<td class=\"text-left\">$line[ok_op] $line[ok_value]</td>";
		    echo "<td class=\"text-left\">$line[fail_op] $line[fail_value]</td>";
		    $current_time = time();
		    $razlika = $current_time - $timestamp;
		    $razlika = secondsToTime($current_time - $timestamp);
		    echo "<td class=\"text-left\">$razlika</td>";
		}
	    }

	
	
    }
    echo '</tr>';
}

?>
</tbody>
</table>
  </body>
</html>