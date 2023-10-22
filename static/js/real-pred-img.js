$.post('/tree-regression', {x_label: xLabel, y_label: yLabel}, function(data) {
    var chart = echarts.init(document.getElementById('main-content'));
    var option = {
        title: {
            text: '真实值与预测值对比图'
        },
        tooltip: {},
        legend: {
            data:['真实值', '预测值']
        },
        xAxis: {
            data: data.xAxis
        },
        yAxis: {},
        series: [{
            name: '真实值',
            type: 'line',
            data: data.real_values
        }, {
            name: '预测值',
            type: 'line',
            data: data.predicted_values
        }]
    };
    chart.setOption(option);
});