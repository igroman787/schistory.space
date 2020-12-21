<?php
	/**
	 * Конфигурационные файлы
	 */
	# Include config file, mysql library and additional functions
	include_once "includes/additional_functions.php";
	include_once "includes/config.php"; // загружаем HOST, USER, PASSWORD
	include_once "includes/mysql.php";
	
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

	# Check if request correct
	if ($nickname == NULL and $uid == NULL)
	{
		Error("invalid request. Example: https://schistory.space/api/v1/userinfo.php?nickname=GOB");
	}
	
	// если uid не указан, узнаем его
	if ($uid == NULL)
	{
		$uid = FindUidFromNickname($nickname);
	}
	
	// Get row from DB
	$sql = "SELECT users.uid, usershistory.date, nicknames.nickname, others.effRating, others.prestigeBonus, others.accountRank, pvps.gamePlayed, pvps.gameWin, pvps.totalAssists, pvps.totalBattleTime, pvps.totalDeath, pvps.totalDmgDone, pvps.totalHealingDone, pvps.totalKill, pvps.totalVpDmgDone, openworlds.karma, usershistory.cid FROM users JOIN usershistory JOIN nicknames JOIN pvps JOIN openworlds JOIN others ON (users.uid=usershistory.uid AND usershistory.nid=nicknames.nid AND usershistory.pvpid=pvps.pvpid AND usershistory.openworldid=openworlds.openworldid AND usershistory.otherid=others.otherid) WHERE users.uid=$uid ORDER BY date LIMIT $limit OFFSET $offset";
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
	
	// Формируем вывод
	$output = ["result" => $result, "text" => "ok", "bigdata" => $bigdata];
	echo json_encode($output); // и отдаем как json


	/**
	 * Дополнительные функции
	 */
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
		list($code, $data) = GetDataFromSC($nickname);
		if($code == 0)
		{
			CheckIfNicknameInDB($nickname);
			$uid = $data["uid"];
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