let loc = window.location
let wsStart = 'ws://'

if (loc.protocol === 'https') {
    wsStart  = 'wss://'
}
let endPoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endPoint)

socket.onopen = async function(e) {
    console.log('open', e)
}
socket.onmessage = async function(e) {
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    appendMessage(message, sent_by_id)
}
socket.onerror = async function(e) {
    console.log('error', e)
}
socket.onclose = async function(e) {
    console.log('close', e)
}

let message = $('#input-message')
let message_body = $('#message-body-append')

function appendMessage(message, sent_by_id) {
    if ($.trim(message) === '') {
        return false;
    }
    let new_message;
    let USER_ID = document.getElementById('user-id').value
    if (sent_by_id == USER_ID) {
        console.log('if')
        new_message = `
            <li class="clearfix">
                <div class="message-data text-right">
                    <span class="message-data-time">10:10 AM, Today</span>
                </div>
                <div class="message other-message float-right">${message}</div>
            </li>
        `
    }
    else {
        console.log('else')
        new_message = `
            <li class="clearfix">
                <div class="message-data">
                    <span class="message-data-time">10:12 AM, Today</span>
                </div>
                <div class="message my-message">${message}</div>
            </li>
        `
    }
    message_body.append(new_message)
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
    document.getElementById('input-message').value = '';
}

function submitMessage() {
    console.log('clicked')
    let message = $('#input-message').val()
    let BUDDY
    let USER_ID = document.getElementById('user-id').value
    if (USER_ID==2) 
        BUDDY = 3
    else
        BUDDY = 2
    let data = {
        'message': message,
        'sent_by': USER_ID,
        'sent_to': BUDDY
    }
    console.log(data)
    data = JSON.stringify(data)
    socket.send(data)
    // $('#input-message').val() = ''
    // $('#send-message').reset()
}