function generatepdf(){
    console.log('click me')
    var imag = 'data:image/jpeg;base64,verylongbase64;'
    var trt = document.getElementById('target');
    const thepdf = new jsPDF();
    thepdf.fromHTML(trt, 15, 15, {'width' : 190})
    thepdf.addImage(imag, 'JPEG', 15, 40,180, 160)
    thepdf.save('form.pdf');
  }