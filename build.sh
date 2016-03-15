#! /bin/sh

PYTHON=bin/python
BIN=node_modules/.bin
SRC=website/src
STATIC=website/static/website/build

${BIN}/eslint ${SRC}/*.js
mkdir -p website/static/website/build
${BIN}/browserify ${SRC}/app.js --debug -t babelify | ${BIN}/exorcist ${STATIC}/app.js.map >${STATIC}/app.js
${PYTHON} ./manage.py collectstatic --no-input
${PYTHON} ./manage.py makemigrations website
${PYTHON} ./manage.py migrate
