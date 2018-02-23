(function($){
  'use strict';

  var pageScript = {
    init: function(){
      // Datatables
      //Setting default values
      $.extend( $.fn.dataTable.defaults,{
        dom: '<"table-responsive" <t>>', // Table
        autoWidth: false
      });

      // Task list
      // Function Arguments: selector
      pageScript.datatablesTasklistInit('.panel-tasks .table');

      // Calendar
      // Function Arguments: selector, events data
      // Events data
      var myDate = new Date();
      var currentYear = myDate.getFullYear();
      var currentMonth = myDate.getMonth() + 1;
      currentMonth = (currentMonth < 10) ? 0 + '' + currentMonth : currentMonth;
      var events = [
        {
          title: 'All Day Event',
          start: currentYear + '-' + currentMonth + '-01'
        },
        {
          title: 'Long Event',
          start: currentYear + '-' + currentMonth + '-07',
          end: currentYear + '-' + currentMonth + '-10'
        },
        {
          id: 999,
          title: 'Repeating Event',
          start: currentYear + '-' + currentMonth + '-09T16:00:00'
        },
        {
          id: 999,
          title: 'Repeating Event',
          start: currentYear + '-' + currentMonth + '-16T16:00:00'
        },
        {
          title: 'Conference',
          start: currentYear + '-' + currentMonth + '-11',
          end: currentYear + '-' + currentMonth + '-13'
        },
        {
          title: 'Meeting',
          start: currentYear + '-' + currentMonth + '-12T10:30:00',
          end: currentYear + '-' + currentMonth + '-12T12:30:00'
        },
        {
          title: 'Lunch',
          start: currentYear + '-' + currentMonth + '-12T12:00:00'
        },
        {
          title: 'Meeting',
          start: currentYear + '-' + currentMonth + '-12T14:30:00'
        },
        {
          title: 'Happy Hour',
          start: currentYear + '-' + currentMonth + '-12T17:30:00'
        },
        {
          title: 'Dinner',
          start: currentYear + '-' + currentMonth + '-12T20:00:00'
        },
        {
          title: 'Birthday Party',
          start: currentYear + '-' + currentMonth + '-13T07:00:00'
        },
        {
          title: 'Click for Google',
          url: 'http://google.com/',
          start: currentYear + '-' + currentMonth + '-28'
        }
      ]
      // Calendar
      pageScript.calendarInit('#calendar', events);

      // Event list
      // Function Arguments: selector
      pageScript.datatablesEventListInit('.panel-events .table');

      // Live search
      // Function Arguments: Selector, search input, parent selector, child selector
      pageScript.contentLiveSearchInit('.panel-tasks-comments', '#search-tasks-comments', '.media', 'div');
      pageScript.contentLiveSearchInit('.panel-activity-monitor', '#search-activity-monitor', '.media', 'div');
      pageScript.contentLiveSearchInit('.panel-chat', '#search-chat', '.media', 'div');

      // Custom scrollbar
      // Function Arguments: selector
      pageScript.slimscrollInit('.panel-tasks-comments .media-wrapper');
      pageScript.slimscrollInit('.panel-activity-monitor .media-wrapper');
      pageScript.slimscrollInit('.panel-chat .media-wrapper');

      // Hide scrollbar when page is loaded
      $('.slimScrollBar').hide();
    },
    slimscrollInit: function(el){
      // Gets max-height
      var height = parseInt($(el).css('max-height'));

      $(el).slimScroll({
        height: height,
        allowPageScroll: true,
        color: '#000'
      });
    },
    icheckInit: function(el){
      $(el).iCheck({
        checkboxClass: 'icheckbox_minimal-grey',
        radioClass: 'iradio_minimal-grey'
      });
    },
    datatablesIcheckChecked: function(){
      var thCheckbox = $(this).closest('th');
      var tdCheckbox = $(this).closest('.table').find('tbody input.icheck');

      if(thCheckbox.length)
        tdCheckbox.iCheck('check');
    },
    datatablesIcheckUnchecked: function(){
      var thCheckbox = $(this).closest('th');
      var tdCheckbox = $(this).closest('.table').find('tbody input.icheck');

      if(thCheckbox.length)
        tdCheckbox.iCheck('uncheck');
    },
    datatablesTasklistChildRow: function(el){
      // Dropdown table with extra info
      function tasksFormat(d){
        // `d` is the original data object for the row
        return  '<table class="table table-bordered">'+
                  '<tr>'+
                      '<td style="width: 35%;">Parent Project:</td>'+
                      '<td>'+d.parentProject+'</td>'+
                  '</tr>'+
                  '<tr>'+
                      '<td>Description:</td>'+
                      '<td>'+d.description+'</td>'+
                  '</tr>'+
                  '<tr>'+
                      '<td>Due Date:</td>'+
                      '<td>'+d.dueDate+'</td>'+
                  '</tr>'+
                  '<tr>'+
                      '<td>Assigned to:</td>'+
                      '<td>'+d.assign+'</td>'+
                  '</tr>'+
                '</table>';
      }

      var tr = $(this).closest('tr');
      var row = el.DataTable().row(tr);

      if (row.child.isShown()){
        // This row is already open - close it
        row.child.hide();
        tr.removeClass('shown');
      }else{
        // Open this row
        row.child( tasksFormat(row.data())).show();
        tr.addClass('shown');
      }
    },
    datatablesTasklistEdit: function(el){
      $(this).removeClass('btn-edit').addClass('btn-save').find('.fa-pencil').removeClass("fa-pencil").addClass('fa-save');
            
      var tr = $(this).closest('tr');
      var td = tr.find('td');

      for(var i = 1; i <= td.length - 2; i++){
        var cellCur = $(el).DataTable().cell(td.eq(i));
        cellCur.data('<input type="text" class="form-control input-sm" value="'+cellCur.data()+'">');
      }
    },
    datatablesTasklistSave: function(el){
      $(this).removeClass('btn-save').addClass('btn-edit').find('.fa-save').removeClass("fa-save").addClass('fa-pencil');
            
      var tr = $(this).closest('tr');
      var td = tr.find('td');

      for(var i = 1; i <= td.length - 2; i++){
        var cellCur = $(el).DataTable().cell(td.eq(i));
        var inputVal = td.eq(i).find('.form-control').val();
        cellCur.data(inputVal).draw();
      }
    },
    datatablesTasklistRemove: function(el){
      $(el).DataTable().row().remove().draw(false);
    },
    datatablesTasklistInit: function(el){
      $(el).DataTable({
        dom:  '<f>'+ // Top section structure(search etc.)
              '<"table-responsive" <t>>', // Table
        language: {
          search: '_INPUT_',
          searchPlaceholder: 'Search...'
        },
        order: [ [1, 'asc'] ],
        columnDefs:[{
          targets: [0,3],
          orderable: false
        }],
        ajax: 'task-list-data.txt',
        columns: [
          {
            className: 'details-control',
            defaultContent: "<input type='checkbox' class='icheck' autocomplete='off'>"
          },
          { data:  'title'},
          { data: 'tag' },
          { defaultContent: '<td>'+
                  '<div class="btn-group btn-group-xs pull-right">'+
                      '<button type="button" class="btn btn-default btn-edit">'+
                          '<i class="fa fa-pencil"></i>'+
                      '</button>'+
                      '<button type="button" class="btn btn-default btn-remove">'+
                        '<i class="fa fa-trash"></i>'+
                      '</button>'+
                  '</div></td>' }
        ],
        initComplete: function(settings, json){
          // After getting data inits iCheck
          pageScript.icheckInit('input.icheck');

          // If checkbox in <th> is checked, marking checked all checkboxes too
          $('.icheck').on('ifChecked', pageScript.datatablesIcheckChecked);

          // If checkbox in <th> is unchecked, marking unchecked all checkboxes too
          $('.icheck').on('ifUnchecked', pageScript.datatablesIcheckUnchecked);

          // Add event listener for opening and closing details
          $(el).find('tbody').on('click', 'td.details-control', $.proxy(pageScript.datatablesTasklistChildRow, null, $(el)));

          // Editing, saving and removing
          $(el).DataTable().on('click','.btn-edit', $.proxy(pageScript.datatablesTasklistEdit, null, el));
          
          $(el).DataTable().on('click','.btn-save', $.proxy(pageScript.datatablesTasklistSave, null, el));
          
          $(el).DataTable().on('click','.btn-remove', $.proxy(pageScript.datatablesTasklistRemove, null, el));
        }
      });
    },
    contentLiveSearchInit: function(container, searchField, selector, childSelector){
      $(container).searchable({
        searchField: searchField,
        selector: selector,
        childSelector: childSelector
      })
    },
    calendarInit: function(el, events){
      $(el).fullCalendar({
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
        eventLimit: true, // allow "more" link when too many events
        events: events
      });
    },
    datatablesEventListChildRow: function(el){
      // Dropdown table with extra info
      function eventsFormat(d){
        // `d` is the original data object for the row
        return  '<table class="table table-bordered">'+
                  '<tr>'+
                      '<td>Description:</td>'+
                      '<td>'+d.description+'</td>'+
                  '</tr>'+
                  '<tr>'+
                      '<td>Invited:</td>'+
                      '<td>'+d.invited+'</td>'+
                  '</tr>'+
                '</table>';
      }

      var tr = $(this).closest('tr');
      var row = el.DataTable().row(tr);

      if (row.child.isShown()){
        // This row is already open - close it
        row.child.hide();
        tr.removeClass('shown');
      }else{
        // Open this row
        row.child( eventsFormat(row.data())).show();
        tr.addClass('shown');
      }
    },
    datatablesEventListInit: function(el){
      $(el).DataTable({
        ordering: false,
        ajax: 'event-list-data.txt',
        columns: [
          {
            className: 'details-control',
            render: function(data, type, full, meta){
              // Showing 2 values in one column
              return '<span class="block">'+full.title+'</span>'+'<span>'+full.date+'</span>';
            }
          },
          { defaultContent: '<button class="btn btn-default-outline">Cancel</button>' }
        ],
        initComplete: function(settings, json){
          // Add event listener for opening and closing details
          $(el).find('tbody').on('click', 'td.details-control', $.proxy(pageScript.datatablesEventListChildRow, null, $(el)));
        }
      });
    }
  };
  
  pageScript.init();
})(jQuery);