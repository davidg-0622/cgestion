
  // Función para validar las fechas
  document.getElementById('fecha_hora_final').addEventListener('change', function() {
      var fechaInicio = document.getElementById('fecha_hora_inicial').value;
      var fechaFinal = this.value;

      if (fechaInicio && fechaFinal) {
          if (new Date(fechaInicio) > new Date(fechaFinal)) {
              alert('La fecha y hora inicial no puede ser mayor que la fecha y hora final.');
              this.setCustomValidity('La fecha final debe ser mayor que la fecha inicial');
          } else {
              this.setCustomValidity('');
          }
      }
  });

  // Limpiar la validación al cambiar la fecha de inicio
  document.getElementById('fecha_hora_inicial').addEventListener('change', function() {
      var fechaInicio = this.value;
      var fechaFinal = document.getElementById('fecha_hora_final').value;

      if (fechaInicio && fechaFinal && new Date(fechaInicio) > new Date(fechaFinal)) {
          document.getElementById('fecha_hora_final').setCustomValidity('La fecha final debe ser mayor que la fecha inicial');
      } else {
          document.getElementById('fecha_hora_final').setCustomValidity('');
      }
  });
