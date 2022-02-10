// EChart: labels vs. time
// author: Zhida Li
// last edit: Feb. 9, 2022

var chartDom0 = document.getElementById('echart_labels');
var myChart0 = echarts.init(chartDom0); //, 'dark');
// initial load the animation
myChart0.showLoading();

myChart0.setOption({
    title: {
        text: 'Results vs. time'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        },
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            saveAsImage: {show: true}
        }
    },
    legend: {
        data: ['Predicted class']
    },
    xAxis: {
        data: [],
        name: 'Time (min)',
        nameLocation: 'middle',
        nameGap: 25
    },
    yAxis: {
        type: 'category',
        data: ['Regular', 'Anomaly']
    },
    series: [
        {
            name: 'Predicted class',
            data: [],  //y values
            type: 'scatter',
            symbolSize: 8,
            color: 'rgb(255, 70, 131)'
        },
    ],
});


var t_ann2 = Array(40).fill(""),
    bgp_labels = Array(40).fill("")

// callback function
var update_mychart0 = function (res) {

    // hide animation
    myChart0.hideLoading();

    // prepare data
    Array.prototype.push.apply(t_ann2, res.data_labels[0]);
    Array.prototype.push.apply(bgp_labels, res.data_labels[1]);

    if (t_ann2.length >= 60 * 2) {
        // remove the first 10 elements
        t_ann2.splice(0, 10);
        bgp_labels.splice(0, 10);
    }

    // fill the data
    myChart0.setOption({
        xAxis:
            {
                data: t_ann2
            },

        series: [
            {
                name: 'Predicted class', // related to the data name in legend
                data: bgp_labels,
            }]

    });

};


// establish socket connection, wait for the server push data, use the callback function update chart
$(document).ready(function () {
    namespace = '/test_conn';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('server_response_echart0', function (res) {
        update_mychart0(res);
    });

});
