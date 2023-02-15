import React from 'react';
import './App.scss';
import axios from 'axios';

function App() {
    const website_url = window.location.hostname;
    const [output, setOutput] = React.useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const username = e.target.username.value;
        const password = e.target.password.value;

        const response = await axios.post(`http://${website_url}:8000/login`, {
            username: username,
            password: password
        }).catch(error => {
                setOutput("Error: " + "Invalid username or password.");
                return;
        });
        setOutput("Logged in as:" + response.data.username);
    }

  return (
    <div className="App">
      <div className="App-header">
        <h1>Login Form</h1>
        <p>Enter your username and password to see output.</p>
        <form onSubmit={handleSubmit}>
            <label>Username</label>
            <input type="text" name="username" />
            <label>Password</label>
            <input type="password" name="password" />
            <input className="submit_button" type="submit" value="Submit" />
        </form>
      </div>
        <div className="App-output">
            <h2>Output</h2>
            <span>{output}</span>
        </div>
    </div>
  );
}

export default App;
