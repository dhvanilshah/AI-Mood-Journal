import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';


function Login() {

    const [user, setUser] = useState('');
    const [password, setPassword] = useState('')
    const navigate = useNavigate();

    const handleUserChange = (event) => {
        setUser(event.target.value)
    }

    const handlePasswordChange = (event) => {
        setPassword(event.target.value)
    }

    const   handleSubmit = () => {
        fetch('/api/login', { 
          method: 'POST', 
          headers: { 'Content-Type': 'application/json' }, 
          body: JSON.stringify({username: user, password: password})
        }).then(res => {
          if (!res.ok) {
            throw new Error('Login failed');
          }
          return res.json();
        }).then(() => {
            navigate('/journals');
        }
        );
      };
    
    const canSubmit = user.length > 0 && password.length > 0;

  return (
    <div className  = "login-main">
        Welcome to the Login page!
        <p> Enter your username and password to see your notes!</p>
        <div className ="login-input">
            <input
            value = {user}
            onChange = {handleUserChange}
            className = "tweet-box-user"
            placeholder="Username"
            />
        </div>

        <div className = "login-input">
            <input
            type = "password"
            value = {password}
            onChange = {handlePasswordChange}
            className = "tweet-box-user"
            placeholder="Password"
            />
        </div>

        <div className='login-input'>

            <Button variant = "primary" size = "lg" onClick={handleSubmit} disabled={!canSubmit}>
                Submit
            </Button>
        </div>
    </div>
  );
}

export default Login;



