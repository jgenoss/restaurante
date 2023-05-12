new Vue({
  el: '#tables',
  delimiters: ['[[', ']]'],
  data () {
    return {
      tables: [],
      selectedTable: {
        id: '',
        name: '',
        orders: []
      },
      form: {
        tableId: '',
        waiter: '',
        comment: '',
        status: ''
      }
    }
  },
  created () {
    this.initializeWebSocket()
    this.loadTablesFromServer()
  },
  methods: {
    initializeWebSocket () {
      const vm = this
      const socket = io()
      socket.on('message', (response) => {
        if (response.data === 'update') {
          console.log(response)
          vm.loadTablesFromServer()
        }
      })
    },
    loadTablesFromServer () {
      axios.post('/tables/get_tables').then((response) => {
        this.tables = response.data
      })
    },
    selectTable (tableId, status) {
      axios.post('/tables/get_orders_table_data', { id: tableId }).then((response) => {
        this.selectedTable = response.data
      })
      this.form.tableId = tableId
      this.form.status = status
    },
    submitOpenTableForm () {
      axios.post('tables/open_table', this.form).then((response) => {
        if (response.data.message === 'error') {
          // Manejar errores
        } else if (response.data.message === 'success') {
          // Cerrar el modal y recargar las mesas
          $('[aria-label="Close"]').click()
          this.loadTablesFromServer()
        } else {
          console.log(response)
        }
      })
    }
  }
})