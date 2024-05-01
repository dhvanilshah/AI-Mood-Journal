import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Tweeter from './Tweeter';
import Auth from './Auth';
import Welcome from './Welcome';
import Journals from './Journals';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/auth" element={<Auth />} />
        <Route path="/journals" element={<Journals />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;



