from flask import render_template, request, redirect,session,flash, url_for,jsonify
from flask_login import login_user, logout_user, login_required, current_user
from PrivateClinics import app,dao,login_manager
from PrivateClinics.admin import *
from PrivateClinics.models import UserRole,HoaDon
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/introduce")
def introduce():
    return render_template("introduce.html")


@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/booking',methods=['POST'])
def book_schedule():
    try:
        if request.method == 'POST':
            tenBN = request.form.get('tenBN')
            SDT = request.form.get('SDT')
            namSinh = request.form.get('namSinh')
            diaChi = request.form.get('diaChi')
            gioiTinh = request.form.get('gioiTinh')
            ngayDL = request.form.get('ngayDL')

            count = dao.count_schedule_by_date(ngayDL)
            dem = len(count)

            if dem < 40:
                dao.add_schedule(ngayTao=ngayDL, tenBN=tenBN, SDT=SDT, namSinh=namSinh, diaChi=diaChi,
                                 gioiTinh=gioiTinh)
            else:
                flash("Đã đủ 40 bệnh nhân trong ngày", "warning")
    except Exception as err:
        flash(f"Hệ thống báo lỗi: {str(err)}", "danger")
    else:
        flash("Đặt lịch thành công", "success")
    return render_template('booking.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/')
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['registerPassword']
        confirm = request.form['registerConfirmPassword']
        if password.__eq__(confirm):
            try:
                dao.register(name=request.form['registerName'],
                             email=request.form['registerEmail'],
                             password=password,
                             username=request.form['registerName'])

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout')
def logout():
    logout_user();
    return redirect('/');


@app.route('/doctor',methods=['GET','POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.check_login(username=username, password=password, role=UserRole.BACSI)
        if user:
            login_user(user=user)
            return redirect(url_for('medical_bill'))
        else:
            return render_template('doctor/doctor_login.html');
    if not current_user.is_authenticated or current_user.user_role != UserRole.BACSI:
        return render_template('doctor/doctor_login.html');
    medicine = Thuoc.query.order_by(Thuoc.name).all()
    return render_template('doctor/medical_bill.html',Thuoc=medicine);


@app.route('/doctor_logout')
def doctor_logout():
    logout_user();
    return redirect('/doctor');


@app.route('/medical_bill',methods=['get', 'post'])
def medical_bill():
    if current_user.is_authenticated and current_user.user_role == UserRole.BACSI:
        err_msg = ""
        msg_success = ""
        if request.method.__eq__('POST'):
            fullname = request.form.get('name')
            ngaylap = request.form.get('ngaylap')
            created_date = datetime.now()
            trieuChung = request.form.get('trieuChung')
            chanDoan = request.form.get('chanDoan')
            try:
                key = app.config['CART_KEY']
                cart = session.get(key)
                dao.add_medical_bill(fullname=fullname, ngay_lap=created_date, chan_doan=chanDoan,
                                     trieu_chung=trieuChung,
                                     cart=cart)
            except Exception as err:
                err_msg = str(err)
            else:
                msg_success = "Lưu phiếu thành công"
            session[key] = {}
        medicine = Thuoc.query.order_by(Thuoc.name).all()
        return render_template('doctor/medical_bill.html',Thuoc=medicine,err_msg=err_msg,msg_success=msg_success)
    return redirect(url_for('doctor_login'))


@app.route('/api/update-quantity', methods=['put'])
def update_quantity():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')
    try:
        key = app.config['CART_KEY']
        cart = session.get(key)
        if cart and id in cart:
            cart[id]['soLuong'] = quantity
        session[key] = cart
        print(cart)
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route('/api/add-medicine-to-cart',methods=['POST'])
def add_medicine_to_cart():
    data = request.json
    thuoc_id = int(data.get('id'))
    p = dao.get_medicine_by_id(id=thuoc_id)
    giaThuoc = p.giaThuoc
    key = app.config['CART_KEY']
    cart = {}
    if key in session:
        cart = session[key]
    if thuoc_id in cart:
        cart[thuoc_id]['soLuong'] = cart[thuoc_id]['soLuong'] + 1
    else:
        cart[str(thuoc_id)] = {
            'id': thuoc_id,
            'giaThuoc': giaThuoc,
            'soLuong': 1
        }
    print(cart)
    session[key] = cart

    return jsonify({
        'donViThuoc_id': p.donViThuoc_id,
        'CachSD': p.CachSD,
        'thuoc_id': p.id
    })


@app.route('/api/timKiem',methods=['POST'])
def timKiem():
    name = []
    quantity = []
    data = request.json
    fullname = str(data.get('fullname'))

    search = dao.timKiem(fullname)

    for x in search:
        name.append(x[1])
        quantity.append(x[2])

    return jsonify({
        'name': name,
        'quantity': quantity
    })


@app.route('/admin_login',methods=['POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.check_login(username=username, password=password,role=UserRole.ADMIN)
        if user:
            login_user(user=user)
        return redirect('/admin')


@app.route('/staff',methods=['GET','POST'])
def staff_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.check_login(username=username, password=password, role=UserRole.NHANVIENTHANHTOAN)
        if user:
            login_user(user=user)
            return redirect(url_for('bills_staff'))
        else:
            return render_template('staff/staff_login.html');
    if not current_user.is_authenticated or current_user.user_role != UserRole.NHANVIENTHANHTOAN:
        return render_template('staff/staff_login.html');
    return render_template('staff/bill.html');


@app.route('/staff_logout')
def staff_logout():
    logout_user();
    return redirect('/staff');

@app.route('/bills_staff',methods=['GET', 'POST'])
def bills_staff():
    hoadon = HoaDon.query.all()
    medicine_bill_id = request.form.get('medicine_bill_id')
    if medicine_bill_id:
        return render_template('staff/bill.html', bills=dao.search_medicine_bill_by_id(medicine_bill_id))
    return render_template('staff/bill.html', bills=hoadon)


@app.route('/api/pay',methods=['POST'])
def pay():
    data = request.json
    id = str(data.get('id'))
    try:
        dao.reload_state_pay(id)
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


if __name__ == "__main__":
    app.run(debug=True)