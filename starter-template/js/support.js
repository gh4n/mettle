(function ($) {
    $(function () {

        //toogle between two tabs in support page
        $('#nav').find('li').on('click', function () {
            $(this).addClass('active');
            var showPage = $(this).find('a').attr('href');
            $(showPage).removeClass('hide');
            $(this).siblings('li').removeClass('active');
            var hidePage = $(showPage).siblings('.section');
            $(hidePage).addClass('hide');
        });

        //pie charts
        var ctx = document.getElementById("myPieChart");
        var pieChartData = {
            datasets: [
                {
                    label: 'Accuracy',
                    data: [30, 70],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)'
                    ]
                }
            ],
            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: [
                'Inaccurate',
                'Accurate',
            ]
        };
        var pieChartOptions = {
            title: {
                display: true,
                text: 'Prediction Accuracy Percentage'
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        var label = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] + '%';
                        return label;
                    }
                }
            }
        };
        var myPieChart = new Chart(ctx, {
            type: 'pie',
            data: pieChartData,
            options: pieChartOptions
        });

        // bar chart
        var ctx = document.getElementById("myBarChart");
        var dataPack1 = [89, 90, 82, 84];
        var dataPack2 = [11, 10, 18, 16];
        var labels = ["Category 1", "Category 2", "Category 3", "Category 4"];
        var barChartData = [
            {
                label: 'Accurate',
                data: dataPack1,
                backgroundColor: "rgba(54, 162, 235, 0.2)"
            },
            {
                label: 'Inaccurate',
                data: dataPack2,
                backgroundColor: "rgba(255, 99, 132, 0.2)"
            }
        ];
        var barChartOptions = {
            title: {
                display: true,
                text: 'Prediction Accuracy Percentage Based on Category'
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        var label = tooltipItem.yLabel + '%';
                        return label;
                    }
                }
            },
            scales: {
                xAxes: [{
                    stacked: true,
                    ticks: {
                        autoSkip: false,
                        maxRotation: 45,
                        minRotation: 45,
                    },
                    gridLines: {
                        display: false
                    },
                }],
                yAxes: [{
                    stacked: true,
                    ticks: {
                        autoSkip: true,
                        stepSize: 20
                    },
                    gridLines: {
                        display: false
                    },
                }]
            },

        };
        var stackedBar = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: barChartData
            },
            options: barChartOptions
        });

        //line chart
        var ctx = document.getElementById("myLineChart");
        var lineChartData = {
            labels: [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
            datasets: [{
                data: [77, 78, 78, 79, 81, 82, 82, 84, 86, 89],
                label: 'Category 1',
                borderColor: 'rgba(255, 159, 64, 0.7)',
                fill: false
            }, {
                data: [74, 74, 75, 79, 81, 82, 82, 84, 86, 90],
                label: 'Category 2',
                borderColor: 'rgba(153, 102, 255, 0.7)',
                fill: false
            }, {
                data: [63, 65, 66, 66, 67, 72, 73, 76, 80, 82],
                label: 'Category 3',
                borderColor: 'rgba(75, 192, 192, 0.7)',
                fill: false
            }, {
                data: [67, 68, 69, 69, 72, 72, 73, 76, 80, 84],
                label: 'Category 4',
                borderColor: 'rgba(255, 206, 86, 0.7)',
                fill: false
            }, {
                data: [71, 72, 72, 76, 79, 81, 82, 84, 85, 86],
                label: 'Average',
                borderColor: 'rgba(54, 162, 235, 0.7)',
                fill: false
            }
            ]
        };
        var lineChartOptions = {
            title: {
                display: true,
                text: 'Model Performance'
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        var label = tooltipItem.yLabel + '%';
                        return label;
                    }
                }
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Size of Dataset'
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display: false
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Accuracy (%)'
                    }
                }]
            }
        };
        var myLineChart = new Chart(ctx, {
            type: 'line',
            data: lineChartData,
            options: lineChartOptions
        });

    }); // end of document ready
})(jQuery); // end of jQuery name spac

function grabFirebaseData() {
    var db = firebase.database()
    var tickets_ref = db.ref('tickets/');

    tickets_ref.orderByKey().once("value", function (snapshot) {
        var data = snapshot.val();
        console.log(data);

        var output = ""
        $.each(data, function (index, value) {
            console.log(value);
            output += "<tr><td>" + value.name + "</td>";
            output += "<td>" + value.email + "</td>"
            output += "<td>" + value.desc + "</td>"
            output += "<td>" + value.prediction + "</td>"
            output += "<td><div class=\"switch\"><label>No<input type=\"checkbox\" checked><span class=\"lever\"></span>Yes</label></div></td></tr>"
        })
        document.getElementById("ticket_table").innerHTML = output;
        //dataTable
        $('#table_wrapper').DataTable();

        //uncheck incorrect items
        $('input:checkbox').each(function () {
            $(this).change(
                function () {
                    if (!$(this).is(':checked')) {
                        $('select').formSelect();
                        $('#modal').modal();
                        $('#modal').modal('open');

                        var confirmBtn = $('#modal').find('#confirm_btn');
                    }
                });
        });

        tickets_ref.on("child_added", function (snapshot) {
            console.log(snapshot.val())
        })
    })

}

grabFirebaseData()