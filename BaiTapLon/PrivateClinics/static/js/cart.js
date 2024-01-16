function addToCart(i){
    let x = document.getElementsByClassName("medicine");
    let unit = document.getElementsByClassName("unit");
    let CachSD = document.getElementsByClassName("CachSD");
    id = x[i].value//mã thuốc
    if(id != 0)
    {
        fetch('/api/add-medicine-to-cart',{
        method: 'post',
        body: JSON.stringify({
            'id': id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data => {
            console.info(data)
            if(data.id == '1'){
                unit[i].innerHTML =  `<span>Chai</span>`
            }
             if(data.donViThuoc_id == '2'){
                unit[i].innerHTML =  `<span>Vỹ</span>`
            }
             if(data.donViThuoc_id == '3'){
                unit[i].innerHTML =  `<span>Viên</span>`
            }

            CachSD[i].innerHTML = data.CachSD

       }).catch(err => console.error(err))
   }
   else
        console.log('id = 0')
}

function updateQuantity(line, obj){
    var x = document.getElementsByClassName("medicine");
    id = x[line].value

    console.log(id)
    console.log(obj.value)

    if(id){
        fetch('/api/update-quantity',{
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
       }),
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => res.json()).then(data => {
            console.info(data)
            if(data.code == 200){
                console.log("Thành công")
            }
       }).catch(err => console.error(err))
    }
    else
    {
      console.log("Không lấy được id")
    }
}

function deleteMedicineCart(line){
    var x = document.getElementsByClassName("medicine");
    id = x[line].value

    if(id){
        if(confirm("Bạn có muốn xóa không?") == true){
            fetch('/api/delete-medicine-cart',{
            method: 'delete',
             body: JSON.stringify({
            'id': id
       }),
        headers: {
            'Content-Type': 'application/json'
        }
            }).then(res => res.json()).then(data => {
                console.info(data)

                let r = document.getElementById(`cart${id}`)
                r.style.display = "none"

                if(data.code == 200){
                    console.log("Thành công")
                }
           }).catch(err => console.error(err))
        }
    }
    else
    {
      console.log("Không lấy được id")
    }
}

function saveMedicalBill(){
    if(confirm("Bạn có muốn lưu phiếu?") == true)
    {
        fetch('/add-phieu-kham',{
            method: 'post'
        }).then(res => res.json()).then(data => {
            console.info(data)
            if(data.code == 200){
                alert("Lưu phiếu khám thành công");
            }
            else
                alert("Hệ thống bị lỗi");
        }).catch(err => console.error(err))
    }
}

function timKiem(){
    let fullname=document.getElementById("fullname").value;
    fetch('/api/timKiem',{
        method: 'post',
        body: JSON.stringify({
            'fullname': fullname
        }),
        headers: {
        'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let html = `<tr>
                            <th>Tên thuốc</th>
                            <th>Số lượng</th>
                        </tr>`
        let dsachThuoc = document.getElementById('dsachThuoc')
        dsachThuoc.style.display = "table"
        for(let i = 0; i < data['name'].length; i++) {
            html += `<tr>
                <td class="name">${data['name'][i]}</td>
                <td class="quantity">${data['quantity'][i]}</td>
                </tr>`
        }
        dsachThuoc.firstElementChild.innerHTML = html
    }).catch(err => console.error(err))
}