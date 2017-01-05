import React, { Component } from 'react';
import './TicTacToe.css';

import TicTacToeGame from './logic/TicTacToeGame';

import image_x from './images/letter-x.svg';
import image_o from './images/letter-o.svg';

class TicTacToe extends Component {
    constructor() {
        super();
        this.game = new TicTacToeGame();
    }

    renderBoard = () => {
        var board = this.game.getBoard();
        console.log(board);
        var displayBoard = [];
        for (var row = 0; row < 3; ++row) {
            var boardRow = [];
            for (var col = 0; col < 3; ++col) {
                var index = row*3 + col;
                var cell = 'cell' + index;
                boardRow.push(<div key={cell} id={cell} className='cell'>{board[index]}</div>);
            }
            var rowId = 'row' + row;
            displayBoard.push(<div key={rowId} id={rowId} className='row'>{boardRow}</div>)
        }
        return displayBoard;
    }

    render = () => {
        var board = this.renderBoard();
        return (
            <div>
                <h1>Tic Tac Toe</h1>
                <div id="tto-gameboard" className="board">
                 {board}
                </div>
                <img src={image_x} alt='here' />
                <img src={image_o} alt='there' />
            </div>
        );
    }
}

export default TicTacToe;