// EChart

// var myChart = echarts.init(document.getElementById('echart_cpu'));
var chartDom2 = document.getElementById('echart_results');
var myChart2 = echarts.init(chartDom2);

myChart2.setOption({
    title: {
        text: 'Number of announcement vs. time'
    },
    tooltip: {},
    legend: {
        data:['Number of announcement']
    },
    xAxis: {
        data: []  //x axis
    },
    yAxis: {},
    series: [{
        name: 'Number of announcement',
        data: [],  //y values
        type: 'bar'
    }],

      visualMap: [
    {
      show: true,  // bar reference
      type: 'continuous',
      seriesIndex: 0,
      min: 0,
      max: 6e3
    }]
});


var t_ann = Array(40).fill(""),
    bgp_ann = Array(40).fill(0)

// callback function
var update_mychart2 = function (res) {

    // hide animation
    myChart2.hideLoading();

    // prepare data
    Array.prototype.push.apply(t_ann, res.data_cpu[0]);
    Array.prototype.push.apply(bgp_ann, res.data_cpu[1]);
    // console.log("push t ann (chart):", t_ann);
    // console.log("push volume ann (chart):", bgp_ann);
    if (t_ann.length >= 60){
        // remove the first 10 elements
        t_ann.splice(0,10);
        bgp_ann.splice(0,10);
    }

    // fill the data
    myChart2.setOption({
        xAxis: {
            data: t_ann
        },
        series: [{
            name: 'Number of announcement', // related to the data name in legend
            data: bgp_ann
        }]

    });

};

// initial load the animation
myChart2.showLoading();


// establish socket connection, wait for the server push data, use the callback function update chart
$(document).ready(function() {
    namespace = '/test_conn';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('server_response_echart2', function(res) {
        console.log("t ann (server):", res.data_cpu[0]);
        console.log("volume ann (server):", res.data_cpu[1]);
        update_mychart2(res);
    });

});

