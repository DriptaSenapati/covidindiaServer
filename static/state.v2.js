$(document).ready(function () {
  $("li:eq(2)").addClass("active");
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");
  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
  $("select").niceSelect();
  GetDataState();
  $("#daily").change(function () {
    GetDataState();
  });
  $(function () {
    $("#my_date_picker").datepicker({
      dateFormat: "dd/mm/yy",
      minDate: new Date("1/30/2020"),
      maxDate: "-1D",
      beforeShow: function () {
        $(".ui-datepicker").css("font-size", 12);
        // $(".ui-datepicker").css("height", 12);
      },
    });
  });
  $("#state_name").change(function () {
    var el = $(this);
    if (el.val() != "All") {
      $.post(
        "/filter",
        {
          place_data: el.val(),
        },
        function (data, status, xhr) {
          console.log(data);
          var children = document.getElementById("state-selector").children;
          console.log(children[children.length - 2].getAttribute("id"));
          if (
            children[children.length - 2].getAttribute("id") !=
            "district-select"
          ) {
            $("#state-selector").append(
              "<select id='district-select'><option>--Select District--</option><option>All</option></select>"
            );
          }
          $("#district-select option").each(function () {
            if (
              $(this).val() != "--Select District--" &&
              $(this).val() != "All"
            ) {
              $(this).remove();
            }
          });
          for (var i = 0; i < data.length; i++) {
            if (data[i] != "Unknown") {
              $("#district-select").append("<option>" + data[i] + "</option>");
            }
          }
          if ($("#state-selector .nice-select").length > 1) {
            $("#state-selector .nice-select")[
              $("#state-selector .nice-select").length - 1
            ].remove();
          }
          $("select").niceSelect();
        }
      );
      $.post(
        "/date/state",
        {
          state: el.val(),
        },
        function (data, status, xhr) {
          $("#my_date_picker").datepicker(
            "option",
            "minDate",
            new Date(data[0])
          );
          $("#my_date_picker").datepicker(
            "option",
            "maxDate",
            new Date(data[1])
          );
        }
      );
    } else {
      $("#district-select").remove();
      $("#state-selector div:nth-child(3)").remove();
      $("#my_date_picker").datepicker(
        "option",
        "minDate",
        new Date("1/30/2020")
      );
      GetDataState();
    }
  });
  $("#my_date_picker").change(function () {
    // var el = $(this);
    // console.log(el.val());
    // if (el.val() != "") {
    //   $("#daily").remove();
    //   $("#Daily_bar .nice-select").last().remove();
    //   $(".Daily").css("display", "none");
    // } else {
    //   var children = document.getElementById("Daily_bar").children;
    //   var id = children[children.length - 2].getAttribute("id");
    //   if (id != "daily") {
    //     $("#Daily_bar").append(
    //       `<select id="daily"><option value="No">No</option><option value="Yes">Yes</option></select>`
    //     );
    //     $("select").niceSelect();
    //     $(".Daily").css("display", "inline");
    //   }
    // }
    GetDataState();
  });
  $(document).on("change", "#district-select", function () {
    GetDataState();
  });
  $(document).on("change", "#daily", function () {
    GetDataState();
  });
  $(".download").click(function () {
    var e = document.getElementById("state_name");
    var state_name = e.options[e.selectedIndex].text;
    if (state_name != "All") {
      var q = document.getElementById("district-select");
      var district_name = q.options[q.selectedIndex].text;
    } else {
      district_name = "none";
    }
    var date = document.getElementById("my_date_picker").value;
    if (date == "") {
      date = "All";
    }
    var p = document.getElementById("daily");
    var daily = p.options[p.selectedIndex].text;
    const a = document.createElement("a");
    a.style.display = "none";
    document.body.appendChild(a);
    if (date != "All") {
      a.href =
        "/get-csv/" +
        state_name +
        "-" +
        district_name +
        "-(" +
        date.split("/").join("-") +
        ")-" +
        daily;
    } else {
      a.href =
        "/get-csv/" +
        state_name +
        "-" +
        district_name +
        "-" +
        date +
        "-" +
        daily;
    }
    // a.setAttribute("download", "Confirmed.csv");
    a.click();
    window.URL.revokeObjectURL(a.href);
    document.body.removeChild(a);
  });
});

function GetDataState() {
  var e = document.getElementById("state_name");
  var state_name = e.options[e.selectedIndex].text;
  if (state_name != "All") {
    var q = document.getElementById("district-select");
    var district_name = q.options[q.selectedIndex].text;
  } else {
    district_name = "none";
  }
  var date = document.getElementById("my_date_picker").value;
  if (date == "") {
    date = "All";
  }
  var p = document.getElementById("daily");
  var daily = p.options[p.selectedIndex].text;

  $.post(
    "/State",
    {
      state_data: state_name,
      district_data: district_name,
      date_data: date,
      daily_data: daily,
    },
    function (data, status, xhr) {
      // Extract value from table header.
      console.log(status);
      if (status == "success") {
        var df = data;
        var col = [];
        for (var i = 0; i < df.length; i++) {
          for (var key in df[i]) {
            if (col.indexOf(key) === -1) {
              col.push(key);
            }
          }
        }

        // Create a table.
        var table = document.createElement("table");

        // Create table header row using the extracted headers above.
        var tr = table.insertRow(-1); // table row.

        for (var i = 0; i < col.length; i++) {
          var th = document.createElement("th"); // table header.
          th.innerHTML = col[i];
          tr.appendChild(th);
        }

        // add json data to the table as rows.
        for (var i = 0; i < df.length; i++) {
          tr = table.insertRow(-1);

          for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = df[i][col[j]];
          }
        }
        var divShowData = document.getElementById("data_show");
        divShowData.innerHTML = "";
        divShowData.appendChild(table);
        divShowData.style.width = "auto";
        divShowData.style.maxWidth = "80vw";
        divShowData.style.maxHeight = "500px";
        // divShowData.style.background = "grey";
        divShowData.style.overflow = "auto";
        divShowData.style.marginTop = "20px";
        // divShowData.style.marginLeft = "50%";
      } else {
        alert("No data available");
      }
    }
  ).fail(function (jqxhr, settings, ex) {
    alert("No data available");
  });
}
