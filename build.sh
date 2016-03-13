#! /bin/sh

BIN=node_modules/.bin
SRC=website/src
STATIC=website/static/website/build

eslint ${SRC}/app.js
${BIN}/browserify ${SRC}/app.js --debug -t babelify | ${BIN}/exorcist ${STATIC}/app.js.map >${STATIC}/app.js
./manage.py collectstatic --no-input
