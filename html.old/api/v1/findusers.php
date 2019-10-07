<?php
	include_once 'includes/config.php'; // загружаем HOST, USER, PASSWORD
	include_once 'counter.php'; // загружаем Counter
	counter_go('1');
	
	$search = $_GET['search'];
	$limit = $_GET['limit'];
	$sort = $_GET['sort'];
	$DESC = $_GET['DESC'];
	$options = $_GET['options'];
	
	// Параметры по умолчанию
	$defaultoptions = 'nickname,uid,kd,kd2,kda,kda2,wr,wr2,wl,wl2,effRating,effRating2,karma,karma2,prestigeBonus,prestigeBonus2,gamePlayed,gamePlayed2,gameWin,gameWin2,totalAssists,totalAssists2,totalBattleTime,totalBattleTime2,totalDeath,totalDeath2,totalDmgDone,totalDmgDone2,totalHealingDone,totalHealingDone2,totalKill,totalKill2,totalVpDmgDone,totalVpDmgDone2,clanName,clanTag';
	
	if (!isset($_GET['search'])) {
		Error('invalid request: ' . $_GET['search']);
	}
	if (!isset($_GET['limit']) or intval($limit)>300) {
		$limit = '300';
	}
	if (!isset($_GET['sort'])) {
		$sort = 'uid';
	}
	
	if (!isset($_GET['options']) or $options == 'max' or $options == 'all') {
		$options = $defaultoptions;
	}
	if ($options == 'min') {
		$options = 'uid,nickname';
	}
	$optionslist = explode(",", $options);
	$defaultoptionslist = explode(",", $defaultoptions);
	
	foreach($optionslist as &$value) {
		if (!in_array($value, $defaultoptionslist)) {
			$str = "unidentified options: " . $value;
			Error($str);
			exit();
		}
	}
	
	// определ¤ем начальные данные
	$db_name = 'sc_history_db';
	
	// соедин¤емс¤ с сервером базы данных
	$connect_to_db = mysql_connect(HOST, USER, PASSWORD)
	or Error("Could not connect: " . mysql_error());
	
	// подключаемс¤ к базе данных
	mysql_select_db($db_name, $connect_to_db)
	or Error("Could not select DB: " . mysql_error());
	
	// выбираем все значени¤ из таблицы
	$qr_result = mysql_query("SELECT * FROM top100 WHERE " . $search . " ORDER BY " . $sort . $DESC . " LIMIT " . $limit)
	or Error('Could not find: ' . mysql_error());
	
	// закрываем соединение с сервером базы данных
	mysql_close($connect_to_db);
	
	$bigdata = [];
	$result = mysql_num_rows($qr_result);
	while($data = mysql_fetch_array($qr_result)) {
		//$bigdata = array_merge_recursive($bigdata, [$data]);
		$buffer = [];
		foreach($optionslist as &$value) {
			$buffer[$value] = $data[$value];
		}
		$bigdata[] = $buffer;
	}
	
	// Формируем вывод
	$output = ['result' => $result, 'text' => 'ok', 'bigdata' => $bigdata];
	echo json_encode($output, JSON_FORCE_OBJECT); // и отдаем как json
	
	function Error($text) {
		$output = ['result' => -1, 'text' => $text, 'data' => null];
		echo json_encode($output, JSON_FORCE_OBJECT);
		exit();
	}
?>