<html>
	
	<?php
		# input additional_functions
		include_once('includes/additional_functions.php');
	
		# input header
		include_once('includes/header.php');
		HeaderGo('dt_index_title', 'dt_index_description');
	?>
	
	<style>
	.body_slides{
		list-style:none;
		margin:0;
		padding:0;
		z-index:-2; 
		background:#000;}
	.body_slides,
	.body_slides:after{
		position: absolute;
		width:100%;
		height:128px;
		top:0px;
		left:0px;}
	.body_slides:after { 
		content: '';
		background: transparent url(includes/pattern.png) repeat top left;}

	@-webkit-keyframes anim_slides {
	0% {opacity:0;}
	6% {opacity:1;}
	24% {opacity:1;}
	30% {opacity:0;}
	100% {opacity:0;}
	}
	@-moz-keyframes anim_slides {
	0% {opacity:0;}
	6% {opacity:1;}
	24% {opacity:1;}
	30% {opacity:0;}
	100% {opacity:0;}
	}
	.body_slides li{
		width:100%;
		height:100%;
		position:absolute;
		top:0;
		left:0;
		background-size:cover;
		background-repeat:none;
		background-position:center;
		opacity:0;
		-webkit-animation: anim_slides 18s linear infinite 0s;
		-moz-animation: anim_slides 18s linear infinite 0s;
		-o-animation: anim_slides 18s linear infinite 0s;
		-ms-animation: anim_slides 18s linear infinite 0s;
		animation: anim_slides 18s linear infinite 0s;
	}
	  
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
				<li></li>
				<li></li>
				<li></li>
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
					<?php DisplayText("<input type='submit' class='button' value='dt_find_button_text'/>") ?>
					<div>
						<select name="sort" style="margin-left: 3px;">
							<?php
								DisplayText("<option disabled>dt_findusers_form_select_sort_text:</option>");
								
								$sort_str = 'nickname, uid, kd, kd2, kda, kda2, wr, wr2, wl, wl2, effRating, effRating2, karma, karma2, prestigeBonus, prestigeBonus2, gamePlayed, gamePlayed2, gameWin, gameWin2, totalAssists, totalAssists2, totalBattleTime, totalBattleTime2, totalDeath, totalDeath2, totalDmgDone, totalDmgDone2, totalHealingDone, totalHealingDone2, totalKill, totalKill2, totalVpDmgDone, totalVpDmgDone2, clanName, clanTag';
								$sort_str = str_replace(' ','',$sort_str);
								$sort_list = explode(',', $sort_str);
								
								foreach ($sort_list as &$value) {
									echo('<option value="' . $value . '">' . $value . '</option>');
								}
							?>
						</select>
						<select name="DESC" style="margin-left: 3px;">
							<?php DisplayText("<option disabled>dt_findusers_form_select_desc_text:</option>") ?>
							<?php DisplayText("<option selected value=''>dt_findusers_form_select_desc_option1_text</option>") ?>
							<?php DisplayText("<option value=' DESC'>dt_findusers_form_select_desc_option2_text</option>") ?>
						</select>
						<select name="limit" style="margin-left: 3px;">
							<?php DisplayText("<option disabled>dt_findusers_form_select_limit_text:</option>") ?>
							<option selected value="50">50</option>
							<option value="100">100</option>
							<option value="500">500</option>
							<option value="1000">1000</option>
							<option value="3000">3000</option>
							<option value="5000">5000</option>
						</select>
					</div>
				</form>
			</div>
			<div id="right">
				<?php DisplayText("<s2>dt_user_history_form_text</s2><br/>") ?>
				<?php DisplayText("<s0>dt_user_history_form_mini_text_step1") ?>
				<?php echo(nicenumber(UserNumbers())) ?>
				<?php DisplayText("dt_user_history_form_mini_text_step2</s0>") ?>
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
				<?php ArrayToTable2(top100("gamePlayed2, gameWin2"), "gamePlayed2, gameWin2") ?>
			</div>
            <div id="mid">
                <?php // TODO для _kb2_ нужно вставить текст типа "лучшие убивцы за сутки" в таблицу трансляции
                DisplayText("<s2>dt_top100_kb2_text</s2>") ?>
                <?php ArrayToTable2(top100("kb2",5000, 10, true), "kb2") ?>
            </div>
			<div id="right">
				<?php DisplayText("<s2>dt_top100_kd2_text</s2>") ?>
				<?php // отсекаем из топа педобиров и статистически недостаточно сыгравших
                ArrayToTable2(top100("kd2", 5000, 10), "kd2") ?>
			</div>
        </div>
	</body>
	
	<?php
		# input footer
		include_once('includes/footer.php');
	?>
	
</html>

<?php
	function RandomImage() {
		$dir = "/var/www/html/downloads/images/";
		$files = scandir($dir);
		$arr = array();
		foreach ($files as &$value) {
			$info = new SplFileInfo($value);
			if ($info->getExtension() == "jpg") {
				array_push($arr, "/downloads/images/". $value);
			}
		}
		$rd = rand(0, count($arr)-1);
		
		return $arr[$rd];
	}
	
	function UserNumbers() {
		include_once 'includes/mysql.php';
		
		$qr_result = MysqlRequest("sc_history_db", "SELECT * FROM nickname_uid");
		$result = mysql_num_rows($qr_result);
		
		return $result;
	}
	
	function top100($sort, $minEffRate=0, $minGamePlayed=0, $kb = false) {
		include_once 'includes/mysql.php';
		if ($minEffRate !== 0) {
		    if ($kb === false) {
                $sql = "SELECT * FROM top100 WHERE gamePlayed!=gamePlayed2 AND gamePlayed2>" .$minGamePlayed. " AND effRating>" . $minEffRate . " ORDER BY " . $sort .  " DESC LIMIT 100";
            } else {
		        // если включен флаг kb вычисляем доп поле убийств за бой в день. *1.0 для приведения целого к float
                $sql = "SELECT uid, nickname, clanTag, (ROUND( (totalKill2*1.0 / gamePlayed2*1.0), 2) as kb2) FROM top100 WHERE gamePlayed!=gamePlayed2 AND gamePlayed2>" .$minGamePlayed. " AND effRating>" . $minEffRate . " ORDER BY " . $sort .  " DESC LIMIT 100";
            }

        } else {
		$sql = "SELECT * FROM top100 WHERE gamePlayed!=gamePlayed2 ORDER BY " . $sort .  " DESC LIMIT 100";
		}
		$qr_result = MysqlRequest("sc_history_db", $sql);
		
		$outputArray = [];
		while($data = mysql_fetch_array($qr_result)){
			$outputArray = array_merge_recursive($outputArray, [$data]);
		}
		return $outputArray;
	}
	
	function ArrayToTable2($inputArray, $sort_str) {
		$sort_str = str_replace(' ','',$sort_str);
		$sort_list = explode(',', $sort_str);
		
		// выводим на страницу сайта заголовки HTML-таблицы
		echo('<table border="1">');
		echo('<thead>');
		echo('<tr>');
		
		if (empty($_COOKIE["defgameopt"])) {
			$defgameopt = "human";
		} else {
			$defgameopt = test_input($_COOKIE["defgameopt"]);
		}
		
		if ($defgameopt == "machine")
		{
		    // uid это техническая информация не нужная пользователям в рейтинге, IMHO
			DisplayText('<th>nickname</th>');
			DisplayText('<th>clanTag</th>');
		} else {
			DisplayText('<th>dt_nickname</th>');
			DisplayText('<th>dt_clanTag</th>');
		}
		
		foreach ($sort_list as &$value) {
			if ($defgameopt == "machine")
			{
				DisplayText('<th>' . $value . '</th>');
			} else {
				DisplayText('<th>' . "dt_" . $value . '</th>');
			}
		}
		
		echo('</tr>');
		echo('</thead>');
		echo('<tbody>');
		
		// выводим в HTML-таблицу все данные клиентов из таблицы MySQL 
		foreach ($inputArray as &$data) { 
			echo('<tr>');
			echo('<td>' . '<a href="userinfo.php?uid=' . $data['uid'] . '" target="_blank">' . $data['nickname'] . '</a></td>');
			echo('<td>' . $data['clanTag'] . '</td>');
			foreach ($sort_list as &$value) {
				echo('<td>' . $data[$value] . '</td>');
			}
			echo('</tr>');
		}
		echo('</tbody>');
		echo('</table>');
	}
?>















