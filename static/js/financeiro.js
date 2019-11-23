function float2real(value){
    return "R$ "+(value).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}