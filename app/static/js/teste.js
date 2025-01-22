// const aux_bd = [];
// document.getElementById('form_player').addEventListener('submit', function(event) {
//     event.preventDefault(); 

//     const player_form = document.getElementById('Adicionar_player').value;
    
//     if (aux_bd.some(player => player.player === player_form)) {
//         alert("Player já cadastrado");
//         return;
//     }
//     if (aux_bd.length > 7) {
//         alert("numero maximo de players atingido");
//         return;
//     }
        
//     let player_ID = aux_bd.length + 1;
//     let new_player = {"ID": player_ID, "player": player_form};
//     aux_bd.push(new_player);


//     console.log(player_form);
//     console.log(aux_bd);
    
//     fetch('/form/adicionar_form', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ aux_bd: aux_bd })
//     })
// });