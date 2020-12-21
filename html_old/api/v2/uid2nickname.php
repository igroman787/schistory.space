<?php
	/**
	 * Конфигурационные файлы
	 */
	# Include config file, mysql library and additional functions
	include_once("includes/additional_functions.php");
	include_once("includes/config.php"); // загружаем HOST, USER, PASSWORD
	include_once("includes/mysql.php");

	/**
	 * Главная программа
	 */
	# Print headers
	header("Access-Control-Allow-Origin: *");
	header("Content-Type: application/json; charset=UTF-8");

	# Get var from HTTP GET
	$uid = GetVarFromHTTPGET("uid", NULL);
	$startTime = GetTimestamp();

	# Check if request correct
	if ($uid == NULL)
	{
		Error("invalid request. Example: https://schistory.space/api/v2/uid2nickname.php?uid=796865");
	}
	
	# Get row from DB
	$qr_result = MysqlRequest("schistory", "SELECT users.uid AS uid, nicknames.nickname AS nickname, usershistory.date AS date FROM users JOIN nicknames JOIN usershistory ON (users.uid=usershistory.uid AND nicknames.nid=usershistory.nid) WHERE users.uid='$uid'");

	# 
	$bigdata = array();
	$result = mysqli_num_rows($qr_result);
	while($row = mysqli_fetch_array($qr_result))
	{
		$uid = $row["uid"];
		$nickname = $row["nickname"];
		$date = $row["date"];
		$data = array("uid" => $uid, "nickname" => $nickname, "date" => $date);
		$bigdata = array_merge_recursive($bigdata, array($data));
	}
	
	// Формируем вывод
	$endTime = GetTimestamp();
	$requestTime = $endTime - $startTime;
	$output = ["result" => $result, "text" => "ok", "requestTime" => $requestTime, "bigdata" => $bigdata];
	echo json_encode($output); // и отдаем как json
?>