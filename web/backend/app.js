const express = require('express')
const app = express()
const morgan = require('morgan')
const cors = require('cors')
const axios = require('axios')

const config = require('./config')

app.use(morgan('dev'))
app.use(cors());
app.use(express.json())

const getData = async () => {
  const res = await axios.get('https://esw-onem2m.iiit.ac.in/~/in-cse/in-name/Team-11/Node-1/Data/?rcn=4', {
    headers: {
        'X-M2M-ORIGIN': config.M2M_SECRET,
        'Content-Type': 'application/json'
    }
  })
  const data = res.data;
  return data['m2m:cnt']['m2m:cin'];
}

app.get('/api/data', async (req, res) => {
  const data = await getData();
  res.json(data.length);
});

module.exports = app
