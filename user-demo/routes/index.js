const express = require('express');
const router = express.Router();
const os = require('os');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.send({
    hostname: os.hostname(),
    version: process.env.npm_package_version,
  });
});

module.exports = router;
