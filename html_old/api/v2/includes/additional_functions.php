<?php
	/**
	 * Дополнительные функции
	 */
	function GetVarFromHTTPGET($varName, $defaultVar)
	{
		if (!isset($_GET[$varName]))
		{
			$var = $defaultVar;
		}
		else
		{
			$var = TestInput($_GET[$varName]);
		}
		return $var;
	}
	function GetTimestamp()
	{
		$date = date_create();
		return date_timestamp_get($date);
	}
	function Error($text)
	{
		$output = ["result" => -1, "text" => $text, "data" => null];
		echo json_encode($output);
		exit();
	}
	function TestInput($data)
	{
		$data = trim($data);
		$data = stripslashes($data);
		$data = htmlspecialchars($data);
		return $data;
	}
	function DebugPrint($var)
	{
		#echo("<pre>");
		print_r($var);
		#echo("</pre>");
	}
?>