<?php
	function HeaderGo($title, $description, $inputArray = array())
	{
		include_once('includes/additional_functions.php');
		
		echo('<head>');
		DisplayText('<title>' . $title . ' | schistory.space</title>');
		echo('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">');
		DisplayText('<meta name="description" content="' . $description . '">', $inputArray);
		echo('<link rel="stylesheet" type="text/css" href="site.css">');
		echo('</head>');
	}
?>























