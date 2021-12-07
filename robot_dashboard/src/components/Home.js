import React, { Component , useState , useEffect } from 'react'
import axios from 'axios'
import Paper from '@material-ui/core/Paper'
import Grid from '@mui/material/Grid'
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';

import {
  ArgumentAxis,
  ValueAxis,
  Chart,
  LineSeries,
  BarSeries,
  Title
} from '@devexpress/dx-react-chart-material-ui'
import { Animation } from '@devexpress/dx-react-chart'

var XMLParser = require('react-xml-parser');

const sleep = time => {
  return new Promise((resolve) => setTimeout(resolve, time));
};


const Home = () => {

  const [obstData, setObstData] = useState([])
  const [direction,setDirection] = useState(
    [{
      "argument": "Left","value":0
    },
    {
      "argument":"Right" , "value":0
    },
    {
      "argument":"Turn Around" , "value":0
    }]
  )

  const [button, setButton] = useState(false)
  
  useEffect(() => {
    func();
  }, [])

  const getAllData = async () => {
  
    const res = await axios.get('/Directions?rcn=4', {
      headers: {
          'X-M2M-ORIGIN': '2vCsok51z6:xB2p5Mj@N2',
          'Content-Type': 'application/json',
      }
    })
  
    var xml = new XMLParser().parseFromString(res.data);
          
    let instances = xml.getElementsByTagName('con')
    let new_num = instances.length
    let time = obstData.length*3
    
    let left = 0
    let right = 0
    let turnaround = 0

    for(let i=0;i<instances.length;i++){
      let val = instances[i].value
      if (val == "Left")left += 1
      else if (val == "Right") right += 1
      else if (val == "180") turnaround += 1
    }
    
    setObstData(obstData => [...obstData, {"argument": obstData.length*3 , "value": new_num}])
    setDirection([
      {
        "argument": "Left","value":left
      },
      {
        "argument":"Right" , "value":right
      },
      {
        "argument":"Turn Around" , "value":turnaround
      }
    ])

    console.log(direction)
    
  }

  const func = async () =>{
    while(true){
      getAllData();
      await sleep(3000);
    }
  }

  const toggleButton = async() =>{
    setButton(!button)
    let body;
    if (button == true){
      console.log(button)
      body = JSON.stringify({
        "m2m:cin":{
            "lbl":[
                "start"
            ],
            "con": "start"
        }
      })
    }
    
    else {
      console.log(button)
      body = JSON.stringify({
        "m2m:cin":{
            "lbl":[
                "stop"
            ],
            "con": "stop"
        }
      })
    }
    
    const res = await axios.post('/State', body , {
      headers: {
          'X-M2M-ORIGIN': '2vCsok51z6:xB2p5Mj@N2',
          'Content-Type': 'application/json;ty=4',
      }
    })
    .then(res => console.log('Sent  ',button))
    .catch(err => console.log('Error', err))
      
  }

  const setSpeedSlow = async() =>{
    
    const body = JSON.stringify({
      "m2m:cin":{
          "lbl":[
              "speed"
          ],
          "con": "slow"
      }
    })

    const res = await axios.post('/Speed', body , {
      headers: {
          'X-M2M-ORIGIN': '2vCsok51z6:xB2p5Mj@N2',
          'Content-Type': 'application/json;ty=4',
      }
    })
    .then(res => console.log('Sent  ',button))
    .catch(err => console.log('Error', err))
      
  }

  const setSpeedMedium = async() =>{
    
    const body = JSON.stringify({
      "m2m:cin":{
          "lbl":[
              "speed"
          ],
          "con": "medium"
      }
    })

    const res = await axios.post('/Speed', body , {
      headers: {
          'X-M2M-ORIGIN': '2vCsok51z6:xB2p5Mj@N2',
          'Content-Type': 'application/json;ty=4',
      }
    })
    .then(res => console.log('Sent  ',button))
    .catch(err => console.log('Error', err))
      
  }

  const setSpeedFast = async() =>{
    
    const body = JSON.stringify({
      "m2m:cin":{
          "lbl":[
              "speed"
          ],
          "con": "fast"
      }
    })

    const res = await axios.post('/Speed', body , {
      headers: {
          'X-M2M-ORIGIN': '2vCsok51z6:xB2p5Mj@N2',
          'Content-Type': 'application/json;ty=4',
      }
    })
    .then(res => console.log('Sent  ',button))
    .catch(err => console.log('Error', err))
      
  }

    return (

      <>

    <h1 margin>Dashboard</h1>
    <h3>Control the start/stop state of the robot from the dashboard:
    </h3>
    <Button style={{justifyContent: 'space-between'}} size="large" variant="contained" onClick={toggleButton} label={button?"Start":"Stop"}>
      {button? "Start":"Stop"}
    </Button>
    
    <br/>
    <br/>


    <h3>This data is obtained in real time as the robot explores its environment.
      The data is pushed and retrieved from the IIIT OM2M server.
    </h3>
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <Paper>
          <Chart
          data={obstData}
          >
            
          <ArgumentAxis>
          <Title text="Time"/>
          </ArgumentAxis>
          
          <ValueAxis>
            <Title text="Number of obstacles"/>
          </ValueAxis>
          
          <LineSeries valueField="value" argumentField="argument" />
          <Title text="Number of Obstacles Encountered VS Time (in s)" />
          </Chart>
        </Paper>
      </Grid>

      <Grid item xs={6}>
        <Paper>
          <Chart
            data={direction}
          >
            <ArgumentAxis>
            <Title text="Direction"/>
            </ArgumentAxis>
            
            <ValueAxis>
              <Title text="Number of occurences"/>
            </ValueAxis>

            <BarSeries
              valueField="value"
              argumentField="argument"
            />
            <Title text="Track of Robot Directions" />
            <Animation />
          </Chart>
        </Paper>
      </Grid>

    </Grid>
    <br></br>

      </>
    )
}

export default Home
