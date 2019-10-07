<html>

	<?php
		# input additional_functions
		include_once('includes/additional_functions.php');
	
		# input header
		include_once('includes/header.php');
		HeaderGo('dt_findusers_title', 'dt_findusers_description');
	?>
	
	<body>
		<form action="findusers.php" method="get" autocomplete="off" style="display: inline;">
			<?php DisplayText('<a href="index.php" class="button"/>dt_home</a>'); ?>
			<?php DisplayText("<input type='text' maxlength='100' size='50' placeholder='dt_findusers_form_input_text' name='search'/>") ?>
			<?php DisplayText("<input type='submit' class='button' value='dt_find_button_text'/>") ?>
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
		</form><br>
		<?php
			$search = $_GET['search'];
			$sort = test_input($_GET['sort']);
			$limit = test_input($_GET['limit']);
			$DESC = $_GET['DESC'];
			
			$sort_str = 'nickname, uid, kd, kd2, kda, kda2, wr, wr2, wl, wl2, effRating, effRating2, karma, karma2, prestigeBonus, prestigeBonus2, gamePlayed, gamePlayed2, gameWin, gameWin2, totalAssists, totalAssists2, totalBattleTime, totalBattleTime2, totalDeath, totalDeath2, totalDmgDone, totalDmgDone2, totalHealingDone, totalHealingDone2, totalKill, totalKill2, totalVpDmgDone, totalVpDmgDone2, clanName, clanTag';
			$sort_str = str_replace(' ','',$sort_str);
			$sort_list = explode(',', $sort_str);
			
			foreach ($sort_list as &$value) {
				if (strpos($search, $value) > -1) {
					$column_str .= $value . ',';
					#array_push($column_list, $value);
				}
			}
			$column_str = substr($column_str, 0, strlen($column_str)-1);
			$column_list = explode(',', $column_str);
			
			
			$dop_oreder = str_replace(',',', ',$column_str);
			
			// соединяемся с сервером базы данных
			$connect_to_db = mysql_connect(HOST, USER, PASSWORD)
			or die("Could not connect: " . mysql_error());
			
			// подключаемся к базе данных
			mysql_select_db("sc_history_db", $connect_to_db)
			or die("Could not select DB: " . mysql_error());
			
			// выбираем все значения из таблицы
			$sql = "SELECT * FROM top100 WHERE " . $search . " ORDER BY " . $sort . $DESC;
			$qr_result_num = mysql_query($sql)
			or usersNotFound($search);
			
			$sql = "SELECT * FROM top100 WHERE " . $search . " ORDER BY " . $sort . $DESC . " LIMIT " . $limit;
			$qr_result = mysql_query($sql)
			or usersNotFound($search);
			echo('найдено ' . mysql_num_rows($qr_result_num) . ' совпадений.');
			
			// выводим на страницу сайта заголовки HTML-таблицы
			DisplayText('<table border="1">');
			DisplayText('<thead>');
			DisplayText('<tr>');
			
			DisplayText('<th>uid</th>');
			DisplayText('<th>nickname</th>');
			foreach ($column_list as &$value) {
				DisplayText('<th>' . $value . '</th>');
			}
			

			DisplayText('</tr>');
			DisplayText('</thead>');
			DisplayText('<tbody>');
			
			// выводим в HTML-таблицу все данные клиентов из таблицы MySQL 
			while($data = mysql_fetch_array($qr_result)){ 
				echo('<tr>');
				
				echo('<td>' . '<a href="userinfo.php?uid=' . $data['uid'] . '" target="_blank">' . $data['uid'] . '</a></td>'); 
				echo('<td>' . $data['nickname'] . '</td>');
				foreach ($column_list as &$value) {
					echo('<td>' . $data[$value] . '</td>');
				}
				
				echo('</tr>');
			}
			
			DisplayText('</tbody>');
			DisplayText('</table>');
			
			// закрываем соединение с сервером базы данных
			mysql_close($connect_to_db);
			
		?>
	</body>
	
	<?php
		# input footer
		include_once('includes/footer.php');
	?>
	
	<?php
		function usersNotFound($inputText) {
			echo('Неправильный поисковый запрос "' . test_input($inputText) . '"');
			
			echo('<p><details>');
			echo('<summary style="cursor: pointer">Пример:</summary><br>');
			echo("gameWin>1000 - Отобразить игроков, у которых больше 1000 побед.<br>clanTag='WSP' - Отобразить игроков, которые состоят в корпорации с тэгом 'WSP'.<br>clanTag='WSP' and gameWin>1000 - Отобразить игроков, которые состоят в корпорации с тэгом 'WSP' и у которых больше 1000 побед.<br>totalKill>10000 or kd>2 and gameWin>1000 - Отобразить игроков, у которых больше 10к убийств или у которых K/D больше двух и больше 1000 побед.<br>wr>0.5 and clanTag='SCORP' or wr>0.5 and clanTag='WSP' - Отобразить игроков, из двух кланов, среди которых WinRate больше 50%<br>Так же в запросе можно использовать регулярные выражения, например:<br>nickname REGEXP '^Igro' - Найти всех пилотов, у которых никнейм начинается на 'Igro'.<br>nickname REGEXP '787$' - Или например мы помним только концовку никнейма и хотим узнать полностью никнейм.<br>nickname REGEXP 'eka' - Или мы помним только несколько букв из никнейма.");
			echo('</details>');
			
			echo('<p><details>');
			echo('<summary style="cursor: pointer">Допустимые параметры:</summary><br>');
			echo('nickname, uid, kd, kd2, kda, kda2, wr, wr2, wl, wl2, effRating, effRating2, karma, karma2, prestigeBonus, prestigeBonus2, gamePlayed, gamePlayed2, gameWin, gameWin2, totalAssists, totalAssists2, totalBattleTime, totalBattleTime2, totalDeath, totalDeath2, totalDmgDone, totalDmgDone2, totalHealingDone, totalHealingDone2, totalKill, totalKill2, totalVpDmgDone, totalVpDmgDone2, clanName, clanTag');
			echo('</details>');
			
			exit();
		}
	?>

</html>