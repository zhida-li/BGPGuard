// EChart

// var myChart = echarts.init(document.getElementById('echart_cpu'));
var chartDom = document.getElementById('echart_cpu');
var myChart = echarts.init(chartDom);

myChart.setOption({
    title: {
        text: 'CPU real-time usage (%)'
    },
    tooltip: {},
    legend: {
        data:['CPU']
    },
    xAxis: {
        data: []
    },
    yAxis: {},
    series: [{
        name: 'CPU',
        data: [],
        type: 'bar'
    }],

    //   visualMap: [
    // {
    //   show: false,
    //   type: 'continuous',
    //   seriesIndex: 0,
    //   min: 0,
    //   max: 30
    // }]
});


var time = ["","","","","","","","","","", "","","","","","","","","",""],
    cpu = [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0]


// callback function
var update_mychart = function (res) {

    // hide animation
    myChart.hideLoading();

    // prepare data
    time.push(res.data_cpu[0]);  //push() add new item to an array
    cpu.push(parseFloat(res.data_cpu[1]));
    if (time.length >= 10){
        time.shift();
        cpu.shift();
    }

    // fill the data
    myChart.setOption({
        xAxis: {
            data: time
        },
        series: [{
            name: 'CPU', // related to the data name in legend
            data: cpu
        }]

    });

};

// initial load the animation
myChart.showLoading();


// establish socket connection, wait for the server push data, use the callback function update chart
$(document).ready(function() {
    namespace = '/test_conn';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('server_response_echart', function(res) {
        console.log("CPU avg:", res.data_cpu[1]);
        update_mychart(res);
    });

});
