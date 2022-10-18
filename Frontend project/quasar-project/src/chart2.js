export const planetChartData = {
  type: "bar",
  data: {
    labels: [
      "Не фрод",
      "Паттерн 1",
      "Паттерн 2",
      "Паттерн 3",
      "Паттерн 4",
      "Паттерн 5",
      "Паттерн 6",
    ],
    datasets: [
      {
        label: "Transactions per pattern",
        data: [500, 100, 56, 652, 50, 568, 123],
        backgroundColor: "rgba(71, 183,132,.5)",
        borderColor: "#47b784",
        borderWidth: 3,
      },
    ],
  },
  options: {
    responsive: true,
    lineTension: 1,
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
            padding: 25,
          },
        },
      ],
    },
  },
};

export default planetChartData;
