<?php
	# Include config file, mysql library and additional functions
	include_once 'includes/additional_functions.php';
	include_once "includes/config.php"; // загружаем HOST, USER, PASSWORD
	include_once "includes/mysql.php";

	# Print headers
	header("Access-Control-Allow-Origin: *");
	header("Content-Type: application/json; charset=UTF-8");
	
	# Get row from DB
	$qr_result = MysqlRequest("schistory", "select name, UNIX_TIMESTAMP(datetime) as timestamp from times");

	# 
	$data = array();
	$result = mysqli_num_rows($qr_result);
	while($row = mysqli_fetch_array($qr_result)) {
		$name = $row["name"];
		$timestamp = (int)$row["timestamp"];
		if ($name == "startDataBaseUpdateTime") {
			$name = "RecordStartTime";
		} elseif ($name == "endDataBaseUpdateTime") {
			$name = "RecordEndTime";
		}
		$data = array_merge_recursive($data, array($name => $timestamp));
	}
	
	// Формируем вывод
	$output = ["result" => $result, "text" => "ok", "data" => $data];
	echo json_encode($output); // и отдаем как json
?>