window.onload = function() {
    document.getElementById("detalleResidencia").onclick = function () {
        window.location.href = "detalle_residencia";
    };
    document.getElementById("altaResidencia").onclick = function () {
        window.location.href = "alta_residencia";
    };
  $('.dropdown-menu a').onclick = function() {
      $('#selected').text($(this).text());
  };
};

