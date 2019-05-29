const ws = new WebSocket('ws://172.16.123.11:8080');

var plot_data = {
    labels: [],
    datasets: []
};
var options = {
    animation: false,
    //Boolean - If we want to override with a hard coded scale
    scales: {
        xAxes: [{
            display: true,
            scaleLabel: {
                display: true,
                labelString: 'Signal'
            }
        }],
        yAxes: [{
            display: true,
            ticks: {
                beginAtZero: true,
                steps: 11,
                stepValue: 10,
                max: 0,
                min: -100
            }
        }]
    }
};


function wsconnect() {


    setInterval(function () { remove_old(); }, 10000);
    ws.onopen = function (evt) { console.log('openend'); };
    //ws.onclose = function (evt) { onClose(evt) };
    ws.onmessage = function (evt) {
        // console.log(evt.data);
        var data = JSON.parse(evt.data);
        var ctx = document.getElementById("rinsChart").getContext("2d");
        update_data(data.station, data);
        console.log(plot_data)
        var lineChart = new Chart(ctx, {
            type: "bar",
            data: plot_data,
            options: options
        });
    };

}


function find_label(datas, label) {
    var result = datas.find(obj => {
        return obj.label === label
    })
    return result

}

function update_data(labelv, value) {
    var d = find_label(plot_data.datasets, labelv);
    if (d != null) {
        d.data = [value.dbm]
        d.seen = Date.now()
        console.log('Update data')
    } else {
        var sid = labelv.split(':');
        var ds = {
            label: labelv,
            backgroundColor: "#" + sid[0] + sid[2] + sid[4],
            data: [value.dbm],
            seen: Date.now()
        };
        plot_data.datasets.push(ds);
        // plot_data.labels.push(labelv)
        console.log('Adding station data')
    }

}


function remove_old() {
    plot_data.datasets = plot_data.datasets.filter(function (v, i) {
        return (((Date.now() - v.seen) < 10000));
    })
}