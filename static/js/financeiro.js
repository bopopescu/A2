function float2real(value){
    return "R$ "+(value).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

var ctx = document.getElementById("myChartPie").getContext("2d");
var chart = new Chart(ctx, {
  // The type of chart we want to create
  type: "pie",
  // The data for our dataset
  data: {
    labels: ["Cartão de Crédito", "Cartão de Débito", "Dinheiro"],
    datasets:[
      {
        label: "Forma de Pagamento",
        borderColor: ['rgba(75, 192, 192, 1)', 'rgba(192, 0, 0, 1)', 'rgba(248, 169, 120, 1)'],
        backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(192, 0, 0, 0.2)', 'rgba(248, 169, 120, 0.2)'],
        pointBorderColor: "#80b6f4",
        data: {{formaPagamento}}
      }
    ]
  },
  // Configuration options go here
  options: {
    responsive: true,
    maintainAspectRatio: false
  }
});