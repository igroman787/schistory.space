<?php
	# Include additional functions
	$mydir = dirname(__FILE__);
	include_once("$mydir/../api/v2/includes/additional_functions.php");
	
	// Save language settings
	$language = TestInput($_POST["language"]);
	setcookie("language", $language, time()+63113904, "/");
	
	// Save columns settings
	$columns = TestInput($_POST["columns"]);
	setcookie("columns", $columns, time()+63113904, "/");

	// Save limit
	$limit = TestInput($_POST["limit"]);
	setcookie("limit", $limit, time()+63113904, "/");

	// Делаем реридект обратно
	header("Location: ". TestInput($_SERVER["HTTP_REFERER"]));
?>