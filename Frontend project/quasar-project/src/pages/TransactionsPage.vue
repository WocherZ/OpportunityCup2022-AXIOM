<template>
  <div class="q-pa-md">
    <q-table
      title="Transactions"
      :rows="rows"
      :columns="columns"
      separator="cell"
    />
  </div>
</template>

<script>
// const rows = [
//     {
//         date: "16.10.22",
//         last_name: "Smth",
//         first_name: "Hi",
//         patronymic: "GHJLK",
//         passport: 57289,
//         phone: 76276029,
//         oper_type: "operation",
//         amount: "150",
//         pattern: "1,2,3"

//     },
//     {
//         date: "15.10.22",
//         last_name: "NAo",
//         first_name: "Hhfak",
//         patronymic: "GHfafaLK",
//         passport: 5789,
//         phone: 762769,
//         oper_type: "operation",
//         amount: 10,
//         pattern: "1,2"

//     },
//     {
//         date: "15.10.22",
//         last_name: "NAo",
//         first_name: "Hhfak",
//         patronymic: "GHfafaLK",
//         passport: 5789,
//         phone: 762769,
//         oper_type: "operation",
//         amount: 10,
//         pattern: "1,2"

//     },
//     {
//         date: "15.10.22",
//         last_name: "NAo",
//         first_name: "Hhfak",
//         patronymic: "GHfafaLK",
//         passport: 5789,
//         phone: 762769,
//         oper_type: "operation",
//         amount: 10,
//         pattern: "1,2"

//     },
//     {
//         date: "15.10.22",
//         last_name: "NAo",
//         first_name: "Hhfak",
//         patronymic: "GHfafaLK",
//         passport: 5789,
//         phone: 762769,
//         oper_type: "operation",
//         amount: 10,
//         pattern: "1,2"

//     },
//     {
//         date: "15.10.22",
//         last_name: "NAo",
//         first_name: "Hhfak",
//         patronymic: "GHfafaLK",
//         passport: 5789,
//         phone: 762769,
//         oper_type: "operation",
//         amount: 10,
//         pattern: "1,2"

//     },
//     {
//         date: "15.10.22",
//         last_name: "NAo",
//         first_name: "Hhfak",
//         patronymic: "GHfafaLK",
//         passport: 5789,
//         phone: 762769,
//         oper_type: "operation",
//         amount: 10,
//         pattern: "1,2"

//     },
// ]

export default {
  name: "TransactionsPage",
  data() {
    return {
      columns: [
        // {
        //   name: "Date",
        //   required: true,
        //   label: "Date",
        //   align: "center",
        //   field: "date",
        //   sortable: true,
        // },

        {
          name: "last_name",
          align: "center",
          label: "Last name",
          field: "last_name",
          sortable: true,
        },
        {
          name: "first_name",
          align: "center",
          label: "First name",
          field: "first_name",
          sortable: true,
        },
        // {
        //   name: "patronymic",
        //   align: "center",
        //   label: "Patronymic",
        //   field: "patronymic",
        // },
        // {
        //   name: "passport",
        //   align: "center",
        //   label: "Passport",
        //   field: "passport",
        // },
        // { name: "phone", align: "center", label: "phone", field: "phone" },
        // {
        //   name: "oper_type",
        //   align: "center",
        //   label: "Oper type",
        //   field: "oper_type",
        //   sortable: true,
        // },
        // {
        //   name: "amount",
        //   align: "center",
        //   label: "Amount",
        //   field: "amount",
        //   sortable: true,
        // },

        // {
        //   name: "pattern",
        //   align: "center",
        //   label: "Pattern",
        //   field: "pattern",
        // },

        // {
        //   name: "pattern_description",
        //   align: "center",
        //   label: "Pattern description",
        //   field: "pattern_description",
        // },
      ],
      rows: [],
      dataTrans: [],
      ready: false,
    };
  },
  created: function () {
    console.log("Starting connection to WebSocket Server");
    let connection = new WebSocket("ws://127.0.0.1:8000/ws/");

    connection.onmessage = function (event) {
      this.dataTrans = JSON.parse(event.data).data;

      //   for (let i = 0; i < this.dataTrans.length; ++i) {
      //     this.rows[i] = Object({
      //       first_name: this.dataTrans[i]["first_name"],
      //       last_name: this.dataTrans[i]["last_name"],
      //     });
      //   }

      this.rows = this.dataTrans;

      console.log(this.rows[0].last_name);
      this.ready = true;
    };

    connection.onopen = function (event) {
      console.log(event);
      console.log(
        "Successfully connected to the echo websocket server (transactions)..."
      );
    };

    connection.onclose = function (event) {
      console.log("End connection");
    };
  },
};
</script>
