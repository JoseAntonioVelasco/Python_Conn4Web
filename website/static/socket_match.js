function _initSocket(socket){
    var solo_play = false;

    //+-------------------------------+
    //| broadcast messages to backend |
    //+-------------------------------+

    //jugador se conecta a la partida
    socket.on('connect', function() {
        socket.emit('join', {})
    })

    //jugador manda un mensaje
    $("#send").click(function(e){
        texto = $('#text').val()
        $('#text').val('')
        socket.emit('text', {msg: texto})
    })

    //listeners para las columnas del conecta 4
    var columns = document.querySelectorAll('.column');
    Array.prototype.forEach.call(columns, function(col) {

        col.addEventListener('click', function() {
            var clicked_col = col.getAttribute('data-x')
            var nextFree = markNextFree(clicked_col);
            if(nextFree !== false){
                socket.emit('place', {x: clicked_col, y: nextFree, color: playerColor})
            }else{
                //alerta de columna llena
                if(nextFree === false) {
                    alert('La columna esta llena :-).');
                    return false;
                }
            }
        });
    });





    //+-----------------------------------+
    //| messages from backend to frontend |
    //+-----------------------------------+

    //un jugador entra en la partida
    socket.on('status', function(data){
        //ha entrado al chat
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);

        //cargar partida y datos
        if(typeof data.board != "undefined"){
            loadBoard(data.board)
        }
        $('#matchInfo').empty().append("Usuario 1: "+data.matchInfo.username1+"<br>Usuario 2: "+data.matchInfo.username2+"<br>Estado de la partida: "+data.matchInfo.status+"<br>Id de partida: "+data.matchInfo.id)

        //ver si es una partida contra la IA 
        if(ai_names.includes(data.matchInfo.username1)){
            solo_play = true;
            ai_name = data.matchInfo.username1;
            ai_color = "red"
            playerColor = "yellow"
            ai_turn = true
            //la ia pone aqui ya porque es la que empieza primero
            soloPlayTurnSystem(solo_play);
        }else if(ai_names.includes(data.matchInfo.username2)){
            solo_play = true;
            ai_name = data.matchInfo.username2;
            ai_color = "yellow"
            ai_turn = true;
        }

        //asignar color
        if(typeof data.color != "undefined"){
            if(playerColor == "None"){
                playerColor = data.color
            }
        }
        
    })

    //un jugador ha escrito un mensaje en el chat
    socket.on('message', function(data){
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    })

    //un jugador ha puesto una ficha en el tablero
    socket.on('place', function(data){
        //pone la ficha en el tablero
        document.querySelector('#column-'+data.x+' .row-'+data.y+' circle').setAttribute(
                        'class', data.color
        );
        gameBoard[data.y][data.x] = data.color;

        //despues de que un jugador ponga ficha si esta jugando contra una ia, la ia pone despues
        soloPlayTurnSystem(solo_play);
    })

    //lanzar un aviso
    socket.on('notice',function(data){
        alert(data.msg)
    })
}

//evento de boton: jugar solo ha seleccionado una IA
function getData(){
    var ai = $("#selectAI :selected").val();
    if(ai === "0"){
        alert("Selecciona una IA");
        return;
    }
    var color = $("input[type='radio'][name='inlineRadioOptions']:checked").val();
    if(color == null){
        alert("Selecciona el color de la IA");
        return;
    }

    socket.emit('aiJoin',{ai: ai, color: color})
}


//-------------------------------------------------------------------------------------------//

function randomIA(){
    //genera una columna aleatoria ente 0 y 6
    var col = Math.floor(Math.random() * 7);
    //comprueba si esa columna esta llena
    while(markNextFree(col) === false){
        col = Math.floor(Math.random() * 7);
    }
    //pone en esa columna
    return col;
}

function soloPlayTurnSystem(solo_play){
    if(solo_play){
        //ver si es turno de la ia
        if(ai_turn){
            var x, y, color;
            switch(ai_name){
                //añadir tantos case como ias halla 
                case "randomIA":
                    x = randomIA();
                    y = markNextFree(x);
                    color = ai_color
                    break;
            }
            //cambia al turno de humano y emitimos
            ai_turn=false;
            socket.emit('place', {x: x, y: y, color: color})
        }else{
            //cambia al turno de la ia
            ai_turn=true;
        }
        
    }
}