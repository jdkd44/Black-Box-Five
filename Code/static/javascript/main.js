// Main code for the Black Box WebUI

//Global Variables
var velChart;
var latAccChart;
var vertAccChart;
var heightChart;
var velChartData = [];
var latAccChartData = [];
var vertAccChartData = [];
var heightChartData = [];

//runs when window loads
window.onload = function() {
  initCharts();
}

function sensorData() {
  chartData = []
  $.getJSON('/data', function(jsonfile) {
    bat_percent = jsonfile.bat_percent.toString();
    gps_lat = jsonfile.gps_lat;
    gps_lon = jsonfile.gps_lon;
    height = jsonfile.height;
    lateral_acc = jsonfile.lateral_acc;
    velocity = jsonfile.velocity;
    vertical_acc = jsonfile.vertical_acc;

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

function initCharts() {
  $.getJSON('/data', function(jsondata) {
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
      dataPoints: velChartData,
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
      dataPoints: vertAccChartData,
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
      dataPoints: latAccChartData,
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
      dataPoints: heightChartData,
    }]
  });

  //render all charts
  renderCharts();
  if(jsondata.dataLogging) {
    updateGUI()
  }
  });
}

function updateGUI() {
  $.getJSON('/data', function(jsondata) {
    //Update Charts
    timeArray = jsondata.time.split(/-| |:|\./);
    timeArray[6] = timeArray[6] % 1000;
    velChartData.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6]), y: jsondata.velocity });
    vertAccChartData.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6]), y: jsondata.vertical_acc });
    latAccChartData.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6]), y: jsondata.lateral_acc });
    heightChartData.push({x: new Date(timeArray[0], timeArray[1], timeArray[2], timeArray[3], timeArray[4], timeArray[5], timeArray[6]), y: jsondata.height });
    renderCharts();

    //Update Live Data Feed
    bat_percent = jsondata.bat_percent.toString();
    gps_lat = jsondata.gps_lat;
    gps_lon = jsondata.gps_lon;
    height = jsondata.height;
    lateral_acc = jsondata.lateral_acc;
    velocity = jsondata.velocity;
    vertical_acc = jsondata.vertical_acc;

    if(jsondata.charge_status = true) charge_status = "Charging";
    else charge_status = "Discharging";
    document.getElementById('batteryCharge').innerText = bat_percent + "%";
    document.getElementById('chargeStatus').innerText = charge_status;
    document.getElementById('liveVelocity').innerText = velocity;
    document.getElementById('liveHeight').innerText = height;
    document.getElementById('liveLatAcc').innerText = lateral_acc;
    document.getElementById('liveVertAcc').innerText = vertical_acc;
    document.getElementById('liveGPSLat').innerText = gps_lat;
    document.getElementById('liveGPSLon').innerText = gps_lon;

    if(jsondata.dataLogging) {
      setTimeout(updateGUI(), (1/parseInt(jsondata.pollingRate))*1000)
    }
  });
}

function renderCharts() {
  velChart.render();
  latAccChart.render();
  vertAccChart.render();
  heightChart.render();
}