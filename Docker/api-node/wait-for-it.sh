#!/bin/bash
x=10
while [ $x -gt 0 ]
do
  sleep ls
  clear
  echo "$x seconds left"
  x=$(( $x - 1 ))
done