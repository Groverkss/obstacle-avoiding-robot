const sleep = time => {
  return new Promise((resolve) => setTimeout(resolve, time));
};

const getData = async () => {
  const response = await fetch('http://localhost:3000/api/data');
  const jsonData = await response.json();
  return jsonData;
};

window.onload = async () => {

  const dps = []; // dataPoints
  const chart = new CanvasJS.Chart("chartContainer", {
    title :{
      text: "Meow meow"
    },
    data: [{
      type: "line",
      dataPoints: dps
    }]
  });

  let currTime = 0;

  const updateChart = async () => {

    const nData = await getData();
    currTime++;
    dps.push({
      x: currTime,
      y: nData,
    });
    chart.render();
  };

  while(true) {
    updateChart();
    await sleep(2000);
  }
}
