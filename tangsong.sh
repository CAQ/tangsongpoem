#!/bin/sh
cd "/home/caq/fortune-zh-1.9/"
fortune tang300 | tr -d ["\133 \033 \063 \062 \155"] > tang.poem
fortune song100 | tr -d ["\133 \033 \063 \062 \155"] > song.poem
/usr/bin/python tangsong.py
