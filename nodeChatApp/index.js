const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const cookie_read = require('cookie');
const url = require('url');

var namespace = io.of('/chatRooms');
app.get('/', function(req, res) {
    res.render('indexold.ejs')

});

users = {};

//var cur_url = url.parse(, true);
var glob_room;
namespace.on('connection', function(socket) {
    socket.on('room', function(room) {
        glob_room = room;
        socket.join(glob_room);
        socket.to(glob_room).emit("you're in this room" + glob_room);
    }) 
    socket.on('username', function(username) {
        socket.username = username;
    });



    socket.on('chat_message', function(message) {
        namespace.to(glob_room).emit('chat_message', '<strong>' + socket.username + '</strong>: ' + message);
    });

});


const server = http.listen(8080, '127.0.0.1', function(req, res) {
    console.log('listening on 127.0.0.1:8080');

});
