import React from "react";
import "./styles.css";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";


export default class App extends React.Component {

  render() {

    return (
      <div className="app">
        Welcome! Here are your journals!
      </div>
    );
  }
}
