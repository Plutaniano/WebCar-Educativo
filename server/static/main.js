connectIndicator = document.getElementById('connectIndicator')

function connect() {
    if (connectIndicator.classList.contains('disconnected')) {
        connectIndicator.classList.remove('disconnected');
        connectIndicator.classList.add('connected');                
    } else {
        connectIndicator.classList.remove('connected');
        connectIndicator.classList.add('disconnected');        
    }
}


function move(str) {
    fetch('/move?status=' + str)
}

function led(str) {
    fetch('/led')
}

upBtn = document.getElementById('up-arrow');
downBtn = document.getElementById('down-arrow');
leftBtn = document.getElementById('left-arrow');
rightBtn = document.getElementById('right-arrow');

ledBtn = document.getElementById('led-button')

upBtn.addEventListener('click', function(){
    move('up');
});

downBtn.addEventListener('click', function(){
    move('down');
});

leftBtn.addEventListener('click', function(){
    move('left');
});

rightBtn.addEventListener('click', function(){
    move('right');
});

ledBtn.addEventListener('click', function(){
    led()
})