<?php
	include_once 'includes/config.php'; // загружаем HOST, USER, PASSWORD
	include_once 'includes/mysql.php';
	
	header('Access-Control-Allow-Origin: *');
	header('Content-Type: application/json; charset=UTF-8');
	
	$qr_result = MysqlRequest('sc_history_db', 'SELECT * FROM lost_uids');
	
	$data = array();
	$result = mysql_num_rows($qr_result);
	while($row = mysql_fetch_array($qr_result)) {
		$data = array_merge_recursive($data, array('uid' => $row['uid']));
	}
	
	$output = ['result' => $result, 'text' => 'ok', 'data' => $data];
	echo json_encode($output); // и отдаем как json
	
	
	
	
	
?>

























