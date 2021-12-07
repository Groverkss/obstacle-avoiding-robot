import React, { Component } from 'react'
import axios from 'axios'
import { useNavigate } from "react-router-dom";

import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';


const bcrypt = require('bcryptjs');
const theme = createTheme();
var XMLParser = require('react-xml-parser');

const Login = () => {
    const navigate = useNavigate();

    const handleSubmit = async (event) => {

      event.preventDefault();
        const data = new FormData(event.currentTarget);
        
    
        let email= data.get('name')
        let password= data.get('password')

        console.log(email,password)

        const res = await axios.get('/Users?rcn=4', {
          headers: {
              'X-M2M-ORIGIN': '2vCsok51z6:xB2p5Mj@N2',
              'Content-Type': 'application/json',
          }
        })

        var xml = new XMLParser().parseFromString(res.data);
        
        let instances = xml.getElementsByTagName('con')
        for(let i=1;i<instances.length;i++){
          let arr = (instances[i].value).split(",")
        
          let name = arr[0]
          let pwd = arr[1]
          
          const isMatch = await bcrypt.compare(password , pwd)

          if(isMatch && name === email){
            navigate('/home')
          
            return
          }
        }
        alert("Incorrect Credentials")         
    };

    return (
        <ThemeProvider theme={theme}>
          <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
              sx={{
                marginTop: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                <LockOutlinedIcon />
              </Avatar>
              <Typography component="h1" variant="h5">
                <div>
                Sign In
                </div>
              </Typography>
              <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="name"
                  label="Name"
                  name="name"
                  autoComplete="name"
                  autoFocus
                />
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                  Sign In
                </Button>
                
              </Box>
            </Box>
            {/* <Copyright sx={{ mt: 8, mb: 4 }} /> */}
          </Container>
        </ThemeProvider>
    )
}

export default Login
