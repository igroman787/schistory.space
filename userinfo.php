<?php
	
	// выводим Мануал, если нет параметров
	if (empty($_GET['nickname']) and empty($_GET['uid'])) {
		header('Location: index.php');
		exit;
	}
	
	# input additional_functions
	include_once('includes/additional_functions.php');
	
	# input config
	include_once('includes/config.php');
	
	# input COOKIE and GET
	if (empty($_COOKIE["gamepar"])) {
		$gamepar = "nickname, clanName, clanTag, kd, kda, wr, wl, kd2, kda2, wr2, wl2, gamePlayed2";
	} else {
		$gamepar = test_input($_COOKIE["gamepar"]);
	}
	if (empty($_COOKIE["limit"])) {
		$limit = 1000;
	} else {
		$limit = test_input($_COOKIE["limit"]);
	}
	if (isset($_GET["nickname"])) {
		$nickname = test_input($_GET["nickname"]);
	}
	if (empty($_GET["uid"])) {
		$uid = FindUidFromnickname($nickname);
	} else {
		$uid = test_input($_GET["uid"]);
	}
	
	// соединяемся с сервером базы данных
	$connect_to_db = mysql_connect(HOST, USER, PASSWORD)
	or die("Could not connect: " . mysql_error());
	
	// подключаемся к базе данных
	mysql_select_db("sc_history_db", $connect_to_db)
	or die("Could not select DB: " . mysql_error());

	// выбираем все значения из таблицы uid
	$db_table_to_show = 'uid_' . $uid;
	$qr_result = mysql_query("SELECT * FROM " . $db_table_to_show . " ORDER BY date DESC LIMIT " . $limit)
	or die("Could not find: " . mysql_error());

	$outputArray = array();
	while($data = mysql_fetch_array($qr_result))
	{
		//echo '<pre>'.print_r($data,true).'</pre>';
		$outputArray = array_merge_recursive($outputArray, array($data));
	}
	$outputArray = array_reverse($outputArray);
	$buffer = array_reverse($outputArray)[0];
	
	// закрываем соединение с сервером базы данных
	mysql_close($connect_to_db);
	
	
	# input header
	include_once('includes/header.php');
	$head_arr = array('%nickname%' => $buffer['nickname'], '%karma%' => $buffer['karma'], '%clanName%' => $buffer['clanName'], '%gamePlayed%' => $buffer['gamePlayed'], '%gameWin%' => $buffer['gameWin']);
	HeaderGo('dt_userinfo_title ' . $buffer['nickname'] . ' Star Conflict', 'dt_userinfo_description', $head_arr);
	#echo '<pre>'.print_r($head_arr,true).'</pre>';
	
	// Шапочка
	DisplayText('<a href="index.php" class="button"/>dt_home</a>');
	echo('<form action="userinfo.php" method="get" autocomplete="off" style="display: inline-block;">');
	DisplayText('<input type="text" maxlength="20" placeholder="dt_user_history_form_input1_text" name="nickname"/>');
	DisplayText('<input type="submit" class="button" value="dt_find_button_text"/>');
	echo('</form>');
	
	// Выводим краткую информацию
	include_once('includes/brief_information.php');
	
	// Отображаем таблицу
	ArrayToTable($outputArray, "date, " . $gamepar);
	
	# input footer
	include_once('includes/footer.php');
	
	
	function FindUidFromNickname($nickname)
	{
		$webform = file_get_contents("http://gmt.star-conflict.com/pubapi/v1/userinfo.php?nickname=" . $nickname);
		if(strpos($webform, '"result":"ok"') !== False ) {
			$uidStartIndex = strpos($webform, '"uid":') + strlen('"uid":');
			$uid_n = substr($webform, $uidStartIndex);
			$uidEndIndex = strpos($uid_n, ',');
			
			$uid = substr($uid_n, 0, $uidEndIndex);
			
			$is_uid_fined = true;
		}
		if (!isset($is_uid_fined)) {
				$str = "<p>Пользователь '" . $nickname . "' не является жителем игровой вселенной Star Conflict.";
				DisplayText($str);
				FindNicknameInMySQL($nickname);
				exit();
			}
		return $uid;
	}
	function FindNicknameInMySQL($nickname) {
		// соединяемся с сервером базы данных
		$connect_to_db = mysql_connect(HOST, USER, PASSWORD)
		or die("Could not connect: " . mysql_error());
		
		// подключаемся к базе данных
		$db_name = 'sc_history_db';
		mysql_select_db($db_name, $connect_to_db)
		or die("Could not select DB: " . mysql_error());
		
		// выбираем все значения из таблицы
		$qr_result = mysql_query("SELECT * FROM nickname_uid WHERE nickname='" . $nickname . "'");
		
		$result = mysql_num_rows($qr_result);
		if ($result == 0) {
			return;
		}
		
		$str = "<p>Однако данный никнейм был использован ранее:<p>";
		DisplayText($str);
		
		// Выводим таблицу
		echo('<table border="1">');
		echo('<thead>');
		echo('<tr>');
		DisplayText('<th>uid</th>');
		DisplayText('<th>Old nickname</th>');
		echo('</tr>');
		echo('</thead>');
		echo('<tbody>');
		
		while($data = mysql_fetch_array($qr_result)){ 
			echo('<tr>');
			echo('<td>' . '<a href="userinfo.php?uid=' . $data['uid'] . '" target="_blank">' . $data['uid'] . '</a></td>'); 
			echo('<td>' . $data['nickname'] . '</td>');
			echo('</tr>');
		}
		echo('</tbody>');
		echo('</table>');
		
		// закрываем соединение с сервером базы данных
		mysql_close($connect_to_db);
	}
	
?>

















