import React from "react";
import "./styles.css";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";


export default class App extends React.Component {

    handleSignUp = () => {
      let navigate = useNavigate(); // Get the navigate function
      navigate('http://localhost:5173/auth');
      };

    handleLogin = () => {
    };


  render() {

    return (
      <div className="app">
        AI Mood Journal
        <div className="tweet-box-actions">
            <button onClick={this.handleSignUp}>
                Sign Up
            </button>
            <button onClick={this.handleLogin}>
                Login
            </button>
        </div>
      </div>
    );
  }
}


