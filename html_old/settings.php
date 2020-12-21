<html>
	<!-- Including additional functions -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/additional_functions.php"); ?>

	<!-- Header -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/header.php"); ?>

	<!-- Шапочка -->
	<?php DisplayText("<a href='index.php' class='button'/>dt_home_button_text</a>") ?>

	<!-- Главная программа -->
	<?php
		$arr = GetSettings();
		$language = $arr["language"];
		$columns = $arr["columns"];
		$limit = $arr["limit"];
	?>

	<!-- Отображение -->
	<div>
		<form action="includes/setsettings.php" method="post" autocomplete="off">
			<div>
				<?php DisplayText("<s2>dt_language_settings_form_text:</s2><br/>") ?>
				<?php DisplayText("<input type='text' size='5' value='$language' name='language'/><br/>") ?>
			</div>

			<div>
				<?php DisplayText("<s2>dt_columns_settings_form_text:</s2><br/>") ?>
				<?php DisplayText("<textarea rows='3' cols='62' name='columns'>$columns</textarea><br/>") ?>
			</div>

			<div>
				<?php DisplayText("<s2>dt_limit_settings_form_text:</s2><br/>") ?>
				<?php DisplayText("<input type='text' size='10' value='$limit' name='limit'/><br/>") ?>
			</div>
			<?php DisplayText("<input type='submit' class='button' value='dt_save_button_text'/>") ?>
		</form>
	</div>

	<!-- Footer -->
	<?php $mydir = dirname(__FILE__); ?>
	<?php include_once("$mydir/includes/footer.php"); ?>
</html>