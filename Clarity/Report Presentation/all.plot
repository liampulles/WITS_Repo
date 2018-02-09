# Gnuplot script file for plotting data in file "force.dat"
# This file is called   force.p
set autoscale
unset log
#unset label
#unset key
set key on left top
set xtic auto
set ytic auto 
set title "Effect of threads on performance"
set ylabel "Time (ns)"
set xlabel "No. of threads"
#set xr [0:50000]
#set yr [0:7000]
#set xtics 5000000,10000000,80000000
#set ytics 0,1000,7000
set terminal png size 1280,720 enhanced
set output "threads.png"
plot	"4cores.txt" using 1:2 w linespoints t "4 core machine", \
	"8cores.txt" using 1:2 w points t "8 core machine"