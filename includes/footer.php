<div style="margin-bottom: 50px"></div>
<footer>
	<div class="poster">
		<?php DisplayText("<s2>dt_footer_poster1_text</s2>") ?>
		<div class="descr">
			<a href="http://t.me/star_conflict_chat_bot" target="_blank">Star Conflict Fun Chat</a> автор <a href="https://forum.star-conflict.ru/index.php?/topic/59734-star-conflict-fun-chat/" target="_blank">StarDen</a><br>
			<a href="http://it4ly.altervista.org/" target="_blank">Калькулятор статистики игроков</a> автор <a href="https://forum.star-conflict.ru/index.php?/topic/57855-kalkulyator-statistiki-igrokov/" target="_blank">ITalianBadBoy</a><br>
			<a href="http://g920448m.bget.ru/scsig/1/ffffff/0/NAME.jpg" target="_blank">Генератор сигнатур автообновляемый</a> автор <a href="https://forum.star-conflict.ru/index.php?/topic/46434-%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80-%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D1%82%D1%83%D1%80-%D0%B0%D0%B2%D1%82%D0%BE%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D0%B9/" target="_blank">SilverWF</a><br>
			<a href="http://sc-userbar.ru/" target="_blank">Инструмент по созданию аватар и юзербаров от Eta</a> автор <a href="https://forum.star-conflict.ru/index.php?/topic/41352-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82-%D0%BF%D0%BE-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D1%8E-%D0%B0%D0%B2%D0%B0%D1%82%D0%B0%D1%80-%D0%B8-%D1%8E%D0%B7%D0%B5%D1%80%D0%B1%D0%B0%D1%80%D0%BE%D0%B2-%D0%BE%D1%82-eta/" target="_blank">Cyrus15</a><br>
			<a href="https://youtu.be/Odp2QvdfshQ" target="_blank">Шикарный трейлер Star Conflict</a> автор <a href="https://forum.star-conflict.ru/index.php?/topic/59563-sc-journey-fan-treiler/" target="_blank">_Mirolog_</a><br>
		</div>
	</div>
	<div class="poster">
		<?php DisplayText("<s2>Музыка</s2>") ?>
		<div class="descr">
			<script src="/includes/audiojs/audio.min.js"></script>
			<script>
				audiojs.events.ready(function() {
					var as = audiojs.createAll();
				});
			</script>
			<?php
				$files = scandir("/var/www/html/downloads/music/");
				foreach ($files as &$value) {
					$info = new SplFileInfo($value);
					if ($info->getExtension() == "mp3") {
						echo("<audio src='/downloads/music/" . $value . "' preload='none' />");
					}
				}
			?>
		</div>
	</div>
	<div class="poster">
		<?php DisplayText("<s2>dt_footer_poster2_text</s2>") ?>
		<div class="descr">
			<form action="includes/save_settings.php" method="post" autocomplete="off">
				<select name="lang" style="margin-left: 10px;">
					<?php DisplayText("<option disabled>dt_footer_poster2_descr1_text:</option>") ?>
					<?php DisplayText("<option selected value='ru'>dt_ru</option>") ?>
					<?php DisplayText("<option value='en'>dt_en</option>") ?>
				</select>
				<select name="defgameopt" style="margin-left: 10px;">
					<?php DisplayText("<option disabled>dt_footer_poster2_descr3_text:</option>") ?>
					<?php DisplayText("<option selected value='human'>dt_human</option>") ?>
					<?php DisplayText("<option value='machine'>dt_machine</option>") ?>
				</select>
				<select name="limit" style="margin-left: 3px;">
					<?php DisplayText("<option disabled>dt_findusers_form_select_limit_text:</option>") ?>
					<option selected value="14">14</option>
					<option value="50">30</option>
					<option value="100">60</option>
					<option value="500">90</option>
					<option value="1000">180</option>
					<option value="3000">365</option>
					<option value="5000">1000</option>
				</select>
				<br>
				<div style="overflow-y: scroll; height: 140; margin: 5; background-color: rgba(244, 244, 244, 0.98); border-style: solid; border-color: #a7a7a7; border-radius: 1px; border-width: 1px;">
					<?php
						$file = file_get_contents("includes/game_parameters.list");
						$parameters_arr = explode("\r\n", $file);
						foreach ($parameters_arr as &$value)
						{
							if (empty($_COOKIE["defgameopt"])) {
								$defgameopt = "machine";
							} else {
								$defgameopt = test_input($_COOKIE["defgameopt"]);
							}
							$machinevalue = str_replace("dt_", "", $value);
							if ($defgameopt == "machine")
							{
								$text = $machinevalue;
							} else {
								$text = $value;
							}
							DisplayText("<input type='checkbox' name='" . $machinevalue . "' value='check' /><s1> " . $text . " </s1><br>");
						}
					?>
				</div>
				
				<?php DisplayText("<input type='submit' class='button' value='dt_save' style='position: absolute; bottom: 10px; right: 10px;'/>") ?>
				
		</div>
	</div>
	<div class="poster">
		<?php DisplayText("<s2>dt_footer_poster3_text</s2>") ?>
		<div class="descr">
			<?php
				DisplayText('Обсуждение данного проекта <a href="https://forum.star-conflict.ru/index.php?/topic/60434-istoriya-pilotov-star-conflict-istoriya-sc-v20/" target="_blank">на форуме SC</a><br>');
				
				$df = disk_free_space("/");
				$ds = disk_total_space("/");
				$freespace = round($df/$ds*100, 2);
				$loadspace = 100 - $freespace;
				if ($loadspace > 90) {
					$color = 'red';
				} elseif ($loadspace > 75) {
					$color = 'darkorange';
				} else {
					$color = 'limegreen';
				}
				DisplayText('dt_footer_poster3_descr1_part1_text: dt_footer_poster3_descr1_part2_text <font style="color: ' . $color . ';">' . $loadspace . '%</font><br>');
			?>
		</div>
	</div>
</footer>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-115916473-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-115916473-1');
</script>
