function markNextFree(board, x){
	var nextY = false;
	//busca la casilla disponible en esa columna
	for(var y = 0; y < 6; y++) {
		if(board[y][x] === 'free') {
			nextY = y;
			break;
		}
	}

	return nextY
}

function loadBoard(board){
	//carga el tablero en el html
	for(var y=0; y<6; y++){
		for(var x=0; x<7; x++){

			document.querySelector('#column-'+x+' .row-'+y+' circle').setAttribute(
					'class', board[y][x]
			);
			
		}
	}
	gameBoard=board
}

function insideBoard(board, x, y){
	//esta funcion esta programada de la misma manera que la de python,
	//para ver documentacion ve al fichero de python
	var columns = board[0].length;
	var rows = board.length;

	//cols 0-6 rows 0-5
	if((x < columns && x >= 0) && (y < rows && y >= 0)){
		return true;
	}else{
		return false;
	}

}

function checkNinRow(board, x, y, turn, n){
	//esta funcion esta programada de la misma manera que la de python,
	//para ver documentacion ve al fichero de python

	//n tiene que ser un entero
	//si n == 3 comprueba si va a ser una victoria
	//si n == 2 comprueba si va a ser un 3 en raya, y asi sucesivamente
	var directions = [[[0, 1], [0, -1]], [[1, 1], [-1, -1]],
	[[1, 0], [-1, 0]], [[1, -1], [-1, 1]]]
	var len_dirs = directions.length;
	for(var i = 0; i < len_dirs; i++){
		var direction = directions[i];
		var counter = 0;
		for(var j = 0, len = direction.length; j < len; j++){
			var vector = direction[j];
			var x_ = x;
			var y_ = y;
			for(var loop=0; loop<4; loop++){
				x_ = x_ + vector[0];
				y_ = y_ + vector[1];
				var cond = insideBoard(board, x_, y_) && board[y_][x_] === turn;
				if(cond){
					counter = counter + 1;
				}else{
					break;
				}
				if(counter == n){
					return true;
				}
			}
		}
	}
	return false;
}

function getFreeColumns(board){
	//retorna los numeros de columnas en las que se puede poner
	var freeCols = [];
	//busca la casilla disponible en esa columna
	for(var x = 0; x < 7; x++) {
		if(board[5][x] === 'free') {
			freeCols.push(x);
		}
	}

	return freeCols;
}

function getFreeValidPlaces(board){
	//retorna las posiciones validas en las que puede poner un jugador
	var freePos = [];

	//conseguimos las columnas libres
	var freeCols = getFreeColumns(board)
	for(var i = 0, len = freeCols.length; i < len; i++){
		var x = freeCols[i];
		var y = markNextFree(board, x);
		freePos.push([x,y]);
	}
	return freePos;
}

function simulateBoard(x, y, turn, board){
	//pone una ficha en el tablero y lo retorna
	var simulatedBoard = JSON.parse(JSON.stringify(board)); //Deep copy
	simulatedBoard[y][x] = turn;
	return simulatedBoard;
}

function changeColor(color){
	//retorna el color contrario al que recibe
	if(color === "red"){
		return "yellow"
	}else{
		return "red"
	}
}

function proxCenter(x){
	//funcion que da puntos en funcion a lo cerca que ponga del centro del tablero
	var score = 0;
	switch(x){
		case 0: case 6:
			score = score + 1;
			break;
		case 1: case 5:
			score = score + 2;
			break;
		case 2: case 4:
			score = score + 3;
			break;
		case 3:
			score = score + 80;
			break;
	}
	return score;
}

function checkNinRowPoints(board, x, y, turn, n){
	//esta funcion esta programada de la misma manera que la de python,
	//para ver documentacion adicional ve al fichero de python
	//es usada para evaluar una posicion en el minimax

	//n tiene que ser un entero
	//si n == 4 comprueba si hay 3 en raya, unico o doble
	//si n == 5 comprueba si hay 2 en raya, unico o doble
	var directions = [[[0, 1], [0, -1]], [[1, 1], [-1, -1]],
	[[1, 0], [-1, 0]], [[1, -1], [-1, 1]]]
	var score = 0;
	var len_dirs = directions.length;
	//coje una direccion, ej: arriba abajo
	for(var i = 0; i < len_dirs; i++){
		var direction = directions[i];
		var counter = 0;
		var freeSpace = 0;
		//coje de la direccion un sentido solo, ej: arriba
		for(var j = 0, len = direction.length; j < len; j++){
			var vector = direction[j];
			var x_ = x;
			var y_ = y;
			//analiza ese sentido
			for(var loop=0; loop < n; loop++){
				x_ = x_ + vector[0];
				y_ = y_ + vector[1];
				var inside = insideBoard(board, x_, y_);

				if(inside){
					var same = board[y_][x_] === turn;
					var free = board[y_][x_] === "free";
					if(same){
						counter = counter + 1;
					}else if(free){
						freeSpace = freeSpace + 1; 
					}else{
						break;
					}
				}else{
					break;
				}
			}
			
		}
		//despues de analizar la direccion, se evalua la direccion
		
		if(n == 4 && counter == 2){
			if(freeSpace >= 2){
				score = score + 20; //3 en raya por dos lados (x2 puntos)
			}else if(freeSpace == 1){
				score = score + 10; //3 en raya por un lado (x1 puntos)
			}
		}else if(n == 5 && counter == 1){
			if(freeSpace == 2){
				score = score + 4; //2 en raya simple
			}else if(freeSpace == 3){
				score = score + 6; //2 en raya mejor
			}else if(freeSpace >= 4){
				score = score + 8; //2 en raya por dos lados
			}
		}	
		
	}
	return score;
}

