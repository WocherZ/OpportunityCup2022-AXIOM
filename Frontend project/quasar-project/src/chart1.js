export const planetChartData = {
  type: "bar",
  data: {
    labels: ["Не фрод", "Фрод"],
    datasets: [
      {
        label: "Number of matches",
        data: [500, 567],
        backgroundColor: "rgba(54,73,93,.5)",
        borderColor: "#36495d",
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
