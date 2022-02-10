//author: Zhida Li
// last edit: Feb. 9, 2022

$(document).ready(function () {
    namespace = '/test_conn';

    var socket = io(namespace);
    // Start the background thread by pressing the "Connect button"
    $('#btn_connect').click(function() {
        socket.emit('main_event');
    });

    // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('server_response_text', function (res) {
        console.log("Min 0 result and local time (server):", res.data_results[0], res.data_t[1]);  // here just show res.data[1]
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
