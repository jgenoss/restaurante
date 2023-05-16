new Vue({
  el: '#tables',
  delimiters: ['[[', ']]'],
  data () {
    return {
      keyupInput:'',
      tables: [],
      selectedTable: {
        tableId: '',
        name: '',
        orders: []
      },
      menus:[],
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
        if (response.data == 'update') {
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
      axios.post('/tables/get_orders_table_data', {tableId}).then((response) => {
        this.selectedTable = response.data
      })
      this.form.tableId = tableId
      this.form.status = status
    },
    submitOpenTableForm () {
      axios.post('/tables/open_table', this.form).then((response) => {
        if (response.data.message === 'error') {
          // Manejar errores
        } else if (response.data.message === 'success') {
          // Cerrar el modal y recargar las mesas
          $('[aria-label="Close"]').click()
          this.resetInputForm()
        } else {
          console.log(response)
        }
      })
    },
    closeTable (tableId) {
      Swal.fire({
        title: 'Estas Segura de hacer esto',
        text: "Esta mesa se cerrara y perderas las informacion!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si!',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.isConfirmed) {
          axios.post('/tables/close_table',{tableId}).then((response) => {
            if (response.data.message === 'error') {
              // Manejar errores
            } else if (response.data.message === 'success') {
              // Cerrar el modal y recargar las mesas
              $('[aria-label="Close"]').click()
              Swal.fire(
                'Exito!',
                'La mesa Esta cerrada.',
                'success'
              )
              this.resetInputForm()
            } else {
              console.log(response)
            }
          })
        }
      })
    },
    keyupSearch(event) {
      if (this.keyupInput.trim().length === 0) {
        this.menus = []
        // Aquí puedes agregar la lógica para manejar el caso en que el valor está vacío
      } else {
        axios.post('/tables/search_menu',{"search":this.keyupInput}).then((response) => {
          if (response.data.message === 'error') {
            // Manejar errores
          } else if (response.data.message === 'success') {
            // Cerrar el modal y recargar las mesas
            this.menus = response.data.list
            console.log(response)
          } else {
            console.log(response)
          }
        })
      }
    },
    addOrder (tableId,menuId,cant) {
     if(cant === 0){
        Swal.fire({
          icon: 'info',
          title: 'Hey Cuidado',
          text: 'El valor debe ser mayor a 0!',
          showConfirmButton: false,
          timer: 5000
        })
     }
    },
    resetInputForm () {
      this.form.tableId='',
      this.form.waiter='',
      this.form.comment='',
      this.form.status=''
    }
  }
})