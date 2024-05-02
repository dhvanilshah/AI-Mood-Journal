import React from "react";

// import "../styles/styles.scss";

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: "",
      password: ""
    };
  }


  handleUserChange = (event) => {
    this.setState({ user: event.target.value });
  };

  handlePasswordChange = (event) => {
    this.setState({ password: event.target.value });
  };

  handleSubmit = () => {
    fetch('/api/addauth', { 
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify({username: this.state.user, password: this.state.password})
    }).then(res => {
      return res.json();
    })
  };



  render() {
    const user = this.state.user;
    const password = this.state.password;

    const canSubmit =
      user.length > 0 && password.length > 0 && password.length <= 280 ;

    return (
      <div className="app">

        <div className="tweet-box">
          <input
            value={user}
            onChange={this.handleUserChange}
            className="tweet-box-user"
            placeholder="Username"
          />
          <input
            value={password}
            onChange={this.handlePasswordChange}
            className="tweet-box-input"
            placeholder="Password"
          ></input>
          <div className="tweet-box-actions">
            <button
              onClick={this.handleSubmit}
              disabled={!canSubmit}
              className="tweet-box-submit"
            >
              Submit Authorization
            </button>
          </div>
        </div>

      </div>
    );
  }
}
