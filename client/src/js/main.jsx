import React from 'react'
import ReactDOM from 'react-dom/client'

import App from './App'

import '../scss/styles.scss'

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Container>
        <App />
    </ Container>
  </React.StrictMode>,
)
