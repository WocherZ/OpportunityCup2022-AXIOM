console.log("Hello");
console.log(window.location.host)
let connectionString = 'ws://' + window.location.host + '/ws';
let socket = new WebSocket(connectionString);


socket.onopen = function() {
    console.log("Connection open");
    socket.send("Hello server!")
}

socket.onclose = function(event) {
    console.groupCollapsed("Connection close");
}

socket.onerror = function(error) {
    console.log(error.message);
}

socket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    console.log(data);
    // There are some logics
}


// 1:
// первые 10 записей из БД для начала
// {'action': 'create'/'update',
// 'num': 10,
// 'data': [
//     {'date': '...',
//     'last_name': '...',
//     'first_name': '...',
//     'patronymic': '...',
//     'passport': '...',
//     'phone': '...',
//     'oper_type': '...',
//     'amount': '...',
//     'pattern': 'Да'/'Нет',
//     'pattern_description': [
//         'pattern1', 'pattern2', ...
//     ]
//     }
// ]    
// }

// 2: страница с двумя гистограммы
// {
//     'first_hist': {
//         'frod': 45,
//         'notford': 32
//     }
//     'second_hist': {
//         'notfrod': 234,
//         'pattern1': 2412,
//         'pattern2': 123213,
//         ...
//         'pattern6': 12312
//     }
//     'patterns_description': ['pattern1', ...]
// }