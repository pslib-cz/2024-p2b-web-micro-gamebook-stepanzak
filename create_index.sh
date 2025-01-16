#!/usr/bin/env sh

cp ./game/skola/trida/zacatek.html ./index.html
#sed search for ../../../ and replace it with ./
sed -i 's/\.\.\/\.\.\/\.\.\//\.\//g' ./index.html

#sed search for ../../ and replace it with ./game/
sed -i 's/\.\.\/\.\.\//\.\/game\//g' ./index.html
