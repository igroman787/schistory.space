<table border="1" style="margin-bottom: 10px;">
	<?php
		#$buffer = array_reverse($outputArray)[0];
		#echo '<pre>'.print_r($buffer,true).'</pre>';
	?>
	<style type="text/css">
		#nohover:hover { background-color: rgba(166, 255, 112, 0.88); }
		#left_block { display: table; margin: 5px; float: left; margin: 0px; }
		#right_block { display: table; margin: 5px; margin: 0px; }
		#avatar { display: table; margin: 5px; border: 1px solid black; width: 128; height: 128; float: left; background-image: url(includes/avatar.jpeg);}
		#nick { display: table; margin: 5px; border: 1px solid black; width: 300; height: 50; }
		#time { display: table; margin: 5px; border: 1px solid black; width: 300; height: 72; }
		#pvp { display: table; margin: 5px; border: 1px solid black; width: 287; height: 128; }
		#ad { display: table; margin: 5px; width: 736; height: 90; }
	</style>
	<tr id="nohover">
		<td>
			<div id="left_block">
				<div id="avatar">
					<?php
						echo("<s2>" . $buffer['nickname'] . "</s2>");
					?>
				</div>
				<div id="nick">
					<?php
						$karma = $buffer['karma'];
						if ($karma > 0) {
							$karma = "<font color='green' style='font-weight: bold;'>" . nicenumber($karma) . "</font>";
						} else if ($karma < 0) {
							$karma = "<font color='red' style='font-weight: bold;'>" . nicenumber($karma) . "</font>";
						}
						DisplayText("<s1>dt_karma: " . $karma . "</s1><br>");
						DisplayText("<s1>dt_clanName: <font style='font-weight: bold;'>" . $buffer['clanName'] . " [" . $buffer['clanTag'] . "] " . "</font></s1>");
					?>
				</div>
				<div id="time">
					<?php
						$arr = second_v_date(intval($buffer['totalBattleTime']/1000));
						$totalBT = $arr['days'] . "д. " . $arr['hours'] . "ч. " . $arr['minutes'] . "м. " . $arr['seconds'] . "с.";
						DisplayText("<s1>dt_totalBattleTime: <font style='font-weight: bold;'>" . $totalBT . "</font></s1><br>");
						DisplayText("<s1>dt_prestigeBonus: <font style='font-weight: bold;'>" . $buffer['prestigeBonus']*100 . "</font></s1><br>");
						DisplayText("<s1>dt_effRating: <font style='font-weight: bold;'>" . nicenumber($buffer['effRating']) . "</font></s1><br>");
					?>
				</div>
				
			</div>
			<div id="right_block">
				<div id="pvp">
					<?php
						DisplayText("<s1>dt_gamePlayed: <font style='font-weight: bold;'>" . nicenumber($buffer['gamePlayed']) . "</font></s1><br>");
						DisplayText("<s1>dt_gameWin: <font style='font-weight: bold;'>" . nicenumber($buffer['gameWin']) . "</font></s1><br>");
						
						$totalKill = intval($buffer['totalKill']);
						$totalDeath = intval($buffer['totalDeath']);
						$totalAssists = intval($buffer['totalAssists']);
						$gameWin = intval($buffer['gameWin']);
						$gamePlayed = intval($buffer['gamePlayed']);
						
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
			<div id="ad">
				<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
				<ins class="adsbygoogle"
					 style="display:inline-block;width:728px;height:90px"
					 data-ad-client="ca-pub-2218108246816430"
					 data-ad-slot="8094381862"></ins>
				<script>
					(adsbygoogle = window.adsbygoogle || []).push({});
				</script>
			</div>
		</td>
	</tr>
</table>