function evaluateMove(board, x, y, turn){
	//retorna los puntos que vale poner una ficha en esa posicion en el tablero
	var score = 0;
	/*
	Esta es la heuristica del minimax, para hacer el minimax mas inteligente añade funciones que comprueben cosas
	y den puntos por ello, el ajustar la heuristica puede ser complicado y si lo haces mal lo puedes volver mas "tonto"
	*/
	
	score = checkNinRowPoints(board, x, y, turn, 4); //3 en raya
	//score = checkNinRowPoints(board, x, y, changeColor(turn), 4) + score; //puntos por bloquear 3 en raya
	//score += checkNinRowPoints(board, x, y, turn, 5); //2 en raya
	//score = checkNinRowPoints(board, x, y, changeColor(turn), 5) + score; //puntos por bloquear 2 en raya
	score += proxCenter(x); //proximidad al centro
	return score;
}

function minimax(x, y, depth, maximizingPlayer, turn, score, board){
	if(depth == 0){
		//evaluamos
		score = evaluateMove(board, x, y, turn) + score;
		return score;
	}
	
	if(maximizingPlayer){
		//maximizamos
		var maxEval = -999999; //-infinito
		var freePlaces = getFreeValidPlaces(board);

		score = evaluateMove(board, x, y, turn) + score;
		
		//da puntuacion a todas las casillas disponibles
		for(var i = 0, len = freePlaces.length; i < len; i++ ){
			var freePlace = freePlaces[i];
			var x = freePlace[0];
			var y = freePlace[1];
			//simula tablero y poda victoria
			var simulatedBoard = simulateBoard(x, y, turn, board);
			if(checkNinRow(simulatedBoard, x, y, turn, 3)){
				maxEval = 999999;
				break;
			}
			var eval = minimax(x, y, depth-1, false, changeColor(turn), score, simulatedBoard);
			//guardamos el maximo que haya
			if(eval >= maxEval){
				maxEval = eval;
			}
		}
		//retorna maximo
		return maxEval;
	}else{
		//minimizamos
		var minEval = 999999; //+infinito
		var freePlaces = getFreeValidPlaces(board);

		score = evaluateMove(board, x, y, turn) + score;

		//da puntuacion a todas las casillas disponibles
		for(var i = 0, len = freePlaces.length; i < len; i++){
			var freePlace = freePlaces[i];
			var x = freePlace[0];
			var y = freePlace[1];
			//simula tablero y poda victoria
			var simulatedBoard = simulateBoard(x, y, turn, board);
			if(checkNinRow(simulatedBoard, x, y, turn, 3)){
				minEval = -999999;
				break;
			}
			var eval = minimax(x, y, depth-1, true, changeColor(turn), score, simulatedBoard);
			//guardamos el minimo que haya
			if(eval <= minEval){
				minEval = eval
			}
		}

		//retorna minimo
		return minEval;
	}
}
function firstBranch(board, turn, depth){
	
	var maxEval = -999999; //-infinito
	var freePlaces = getFreeValidPlaces(board);
	var max_x = -1;

	for(var i = 0, len = freePlaces.length; i < len; i++){
		var freePlace = freePlaces[i];
		var x = freePlace[0];
		var y = freePlace[1];

		var simulatedBoard = simulateBoard(x, y, turn, board);
		if(checkNinRow(simulatedBoard, x, y, turn, 3)){
			maxEval = 999999;
			max_x = x;
			break;
		}
		var eval = minimax(x, y, depth-1, false, changeColor(turn), 0, simulatedBoard);
		if(eval >= maxEval){
			maxEval = eval;
			max_x = x;
		}
	}

	return max_x;
}

// +--------------------------------------------+
// |*************TESTING FUNCTIONS**************|
// +--------------------------------------------+

function test_checkNinRow(){
	/*Test de la funcion checkNinRow para comprobar su correcto funcionamiento*/
	var boardlimpio = [
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
	]
	var coordenadas_xy = [
		['00','10','20','30','40','50','60'],
		['01','11','21','31','41','51','61'],
		['02','12','22','32','42','52','62'],
		['03','13','23','33','43','53','63'],
		['04','14','24','34','44','54','64'],
		['05','15','25','35','45','55','65'],
	]
	var board1 = [
		['red','red','red','free','free','free','free'],
		['yellow','free','free','free','free','free','free'],
		['yellow','free','free','free','free','free','free'],
		['yellow','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
	]
	var board2 = [
		['red','yellow','yellow','yellow','free','free','free'],
		['free','free','yellow','yellow','free','free','free'],
		['free','free','red','yellow','free','free','free'],
		['free','free','free','red','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
	]
	var board3 = [
		['free','red','free','red','red','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
	]
	var cond0 = checkNinRow(board1, 3, 0, 'red', 3); //True win horizontal, este ha fallado (arreglado)
	var cond1 = checkNinRow(board1, 0, 4, 'yellow', 3); //True win vertical

	var cond2 = checkNinRow(board2, 1, 1, 'red', 3); //True win diagonal
	var cond3 = checkNinRow(board3, 2, 0, 'red', 3); //True win horizontal con hueco, este ha fallado (arreglado)
}

function test_checkNinRowPoints(){
	var board1 = [
		['free','red','red','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
		['free','free','free','free','free','free','free'],
	]
	var score = checkNinRowPoints(board1, 3, 0, 'red', 4); //10 puntos tiene que dar
}
