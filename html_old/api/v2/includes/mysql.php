<?php
	/**
	 * Дополнительные функции
	 */
	function MysqlRequest($db_name, $sql)
	{
		# Include config file and additional functions
		$mydir = dirname(__FILE__);
		include_once("$mydir/additional_functions.php");
		include_once("$mydir/config.php");
		
		# Create connect to DB
		$connect_to_db = mysqli_connect(HOST, USER, PASSWORD)
		or Error("Could not connect: " . mysqli_connect_error());
		
		# Select to DB
		mysqli_select_db($connect_to_db, $db_name)
		or Error("Could not select DB: " . mysqli_error($connect_to_db));
		
		# Request to DB
		$qr_result = mysqli_query($connect_to_db, $sql)
		or Error("Could not found: " . mysqli_error($connect_to_db));
		
		# Close to DB
		mysqli_close($connect_to_db);
		
		# Return result
		return $qr_result;
	}
?>