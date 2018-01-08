top -b -n 5 -d.2 | grep "Cpu" |  tail -n 1 | awk '{ print($2)}'
free | grep Mem | awk '{print $3/$2 * 100.0}'
uptime