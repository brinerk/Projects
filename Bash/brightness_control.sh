#!/bin/bash
let "disp=$(xrandr | grep -w connected | awk -F'[ +]' '{print $1}' | head -n 1)"
let "i=$(cat /home/chiisai/.bright)"
if [ "$1" = "+" ]; then
	let "i+=1"
	if [ "$i" = 10 ]; then
		exit 1
	else
		xrandr --output eDP --brightness 0.$i
		echo "$i" > /home/chiisai/.bright
	fi
elif [ "$1" = "-" ]; then
	let "i-=1"
	if [ "$i" = 0 ]; then
		exit 1
	else
		xrandr --output eDP --brightness 0.$i
		echo "$i" > /home/chiisai/.bright
	fi
elif [ "$1" = "r" ]; then
	xrandr --output eDP --brightness 0.$i
fi
