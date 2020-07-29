$(document).ready(function () {
  $("li:eq(0)").addClass("active");
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");

  // $("#map").vectorMap({ map: "in_mill" });

  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });

  $.post(
    "/statistics/mapdata",
    {
      dtype: "confirmed",
    },
    function (data, status, xhr) {
      console.log(data);
      var map = data[0];
      jvmGraph(map, "#ffe6e6", "#ff1c1c", "Confirmed");
    }
  );
  $(".Recovered-1").hover(function () {
    var up_recover = document.querySelector(".up_recover");
    up_recover.classList.toggle("up_activate");
    $.post(
      "/statistics/mapdata",
      {
        dtype: "recovered",
      },
      function (data, status, xhr) {
        console.log(data);
        var map = data[0];
        jvmGraph(map, "#e3ffe3", "#00bf00", "Recovered");
        // var c = jQuery("#map").vectorMap("get", "mapObject");
        // console.log(c.series.regions[0]);
        // console.log(Object.values(data[0]));
        // c.series.regions[0].setValues(Object.values(data[1]));
        // console.log(chart);
      }
    );
  });
  $(".Deceased-1").hover(function () {
    var up_death = document.querySelector(".up_death");
    up_death.classList.toggle("up_activate");
    $.post(
      "/statistics/mapdata",
      {
        dtype: "death",
      },
      function (data, status, xhr) {
        console.log(data);
        var map = data[0];
        jvmGraph(map, "#b0d0ff", "#0046ad", "Deceased");
        // var c = jQuery("#map").vectorMap("get", "mapObject");
        // console.log(c.series.regions[0]);
        // console.log(Object.values(data[0]));
        // c.series.regions[0].setValues(Object.values(data[1]));
        // console.log(chart);
      }
    );
  });
  $(".confirmed-1").hover(function () {
    var up_conf = document.querySelector(".up_text");
    up_conf.classList.toggle("up_activate");
    $.post(
      "/statistics/mapdata",
      {
        dtype: "confirmed",
      },
      function (data, status, xhr) {
        console.log(data);
        var map = data[0];
        jvmGraph(map, "#ffe6e6", "#ff1c1c", "Confirmed");
        // var c = jQuery("#map").vectorMap("get", "mapObject");
        // console.log(c.series.regions[0]);
        // console.log(Object.values(data[0]));
        // c.series.regions[0].setValues(Object.values(data[1]));
        // console.log(chart);
      }
    );
  });
  $(".Active-1").hover(function () {
    var up_active = document.querySelector(".up_active");
    up_active.classList.toggle("up_activate");
    $.post(
      "/statistics/mapdata",
      {
        dtype: "active",
      },
      function (data, status, xhr) {
        console.log(data);
        var map = data[0];
        jvmGraph(map, "#fbe0ff", "#9500ab", "Active");
        // var c = jQuery("#map").vectorMap("get", "mapObject");
        // console.log(c.series.regions[0]);
        // console.log(Object.values(data[0]));
        // c.series.regions[0].setValues(Object.values(data[1]));
        // console.log(chart);
      }
    );
  });
  $.post(
    "/State",
    {
      state_data: "All",
      district_data: "none",
      date_data: "All",
      daily_data: "No",
    },
    function (data, status, xhr) {
      var df = data;
      console.log(df);
      var datalist = [];
      var datalist_death = [];
      var datalist_recover = [];
      var label = [];
      var color = [];
      var color_death = [];
      var color_recover = [];
      for (i = 0; i < df.length - 2; i++) {
        datalist.push(Object.values(df[i])[1]);
        datalist_death.push(Object.values(df[i])[3]);
        datalist_recover.push(Object.values(df[i])[2]);
        label.push(Object.values(df[i])[0]);
        color.push(getRandomColor());
        color_death.push(getRandomColor());
        color_recover.push(getRandomColor());
      }
      var ctx = document.getElementById("graph").getContext("2d");
      var ctx_death = document.getElementById("graph_death").getContext("2d");
      var ctx_recover = document
        .getElementById("graph_recover")
        .getContext("2d");
      var myPieChart = new Chart(ctx, {
        type: "pie",
        data: {
          datasets: [
            {
              data: datalist,
              backgroundColor: color,
            },
          ],
          labels: label,
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: {
            duration: 2000,
          },
          legend: {
            display: true,
          },
        },
      });
      console.log(window.innerWidth);
      var myPieChart_death = new Chart(ctx_death, {
        type: "pie",
        data: {
          datasets: [
            {
              data: datalist_death,
              backgroundColor: color_death,
            },
          ],
          labels: label,
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: {
            duration: 2000,
          },
          legend: {
            display: true,
          },
        },
      });
      var myPieChart_recover = new Chart(ctx_recover, {
        type: "pie",
        data: {
          datasets: [
            {
              data: datalist_recover,
              backgroundColor: color_recover,
            },
          ],
          labels: label,
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: {
            duration: 2000,
          },
          legend: {
            display: true,
          },
        },
      });
      if (window.innerWidth < 1000) {
        myPieChart.options.legend.display = false;
        myPieChart_death.options.legend.display = false;
        myPieChart_recover.options.legend.display = false;
        myPieChart.update();
        myPieChart_death.update();
        myPieChart_recover.update();
        // console.log(myPieChart.options.legend.display);
      }
    }
  );
});
function jvmGraph(data, Colormin, colormax, tooltip) {
  if (window.chart) {
    window.chart.remove();
  }
  window.chart = new jvm.Map({
    container: $("#map"),
    map: "in_mill",
    // backgroundColor: "#ff0000",
    series: {
      regions: [
        {
          values: data,
          scale: [Colormin, colormax],
          hoverColor: "#ff0000",
          normalizeFunction: "polynomial",
          legend: {
            horizontal: true,
            title: "Color Scale",
          },
        },
      ],
    },
    onRegionTipShow: function (e, el, code) {
      el.html(el.html() + " (" + tooltip + " - " + data[code] + ")");
    },
  });
  window.chart.updateSize();
  console.log(window.chart);
}
function myloader() {
  var load = document.getElementById("loader");
  load.style.display = "none";
}
function getRandomColor() {
  var letters = "0123456789ABCDEF";
  var color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
