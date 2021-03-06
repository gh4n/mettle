var myPieChart;
var stackedBar;

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
        myPieChart = new Chart(ctx, {
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
        stackedBar = new Chart(ctx, {
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
        'N/W': 4,
        'S/W': 5
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
                null,
                {"width": "20%"},
                {"width": "20%"},
                null
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
                5: 0,
            }
        };

        document.getElementById("ticket_table").innerHTML = output;
        console.log('table refreshed');
        console.log(data);
        $.each(data, function (index, value) {
            output += "<tr><td>" + value.name + "</td>";
            output += "<td>" + value.email + "</td>";
            output += "<td style='text-align: left;'>" + value.desc + "</td>";
            output += "<td>" + value.prediction + "</td>";
            output += "<td>" + (value.confidence * 100).toFixed(2) + "%</td>";
            if (value.actual === "NULL") {
                output += "<td><div class=\"switch \"><label>No<input type=\"checkbox\" onchange=\"uncheckSwitchBox(this)\" href=\"#modal\" target=\"" + index + "\" prediction=\"" + value.prediction + "\" checked><span class=\"lever\"></span>Yes</label></div></td>";
            }
            else {
                output += "<td><div class=\"switch \"><label>No<input type=\"checkbox\" onchange=\"uncheckSwitchBox(this)\" href=\"#modal\" target=\"" + index + "\" prediction=\"" + value.prediction + "\"><span class=\"lever\"></span>Yes</label></div></td>";

            }
            output += "<td><label><input type='checkbox' target=\"" + index + "\" onchange=\"resolveTicket(this)\" /><span></span></label></td></tr>";

            analytics.total.total += 1;
            var category_int = mapping_table[value.prediction];
            console.log(category_int);
            // Make sure prediction is not NULL
            analytics.total[category_int] += 1

            if (value.actual === "NULL") {
                console.log('updating category');
                analytics.no_correct.total += 1;
                analytics.no_correct[category_int] += 1
            }

        });
        document.getElementById("ticket_table").innerHTML += output;
        $('#table_wrapper').DataTable(
            {
                "columns": [
                    null,
                    null,
                    null,
                    null,
                    {"width": "20%"},
                    {"width": "20%"},
                    null
                ],
                // "bDestroy": true,
                // "bServerSide": true,
            }
        );

        var percentage_correct = (analytics.no_correct.total / analytics.total.total) * 100
        percentage_correct = percentage_correct.toFixed(2);
        console.log(percentage_correct)
        myPieChart.config.data.datasets[0].data = [100 - percentage_correct, percentage_correct]
        myPieChart.update()

        var category_correct = [];
        var category_incorrect = [];
        // var cat_0_pc = (analytics.no_correct[0]/analytics.total[0]) * 100;
        // cat_0_pc.toFixed(2)

        for (var i = 0; i < 6; i++) {
            category_correct[i] = (analytics.no_correct[i] / analytics.total[i]) * 100;
            category_correct[i].toFixed(2);
            category_incorrect[i] = 100 - category_correct[i];
        }

        stackedBar.config.data.datasets[0].data = category_correct;
        stackedBar.config.data.datasets[1].data = category_incorrect;
        stackedBar.update()

        console.log(analytics)
        console.log(category_correct)
    })

}

function uncheckSwitchBox(element) {
    var db = firebase.database();
    var dataIndex = $(element).attr("target");
    var prediction = $(element).attr("prediction");

    if (!$(element).is(':checked')) {
        console.log(dataIndex);
        console.log(prediction);
        $('select').formSelect();
        $('#modal').modal();
        $('#modal').modal('open');

        var confirmBtn = $('#modal').find('#confirm_btn');
        confirmBtn.on('click', function () {
            var corrected = $('#actualCategory_select').find('select').val();
            console.log(corrected);
            db.ref('tickets/' + dataIndex).update({
                actual: corrected
            });
            $('select').val("");

        });
    }
    else {
        db.ref('tickets/' + dataIndex).update({
            actual: "NULL"
        });
    }
}

function resolveTicket(element) {
    if ($(element).is(':checked')) {
        var dataIndex = $(element).attr("target");
        console.log(dataIndex);

        var db = firebase.database()
        db.ref('tickets/' + dataIndex).update({
            resolved: true
        });

    }
}

grabFirebaseData();