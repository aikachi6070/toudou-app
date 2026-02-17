

const input = document.getElementById('todoInput');
const button = document.getElementById('addBtn');
const liste = document.getElementById('todoList');
const API_URL = 'https://toudou-backend-c2x1.onrender.com';

function deleteTodo(id){
    fetch(API_URL+'/todos/'+id, {
        method:'DELETE'
    })
    .then(() => {
        location.reload();
    });
}

function doneTodo(id,currentDone){
    const newDone = !currentDone;

    fetch(API_URL+'/todos/'+id + '?done='+newDone, {
        method:'PUT'
    })
    .then(() => {
        location.reload();
    })
}
function modifTodo(id){
    const textSpan=document.getElementById('text-'+id);
    const text = textSpan.innerText;
    
    textSpan.classList.add('hidden');

    liste.innerHTML+="<input type=text id=todoModif placeholder="+text+">";
    liste.innerHTML+="<button onclick='validerModif("+id+")'>Modifier</button>";

    const addBtn2_2=document.getElementById('addBtn2');
    const newtext=document.getElementById('todoModif');
};

function validerModif(id) {
    const newtext = document.getElementById('todoModif');
    const newtextfinal = newtext.value;
    console.log("Valeur:", newtextfinal);
    
    fetch(API_URL+'/todos/' + id + '?text=' + newtextfinal, {
        method: 'PUT'
    })
    .then(() => location.reload());
}

//pour afficher la liste dans le HTML
fetch(API_URL+'/todos')
.then(response=>response.json())
.then(data=> {
    data.forEach(todo => {
        if(todo.done==1){
            emoji="✅";
        }
        else {
            emoji="☑️";
        }
        liste.innerHTML += '<li>'+emoji+'<span id="text-'+todo.id+'">'+ todo.text +'</span><button onclick="deleteTodo(' + todo.id + ')">🗑️</button><button onclick="doneTodo(' + todo.id + "," +todo.done+ ')">✔️</button><button onclick="modifTodo(' + todo.id + ')">✏️</button></li>';
    });
});



//pour creer dans la database
button.addEventListener('click', function(){
    const texte = input.value;
    fetch(API_URL+'/todos?text='+texte,{
        method: 'POST'
    }
    )
    .then(response => response.json())
    .then(data => {
        liste.innerHTML += '<li>'+texte+'</li>';
        location.reload();
    });
}
);