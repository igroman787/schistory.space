<?php
	# Include config file, mysql library and additional functions
	include_once 'includes/additional_functions.php';
	include_once "includes/config.php"; // загружаем HOST, USER, PASSWORD
	include_once "includes/mysql.php";
	
	# Print headers
	header("Access-Control-Allow-Origin: *");
	header("Content-Type: application/json; charset=UTF-8");
	
	# Get var from HTTP GET
	$limit = GetVarFromHTTPGET("limit", 300);
	$offset = GetVarFromHTTPGET("offset", 0);

	# Get row from DB
	$qr_result = MysqlRequest("schistory", "SELECT * FROM lostuids LIMIT $limit OFFSET $offset");
	
	# 
	$data = array("uid" => array());
	$result = mysqli_num_rows($qr_result);
	while ($row = mysqli_fetch_array($qr_result)) {
		$data = array_merge_recursive($data, array("uid" => $row["uid"]));
	}
	
	// Формируем вывод
	$output = ["result" => $result, "text" => "ok", "data" => $data];
	echo json_encode($output); // и отдаем как json
	
	
?>