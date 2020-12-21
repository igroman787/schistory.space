<html>
	<!-- Including additional functions -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/additional_functions.php"); ?>

	<!-- Header -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/header.php"); ?>

	<!-- Шапочка -->
	<?php DisplayText("<a href='index.php' class='button'/>dt_home_button_text</a>"); ?>
	<form action="userinfo.php" method="get" autocomplete="off" style="display: inline-block;">
		<?php DisplayText("<input type='text' maxlength='20' placeholder='dt_user_history_form_input1_text' name='nickname'/>"); ?>
		<?php DisplayText("<input type='submit' class='button' value='dt_find_button_text'/>"); ?>
	</form>

	<!-- Главная программа -->
	<?php
		# Get settings
		$arr = GetSettings();
		$columns = $arr["columns"];
		$limit = $arr["limit"];

		# Get data from schistory api
		$url = "http://127.0.0.1:8007/api/v2/userinfo.php?".http_build_query($_GET)."&limit=$limit";
		$result = file_get_contents($url);
		$data = json_decode($result, true);
		$bigdata = $data["bigdata"];

		# Prepare data
		$outputBigdata = array();
		$columns = trim(preg_replace('/\s\s+/', ' ', $columns));
		$columns = str_replace(' ', '', $columns);
		$columns = explode(',', $columns);
		foreach ($bigdata as $line) {
			$data = array();
			foreach ($columns as $key) {
				if (in_array($key, $columns)) {
					$data[$key] = $line[$key];
				}
			}
			$outputBigdata = array_merge_recursive($outputBigdata, array($data));
		}

		# Get data from sc api
		$data = $bigdata[0];
	?>

	<!-- Отображение -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/brief_information.php"); ?>
	<?php ArrayToTable($outputBigdata); ?>

	<!-- Footer -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/footer.php"); ?>
</html>