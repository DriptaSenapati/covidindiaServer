$(document).ready(function () {
  $("li:eq(5)").addClass("active");
  var slider_1 = document.getElementById("slider-1");
  var silder_value_1 = document.getElementById("value-1");
  var slider_2 = document.getElementById("slider-2");
  var silder_value_2 = document.getElementById("value-2");
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");
  $("svg").click(function () {
    // console.log($(this));
    var info = document.querySelector(".status");
    info.classList.remove("animate1");
    info.classList.remove("animate2");
    var reload = document.querySelector("svg");
    reload.classList.add("reload");
    $.get("/refresh/analysis", function (data, textStatus, jqXHR) {
      if (data == "Updated") {
        $(".status").text("Already Updated");
        info.classList.add("animate1");
      } else {
        location.reload();
      }

      // $(".status").text(null);
      reload.classList.remove("reload");
      // info.classList.remove("animate");
    });
  });
  slider_1.oninput = function () {
    silder_value_1.innerHTML = this.value;
  };
  slider_2.oninput = function () {
    silder_value_2.innerHTML = this.value;
  };
  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
  $("select").niceSelect();
  var state = $("#graph-state").val();
  var Daily = $("#daily").val();
  var cond = $("#cond-id").val();
  var slide = $("#slider-1").val();
  if (Daily === "Yes") {
    var q = "Daily";
  } else {
    var q = "cumulative";
  }
  $.post(
    "/statistics/corona_graph",
    {
      state_data: JSON.stringify(state),
      daily_data: JSON.stringify(Daily),
      condition_data: JSON.stringify(cond),
      silder_data: slide,
    },
    function (data, status, xhr) {
      // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
      if (cond != "Together") {
        var response = {
          labels: Object.keys(data[0]).slice(1),
          datasets: [
            {
              label: state + " " + q + " Count cases " + cond,
              data: Object.values(data[data.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: ["rgba(255, 0, 0, 1)"],
              fill: false,
              borderWidth: 1,
            },
          ],
        };
        var ctx = document.getElementById("graph").getContext("2d");
        GetGraphData("line", response, ctx, (id = 1));
      } else {
        var cond_list = ["Confirmed", "Recovered", "Deceased"];
        var border_Color = [
          "rgba(255, 0, 0, 1)",
          "rgba(0, 255, 0, 1)",
          "rgba(0, 0, 255, 1)",
        ];
        var d = [];
        for (i = 0; i < data.length; i++) {
          var df = JSON.parse(data[i]);
          d.push({
            label: state + " " + q + " Count cases " + cond_list[i],
            data: Object.values(df[df.length - 1]).slice(1),
            backgroundColor: ["rgba(255, 50, 50, 1)"],
            borderColor: border_Color[i],
            fill: false,
            borderWidth: 1,
          });
        }
        var response = {
          labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
          datasets: d,
        };
        var ctx = document.getElementById("graph").getContext("2d");
        GetGraphData("line", response, ctx, (id = 1));
      }
    }
  );
  $("#graph-state").change(function () {
    var state = $(this).val();
    var Daily = $("#daily").val();
    var cond = $("#cond-id").val();
    var slide = $("#slider-1").val();
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/statistics/corona_graph",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  $("#daily").change(function () {
    var state = $("#graph-state").val();
    var Daily = $(this).val();
    var cond = $("#cond-id").val();
    var slide = $("#slider-1").val();
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/statistics/corona_graph",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  $("#cond-id").change(function () {
    var state = $("#graph-state").val();
    var Daily = $("#daily").val();
    var cond = $(this).val();
    var slide = $("#slider-1").val();
    // console.log(cond);
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/statistics/corona_graph",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  $("#slider-1").change(function () {
    var state = $("#graph-state").val();
    var Daily = $("#daily").val();
    var cond = $("#cond-id").val();
    var slide = $(this).val();
    // console.log(cond);
    if (Daily === "Yes") {
      var q = "Daily";
    } else {
      var q = "cumulative";
    }
    $.post(
      "/statistics/corona_graph",
      {
        state_data: JSON.stringify(state),
        daily_data: JSON.stringify(Daily),
        condition_data: JSON.stringify(cond),
        silder_data: slide,
      },
      function (data, status, xhr) {
        // console.log(Object.keys(JSON.parse(data[0])[0]).slice(1));
        if (cond != "Together") {
          var response = {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state + " " + q + " Count cases " + cond,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: ["rgba(255, 50, 50, 1)"],
                borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        } else {
          var cond_list = ["Confirmed", "Recovered", "Deceased"];
          var border_Color = [
            "rgba(255, 0, 0, 1)",
            "rgba(0, 255, 0, 1)",
            "rgba(0, 0, 255, 1)",
          ];
          var d = [];
          for (i = 0; i < data.length; i++) {
            var df = JSON.parse(data[i]);
            d.push({
              label: state + " " + q + " Count cases " + cond_list[i],
              data: Object.values(df[df.length - 1]).slice(1),
              backgroundColor: ["rgba(255, 50, 50, 1)"],
              borderColor: border_Color[i],
              fill: false,
              borderWidth: 1,
            });
          }
          var response = {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: d,
          };
          var ctx = document.getElementById("graph").getContext("2d");
          GetGraphData("line", response, ctx, (id = 1));
        }
      }
    );
  });
  if ($("#g-2_chk-2").is(":checked")) {
    $.post(
      "/tested",
      {
        ratio_data: "true",
      },
      function (data, status, xhr) {
        var xlabel = [];
        var ylabel = [];
        var color = [];
        var op = 1;
        for (i = 0; i < data.length; i++) {
          xlabel.push(Object.values(data[i])[0]);
          ylabel.push(Object.values(data[i])[4]);
          color.push("rgba(0,255,0," + op + ")");
          op = op - 1 / (data.length + 5);
        }

        var response = {
          labels: xlabel,
          datasets: [
            {
              label: "Confirmed to Test Ratio(F)",
              data: ylabel,
              backgroundColor: color,
              // borderColor: ["rgba(255, 0, 0, 1)"],
              fill: false,
              borderWidth: 1,
            },
          ],
        };
        var ctx = document.getElementById("graph-2").getContext("2d");
        GetGraphData("bar", response, ctx, (id = 2));
      }
    );
  }
  $("#g-2_chk-2").change(function () {
    if ($("#g-2_chk-2").is(":checked")) {
      $.post(
        "/tested",
        {
          ratio_data: "true",
        },
        function (data, status, xhr) {
          var xlabel = [];
          var ylabel = [];
          var color = [];
          var op = 1;
          for (i = 0; i < data.length; i++) {
            xlabel.push(Object.values(data[i])[0]);
            ylabel.push(Object.values(data[i])[4]);
            color.push("rgba(0,255,0," + op + ")");
            op = op - 1 / (data.length + 5);
          }

          var response = {
            labels: xlabel,
            datasets: [
              {
                label: "Confirmed to Test Ratio(F)",
                data: ylabel,
                backgroundColor: color,
                // borderColor: ["rgba(255, 0, 0, 1)"],
                fill: false,
                borderWidth: 1,
              },
            ],
          };
          var ctx = document.getElementById("graph-2").getContext("2d");
          GetGraphData("bar", response, ctx, (id = 2));
        }
      );
    }
  });
  $("#g-2_chk-1").change(function () {
    if ($("#g-2_chk-1").is(":checked")) {
      {
        $.post(
          "/tested",
          {
            ratio_data: "false",
          },
          function (data, status, xhr) {
            console.log(data);
            var xlabel = [];
            var ylabel = [];
            var color = [];
            var op = 1;
            for (i = 0; i < data.length; i++) {
              xlabel.push(Object.values(data[i])[0]);
              ylabel.push(Object.values(data[i])[6]);
              color.push("rgba(0,255,0," + op + ")");
              op = op - 1 / (data.length + 5);
            }
            var response = {
              labels: xlabel,
              datasets: [
                {
                  label: "Total tested",
                  data: ylabel,
                  backgroundColor: color,
                  // borderColor: ["rgba(255, 0, 0, 1)"],
                  fill: false,
                  borderWidth: 1,
                },
              ],
            };
            var ctx = document.getElementById("graph-2").getContext("2d");
            GetGraphData("bar", response, ctx, (id = 2));
          }
        );
      }
    }
  });
  $.post(
    "/rec_dec_rate",
    {
      rate: "recovered",
    },
    function (data, status, xhr) {
      console.log(data);
      var xlabel = [];
      var ylabel = [];
      var color = [];
      var border = [];
      var op = 0.83;
      for (i = 0; i < data.length; i++) {
        xlabel.push(Object.values(data[i])[0]);
        ylabel.push(Object.values(data[i])[4]);
        color.push("rgba(174,255,215," + op + ")");
        border.push("rgba(174,255,215,0.91)");
        op = op - 1 / (data.length + 5);
      }
      var response = {
        labels: xlabel,
        datasets: [
          {
            label: "Recovery Rate(R)",
            data: ylabel,
            backgroundColor: color,
            // barThickness: 15,
            borderColor: border,
            fill: false,
            borderWidth: 1,
          },
        ],
      };
      var ctx = document.getElementById("graph-3").getContext("2d");
      GetGraphData("horizontalBar", response, ctx, (id = 3));
    }
  );
  $.post(
    "/rec_dec_rate",
    {
      rate: "deceased",
    },
    function (data, status, xhr) {
      console.log(data);
      var xlabel = [];
      var ylabel = [];
      var color = [];
      var border = [];
      var op = 0.83;
      for (i = 0; i < data.length; i++) {
        xlabel.push(Object.values(data[i])[0]);
        ylabel.push(Object.values(data[i])[5]);
        color.push("rgba(131,247,244," + op + ")");
        border.push("rgba(131,247,244,0.91)");
        op = op - 1 / (data.length + 5);
      }
      var response = {
        labels: xlabel,
        datasets: [
          {
            label: "Deceased Rate(D)",
            data: ylabel,
            backgroundColor: color,
            // barThickness: 15,
            borderColor: border,
            fill: false,
            borderWidth: 1,
          },
        ],
      };
      var ctx = document.getElementById("graph-4").getContext("2d");
      GetGraphData("horizontalBar", response, ctx, (id = 4));
    }
  );
  $.get("/statistics/age_bar_chart", function (data, textStatus, jqXHR) {
    console.log(data);
    var xlabel = [];
    var ylabel = [];
    for (i = 0; i < data.length; i++) {
      xlabel.push(Object.values(data[i])[0]);
      ylabel.push(Object.values(data[i])[1]);
    }
    var response = {
      labels: xlabel,
      datasets: [
        {
          label: "Cases",
          data: ylabel,
          backgroundColor: "rgba(255, 0, 255,0.5)",
          borderColor: "rgba(255, 0, 255,1)",
          fill: false,
          borderWidth: 1,
        },
      ],
    };
    var ctx = document.getElementById("graph-5").getContext("2d");
    GetGraphData("bar", response, ctx, (id = 5));
  });
  $.post(
    "/statistics/rolling_growth",
    {
      rolling: $("#slider-2").val(),
    },
    function (data, status, xhr) {
      console.log(data);
      var xlabel = Object.keys(data[0]).slice(1);
      var dataset = [];
      window.color = [];
      for (i = 0; i < data.length; i++) {
        window.color.push(getRandomColor());
        var tip = Object.values(data[i])[0];
        var ylabel = Object.values(data[i]).slice(1);
        if (window.innerWidth < 1000) {
          var pointradius = 1;
        } else {
          var pointradius = 2;
        }
        var dict = {
          label: tip,
          data: ylabel,
          backgroundColor: color[i],
          borderColor: color[i],
          fill: false,
          borderWidth: 1,
          pointRadius: pointradius,
        };
        dataset.push(dict);
      }
      var response = {
        labels: xlabel,
        datasets: dataset,
      };
      var ctx = document.getElementById("graph-6").getContext("2d");
      GetGraphData("line", response, ctx, (id = 6));
    }
  );
  $("#slider-2").change(function () {
    $.post(
      "/statistics/rolling_growth",
      {
        rolling: $("#slider-2").val(),
      },
      function (data, status, xhr) {
        // console.log(data);
        var xlabel = Object.keys(data[0]).slice(1);
        var dataset = [];
        for (i = 0; i < data.length; i++) {
          // var color = getRandomColor();
          var tip = Object.values(data[i])[0];
          var ylabel = Object.values(data[i]).slice(1);
          if (window.innerWidth < 1000) {
            var pointradius = 1;
          } else {
            var pointradius = 2;
          }
          var dict = {
            label: tip,
            data: ylabel,
            backgroundColor: window.color[i],
            borderColor: window.color[i],
            fill: false,
            borderWidth: 1,
            pointRadius: pointradius,
          };
          dataset.push(dict);
        }
        var response = {
          labels: xlabel,
          datasets: dataset,
        };
        // var ctx = document.getElementById("graph-6").getContext("2d");
        // GetGraphData("line", response, ctx, (id = 6));
        window.myChart6.data.labels = xlabel;
        window.myChart6.data.datasets = dataset;
        window.myChart6.update();
      }
    );
  });
});
function getRandomColor() {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
function GetGraphData(e, f, g, id) {
  if (id == 1) {
    if (window.myChart) window.myChart.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart = new Chart(g, {
      type: e,
      data: f,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "#735959",
              },
            },
          ],
          xAxes: [
            {
              ticks: {
                fontColor: "#735959",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
          intersect: true,
        },
        legend: {
          display: true,
          labels: {
            fontColor: "#735959",
          },
        },
      },
    });
  }
  if (id == 2) {
    if (window.myChart2) window.myChart2.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart2 = new Chart(g, {
      type: e,
      data: f,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "#735959",
              },
            },
          ],
          xAxes: [
            {
              ticks: {
                fontColor: "#735959",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
          intersect: true,
        },
        legend: {
          display: true,
          labels: {
            fontColor: "#735959",
          },
        },
      },
    });
  }
  if (id == 3) {
    if (window.myChart3) window.myChart3.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart3 = new Chart(g, {
      type: e,
      data: f,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "#735959",
              },
            },
          ],
          xAxes: [
            {
              // categoryPercentage: 1.0,
              // barPercentage: 0.5,
              ticks: {
                fontColor: "#735959",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
          intersect: true,
        },
        legend: {
          display: true,
          labels: {
            fontColor: "#735959",
          },
        },
      },
    });
  }
  if (id == 4) {
    if (window.myChart4) window.myChart4.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart4 = new Chart(g, {
      type: e,
      data: f,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "#735959",
              },
            },
          ],
          xAxes: [
            {
              categoryPercentage: 1.0,
              barPercentage: 0.5,
              ticks: {
                fontColor: "#735959",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
          intersect: true,
        },
        legend: {
          display: true,
          labels: {
            fontColor: "#735959",
          },
        },
      },
    });
  }
  if (id == 5) {
    if (window.myChart5) window.myChart5.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart5 = new Chart(g, {
      type: e,
      data: f,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 2000,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "#735959",
              },
            },
          ],
          xAxes: [
            {
              ticks: {
                fontColor: "#735959",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
          intersect: true,
        },
        legend: {
          display: true,
          labels: {
            fontColor: "#735959",
          },
        },
      },
    });
  }
  if (id == 6) {
    if (window.myChart6) window.myChart6.destroy();
    // var ctx = document.getElementById("graph").getContext("2d");
    // console.log(window.myChart);

    window.myChart6 = new Chart(g, {
      type: e,
      data: f,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 2000,
        },
        layout: {
          padding: {
            top: 25, //set that fits the best
          },
        },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                fontColor: "#735959",
              },
            },
          ],
          xAxes: [
            {
              ticks: {
                fontColor: "#735959",
              },
            },
          ],
        },
        tooltips: {
          mode: "index",
          intersect: true,
          yAlign: "bottom",
          position: "average",
        },
        legend: {
          display: true,
          labels: {
            fontColor: "#735959",
          },
          onClick: function (e, legendItem) {
            var index = legendItem.datasetIndex;
            var ci = this.chart;
            var alreadyHidden =
              ci.getDatasetMeta(index).hidden === null
                ? false
                : ci.getDatasetMeta(index).hidden;

            ci.data.datasets.forEach(function (e, i) {
              var meta = ci.getDatasetMeta(i);

              if (i !== index) {
                if (!alreadyHidden) {
                  meta.hidden = meta.hidden === null ? !meta.hidden : null;
                } else if (meta.hidden === null) {
                  meta.hidden = true;
                }
              } else if (i === index) {
                meta.hidden = null;
              }
            });

            ci.update();
          },
        },
      },
    });
  }
}
