<?php
$count = count(glob('./img/*.png'));
echo number_format($count, 0, ',', '.');