function markNextFree(x){
	var nextY = false;
	//busca la casilla disponible en esa columna
	for(var y = 0; y < 6; y++) {
		if(gameBoard[y][x] === 'free') {
			nextY = y;
			break;
		}
	}

	return nextY
}

function loadBoard(board){
	for(var y=0; y<6; y++){
		for(var x=0; x<7; x++){

			document.querySelector('#column-'+x+' .row-'+y+' circle').setAttribute(
					'class', board[y][x]
			);
			
		}
	}
	gameBoard=board
}

