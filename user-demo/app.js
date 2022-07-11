const createError = require('http-errors');
const express = require('express');
const path = require('path');
const logger = require('morgan');
const promBundle = require("express-prom-bundle");

const jaegerEndpoint = process.env.JAEGER_EXPORTER_ENDPOINT || '';
if (isNaN(jaegerEndpoint)) {
const tracer = require('./tracing')('user-demo');
}

const indexRouter = require('./routes/index');
const usersRouter = require('./routes/users');
const crashRouter = require('./routes/crash');

const app = express();

function structuredLogFormat(tokens, req, res) {
  return JSON.stringify({
    'remote-address': tokens['remote-addr'](req, res),
    'time': tokens['date'](req, res, 'iso'),
    'method': tokens['method'](req, res),
    'url': tokens['url'](req, res),
    'http-version': tokens['http-version'](req, res),
    'status-code': tokens['status'](req, res),
    'content-length': tokens['res'](req, res, 'content-length'),
    'referrer': tokens['referrer'](req, res),
    'user-agent': tokens['user-agent'](req, res),
    'request-headers': req.headers,
  });
}

app.use(logger(structuredLogFormat));
app.use(promBundle({includeMethod: true, includePath: true}));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/crash', crashRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.json({'error': err});
});

module.exports = app;
