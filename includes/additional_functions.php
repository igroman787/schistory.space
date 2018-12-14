<?php
	function second_v_date($sekund)
	{
		$dt = new DateTime('@' . $sekund);
		return array('days'    => $dt->format('z'),
					 'hours'   => $dt->format('G'),
					 'minutes' => $dt->format('i'),
					 'seconds' => $dt->format('s'));
	}
	function nicenumber($input) {
		return number_format($input, 0, ".", "&thinsp;");
	}
	function ArrayToTable($inputArray, $sort_str, $is_link = false) {
		$sort_str = str_replace(' ','',$sort_str);
		$sort_list = explode(',', $sort_str);
		
		if (empty($_COOKIE["defgameopt"])) {
			$defgameopt = "human";
		} else {
			$defgameopt = test_input($_COOKIE["defgameopt"]);
		}
		
		// выводим на страницу сайта заголовки HTML-таблицы
		echo('<table border="1">');
		echo('<thead>');
		
		foreach ($sort_list as &$machinevalue) {
			if ($defgameopt == "machine")
			{
				DisplayText('<th>' . $machinevalue . '</th>');
			} else {
				DisplayText('<th>' . "dt_" . $machinevalue . '</th>');
			}
		}
		
		echo('</tr>');
		echo('</thead>');
		echo('<tbody>');
		
		// выводим в HTML-таблицу все данные клиентов из таблицы MySQL 
		foreach ($inputArray as &$data) { 
			
			$totalKill = intval($data['totalKill']);
			$totalDeath = intval($data['totalDeath']);
			$totalAssists = intval($data['totalAssists']);
			$gameWin = intval($data['gameWin']);
			$gamePlayed = intval($data['gamePlayed']);
			
			if (empty($totalKill_old)) {
				$totalKill_old = 0;
			}
			if (empty($totalDeath_old)) {
				$totalDeath_old = 0;
			}
			if (empty($totalAssists_old)) {
				$totalAssists_old = 0;
			}
			if (empty($gameWin_old)) {
				$gameWin_old = 0;
			}
			if (empty($gamePlayed_old)) {
				$gamePlayed_old = 0;
			}

            if ($gamePlayed == 0) {
                $gamePlayed = 1;
            }

            $kb = $totalKill / $gamePlayed;
            $kb = round($kb, 2);
			$kd = $totalKill / $totalDeath;
			$kd = round($kd, 2);
			$kda = ($totalKill + $totalAssists) / $totalDeath;
			$kda = round($kda, 2);
			$wr = $gameWin / $gamePlayed;
			$wr = round($wr, 2);
			$wl = $gameWin / ($gamePlayed - $gameWin);
			$wl = round($wl, 2);
			
			$kd2_den = $totalDeath - $totalDeath_old;
			$kd2_num = $totalKill - $totalKill_old;
			if ($kd2_den == 0) {
				$kd2_den = 1;
			}
			$kd2 = $kd2_num / $kd2_den;
			$kd2 = round($kd2, 2);

            $kb2_den = $gamePlayed - $gamePlayed_old;
            $kb2_num = $totalKill - $totalKill_old;
            if ($kb2_den == 0) {
                $kb2_den = 1;
            }
            $kb2 = $kb2_num / $kb2_den;
            $kb2 = round($kb2, 2);

			$kda2_num = ($totalKill - $totalKill_old) + ($totalAssists - $totalAssists_old);
			$kda2_den = $totalDeath - $totalDeath_old;
			if ($kda2_den == 0) {
				$kda2_den = 1;
			}
			$kda2 = $kda2_num / $kda2_den;
			$kda2 = round($kda2, 2);
			
			$wr2_num = $gameWin - $gameWin_old;
			$wr2_den = $gamePlayed - $gamePlayed_old;
			if ($wr2_den == 0) {
				$wr2_den = 1;
			}
			$wr2 = $wr2_num / $wr2_den;
			$wr2 = round($wr2, 2);
			
			$wl2_num = $gameWin - $gameWin_old;
			$wl2_den = ($gamePlayed - $gamePlayed_old) - ($gameWin - $gameWin_old);
			if ($wl2_den == 0) {
				$wl2_den = 1;
			}
			$wl2 = $wl2_num / $wl2_den;
			$wl2 = round($wl2, 2);
			
			$gamePlayed2 = $gamePlayed - $gamePlayed_old;
			
			$totalKill_old = intval($data['totalKill']);
			$totalDeath_old = intval($data['totalDeath']);
			$totalAssists_old = intval($data['totalAssists']);
			$gameWin_old = intval($data['gameWin']);
			$gamePlayed_old = intval($data['gamePlayed']);
			
			$date = new DateTime($data['date']);
			$date->modify('-1 day');
			$date = $date->format('Y-m-d');
			
			echo('<tr>');
			
			foreach ($sort_list as &$machinevalue) {
				if ($machinevalue == "date") {
					echo('<td>' . $date . '</td>');
					// столбец UID выпилен потому что значение неизменно, UID в шапке
				} else if ($machinevalue == "gamePlayed2") {
					echo('<td>' . $gamePlayed2 . '</td>');
				} else if ($machinevalue == "kd") {
					echo('<td>' . $kd . '</td>');
				} else if ($machinevalue == "kd2") {
					echo('<td>' . $kd2 . '</td>');
				}  else if ($machinevalue == "kb") {
                    echo('<td>' . $kb . '</td>');
                } else if ($machinevalue == "kb2") {
                    echo('<td>' . $kb2 . '</td>');
                } else if ($machinevalue == "kda") {
					echo('<td>' . $kda . '</td>');
				} else if ($machinevalue == "kda2") {
					echo('<td>' . $kda2 . '</td>');
				} else if ($machinevalue == "wr") {
					echo('<td>' . $wr*100 . '%</td>');
				} else if ($machinevalue == "wr2") {
					echo('<td>' . $wr2*100 . '%</td>');
				} else if ($machinevalue == "wl") {
					echo('<td>' . $wl . '</td>');
				} else if ($machinevalue == "wl2") {
					echo('<td>' . $wl2 . '</td>');
				} else {
					echo('<td>' . $data[$machinevalue] . '</td>');
				}
			}
			echo('</tr>');
		}
		
		echo('<thead>');
		
		foreach ($sort_list as &$machinevalue) {
			if ($defgameopt == "machine")
			{
				DisplayText('<th>' . $machinevalue . '</th>');
			} else {
				DisplayText('<th>' . "dt_" . $machinevalue . '</th>');
			}
		}
		
		echo('</tr>');
		echo('</thead>');
		
		echo('</tbody>');
		echo('</table>');
	}
	
	function DisplayText($inputString, $inputArray = array())
	{
		#INSERT INTO other_db.translate (input, ru, en) VALUES ("dt_findusers_form_text", "Здесь можно найти пилотов Star Conflict по определенным параметрам", "Here you can find the pilots Star Conflict by certain parameters");
		
		$lang = GetLang();
		
		// заменить символы на пробелы
		$buffer = $inputString;
		$arr = array('"', "'", "|", "/", "=", "+", "-", "<", ">", ".", ",", ":", ";", "(", ")");
		foreach ($arr as &$value)
		{
			$buffer = str_replace($value, " ", $buffer);
		}
		
		// разделить на слова
		$outputString = $inputString;
		$buffer_arr = explode(" ", $buffer);
		foreach ($buffer_arr as &$value)
		{
			if (strpos($value, 'dt_') > -1)
			{
				$outputString = str_replace($value, Translate($value, $lang), $outputString);
			}
		}
		if (strpos($outputString, '%') > -1) {
			$outputString = ReplaceArray($outputString, $inputArray);
		}
		
		echo($outputString);
	}
	
	function ReplaceArray($inputString, $inputArray)
	{
		$outputString = $inputString;		
		$buffer_arr = explode(" ", $outputString);
		foreach ($buffer_arr as &$value)
		{
			$value = str_replace('.', '', $value);
			if (substr_count($value, '%') == 2)
			{
				$outputString = str_replace($value, $inputArray[$value], $outputString);
			}
		}
		
		return $outputString;
	}
	
	function GetLang()
	{
		if (empty($_COOKIE["lang"])) {
			if (empty($_SERVER['HTTP_ACCEPT_LANGUAGE'])) {
				$lang = "ru";
			} else {
				if (substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2) == "ru")
				{
					$lang = "ru";
				} else {
					$lang = "en";
				}
			}
		} else {
			$lang = test_input($_COOKIE["lang"]);
		}
		return $lang;
	}
	
	function Translate($inputString, $lang)
	{
		$outputString = $inputString;
		
		# input config
		include_once('includes/config.php');
		
		// соединяемся с сервером базы данных
		$connect_to_db = mysql_connect(HOST, USER, PASSWORD)
		or die("Could not connect: " . mysql_error());
		
		// подключаемся к базе данных
		mysql_select_db("other_db", $connect_to_db)
		or die("Could not select DB: " . mysql_error());
		
		// ставим кодировку
		$qr_result = mysql_query("SET NAMES utf8");
		
		// выбираем все значения из таблицы translate
		$db_table_to_show = 'translate';
		$sql = "SELECT " . $lang . " FROM " . $db_table_to_show . " WHERE BINARY input='" . $inputString . "'";
		$qr_result = mysql_query($sql)
		or die("Could not find: " . mysql_error());
		
		if (mysql_num_rows($qr_result) > 0)
		{
			while($data = mysql_fetch_array($qr_result)){ 
				$outputString = $data[$lang];
			}
		}
		
		// закрываем соединение с сервером базы данных
		mysql_close($connect_to_db);
		
		return $outputString;
	}

	
	
	function test_input($data) {
		$data = trim($data);
		$data = stripslashes($data);
		$data = htmlspecialchars($data);
		return $data;
	}
?>

























