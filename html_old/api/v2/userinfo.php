<?php
	/**
	 * Конфигурационные файлы
	 */
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
	$nickname = GetVarFromHTTPGET("nickname", NULL);
	$uid = GetVarFromHTTPGET("uid", NULL);
	$limit = GetVarFromHTTPGET("limit", 300);
	$offset = GetVarFromHTTPGET("offset", 0);
	$startTime = GetTimestamp();

	# Check if request correct
	if ($nickname == NULL and $uid == NULL)
	{
		Error("invalid request. Example: https://schistory.space/api/v2/userinfo.php?nickname=GOB");
	}
	
	// если uid не указан, узнаем его
	if ($uid == NULL)
	{
		$uid = FindUidFromNickname($nickname);
	}
	
	// Get row from DB
	$sql = "SELECT users.uid, usershistory.date, nicknames.nickname, others.effRating, others.prestigeBonus, others.accountRank, pvps.gamePlayed, pvps.gameWin, pvps.totalAssists, pvps.totalBattleTime, pvps.totalDeath, pvps.totalDmgDone, pvps.totalHealingDone, pvps.totalKill, pvps.totalVpDmgDone, openworlds.karma, usershistory.cid FROM users JOIN usershistory JOIN nicknames JOIN pvps JOIN openworlds JOIN others ON (users.uid=usershistory.uid AND usershistory.nid=nicknames.nid AND usershistory.pvpid=pvps.pvpid AND usershistory.openworldid=openworlds.openworldid AND usershistory.otherid=others.otherid) WHERE users.uid=$uid ORDER BY date DESC LIMIT $limit OFFSET $offset";
	$qr_result = MysqlRequest("schistory", $sql);
	$result = mysqli_num_rows($qr_result);
	if ($result == 0)
	{
		Error("history is empty");
	}

	# 
	$bigdata = array();
	while($item = mysqli_fetch_array($qr_result))
	{
		$date = new DateTime($item["date"]);
		$date->modify("-1 day");
		$date = $date->format("Y-m-d");
		$arr = GetClan($item["cid"]);
		$data = array("date" => $date, "uid" => (int)$item["uid"], "nickname" => $item["nickname"], "effRating" => (int)$item["effRating"], "karma" => (int)$item["karma"], "prestigeBonus" => (float)$item["prestigeBonus"], "accountRank" => (int)$item["accountRank"], "gamePlayed" => (int)$item["gamePlayed"], "gameWin" => (int)$item["gameWin"], "totalAssists" => (int)$item["totalAssists"], "totalBattleTime" => (int)$item["totalBattleTime"], "totalDeath" => (int)$item["totalDeath"], "totalDmgDone" => (int)$item["totalDmgDone"], "totalHealingDone" => (int)$item["totalHealingDone"], "totalKill" => (int)$item["totalKill"], "totalVpDmgDone" => (int)$item["totalVpDmgDone"], "clanName" => $arr["name"], "clanTag" => $arr["tag"]);
		$bigdata = array_merge_recursive($bigdata, array($data));
	}
	$bigdata = array_reverse($bigdata);
	$bigdata = CalculateAdditionalVariables($bigdata);
	
	// Формируем вывод
	$endTime = GetTimestamp();
	$requestTime = $endTime - $startTime;
	$output = ["result" => $result, "text" => "ok", "requestTime" => $requestTime, "bigdata" => $bigdata];
	echo json_encode($output); // и отдаем как json


	/**
	 * Дополнительные функции
	 */
	function CalculateAdditionalVariables($inputArray)
	{
		foreach ($inputArray as &$data)
		{
			$totalKill = intval($data["totalKill"]);
			$totalDeath = intval($data["totalDeath"]);
			$totalAssists = intval($data["totalAssists"]);
			$gameWin = intval($data["gameWin"]);
			$gamePlayed = intval($data["gamePlayed"]);
			
			if (empty($totalKill_old))
			{
				$totalKill_old = 0;
			}
			if (empty($totalDeath_old))
			{
				$totalDeath_old = 0;
			}
			if (empty($totalAssists_old))
			{
				$totalAssists_old = 0;
			}
			if (empty($gameWin_old))
			{
				$gameWin_old = 0;
			}
			if (empty($gamePlayed_old))
			{
				$gamePlayed_old = 0;
			}
			
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
			if ($kd2_den == 0)
			{
				$kd2_den = 1;
			}
			$kd2 = $kd2_num / $kd2_den;
			$kd2 = round($kd2, 2);
			
			$kda2_num = ($totalKill - $totalKill_old) + ($totalAssists - $totalAssists_old);
			$kda2_den = $totalDeath - $totalDeath_old;
			if ($kda2_den == 0)
			{
				$kda2_den = 1;
			}
			$kda2 = $kda2_num / $kda2_den;
			$kda2 = round($kda2, 2);
			
			$wr2_num = $gameWin - $gameWin_old;
			$wr2_den = $gamePlayed - $gamePlayed_old;
			if ($wr2_den == 0)
			{
				$wr2_den = 1;
			}
			$wr2 = $wr2_num / $wr2_den;
			$wr2 = round($wr2, 2);
			
			$wl2_num = $gameWin - $gameWin_old;
			$wl2_den = ($gamePlayed - $gamePlayed_old) - ($gameWin - $gameWin_old);
			if ($wl2_den == 0)
			{
				$wl2_den = 1;
			}
			$wl2 = $wl2_num / $wl2_den;
			$wl2 = round($wl2, 2);
			
			$gamePlayed2 = $gamePlayed - $gamePlayed_old;
			
			$totalKill_old = intval($data["totalKill"]);
			$totalDeath_old = intval($data["totalDeath"]);
			$totalAssists_old = intval($data["totalAssists"]);
			$gameWin_old = intval($data["gameWin"]);
			$gamePlayed_old = intval($data["gamePlayed"]);

			$data["kd"] = $kd;
			$data["kda"] = $kda;
			$data["wr"] = $wr;
			$data["wl"] = $wl;
			$data["kd2"] = $kd2;
			$data["kda2"] = $kda2;
			$data["wr2"] = $wr2;
			$data["wl2"] = $wl2;
			$data["gamePlayed2"] = $gamePlayed2;
		}
		return $inputArray;
	}
	function GetDataFromSC($nickname)
	{
		$json = file_get_contents("http://gmt.star-conflict.com/pubapi/v1/userinfo.php?nickname=$nickname");
		$bigdata = json_decode($json, true);
		$code = $bigdata["code"];
		$data = $bigdata["data"];
		return [$code, $data];
	}
	function FindUidFromNickname($nickname)
	{
		$qr_result = MysqlRequest("schistory", "SELECT usershistory.uid, nicknames.nickname FROM usershistory JOIN nicknames ON (usershistory.nid=nicknames.nid) WHERE nickname='$nickname' ORDER BY usershistory.uhid DESC LIMIT 1");;
		$result = mysqli_num_rows($qr_result);
		if ($result > 0)
		{
			$item = mysqli_fetch_array($qr_result);
			$uid = $item["uid"];
			return $uid;
		}
		else
		{
			Error("invalid nickname");
		}
	}
	function CheckIfNicknameInDB($nickname)
	{
		$qr_result = MysqlRequest("schistory", "SELECT * FROM nicknames WHERE nickname='$nickname'");
		$result = mysqli_num_rows($qr_result);
		if($result == 0)
		{
			TcpSend($nickname);
			Error("add new nickname");
		}
	}
	function GetClan($cid)
	{
		if ($cid == NULL)
		{
			return;
		}
		$qr_result = MysqlRequest("schistory", "SELECT clans.cid, name, tag FROM clans JOIN clanshistory JOIN clannames ON (clans.cid=clanshistory.cid and clanshistory.cnid=clannames.cnid) WHERE clans.cid=$cid LIMIT 1");
		$item = mysqli_fetch_array($qr_result);
		$arr = array("name" => $item["name"], "tag" => $item["tag"]);
		return $arr;
	}
	function TcpSend($nickname)
	{
		// Создаём сокет TCP/IP.
		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($socket === false)
		{
			Error("Failed socket_create(): Error: " . socket_strerror(socket_last_error($socket)));
		}
		
		// Подключаемся
		$result = socket_connect($socket, "127.0.0.1", 4800);
		if ($result === false)
		{
			Error("Failed socket_connect(). Error: " . socket_strerror(socket_last_error($socket)));
		}
		
		// Передаем
		$in = "<nickname>" . $nickname . "</nickname>";
		socket_write($socket, $in, strlen($in));
		
		// Закрываем
		socket_close($socket);
	}
?>