new Vue({
  el: "#tables",
  delimiters: ["[[", "]]"],
  data() {
    return {
      tables: [],
      form:{
        table_id:"",
        waiter:"",
        comment:"",
        status:""
      }
    };
  },
  created() {
    this.loadTables();
  },
  methods: {
    loadTables: function () {
      axios.post("/tables/get_tables").then((Response) => {
        this.tables = Response.data;
        this.tables.forEach((value,index) => {
          if(value["status"] == "open"){
            this.get_open_table_id(index,value['table_id']);
            console.log(value);
          }
        });
      });
    },
    get_open_table_id: function (key,id){
      axios.post("/tables/get_open_table_id",{id:id}).then((Response) => {
        this.tables[key]={
          comment: Response.data.comment,
          reservation_date: Response.data.reservation_date,
          reservation_id: Response.data.reservation_id,
          start_time: Response.data.start_time
        }
        console.log(this.tables);
      });
    },
    get_table_id: function (table_id, status) {
      this.form.table_id = table_id;
      this.form.status = status;
      //console.log(table_id, status);
    },
    submitOpenTable: function () {
      axios.post("tables/open_table",this.form).then((Response) =>{
        if(Response.data.message == "error") {
          console.log(Response);
        }else if(Response.data.message == "success") {
          $('[aria-label="Close"]').click();
          this.loadTables();
        }else{
          console.log(Response);
        }
      });
    }
  },
});
