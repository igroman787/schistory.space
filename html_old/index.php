<html>
	<!-- Including additional functions -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/additional_functions.php"); ?>
	<?php include_once("$mydir/api/v2/includes/mysql.php"); ?>

	<!-- Header -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/header.php"); ?>

	<!-- Slider stiles -->
	<style>
	.body_slides li:nth-child(1){
	<?php echo("background-image: url('" . RandomImage() . "')") ?>
	}
	.body_slides li:nth-child(2){
	-webkit-animation-delay: 6.0s;
	-moz-animation-delay: 6.0s;
	<?php echo("background-image: url('" . RandomImage() . "')") ?>
	}
	.body_slides li:nth-child(3){
	-webkit-animation-delay: 12.0s;
	-moz-animation-delay: 12.0s;
	<?php echo("background-image: url('" . RandomImage() . "')") ?>
	}
	</style>

	<body>
		<div id="slider">
			<ul class="body_slides">
				<li></li>
				<li></li>
				<li></li>
			</ul>
		</div>
		<div id="top" style="margin-top: 148px">
			<div id="left">
				<?php DisplayText("<s2>dt_findusers_form_text</s2><br/>") ?>
				<form action="findusers.php" method="get" autocomplete="off" style="display: inline;">
					<?php DisplayText("<input type='text' maxlength='100' size='50' placeholder='dt_findusers_form_input_text' name='search'/>") ?>
					<?php DisplayText("<input type='submit' class='button' value='dt_find_button_text' disabled/>") ?>
				</form>
			</div>
			<div id="right">
				<?php DisplayText("<s2>dt_user_history_form_text</s2><br/>") ?>
				<?php DisplayText("<s0>dt_user_history_form_mini_text:") ?>
				<?php echo(nicenumber(UserNumbers())) ?>
				<form action="userinfo.php" method="get" autocomplete="off">
					<?php DisplayText("<input type='text' maxlength='20' placeholder='dt_user_history_form_input1_text' name='nickname'/>") ?>
					<?php DisplayText("<input type='submit' class='button' value='dt_find_button_text'/>") ?>
				</form>
				<form action="userinfo.php" method="get" autocomplete="off">
					<?php DisplayText("<input type='text' maxlength='20' placeholder='dt_user_history_form_input2_text' name='uid'/>") ?>
					<?php DisplayText("<input type='submit' class='button' value='dt_find_button_text'/>") ?>
				</form>
			</div>
		</div>
		<div id="bottom" style="margin-top: 30px">
			<div id="left">
				<?php DisplayText("<s2>dt_top100_gamePlayed2_text</s2>") ?>
				<?php #ArrayToTable(GetTop100("gamePlayed2"), "gamePlayed2, gameWin2") ?>
			</div>
			<div id="right">
				<?php DisplayText("<s2>dt_top100_kd2_text</s2>") ?>
				<?php #ArrayToTable(GetTop100("kd2"), "kd2") ?>
			</div>
		</div>
	</body>

	<!-- Footer -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/footer.php"); ?>
</html>

<?php
	/**
	 * Дополнительные функции
	 */
	function RandomImage()
	{
		$dir = "includes/images/";
		$files = scandir($dir);
		$arr = array();
		foreach ($files as &$value)
		{
			$info = new SplFileInfo($value);
			if ($info->getExtension() == "jpg")
			{
				array_push($arr, $dir.$value);
			}
		}
		$rd = rand(0, count($arr)-1);
		return $arr[$rd];
	}
	function UserNumbers()
	{
		// Get row from DB
		$sql = "SELECT * FROM users ORDER BY uid DESC LIMIT 1";
		$qr_result = MysqlRequest("schistory", $sql);
		$item = mysqli_fetch_array($qr_result);
		return $item["uid"];
	}
	function GetTop100()
	{

	}
?>