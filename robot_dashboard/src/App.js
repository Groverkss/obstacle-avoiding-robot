import React from 'react';
import { BrowserRouter as Router, Route ,Routes} from "react-router-dom";

import Login from './components/Login'
import Home from './components/Home'

function App() {
  return (
    <Router>
    <Routes>
      <Route path="/" exact element={<Login/>} />
      <Route path="/home" exact element={<Home/>}/>
    </Routes>
    </Router>
  );
}

export default App;