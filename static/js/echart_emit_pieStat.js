// EChart: Pie chart: total number of regular and anomaly
// author: Zhida Li
// last modified: Feb. 24, 2022

var myChart_pie = echarts.init(document.getElementById('echart_pie'));
// initial load the animation
myChart_pie.showLoading();

var bgp_regular = 5,
    bgp_anomaly = 0

pie_regular = 'rgba(56,118,143,0.65)'
pie_anomaly = 'rgba(180,118,118,0.76)'

myChart_pie.setOption({
    title: {
        text: 'Detection Statistics',
        // subtext: '',
        left: 'center'
    },
    tooltip: {
        trigger: 'item'
    },
    series: [
        {
            name: 'Number of data points',
            type: 'pie',
            radius: '65%',
            data: [
                {value: bgp_regular, name: 'Regular'},
                // {value: bgp_anomaly, name: 'Anomaly'},
            ],
            color: [
                pie_regular
            ],
        }
    ]
})

// callback function
var update_mychart_pie = function (res) {

    // hide animation
    myChart_pie.hideLoading();

    // prepare data
    bgp_regular = res.data_pie[0]
    bgp_anomaly = res.data_pie[1]

    if (bgp_anomaly === 0) {
        // fill the data
        myChart_pie.setOption({
            series: [
                {
                    name: 'Number of data points',
                    data: [
                        {value: bgp_regular, name: 'Regular'}
                    ],
                    color: [
                        pie_regular
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        })
    } else {
        // fill the data
        myChart_pie.setOption({
            series: [
                {
                    name: 'Number of data points',
                    data: [
                        {value: bgp_regular, name: 'Regular'},
                        {value: bgp_anomaly, name: 'Anomaly'},
                    ],
                    color: [
                        pie_regular,
                        pie_anomaly
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        })
    }
};


// establish socket connection, wait for the server push data
$(document).ready(function () {
    namespace = '/test_conn';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('server_response_echart_pie', function (res) {
        // console.log("Regular (server -> client):", res.data_pie[0]);  // for debug
        // console.log("Anomaly (server -> client):", res.data_pie[1]);  // for debug
        update_mychart_pie(res);
        var results_total_time = res.data_pie[2];
        $('#results_total_time').text(results_total_time + " " + " minutes");
        // console.log("Total time (server -> client):", results_total_time);  // for debug
    });
});
