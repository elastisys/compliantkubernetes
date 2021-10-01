const express = require('express');
const router = express.Router();
const os = require('os');

/* GET home page. */
router.get('/', function(req, res, next) {
  setTimeout(() => {
    throw new Error('something bad happened');
  }, 0);
});

module.exports = router;
