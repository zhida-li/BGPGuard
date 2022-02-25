//author: Zhida Li
// last modified: Feb. 22, 2022
// task: enable disconnect btn

$(document).ready(function () {
    namespace = '/test_conn';

    var socket = io(namespace);
    // Start the background thread by pressing the "Connect button"
    $('#btn_connect').click(function () {
        socket.emit('main_event');
    });

    // Disconnect the real-time task (client -> server)
    $('form#form_disconnect').submit(function (event) {
        socket.emit('disconnect_request');
        return false;
    });

    // Server sends the confirmation msg to the client
    socket.on('disconnect_response', function (msg, cb) {
        $('#log_disconnect').append($('<span/>').text('Server received' + ': ' + msg.data).html());
        if (cb)
            cb();
    });

    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('server_response_text', function (res) {
        // console.log("Minute 0 result and local time (server ->):", res.data_results[0], res.data_t[0]);  // for debug
        var t_utc = res.data_t[0];
        $('#t_utc').text(t_utc);

        //document.getElementById("t1_num").innerHTML = t1; // both methods are fine
        var results_text0 = res.data_results[0];
        $('#results0_p').text(results_text0);

        var results_text1 = res.data_results[1];
        $('#results1_p').text(results_text1);

        var results_text2 = res.data_results[2];
        $('#results2_p').text(results_text2);

        var results_text3 = res.data_results[3];
        $('#results3_p').text(results_text3);

        var results_text4 = res.data_results[4];
        $('#results4_p').text(results_text4);
    });
});
