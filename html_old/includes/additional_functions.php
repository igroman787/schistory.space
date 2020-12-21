<?php
	/**
	 * Дополнительные функции
	 */
	function GetSettings() {
		$language = GetVarFromCookies("language", NULL);
		$columns = GetVarFromCookies("columns", "date, uid, nickname, karma, gamePlayed, gamePlayed2, kd, kd2, kda, kda2, wr, wr2, wl, wl2");
		$limit = GetVarFromCookies("limit", "300");

		if ($language != "ru" && $language != "en" ) {
			$language = GetLanguage();
		}
		if ($limit > 1000 || $limit < 1) {
			$limit = 300;
		}

		$arr = array();
		$arr["language"] = $language;
		$arr["columns"] = $columns;
		$arr["limit"] = $limit;

		return $arr;
	}
	function GetVarFromCookies($varName, $defaultVar) {
		if (!isset($_COOKIE[$varName])) {
			$var = $defaultVar;
		} else {
			$var = TestInput($_COOKIE[$varName]);
		}
		return $var;
	}
	function ArrayToTable($arr) {
		if (count($arr) == 0) {
			return;
		}
		
		// Начало таблицы
		echo("<table border='1'>");
		
		// Вывод заголовка
		$header = $arr[0];
		echo("<tr>");
		foreach ($header as $key => $value)
		{
			echo("<th>" . $key . "</th>");
		}
		echo("</tr>");
		
		// Вывод строк
		for ($i = 0; $i < count($arr); $i++) {
			$line = $arr[$i];
			echo("<tr>");
			foreach($line as &$value)
			{
				echo("<td>" . $value . "</td>");
			}
			echo("</tr>");
		}
		
		// Вывод заголовка
		$header = $arr[0];
		echo("<tr>");
		foreach ($header as $key => $value) {
			echo("<th>" . $key . "</th>");
		}
		echo("</tr>");
		
		// Конец таблицы
		echo("</table>");
	}
	function second_v_date($seconds) {
		$dt = new DateTime('@' . $seconds);
		return array('days'    => $dt->format('z'),
					 'hours'   => $dt->format('G'),
					 'minutes' => $dt->format('i'),
					 'seconds' => $dt->format('s'));
	}
	function nicenumber($input)	{
		return number_format($input, 0, ".", "&thinsp;");
	}
	function DisplayText($inputString) {
		#INSERT INTO other_db.translate (input, ru, en) VALUES ("dt_findusers_form_text", "Здесь можно найти пилотов Star Conflict по определенным параметрам", "Here you can find the pilots Star Conflict by certain parameters");
		
		// заменить символы на пробелы
		$buffer = $inputString;
		$arr = array('"', "'", "|", "/", "=", "+", "-", "<", ">", ".", ",", ":", ";", "(", ")");
		foreach ($arr as &$value) {
			$buffer = str_replace($value, " ", $buffer);
		}
		
		// разделить на слова
		$outputString = $inputString;
		$buffer_arr = explode(" ", $buffer);
		foreach ($buffer_arr as &$value) {
			if (strpos($value, 'dt_') > -1) {
				$outputString = str_replace($value, Translate($value), $outputString);
			}
		}
		if (strpos($outputString, '%') > -1) {
			$outputString = ReplaceArray($outputString, $inputArray);
		}
		
		echo($outputString);
	}
	function ReplaceArray($inputString, $inputArray) {
		$outputString = $inputString;		
		$buffer_arr = explode(" ", $outputString);
		foreach ($buffer_arr as &$value) {
			$value = str_replace('.', '', $value);
			if (substr_count($value, '%') == 2) {
				$outputString = str_replace($value, $inputArray[$value], $outputString);
			}
		}
		return $outputString;
	}
	function GetLanguage() {
		if (empty($_SERVER["HTTP_ACCEPT_LANGUAGE"])) {
			$language = "ru";
		} else {
			if (substr($_SERVER["HTTP_ACCEPT_LANGUAGE"], 0, 2) == "ru") {
				$language = "ru";
			} else {
				$language = "en";
			}
		}
		return $language;
	}
	function Translate($inputString) {
		#INSERT INTO other_db.translate (input, ru, en) VALUES ("dt_findusers_form_text", "Здесь можно найти пилотов Star Conflict по определенным параметрам", "Here you can find the pilots Star Conflict by certain parameters");
		
		$arr = GetSettings();
		$language = $arr["language"];
		$outputString = $inputString;
		
		# input config
		$mydir = dirname(__FILE__);
		include_once("$mydir/../api/v2/includes/config.php");
		
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
		$sql = "SELECT " . $language . " FROM " . $db_table_to_show . " WHERE BINARY input='" . $inputString . "'";
		$qr_result = mysql_query($sql)
		or die("Could not find: " . mysql_error());
		
		if (mysql_num_rows($qr_result) > 0) {
			while($data = mysql_fetch_array($qr_result)) { 
				$outputString = $data[$language];
			}
		}
		
		// закрываем соединение с сервером базы данных
		mysql_close($connect_to_db);
		
		return $outputString;
	}
?>

























