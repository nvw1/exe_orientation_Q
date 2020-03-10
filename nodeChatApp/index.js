const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
var namespace = io.of('/chatRooms');
app.get('/', function(req, res) {
    res.render('indexold.ejs')
});

users = {};

/*
io.sockets.on('connection', function(socket) {
    console.log("user connected");

socket.on('new', function(data, callback) {
    console.log(data.name);
    if(data in users)
    callback(false);
    else {
        callback(true);
        socket.name = data.name;
        users[socket.name] = socket;
    }
})
socket.on('msg', function(data,callback) {
    callback(data.msg);
    io.to(users[data.to].emit('priv',data.msg));
})
})
*/

var glob_room;
namespace.on('connection', function(socket) {
    socket.on('room', function(room) {
        glob_room = room;
        socket.join(glob_room);
        socket.to(glob_room).emit("you're in this room" + room);
    }) 
    socket.on('username', function(username) {
        socket.username = username;
    });


    socket.on('chat_message', function(message) {
        namespace.to(glob_room).emit('chat_message', '<strong>' + socket.username + '</strong>: ' + message);
    });

});


const server = http.listen(8080, '127.0.0.1', function() {
    console.log('listening on *:8080');
});
