(function() {

	var ConnectFour = function() {

		gameBoard = [];
		currentPlayer = 'red';
		numRows = 6;
		numCols = 7;
		numTurns = 0;
		
		_init = function() {
			
			var columns;
			
			columns = document.querySelectorAll('.column');
			
			Array.prototype.forEach.call(columns, function(col) {
				col.addEventListener('click', function() {
					markNextFree(col.getAttribute('data-x'));
				});
			});
			
			//inicializo el array
			for(var i=0; i<7; i++){
				gameBoard.push(['free','free','free','free','free','free']);
			}
		};
		
		var markNextFree = function(x) {
			
			var nextY;
			nextY = false;
			
			//busca la casilla disponible en esa columna
			for(var y = 0; y < numRows; y++) {
				if(gameBoard[x][y] === 'free') {
					nextY = y;
					break;
				}
			}
			
			if(nextY === false) {
				alert('No free spaces in this column. Try another.');
				return false;
			}
			
			//pone el color en el tablero
			gameBoard[x][nextY] = currentPlayer;
			
			//pone ficha en esa casilla
			document.querySelector('#column-'+x+' .row-'+nextY+' circle').setAttribute(
					'class', currentPlayer
			);
			
			//rota color
			currentPlayer = currentPlayer === 'red' ? 'yellow' : 'red';

		};
		
		
		_init();
		
	};

	ConnectFour();
  
	
})();
