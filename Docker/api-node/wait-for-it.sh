#!/bin/bash
x=85
while [ $x -gt 0 ]
do
  sleep ls
  clear
  echo "$x seconds left"
  x=$(( $x - 1 ))
done
node /App/index.js