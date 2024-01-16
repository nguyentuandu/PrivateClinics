import hashlib
from flask_login import current_user
from sqlalchemy import extract, func
from PrivateClinics import utils
from PrivateClinics.models import *


def get_user_by_id(user_id):
    return User.query.get(user_id)


def register(name, username, password, email):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=username, username=username.strip(), password=password, email=email, user_role=UserRole.KHACHHANG)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def check_login(username, password, role):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def add_schedule(ngayTao, tenBN, **kwargs):
    list = DanhSachLichKham.query.filter(DanhSachLichKham.ngayTao == ngayTao).first()

    if list is None:
        list = DanhSachLichKham(ngayTao=ngayTao)
        db.session.add(list)
        db.session.commit()

        d = DanhSachDatLich(DSLichKham_id=list.id, user=current_user,
                            tenBN=tenBN.strip(),
                            SDT=kwargs.get('SDT'),
                            gioiTinh=kwargs.get('gioiTinh'),
                            diaChi=kwargs.get('diaChi'),
                            namSinh=kwargs.get('namSinh'))
    else:
        d = DanhSachDatLich(DSLichKham_id=list.id, user=current_user,
                            tenBN=tenBN.strip(),
                            SDT=kwargs.get('SDT'),
                            gioiTinh=kwargs.get('gioiTinh'),
                            diaChi=kwargs.get('diaChi'),
                            namSinh=kwargs.get('namSinh'))

    db.session.add(d)
    db.session.commit()


def count_schedule_by_date(ngayTao='2022-01-10'):
    return db.session.query(func.count().label('count_records'), DanhSachLichKham.ngayTao) \
        .join(DanhSachDatLich, DanhSachDatLich.DSLichKham_id.__eq__(DanhSachLichKham.id)) \
        .filter(DanhSachLichKham.ngayTao == ngayTao) \
        .group_by(DanhSachDatLich.id, DanhSachLichKham.ngayTao).all()


def get_medicine_by_id(id):
    return Thuoc.query.get(id)


def add_medical_bill(fullname, ngay_lap, chan_doan, trieu_chung, cart):
    # print(fullname, ngay_lap, chan_doan, trieu_chung)
    # print('cart: ', cart)
    medicinal_bill = PhieuKhamBenh(fullname=fullname,
                                   ngaylap=ngay_lap,
                                   chanDoan=chan_doan,
                                   trieuChung=trieu_chung,
                                   user_id=current_user.id)

    db.session.add(medicinal_bill)
    db.session.commit()
    # tạo một cái bill
    add_Bills(medical_bill=medicinal_bill, cart=cart)
    # add medicalBillDetail
    for c in cart.values():
        medical_bill_detail = ChiTietDonThuoc(phieuKhamBenh_id=medicinal_bill.id,
                                              Thuoc_id=c['id'],
                                              soLuong=c['soLuong'])
        db.session.add(medical_bill_detail)
    db.session.commit()


def add_Bills(medical_bill, cart):
    user = get_user_by_id(medical_bill.user_id)
    bills = HoaDon(tenHD=medical_bill.fullname, ngayLapHD=medical_bill.ngaylap,
                   tienThuoc=utils.count_cart(cart),
                   tienKham=100000,
                   user_id=user.id,
                   phieuKhamBenh_id=medical_bill.id)
    db.session.add(bills)
    db.session.commit()


def total_bill(month):
    return db.session.query(func.sum(HoaDon.tienThuoc + HoaDon.tienKham))\
        .filter(extract('month', HoaDon.ngayLapHD) == month).all()


def bill_stats(month):
    p = total_bill(month)
    q = p[0]
    x = q[0]
    p = db.session.query(extract('day', HoaDon.ngayLapHD), func.sum(HoaDon.tienThuoc + HoaDon.tienKham),
                         func.count(HoaDon.phieuKhamBenh_id),
                         func.round(((func.sum(HoaDon.tienThuoc + HoaDon.tienKham) / x) * 100), 2)) \
        .filter(extract('month', HoaDon.ngayLapHD) == month) \
        .group_by(extract('day', HoaDon.ngayLapHD)) \
        .order_by(extract('day', HoaDon.ngayLapHD))

    return p.all()


def search_medicine_bill_by_id(medicine_bill_id):
    return HoaDon.query.filter(HoaDon.id.__eq__(medicine_bill_id))


def reload_state_pay(bill_id):
    p = HoaDon.query.filter(HoaDon.id.__eq__(bill_id)).first()
    p.trangThai = True
    db.session.commit()


def timKiem(fullname):
    return db.session.query(PhieuKhamBenh.fullname, Thuoc.name, func.sum(ChiTietDonThuoc.soLuong)) \
                     .join(ChiTietDonThuoc, PhieuKhamBenh.id.__eq__(ChiTietDonThuoc.phieuKhamBenh_id))\
                     .join(Thuoc, Thuoc.id.__eq__(ChiTietDonThuoc.Thuoc_id)) \
                     .filter(PhieuKhamBenh.fullname.__eq__(fullname)) \
                     .group_by(PhieuKhamBenh.fullname, Thuoc.name).all()

# def medicine_month_stats(month, kw=None, id=None):
#     p = db.session.query(Thuoc.id, Thuoc.name, DonViThuoc.name, ChiTietDonThuoc.soLuong)\
#                     .join(ChiTietDonThuoc, ChiTietDonThuoc.Thuoc_id.__eq__(Thuoc.id), isouter=True)\
#                     .join(PhieuKhamBenh, PhieuKhamBenh.id.__eq__(ChiTietDonThuoc.phieuKhamBenh_id))\
#                     .join(DonViThuoc, Thuoc.donViThuoc_id.__eq__(DonViThuoc.id)) \
#                     .join(HoaDon, HoaDon.phieuKhamBenh_id.__eq__(PhieuKhamBenh.id)) \
#                     .filter(extract('month', HoaDon.ngayLapHD) == month) \
#                     .group_by(Thuoc.id, Thuoc.name) \
#                     .order_by(ChiTietDonThuoc.soLuong)
#
#     if kw:
#         p = p.filter(Thuoc.name.contains(kw))
#     if id:
#         p = p.filter(Thuoc.id.contains(id))
#     return p.all()


def medicine_month_stats(month, kw=None, id=None):
    p = db.session.query(
        Thuoc.id,
        Thuoc.name,
        DonViThuoc.name,
        func.sum(ChiTietDonThuoc.soLuong)
    ) \
        .join(ChiTietDonThuoc, ChiTietDonThuoc.Thuoc_id.__eq__(Thuoc.id), isouter=True) \
        .join(PhieuKhamBenh, PhieuKhamBenh.id.__eq__(ChiTietDonThuoc.phieuKhamBenh_id)) \
        .join(DonViThuoc, Thuoc.donViThuoc_id.__eq__(DonViThuoc.id)) \
        .join(HoaDon, HoaDon.phieuKhamBenh_id.__eq__(PhieuKhamBenh.id)) \
        .filter(extract('month', HoaDon.ngayLapHD) == month) \
        .group_by(Thuoc.id, Thuoc.name, DonViThuoc.name) \
        .order_by(func.sum(ChiTietDonThuoc.soLuong))

    if kw:
        p = p.filter(Thuoc.name.contains(kw))
    if id:
        p = p.filter(Thuoc.id.contains(id))
    return p.all()


if __name__=="__main__":
    with app.app_context():
        pass