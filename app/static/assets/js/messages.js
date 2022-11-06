let loc = window.location;
let wsStart = 'ws://';

if (loc.protocol === 'https') {
    wsStart  = 'wss://';
}
let endPoint = wsStart + loc.host + loc.pathname;

var socket = new WebSocket(endPoint), USER_ID = document.getElementById('user-id').value;
var BUDDY, CHAT_ROOM_ID;
        
var today = new Date();
var yesterday = new Date();
yesterday.setDate(today.getDate() - 1)
yesterday = yesterday.toLocaleDateString('en-US', {weekday:"short", year:"numeric", month:"short", day:"numeric"}).replace(',', '').replace(',', '');

function DateFormat(date) {
    if (today.toDateString() === date.toDateString())
        return 'Today at ' + date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
    else if (yesterday === date.toDateString())
        return 'Yesterday at ' + date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
    else
        return date.toLocaleDateString('en-US', {year:"numeric", month:"short", day:"numeric"}) + ' ' + date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
}

socket.onopen = async function(e) {
    console.log('open', e);
    $('#submit-button').on('click', function (){
        console.log('clicked')
        let message = $('#input-message').val()
        let data = {
            'message': message,
            'sent_by': USER_ID,
            'sent_to': BUDDY,
            'room_id': CHAT_ROOM_ID
        }
        console.log(data)
        data = JSON.stringify(data)
        socket.send(data)
    })
}
socket.onmessage = async function(e) {
    console.log('message', e);
    let data = JSON.parse(e.data);
    let message = data['message'];
    let sent_by_id = data['sent_by'];
    appendMessage(message, sent_by_id);
    let x = `chat_${data["room_id"]}`;
    console.log(document.querySelectorAll(`[chat-id=${x}]`)[0].querySelectorAll('.status')[0]);
    if (sent_by_id != USER_ID) {
        document.querySelectorAll(`[chat-id=${x}]`)[0].querySelectorAll('.status')[0].innerHTML = '<i class="fa fa-circle online"> New Message!</i>';
    }
    else {
        document.querySelectorAll(`[chat-id=${x}]`)[0].querySelectorAll('.status')[0].innerHTML = '<i class="fa fa-circle blank"> Message Delivered</i>';
    }
}
socket.onerror = async function(e) {
    console.log('error', e);
}
socket.onclose = async function(e) {
    console.log('close', e);
}

let message = $('#input-message');
let message_body = $('#message-body-append');

function appendMessage(message, sent_by_id) {
    if ($.trim(message) === '') {
        return false;
    }
    let new_message;
    if (sent_by_id == USER_ID) {
        new_message = `
            <li class="clearfix">
                <div class="message-data text-right">
                    <span class="message-data-time">10:10 AM, Today</span>
                </div>
                <div class="message other-message float-right">${message}</div>
            </li>
        `;
    }
    else {
        new_message = `
            <li class="clearfix">
                <div class="message-data">
                    <span class="message-data-time">10:12 AM, Today</span>
                </div>
                <div class="message my-message">${message}</div>
            </li>
        `;
    }
    message_body.append(new_message);
    document.getElementById("chat-body-main").scrollTop = document.getElementById("chat-body-main").scrollHeight;
    document.getElementById('input-message').value = '';
}


function displayNewChat(element) {
    document.querySelectorAll('.active')[0].classList.remove('active');
    element.classList.add('active');
    CHAT_ROOM_ID = element.getAttribute('chat-id').split('_')[1];
    document.getElementById('chat-header-name').innerHTML = document.getElementsByClassName('active')[0].querySelectorAll('.about')[0].querySelectorAll('.name')[0].innerHTML;
    BUDDY = document.getElementsByClassName('active')[0].getAttribute('other_user_id');

    $.ajax({
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'chat_room_id': CHAT_ROOM_ID
        },
        url: `/chat/`,
        success: function(r) {
            document.getElementById('message-body-append').innerHTML = '';
            displayMessage(r.data);
            document.getElementById("chat-body-main").scrollTop = document.getElementById("chat-body-main").scrollHeight;
            if (r.last != USER_ID) {
                element.querySelectorAll('.status')[0].innerHTML = '<i class="fa fa-circle offline"> Respond</i>';
            }
        }
    });
}

function displayMessage(data) {
    var messageObj, formatedDate;
    for (let i=0 ; i<data.length ; i++) {

        messageObj = data[i]
        // console.log(messageObj.datetime + ' .... ' + new Date(messageObj.datetime))
        formatedDate = DateFormat(new Date(messageObj.datetime));

        if (messageObj.sent_by == document.getElementById('user-id').value) {
            $('#message-body-append').append(`
                <li class="clearfix">
                    <div class="message-data text-right">
                        <span class="message-data-time">${formatedDate}</span>
                    </div>
                    <div class="message other-message float-right">${messageObj.text}</div>
                </li>
            `)
        }
        else {
            $('#message-body-append').append(`
                <li class="clearfix">
                    <div class="message-data">
                        <span class="message-data-time">${formatedDate}</span>
                    </div>
                    <div class="message my-message">${messageObj.text}</div>                                    
                </li>
            `)
        }
    }
}