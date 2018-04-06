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
        var dataPack1 = [89, 90, 82, 84, 88, 81];
        var dataPack2 = [11, 10, 18, 16, 12, 19];
        var labels = ["A/S", "Application", "H/W", "Job Failures", "N/W", "S/W"];
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
            labels: [4000, 8000, 12000, 16000],
            datasets: [{
                data: [98, 99, 99, 99],
                label: 'Access Issues / Security Enablement',
                borderColor: 'rgba(255, 159, 64, 0.7)',
                fill: false
            }, {
                data: [93, 95, 96, 96],
                label: 'Application',
                borderColor: 'rgba(153, 102, 255, 0.7)',
                fill: false
            }, {
                data: [77, 80, 85, 85],
                label: 'H/W',
                borderColor: 'rgba(75, 192, 192, 0.7)',
                fill: false
            }, {
                data: [76, 86, 88, 89],
                label: 'Job Failures',
                borderColor: 'rgba(62, 39, 35, 0.7)',
                fill: false
            }, {
                data: [75, 81, 85, 86],
                label: 'N/W',
                borderColor: 'rgba(255, 109, 0, 0.7)',
                fill: false
            }, {
                data: [80, 80, 87, 89],
                label: 'S/W',
                borderColor: 'rgba(255, 23, 68, 0.7)',
                fill: false
            }, {
                data: [94, 95, 96, 97],
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

var analytics = {}
var mapping_table =
    {
        'Access Issues / Security Enablement': 0,
        'Application': 1,
        'H/W': 2,
        'Job Failures': 3,
        'Misc': 4,
        'N/W': 5,
        'S/W': 6
    };

function grabFirebaseData() {
    var db = firebase.database()
    var tickets_ref = db.ref('tickets/');

    //dataTable
    $('#table_wrapper').DataTable(
        {
            "columns": [
                null,
                null,
                null,
                {"width": "20%"},
                {"width": "20%"},
            ],
            // "bDestroy": true,
            // "bServerSide": true,
        }
    );

    tickets_ref.on("value", function (snapshot) {
        var data = snapshot.val();
        var output = "";

        //
        $("#table_wrapper").DataTable().clear().destroy();
        analytics = {
            total: {
                total: 0,
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0
            },
            no_correct: {
                total: 0,
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0
            }
        };

        document.getElementById("ticket_table").innerHTML = output;
        console.log(data);
        $.each(data, function (index, value) {
            output += "<tr><td>" + value.name + "</td>";
            output += "<td>" + value.email + "</td>";
            output += "<td style='text-align: left;'>" + value.desc + "</td>";
            output += "<td>" + value.prediction + "</td>";
            output += "<td>" + (value.confidence * 100).toFixed(2) + "%</td>";
            output += "<td><div class=\"switch \"><label>No<input type=\"checkbox\" onchange=\"uncheckSwitchBox(this)\" href=\"#modal\" target=\"" + index + "\" prediction=\"" + value.prediction + "\" checked><span class=\"lever\"></span>Yes</label></div></td></tr>"

            analytics.total.total += 1

        });
        document.getElementById("ticket_table").innerHTML += output;

        $('#table_wrapper').DataTable(
            {
                "columns": [
                    null,
                    null,
                    null,
                    {"width": "20%"},
                    {"width": "20%"},
                ],
                // "bDestroy": true,
                // "bServerSide": true,
            }
        );

        // dataTable.row.add([
        //     data.name,
        //     data.email,
        //     data.desc,
        //     data.prediction
        //
        // ]).draw(false);


        // tickets_ref.on("child_added", function (snapshot) {
        //     console.log(snapshot.val())
        // })
    })

}

function uncheckSwitchBox(element) {
    if (!$(element).is(':checked')) {
        var dataIndex = $(element).attr("target");
        var prediction = $(element).attr("prediction");
        console.log(dataIndex);
        console.log(prediction);
        $('select').formSelect();
        $('#modal').modal();
        $('#modal').modal('open');

        var confirmBtn = $('#modal').find('#confirm_btn');
        confirmBtn.on('click', function () {
            var actual = $('#actualCategory_select').find('select').val();
            console.log(actual);

        });
    }
}

grabFirebaseData();