new Vue({
  el: "#tables",
  delimiters: ["[[", "]]"],
  data() {
    return {
      tables: [],
      table: {
        id: "",
        name: "",
        orders: []
      },
      form: {
        table_id: "",
        waiter: "",
        comment: "",
        status: "",
      },
    };
  },
  created() {
    this.Initfunction();
    this.loadTables();
  },
  methods: {
    Initfunction: function () {
      java = this;
      var socketio = io();
      socketio.on("message", function (Response) {
        if (Response.data == "update") {
          console.log(Response)
          java.loadTables();
        }
      });
    },
    loadTables: function () {
      axios.post("/tables/get_tables").then((Response) => {
        this.tables = Response.data;
      });
    },
    get_table_id: function (table_id, status) {
      axios.post("/tables/getOrdersTableData", { id: table_id }).then((Response) => {
        this.table = Response.data;
      });
      this.form.table_id = table_id;
      this.form.status = status;
      //console.log(table_id, status);
    },
    submitOpenTable: function () {
      axios.post("tables/open_table", this.form).then((Response) => {
        if (Response.data.message == "error") {
        } else if (Response.data.message == "success") {
          $('[aria-label="Close"]').click();
          this.loadTables();
        } else {
          console.log(Response);
        }
      });
    },
  },
});
