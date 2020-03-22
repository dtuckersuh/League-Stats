var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['03/14','03/15', '03/16', '03/17', '03/18', '03/19', '03/20'],
        datasets : [{
            label: 'LP',
            data : [64, 50, 74, 56, 45, 55, 78],
            backgroundColor: "rgba(44, 144, 61, 1)"
        }]
    },
    options: {
        title: {
            display: true,
            text: 'LP History'
        }
    }
});