import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import bcrypt from 'bcryptjs'
import { v4 as uuidv4 } from 'uuid';

// Enter a username and password. Check that the username is not already in the user database
// If not then add the user to the database 

// Cookie/ Encryption stuff after


function Signup() {
    const salt = bcrypt.genSaltSync(10);

    const [user, setUser] = useState('');
    const [password, setPassword] = useState('')
    const navigate = useNavigate();

    const handleUserChange = (event) => {
        setUser(event.target.value)
    }

    const handlePasswordChange = (event) => {
        setPassword(event.target.value)
    }

    const handleSubmit = () => {

      var hash = bcrypt.hashSync(password, salt)
      var uuid_key = uuidv4()

        fetch('/api/addauth', { 
          method: 'POST', 
          headers: { 'Content-Type': 'application/json' }, 
          body: JSON.stringify({username: user, password: hash, uuid_key: uuid_key})
        }).then(res => {
          return res.json();
        }).then(() => {
            navigate('/journals');
        }
        );
      };
    
    const canSubmit = user.length > 0 && password.length > 0;

  return (
    <div className  = "sign-up-main">
        Welcome to the Sign-In page!
        <p>Enter a username and password to get started</p>
        <div className = "sign-up-input">

            <input
            value = {user}
            onChange = {handleUserChange}
            className = "tweet-box-user"
            placeholder="Username"
            />
        </div>

        <div className = "sign-up-input"> 
            <input
            type = "password"
            value = {password}
            onChange = {handlePasswordChange}
            className = "tweet-box-user"
            placeholder="Password"
            />
        </div>

        <div>
            <Button variant = "primary" size = "lg" onClick={handleSubmit} disabled={!canSubmit}>
                Submit
            </Button>
        </div>
    </div>
  );
}

export default Signup;



