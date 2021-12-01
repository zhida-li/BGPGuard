//
$(document).ready(function () {
    namespace = '/test_conn';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('server_response', function (res) {
        console.log(res.data[0], res.data[1]);
        var t = res.data[0];
        $('#t_currentTime').text(t);
        //document.getElementById("t1_num").innerHTML = t1; // both methods are fine
        var t2 = res.data[1];
        $('#t2_num').text(t2);
    });
});
