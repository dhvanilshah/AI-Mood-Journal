import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';


function Welcome() {
    const navigate = useNavigate();

    const handleSignup = () => {
        navigate('/sign-up');
    }

    const handleLogin = () => {
        navigate('/login');
    }


  return (
    <div className  = "welcome-main">
        AI Mood Journal
        <p> Organize your thoughts and emotions easily and effecitvly</p>
        <div>
            <Button variant = "primary" size = "lg" onClick={handleSignup}>
                Sign Up!
            </Button>
        </div>
        <div>            
            <Button variant = "primary" size = "lg" onClick = {handleLogin}>
                Login!
            </Button>

        </div>
    </div>
  );
}

export default Welcome;



