class TicTacToeGame {
    constructor() {
        this.board = [' ',' ',' ',
                      ' ',' ',' ',
                      ' ',' ',' '];

    }

    getBoard = () => {
        return this.board;
    } 

    toString() {
        return this.board.toString();
    }
}

export default TicTacToeGame;