#! /bin/sh

BIN=node_modules/.bin
SRC=website/src
STATIC=website/static/website/build

${BIN}/watchify ${SRC}/app.js --debug -t babelify -o ${STATIC}/app.js &
./manage.py runserver
