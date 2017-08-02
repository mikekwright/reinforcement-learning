import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import TicTacToe from './tic-tac-toe/TicTacToe';

class App extends Component {
  render() {
    return (
      <div className="app">
        <div className="app-header">
          <h2>Welcome to Reinforcement Learning</h2>
        </div>
        <div id="page" className="page-body">
          <TicTacToe />
        </div>
      </div>
    );
  }
}

export default App;
