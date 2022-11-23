var inputTongTien = document.getElementById('inputTotal');
var inputchuyen = document.getElementById('selectPercent');
var inputSoNguoi = document.getElementById('inputPeople');
// khai báo hàm

function chonchuyen() {
    var tongTien = document.getElementById('inputTotal').value;
    var inputchuyen = document.getElementById('selectPercent').value;
    var soghe = document.getElementById('inputPeople').value;


    document.getElementById('txtResult').innerHTML = "Số tiền :" +  tongTien +"<span style=' vertical-align: super;'>$</span>" + " <br> Chuyến được chọn : "+ inputchuyen + " <br>Hàng ghế : " + soghe;
    document.getElementById('txtResult').style.textAlign = 'center';
    document.getElementById('txtResult').style.marginTop = '15px';
}

document.getElementById('btnCalc').onclick = chonchuyen;