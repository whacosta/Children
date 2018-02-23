


(function($){
  'use strict';

  var demo = {
    init: function(){
      
      // actividades stats pie chart ( When tab is shown )
      // Function Arguments: selector, data
      // Country sales data
      var countrySalesData = [
        { label : "Club 1", data: 40, color: "#5ebdec" },
        { label : "Club 2", data: 25, color: "#EE6567" },
        { label : "Club 3", data: 15, color: "#F9B56A" },
      ];
      $('[href="#sales-chart-view"]').on('shown.bs.tab', $.proxy(demo.pieChartInit, null, '#chart-country-sales', countrySalesData));

      // Easy pie chart
      // Function Arguments: selector
      demo.easyPieChartInit('.easy-pie-chart');


    },

    pieChartInit: function(el, data){
      $.plot(el, data, {
        series: {
          pie: { 
            show: true,
            radius: 1,
            startAngle: 1,
            highlight: {
              opacity: .3
            },
            label: {
              show: true,
              radius: 55,
              formatter: function (label, series){
                return "<div class='chart-label'>"+Math.round(series.percent)+"%</div>";
              },
            }
          }
        },
        legend: {
          show: true
        },
        grid: {
          hoverable: true
        }
      });
    },

    easyPieChartInit: function(el){
      $(el).easyPieChart({
        onStep: function(from, to, percent){
          $(this.el).find('.percent').text(Math.round(percent))
        }
      });
    },
  };
  
  demo.init();
})(jQuery);