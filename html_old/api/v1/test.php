<?php
	# Print headers
	header("Access-Control-Allow-Origin: *");
	header("Content-Type: application/json; charset=UTF-8");
	
	$input = file_get_contents("php://input");
	$input = json_decode($input, true);
	
	// Формируем вывод
	$data = array("_SERVER" => $_SERVER, "_GET" => $_GET, "_POST" => $_POST, "_COOKIE" => $_COOKIE, "input" => $input);
	$output = array("result" => 4, "text" => "ok", "data" => $data);
	echo json_encode($output); // и отдаем как json
	
?>