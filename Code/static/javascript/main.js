// Main code for the Black Box WebUI
  
window.onload = function() {
  setTimeout(renderCharts(),1000);
  sensorData()
}

function sensorData() {
  $.getJSON('/data', function(jsonfile) {
    bat_percent = jsonfile.bat_percent.toString();
    gps_lat = jsonfile.gps_lat.toString();
    gps_lon = jsonfile.gps_lon.toString();
    height = jsonfile.height.toString();
    lateral_acc = jsonfile.lateral_acc.toString();
    velocity = jsonfile.velocity.toString();
    vertical_acc = jsonfile.vertical_acc.toString();

    if(jsonfile.charge_status = true) charge_status = "Charging";
    else charge_status = "Discharging";
    document.getElementById('batteryCharge').innerText = bat_percent + "%";
    document.getElementById('chargeStatus').innerText = charge_status;
    document.getElementById('liveVelocity').innerText = velocity;
    document.getElementById('liveHeight').innerText = height;
    document.getElementById('liveLatAcc').innerText = lateral_acc;
    document.getElementById('liveVertAcc').innerText = vertical_acc;
    document.getElementById('liveGPSLat').innerText = gps_lat;
    document.getElementById('liveGPSLon').innerText = gps_lon;
  });
}

function renderCharts() {
  var velChart, latAccChart, vertAccChart, heightChart;
  $.getJSON('/chart', function(jsonfile) {
    function getDataPoints(dataType) {
      var entries = jsonfile.time.length;
      var dataPoints = timeArray = [];
      for (var i = 0; i < entries; i++) {
        timeArray = jsonfile.time[i].split(/-| |:|\./);
        switch(dataType) {
          case 'lateral acceleration':
            dataPoints.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6])}, {y: jsonfile.lateral_acc[i]});
            break;
          case 'vertical acceleration':
            dataPoints.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6])}, {y: jsonfile.vertical_acc[i]});
            break;
          case 'velocity':
            dataPoints.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6])}, {y: jsonfile.velocity[i]});
            break;
          case 'height':
            dataPoints.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6])}, {y: jsonfile.height[i]});
            break;
        }
      }
      return dataPoints;
    }

  //chart definitions and settings
  velChart = new CanvasJS.Chart("vel_chart",{
    title:{
      text:"Velocity Chart",
    },
    axisX:{
      valueFormatString: "h:m:s.f",
    },
    backgroundColor: "#ECDBBA",
    data: [{
      lineColor: "#C84B31",
      color: "#191919",
      type: "line",
      dataPoints: getDataPoints('velocity'),
    }]
  });
  vertAccChart = new CanvasJS.Chart("vert_acc_chart",{
    title:{
      text:"Vertical Acceleration Chart",
    },
    axisX:{
      valueFormatString: "h:m:s.f",
    },
    backgroundColor: "#ECDBBA",
    data: [{
      lineColor: "#C84B31",
      color: "#191919",
      type: "line",
      dataPoints: getDataPoints('vertical acceleration'),
    }]
  });
  latAccChart = new CanvasJS.Chart("lat_acc_chart",{
    title:{
      text:"Lateral Acceleration Chart",
    },
    axisX:{
      valueFormatString: "h:m:s.f",
    },
    backgroundColor: "#ECDBBA",
    data: [{
      lineColor: "#C84B31",
      color: "#191919",
      type: "line",
      dataPoints: getDataPoints('lateral acceleration'),
    }]
  });
  heightChart = new CanvasJS.Chart("height_chart",{
    title:{
      text:"Height Chart",
    },
    axisX:{
      valueFormatString: "h:m:s.f",
    },
    backgroundColor: "#ECDBBA",
    data: [{
      lineColor: "#C84B31",
      color: "#191919",
      type: "line",
      dataPoints: getDataPoints('height'),
    }]
  });

  //render all charts
  velChart.render();
  latAccChart.render();
  vertAccChart.render();
  heightChart.render();
});
}