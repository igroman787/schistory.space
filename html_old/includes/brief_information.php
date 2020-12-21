<table border="1" style="margin-bottom: 10px;">
	<?php
		echo '<pre>'.print_r($data,true).'</pre>';
	?>
	<style type="text/css">
		#nohover:hover { background-color: rgba(166, 255, 112, 0.88); }
		#left_block { display: table; margin: 5px; float: left; margin: 0px; }
		#right_block { display: table; margin: 5px; margin: 0px; }
		#avatar { display: table; margin: 5px; border: 1px solid black; width: 128; height: 128; float: left; background-image: url(includes/avatar.jpeg);}
		#nick { display: table; margin: 5px; border: 1px solid black; width: 300; height: 50; }
		#time { display: table; margin: 5px; border: 1px solid black; width: 300; height: 72; }
		#pvp { display: table; margin: 5px; border: 1px solid black; width: 287; height: 128; }
	</style>
	<tr id="nohover">
		<td>
			<div id="left_block">
				<div id="avatar">
					<?php
						echo("<s2>" . $data["nickname"] . "</s2>");
					?>
				</div>
				<div id="nick">
					<?php
						$karma = $data["karma"];
						if ($karma > 0) {
							$karma = "<font color='green' style='font-weight: bold;'>" . nicenumber($karma) . "</font>";
						} else if ($karma < 0) {
							$karma = "<font color='red' style='font-weight: bold;'>" . nicenumber($karma) . "</font>";
						}
						DisplayText("<s1>dt_karma: $karma</s1><br>");
						DisplayText("<s1>dt_clanName: <font style='font-weight: bold;'>" . $data["clan"]["name"] . " [" . $data["clan"]["tag"] . "] " . "</font></s1>");
					?>
				</div>
				<div id="time">
					<?php
						$arr = second_v_date(intval($data["pvp"]["totalBattleTime"]/1000));
						$totalBT = $arr["days"] . "д. " . $arr["hours"] . "ч. " . $arr["minutes"] . "м. " . $arr["seconds"] . "с.";
						DisplayText("<s1>dt_totalBattleTime: <font style='font-weight: bold;'>" . $totalBT . "</font></s1><br>");
						DisplayText("<s1>dt_prestigeBonus: <font style='font-weight: bold;'>" . $data["prestigeBonus"]*100 . "</font></s1><br>");
						DisplayText("<s1>dt_effRating: <font style='font-weight: bold;'>" . nicenumber($data["effRating"]) . "</font></s1><br>");
					?>
				</div>
				
			</div>
			<div id="right_block">
				<div id="pvp">
					<?php
						DisplayText("<s1>dt_gamePlayed: <font style='font-weight: bold;'>" . nicenumber($data["pvp"]["gamePlayed"]) . "</font></s1><br>");
						DisplayText("<s1>dt_gameWin: <font style='font-weight: bold;'>" . nicenumber($data["pvp"]["gameWin"]) . "</font></s1><br>");
						
						$totalKill = intval($data["pvp"]["totalKill"]);
						$totalDeath = intval($data["pvp"]["totalDeath"]);
						$totalAssists = intval($data["pvp"]["totalAssists"]);
						$gameWin = intval($data["pvp"]["gameWin"]);
						$gamePlayed = intval($data["pvp"]["gamePlayed"]);
						
						if ($totalDeath == 0) {
							$totalDeath = 1;
						}
						if ($gamePlayed == 0) {
							$gamePlayed = 1;
						}
						if ($gamePlayed == $gameWin) {
							$gamePlayed = $gameWin + 1;
						}
			
						$kd = $totalKill / $totalDeath;
						$kd = round($kd, 2);
						$kda = ($totalKill + $totalAssists) / $totalDeath;
						$kda = round($kda, 2);
						$wr = $gameWin / $gamePlayed;
						$wr = round($wr, 2);
						$wl = $gameWin / ($gamePlayed - $gameWin);
						$wl = round($wl, 2);
						
						echo("<s1>K/D: <font style='font-weight: bold;'>" . $kd . "</font></s1><br>");
						echo("<s1>KDA: <font style='font-weight: bold;'>" . $kda . "</font></s1><br>");
						echo("<s1>WinRate: <font style='font-weight: bold;'>" . $wr*100 . "%</font></s1><br>");
						echo("<s1>W/L: <font style='font-weight: bold;'>" . $wl . "</font></s1><br>");
					?>
				</div>
			</div>
		</td>
	</tr>
</table>