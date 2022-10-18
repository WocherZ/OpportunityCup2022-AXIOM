<template>
  <div class="charts row col-12 q-pt-xl">
    <div class="chart-1 col-6">
      <canvas id="planet1-chart"></canvas>
    </div>
    <div class="chart-2 col-6">
      <canvas id="planet2-chart"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js";
// import planet1ChartData from "../chart1.js";
// import planet2ChartData from "../chart2.js";

export default {
  name: "PlanetChart",
  data() {
    return {
      planet1ChartData: [],
      planet2ChartData: [],

      dataToParse: [],
      connection: "",
    };
  },
  //   mounted() {
  //     const ctx = document.getElementById("planet1-chart");
  //     new Chart(ctx, this.planet1ChartData);

  //     const ctx1 = document.getElementById("planet2-chart");
  //     new Chart(ctx1, this.planet2ChartData);
  //   },

  watch: {
    planet1ChartData: {
      handler() {
        this.connection.onmessage = function (event) {
          this.dataChart1 = JSON.parse(event.data).first_hist;
          this.dataChart2 = JSON.parse(event.data).second_hist;

          this.planet1ChartData = {
            type: "bar",
            data: {
              labels: ["Фрод", "Не фрод"],
              datasets: [
                {
                  label: "Количество транзакций",
                  data: [this.dataChart1["frod"], this.dataChart1["notfrod"]],
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

          this.planet2ChartData = {
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
                  label: "Транзакции каждого паттерна",
                  data: [
                    this.dataChart2["notfrod"],
                    this.dataChart2["pattern1"],
                    this.dataChart2["pattern2"],
                    this.dataChart2["pattern3"],
                    this.dataChart2["pattern4"],
                    this.dataChart2["pattern5"],
                    this.dataChart2["pattern6"],
                  ],
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

          const ctx = document.getElementById("planet1-chart");
          new Chart(ctx, this.planet1ChartData);

          const ctx1 = document.getElementById("planet2-chart");
          new Chart(ctx1, this.planet2ChartData);
        };
      },
      deep: true,
    },
  },

  created: function () {
    console.log("Starting connection to WebSocket Server");
    this.connection = new WebSocket("ws://127.0.0.1:8000/ws/");

    this.connection.onmessage = function (event) {
      this.dataChart1 = JSON.parse(event.data).first_hist;
      this.dataChart2 = JSON.parse(event.data).second_hist;

      this.planet1ChartData = {
        type: "bar",
        data: {
          labels: ["Фрод", "Не фрод"],
          datasets: [
            {
              label: "Количество транзакций",
              data: [this.dataChart1["frod"], this.dataChart1["notfrod"]],
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

      this.planet2ChartData = {
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
              label: "Транзакции каждого паттерна",
              data: [
                this.dataChart2["notfrod"],
                this.dataChart2["pattern1"],
                this.dataChart2["pattern2"],
                this.dataChart2["pattern3"],
                this.dataChart2["pattern4"],
                this.dataChart2["pattern5"],
                this.dataChart2["pattern6"],
              ],
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

      const ctx = document.getElementById("planet1-chart");
      new Chart(ctx, this.planet1ChartData);

      const ctx1 = document.getElementById("planet2-chart");
      new Chart(ctx1, this.planet2ChartData);

      console.log(JSON.parse(event.data));
      this.connection.send("DATA");
    };

    this.connection.onopen = function (event) {
      console.log(event);
      console.log("Successfully connected to the echo websocket server...");
    };
  },
};
</script>

<style>
/* html {
        overflow-y: hidden;
    } */

/* .charts {
        display: flex;
        flex-direction: row;
        height: 80vh;
        width: 100%;
    }
    .chart-1 {
        width: 65%;
        margin: 0 auto;
        justify-content: center;
    }
    .chart-2 {
        width: 50vw;
        height: 60vh;
    } */
</style>
