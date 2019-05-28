const mqtt = require('mqtt')
const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', function connection(ws) {
    var client = mqtt.connect({ host: '172.16.123.10', port: 1883 })

    client.on('connect', function () {
        client.subscribe('//1/rins', function (err) {
            if (!err) {
                console.log('subscribed')
            }
        })
    })

    client.on('message', function (topic, message) {
        // message is Buffer
        console.log(message.toString())
        if (ws.readyState != ws.OPEN) {
            console.error('Client state is ' + ws.readyState);
            if (ws.readyState == 3) {
                console.log('Closing WebSocket')
                client.unsubscribe('//1/rins')
                client.end()
                ws.close()
            }
            //or any message you want
        } else {
            ws.send(message.toString()); //send data to client
        }
        //client.end()
    })


    ws.on('disconnect', function () {
        client.unsubscribe('//1/rins')
        client.end()
    });
});
