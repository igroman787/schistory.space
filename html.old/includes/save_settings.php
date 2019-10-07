<?php
	# input additional_functions
	include_once('additional_functions.php');
	//echo '<pre>'.print_r($_POST,true).'</pre>';
	
	// save lang settings
	$lang = test_input($_POST["lang"]);
	setcookie("lang", $lang, time()+63113904, "/");
	
	// save note settings
	$note = test_input($_POST["note"]);
	setcookie("note", $note, time()+63113904, "/");
	
	// save defgameopt settings
	$defgameopt = test_input($_POST["defgameopt"]);
	setcookie("defgameopt", $defgameopt, time()+63113904, "/");
	
	// save game parameters
	$file = file_get_contents("game_parameters.list");
	$file_arr = explode("\r\n", $file);
	$gamepar_arr = array();
	foreach ($file_arr as &$value)
	{
		$machinevalue = str_replace("dt_", "", $value);
		$buffer = test_input($_POST[$machinevalue]);
		if ($buffer == "check")
		{
			array_push($gamepar_arr, $machinevalue);
		}
	}
	$gamepar = implode(",", $gamepar_arr);
	setcookie("gamepar", $gamepar, time()+63113904, "/");
	
	// save limit
	$limit = test_input($_POST["limit"]);
	setcookie("limit", $limit, time()+63113904, "/");
	
	// Делаем реридект обратно
	header("Location: ". $_SERVER["HTTP_REFERER"]);
?>