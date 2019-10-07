<?php
	include_once 'includes/config.php'; // загружаем HOST, USER, PASSWORD
	
	header('Access-Control-Allow-Origin: *');
	header('Content-Type: application/json; charset=UTF-8');
	
	// определ¤ем начальные данные
	$db_name = 'other_db';
	$db_table_to_show = 'timestamps';
	
	// соедин¤емс¤ с сервером базы данных
	$connect_to_db = mysql_connect(HOST, USER, PASSWORD)
	or Error("Could not connect: " . mysql_error());
	
	// подключаемс§ к базе данных
	mysql_select_db($db_name, $connect_to_db)
	or Error("Could not select DB: " . mysql_error());
	
	// выбираем все значени¤ из таблицы
	$qr_result = mysql_query("SELECT * FROM " . $db_table_to_show)
	or Error('Could not find: ' . mysql_error());
	
	// закрываем соединение с сервером базы данных
	mysql_close($connect_to_db);
	
	$data = [];
	$result = mysql_num_rows($qr_result);
	while($row = mysql_fetch_array($qr_result)) {
		$nomination = $row['nomination'];
		$value = $row['value'];
		$data = array_merge_recursive($data, [$nomination => $value]);
	}
	
	// ‘ормируем вывод
	$output = ['result' => $result, 'text' => 'ok', 'data' => $data];
	echo json_encode($output); // и отдаем как json
	
	function Error($text) {
		$output = ['result' => -1, 'text' => $text, 'data' => null];
		echo json_encode($output);
		exit();
	}
?>