let form = document.getElementById('6')
form.style.display = 'none'
let button = document.getElementById('7')
button.addEventListener('click', function(){
    form.style.display = 'block'
})
let error_div = document.getElementById('10')
if(error_div){
    alert(error_div.textContent)
}
let msgs = document.getElementById('msgs1')
let socket = io()
socket.on('new msg', function(list){
if(list[1]===null){
    msgs.innerHTML += `<h2><h3>${list[2]}</h3>${list[0]}</h2>`
}
else{
    msgs.innerHTML += `<h2><h3>${list[2]}</h3>${list[0]}<img src="/image/${list[1]}"></h2>`
    
}
})
let buttons = document.getElementsByClassName('tresh_button')
let room_idx = document.getElementsByTagName('title')[0].textContent.split(' ').indexOf('ROOM')+1
let room_id = document.getElementsByTagName('title')[0].textContent.split(' ')[room_idx]
room_id = parseInt(room_id)
function strange(x){
    return function(){
        socket.emit('remove_msg', x, room_id)
    }
}
console.log(room_id)
for(let button of buttons){
    button.addEventListener('click', strange(button.dataset.id))
}
socket.on('remove_msg', function(list){
    console.log(list)
    if(list[0]===room_id){
        let msg_index = list[1]
        let msgs1 = document.getElementsByClassName('body_msg') 
        for(let msg of msgs1){
            if(msg.dataset.id == msg_index){
                msg.innerHTML = 'This message has been removed'
            }
        }
        let imgs = document.getElementsByClassName('img')
        for(let img of imgs){
            if(img.dataset.id == msg_index){
                img.remove()
            }
        }
    }
})
socket.on('neg_msg', function(list){
      if(list[0]===room_id){
        let msg_index = list[1]
        let msgs1 = document.getElementsByClassName('body_msg') 
        for(let msg of msgs1){
            if(msg.dataset.id == msg_index){
                msg.dataset.text = msg.innerHTML
                msg.innerHTML = 'This message has negative content. Click here to see the msg'
                msg.classList.add('negative')
                msg.addEventListener('click', function(){
                    msg.innerHTML = msg.dataset.text
                    msg.classList.remove('negative')
                })
            }
        }
        let imgs = document.getElementsByClassName('img')
        for(let img of imgs){
            if(img.dataset.id == msg_index){
                img.style.visible = 'none'
            }
        }
    }  
})