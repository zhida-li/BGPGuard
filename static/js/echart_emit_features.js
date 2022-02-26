// EChart: features vs. time
// author: Zhida Li
// last modified: Feb. 22, 2022

var chartDom2 = document.getElementById('echart_features');
var myChart2 = echarts.init(chartDom2); //, 'dark');
// initial load the animation
myChart2.showLoading();

myChart2.setOption({
    title: {
        text: 'Volume features vs. time'
    },
    // The border frame is shown when using grid function
    grid: [
        {
            bottom: '55%', show: true
        },
        {
            top: '55%', show: true
        }
    ],
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
        data: ['BGP announcements', 'BGP withdrawals']
    },
    xAxis: [
        {
            data: [],
            gridIndex: 0
        },
        {
            data: [],
            gridIndex: 1,
            name: 'Time (min)',
            nameLocation: 'middle',
            nameGap: 25
        }
    ],
    yAxis: [
        {
            gridIndex: 0,
            name: 'Number of announcements',
            nameLocation: 'middle',
            nameGap: 50
        },
        {
            gridIndex: 1,
            name: 'Number of withdrawals',
            nameLocation: 'middle',
            nameGap: 50
        },
    ],
    series: [
        {
            name: 'BGP announcements',
            data: [],  //y values
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            color: 'rgba(0,51,180,0.62)'

        },
        {
            name: 'BGP withdrawals',
            data: [],  //y values
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            color: 'rgba(99,140,78,0.69)'  // '#25afb4'
        }
    ],

    // visualMap: [
    //     {
    //         show: false,  // bar reference
    //         type: 'continuous',
    //         seriesIndex: 0,
    //         min: 0,
    //         max: 6e3
    //     }]
    //     // {
    //     //     show: true,  // bar reference
    //     //     type: 'continuous',
    //     //     seriesIndex: 1,
    //     //     min: 0,
    //     //     max: 1e3
    //     // }]
});


var t_ann = Array(25).fill(""),
    bgp_ann = Array(25).fill(""),
    bgp_wd = Array(25).fill("")

// callback function
var update_mychart2 = function (res) {

    // hide animation if comment it
    myChart2.hideLoading();

    // prepare data
    Array.prototype.push.apply(t_ann, res.data_features[0]);
    Array.prototype.push.apply(bgp_ann, res.data_features[1]);
    Array.prototype.push.apply(bgp_wd, res.data_features[2]);
    // console.log("push t (chart):", t_ann);  // for debug
    // console.log("push volume ann (chart):", bgp_ann);  // for debug
    if (t_ann.length >= 60 * 2 + 5) {
        // remove the first 5 elements
        t_ann.splice(0, 5);
        bgp_ann.splice(0, 5);
        bgp_wd.splice(0, 5);
    }

    // fill the data
    myChart2.setOption({
        xAxis: [
            {
                data: t_ann,
                show: true,  //false will remove the x-axis
                gridIndex: 0
            },
            {
                data: t_ann,
                gridIndex: 1,
            }],
        series: [
            {
                name: 'BGP announcements', // related to the data name in legend
                data: bgp_ann,
                xAxisIndex: 0,
                yAxisIndex: 0
            },
            {
                name: 'BGP withdrawals', // related to the data name in legend
                data: bgp_wd,
                xAxisIndex: 1,
                yAxisIndex: 1
            }]
    });
};


// establish socket connection, wait for the server push data, use the callback function update chart
$(document).ready(function () {
    namespace = '/test_conn';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('server_response_echart2', function (res) {
        // console.log("t (server -> client):", res.data_features[0]);  // for debug
        // console.log("volume ann (server -> client):", res.data_features[1]);  // for debug
        // console.log("volume wdrl (server -> client):", res.data_features[2]);  // for debug
        update_mychart2(res);
    });
});
