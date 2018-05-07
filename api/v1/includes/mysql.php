<?php
	function MysqlRequest($db_name, $sql) {
		include_once 'includes/config.php';
		
		$connect_to_db = mysql_connect(HOST, USER, PASSWORD)
		or exit("Could not connect: " . mysql_error());
		
		mysql_select_db($db_name, $connect_to_db)
		or exit("Could not select DB: " . mysql_error());
		
		$qr_result = mysql_query($sql)
		or exit("Could not found: " . mysql_error());
		
		mysql_close($connect_to_db);
		
		return $qr_result;
	}
?>