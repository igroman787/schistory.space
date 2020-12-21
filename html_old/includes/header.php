<head>
	<!-- Including additional functions -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include("$mydir/../api/v2/includes/additional_functions.php"); ?>

	<!-- Check https -->
	

	<!-- Header -->
	<?php $requestUrl = TestInput($_SERVER["REQUEST_URI"]); ?>
	<?php $queryString = TestInput($_SERVER["QUERY_STRING"]); ?>
	<?php $myname = basename($requestUrl, '?' . $queryString); ?>
	<?php echo("<title>$myname | schistory.space</title>"); ?>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<link rel="stylesheet" type="text/css" href="site.css">
</head>