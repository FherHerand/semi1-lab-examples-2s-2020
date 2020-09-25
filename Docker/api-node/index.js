// -*- mode: js; js-indent-level: 2; -*-
'use strict'
const express = require('express')
const mysql = require('mysql'); 
const dotenv = require('dotenv');
dotenv.config();

const app = express()
const port = process.env.PORT || 3000
const ip = process.env.IP || 'localhost'

const db_user = process.env.DB_USER || "root"
const db_password = process.env.DB_PASS || "root"
const db_host = process.env.DB_HOST || "172.17.0.2"//si solo es docker run, debo agregar la ip que me brinda el contenedor de docker
const db_name = process.env.DB_NAME || "db"

var conn = mysql.createConnection({
  host: db_host,
  user: db_user,
  password: db_password,
  database: db_name,
  port: 3306
});

conn.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

app.listen(port, () => {
  console.log(`Server is listening on http://${ip}:${port}`)
})

app.get('/', (req, res) => {
  res.send(`Server is listening on http://${ip}:${port}`)
})

app.get('/products', (req, res) => {
  conn.query('SELECT * FROM product', function (err, result) {
    if (err) throw err
    console.log(result)
    res.send(result)
  });
})
