// Script Requiere:
// Array cita : 'id', 'evento', 'club', 'inicio', 'final'\
// un modal con id info_cita y una div con clase  cita dentro para mostrar el contenido
// un div con id calendar para instanciar el calendario de citas
// Haber llamado el script y el estilo de full-calendar

function mostraCitaPorID(id){
        for(i in citas){
          var cita = citas[i];
          if (cita.id == id) {
            mostrarCita(i);
          }
        }
    }

function mostraCitaPorID(id){
    for(i in citas){
      var cita = citas[i];
      if (cita.id == id) {
        mostrarCita(i);
      }
    }
}

function mostrarCita(index){
    ID_EVENTO_ACTUAL = index;
    var cita = citas[index];
    var inicio = new Date(cita.inicio);
    var fin = new Date(cita.final);
    var dia = inicio.getDate()+"/"+(inicio.getMonth()+1)+"/"+inicio.getFullYear();
    var clubes = jQuery.parseJSON(cita.club);
    html_clubes="<ul>";
    for(c in clubes){
        club = clubes[c];
        html_clubes += "<li>"+club+"</li>";
    }
    html_clubes += "</ul>";

    minutos = inicio.getMinutes() < 10 ? '0'+inicio.getMinutes() : inicio.getMinutes();
    var hora_ini = inicio.getHours()+":"+minutos;
    minutos = fin.getMinutes() < 10 ? '0'+fin.getMinutes() : fin.getMinutes();
    var hora_fin = fin.getHours()+":"+minutos;
     
    $("#info_cita .cita").html(
        `<p><b>Día: </b>`+dia+`</p>`+
        `<p><b>Club: </b>`+html_clubes+`</p>`+
        `<p><b>Hora Inicial: </b>`+hora_ini+`</p>`+
        `<p><b>Hora Final: </b>`+hora_fin+`</p>`
    );
    $("#info_cita .modal-title").html(cita.evento);
    $("#info_cita").modal('toggle');

}
var eventos = [];

$(document).ready(function(){
    for( index in citas){
        cita = citas[index];
        console.log(cita.inicio);
        console.log(cita.final);
        eventos.push({
            id: index,
            title  : cita.evento,
            start : cita.inicio,
            end : cita.final,
            allDay: false,
        })
        
    }

    $("#calendar").fullCalendar({
      lang: 'es',
      header: {
        left: "prev,next,title",
        right: "today,month,agendaWeek,agendaDay"
      },
      buttonText: {
        today: 'Today',
        month: 'Month',
        week:  'Week',
        day:   'Day'
      },
      editable: true,
      droppable: false, // this allows things to be dropped onto the calendar
      eventDurationEditable: false,
      eventStartEditable: false,
      drop: function() {
        // is the "remove after drop" checkbox checked?
        if ($("#drop-remove").is(":checked")) {
          // if so, remove the element from the "Draggable Events" list
          $(this).remove();
        }
      },
      eventLimit: true, // allow "more" link when too many events
      eventClick: function(calEvent, jsEvent, view) {
          ID_EVENTO_ACTUAL = calEvent.id;
          mostrarCita(calEvent.id);

      },
    });

    $('#calendar').fullCalendar('addEventSource',eventos);

});
