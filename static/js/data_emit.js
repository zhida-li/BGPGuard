//
$(document).ready(function () {
    namespace = '/test_conn';

    var socket = io(namespace);
    // Start the background thread by pressing the "Connect button"
    $('#btn_connect').click(function() {
        socket.emit('main_event');
    });

    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('server_response_text', function (res) {
        console.log(res.data[0], res.data[1]);  // here just show res.data[1]
        var t = res.data[0];
        $('#t_utc').text(t);

        //document.getElementById("t1_num").innerHTML = t1; // both methods are fine
        var results_text1 = res.data[1];
        $('#results1_p').text(results_text1);

        var results_text2 = res.data[2];
        $('#results2_p').text(results_text2);

        var results_text3 = res.data[3];
        $('#results3_p').text(results_text3);

        var results_text4 = res.data[4];
        $('#results4_p').text(results_text4);

        var results_text5 = res.data[5];
        $('#results5_p').text(results_text5);

    });
    
});
