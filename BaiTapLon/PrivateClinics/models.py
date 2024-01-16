from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from PrivateClinics import app, db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    KHACHHANG = 2
    BACSI = 3
    YTA = 4
    NHANVIENTHANHTOAN = 5


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    ngayThamGia = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.ADMIN)
    DSDatLich = relationship('DanhSachDatLich', backref='user', lazy=True)
    hoadon = relationship('HoaDon', backref='user', lazy=True)

    def __str__(self):
        return self.name


class DanhSachLichKham(BaseModel):
    ngayTao = Column(DateTime, default=datetime.now(), nullable=False)
    DSDatLich = relationship('DanhSachDatLich', backref='DanhSachLichKham', lazy=True)

    def __str__(self):
        return self.ngayTao.__str__()


class DanhSachDatLich(BaseModel):
    tenBN = Column(String(255), nullable=False)
    gioiTinh = Column(String(50), nullable=False)
    namSinh = Column(String(100))
    SDT = Column(String(100))
    diaChi = Column(String(100))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    DSLichKham_id = Column(Integer, ForeignKey(DanhSachLichKham.id), nullable=False)


class DonViThuoc(BaseModel):
    __tablename__ = 'DonViThuoc'
    name = Column(String(20), nullable=False)
    thuoc = relationship('Thuoc', backref='DonViThuoc', lazy=True)

    def __str__(self):
        return self.name


class DanhMuc(BaseModel):
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Thuoc(BaseModel):
    name = Column(String(50), nullable=False)
    giaThuoc = Column(Float, default=0)
    CachSD = Column(String(500))
    donViThuoc_id = Column(Integer, ForeignKey(DonViThuoc.id), nullable=False)
    phieuKhamBenh = relationship('ChiTietDonThuoc', backref='Thuoc', lazy=True)
    # danh_muc = relationship('DanhMuc', secondary='DanhMucThuoc', lazy='subquery', backref=backref('Thuoc', lazy=True))
    # danh_muc_thuoc = relationship('DanhMucThuoc', backref='thuoc', lazy=True)
    def __str__(self):
        return self.name


class DanhMucThuoc(BaseModel):
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id))
    danh_muc_id = Column(Integer, ForeignKey(DanhMuc.id))
    __table_args__ = (
        db.UniqueConstraint('thuoc_id', 'danh_muc_id', name='unique_thuoc_danh_muc'),
    )
    thuocs = relationship('Thuoc', backref='danh_muc_thuoc', lazy=True)
    danh_mucs = relationship('DanhMuc', backref='danh_muc_thuoc', lazy=True)
    def __str__(self):
        return str(self.danh_mucs)


class PhieuKhamBenh(BaseModel):
    fullname = Column(String(300),nullable=False)
    chanDoan = Column(String(300), nullable=False)
    trieuChung = Column(String(300), nullable=False)
    ngaylap = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    thuoc = relationship('ChiTietDonThuoc', backref='PhieuKhamBenh', lazy=True)

    def __str__(self):
        return self.id.__str__()


class HoaDon(BaseModel):
    tenHD = Column(String(100), nullable=False)
    ngayLapHD = Column(DateTime, default=datetime.now())
    tienKham = Column(Float, default=100000)
    tienThuoc = Column(Float, default=0)
    trangThai = Column(Boolean, default=False, nullable=False)  # trang thai thanh toan
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    phieuKhamBenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)


class ChiTietDonThuoc(db.Model):
    soLuong = Column(Integer, nullable=False, default=1)  # số lượng thuốc
    Thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False, primary_key=True)  # id thuốc
    phieuKhamBenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False, primary_key=True)

    def __str__(self):
        return self.phieuKhamBenh_id.__str__()









if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # u1 = DonViThuoc(name='Chai')
        # u2 = DonViThuoc(name='Vỹ')
        # u3 = DonViThuoc(name='Viên')
        # db.session.add(u1)
        # db.session.add(u2)
        # db.session.add(u3)
        #  c1 = DanhMuc(name='Say xe')
        #  c2 = DanhMuc(name='Đau bụng')
        #  c3 = DanhMuc(name='Nhức đầu')
        #  c4 = DanhMuc(name='Cảm cúm')
        #  db.session.add(c1)
        #  db.session.add(c2)
        #  db.session.add(c3)
        #  db.session.add(c4)
        #  t1 = Thuoc(name='Anerol', donViThuoc_id=3, giaThuoc=6000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t2 = Thuoc(name='Dimenhydrinate', donViThuoc_id=2, giaThuoc=20000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t3 = Thuoc(name='Scopolamine Patch', donViThuoc_id=1, giaThuoc=70000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t4 = Thuoc(name='Dong Sung', donViThuoc_id=3, giaThuoc=10000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t5 = Thuoc(name='Prince of Peace Ginger Chews', donViThuoc_id=3, giaThuoc=8000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t6 = Thuoc(name="Sea Band", donViThuoc_id=2, giaThuoc=20000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t7 = Thuoc(name='Benadryl', donViThuoc_id=1, giaThuoc=150000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t8 = Thuoc(name='Bonine', donViThuoc_id=3, giaThuoc=7000,
        #             CachSD='Uống trước giờ khởi hành 30p', )
        #  t9 = Thuoc(name='Yspbio Tase', donViThuoc_id=3, giaThuoc=5000,
        #             CachSD='Mỗi lần uống 1 viên, uống 2 lần 1 ngày', )
        #  t10 = Thuoc(name='Mozoly 5mg Cadila', donViThuoc_id=1, giaThuoc=60000,
        #              CachSD='Mỗi lần uống 1 viên, uống 2 lần 1 ngày', )
        #  t11 = Thuoc(name='Uvomo', donViThuoc_id=1,
        #              giaThuoc=35000, CachSD='Mỗi lần uống 1 viên, uống 2 lần 1 ngày')
        #  t12 = Thuoc(name='Carbomint', donViThuoc_id=3, giaThuoc=7000,
        #             CachSD='Mỗi lần uống 1 viên, uống 2 lần 1 ngày', )
        #  t13 = Thuoc(name='Cumargold Daily Cvi', donViThuoc_id=2, giaThuoc=15000,
        #             CachSD='Mỗi lần uống 1 viên, uống 2 lần 1 ngày', )
        #  t14 = Thuoc(name='Doglitazon', donViThuoc_id=1, giaThuoc=50000,
        #             CachSD='Mỗi lần uống 1 viên, uống 2 lần 1 ngày', )
        #  t15 = Thuoc(name='Nabumetone', donViThuoc_id=2, giaThuoc=20000,
        #             CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h', )
        #  t16 = Thuoc(name='Diclofenac', donViThuoc_id=3, giaThuoc=7000,
        #             CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h', )
        #  t17 = Thuoc(name="Oxaprozin", donViThuoc_id=1, giaThuoc=40000,
        #             CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h', )
        #  t18 = Thuoc(name='Etodolac', donViThuoc_id=2, giaThuoc=15000,
        #             CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h', )
        #  t19 = Thuoc(name='Naproxen', donViThuoc_id=1, giaThuoc=35000,
        #             CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h', )
        #  t20 = Thuoc(name='Ibuprofen', donViThuoc_id=2, giaThuoc=20000,
        #             CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h', )
        #  t21 = Thuoc(name='Aspirin', donViThuoc_id=3, giaThuoc=7000,
        #              CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h', )
        #  t22 = Thuoc(name='Acetaminophen', donViThuoc_id=3, giaThuoc=8000,
        #              CachSD='Dùng 2 viên trong 1 lần, mỗi lần cách nhau 4h, không quá 4 lần trong 24h')
        #  t23 = Thuoc(name='Hapacol CS Day', donViThuoc_id=3, giaThuoc=5000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  t24 = Thuoc(name='Glotadol Cold', donViThuoc_id=2, giaThuoc=13000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  t25 = Thuoc(name='Euquimol', donViThuoc_id=1, giaThuoc=26000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  t26 = Thuoc(name='Decolgen Forte', donViThuoc_id=2, giaThuoc=9000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  t27 = Thuoc(name='Naphazolin', donViThuoc_id=1, giaThuoc=20000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  t28 = Thuoc(name="Xylometazolin", donViThuoc_id=1, giaThuoc=25000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  t29 = Thuoc(name='Paracetamol', donViThuoc_id=3, giaThuoc=10000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  t30 = Thuoc(name='Coldfed', donViThuoc_id=1, giaThuoc=22000,
        #             CachSD='Uống sau mỗi bữa ăn', )
        #  db.session.add(t1)
        #  db.session.add(t2)
        #  db.session.add(t3)
        #  db.session.add(t4)
        #  db.session.add(t5)
        #  db.session.add(t6)
        #  db.session.add(t7)
        #  db.session.add(t8)
        #  db.session.add(t9)
        #  db.session.add(t10)
        #  db.session.add(t11)
        #  db.session.add(t12)
        #  db.session.add(t13)
        #  db.session.add(t14)
        #  db.session.add(t15)
        #  db.session.add(t16)
        #  db.session.add(t17)
        #  db.session.add(t18)
        #  db.session.add(t19)
        #  db.session.add(t20)
        #  db.session.add(t21)
        #  db.session.add(t22)
        #  db.session.add(t23)
        #  db.session.add(t24)
        #  db.session.add(t25)
        #  db.session.add(t26)
        #  db.session.add(t27)
        #  db.session.add(t28)
        #  db.session.add(t29)
        #  db.session.add(t30)
        #  dmt1 = DanhMucThuoc(thuoc_id=1, danh_muc_id=1)
        #  dmt2 = DanhMucThuoc(thuoc_id=2, danh_muc_id=1)
        #  dmt3 = DanhMucThuoc(thuoc_id=3, danh_muc_id=1)
        #  dmt4 = DanhMucThuoc(thuoc_id=4, danh_muc_id=1)
        #  dmt5 = DanhMucThuoc(thuoc_id=5, danh_muc_id=1)
        #  dmt6 = DanhMucThuoc(thuoc_id=6, danh_muc_id=1)
        #  dmt7 = DanhMucThuoc(thuoc_id=7, danh_muc_id=1)
        #  dmt8 = DanhMucThuoc(thuoc_id=8, danh_muc_id=1)
        #  dmt9 = DanhMucThuoc(thuoc_id=9, danh_muc_id=2)
        #  dmt10 = DanhMucThuoc(thuoc_id=10, danh_muc_id=2)
        #  dmt11 = DanhMucThuoc(thuoc_id=11, danh_muc_id=2)
        #  dmt12 = DanhMucThuoc(thuoc_id=12, danh_muc_id=2)
        #  dmt13 = DanhMucThuoc(thuoc_id=13, danh_muc_id=2)
        #  dmt14 = DanhMucThuoc(thuoc_id=14, danh_muc_id=2)
        #  dmt15 = DanhMucThuoc(thuoc_id=15, danh_muc_id=3)
        #  dmt16 = DanhMucThuoc(thuoc_id=16, danh_muc_id=3)
        #  dmt17 = DanhMucThuoc(thuoc_id=17, danh_muc_id=3)
        #  dmt18 = DanhMucThuoc(thuoc_id=18, danh_muc_id=3)
        #  dmt19 = DanhMucThuoc(thuoc_id=19, danh_muc_id=3)
        #  dmt20 = DanhMucThuoc(thuoc_id=20, danh_muc_id=3)
        #  dmt21 = DanhMucThuoc(thuoc_id=21, danh_muc_id=3)
        #  dmt22 = DanhMucThuoc(thuoc_id=22, danh_muc_id=3)
        #  dmt23 = DanhMucThuoc(thuoc_id=23, danh_muc_id=4)
        #  dmt24 = DanhMucThuoc(thuoc_id=24, danh_muc_id=4)
        #  dmt25 = DanhMucThuoc(thuoc_id=25, danh_muc_id=4)
        #  dmt26 = DanhMucThuoc(thuoc_id=26, danh_muc_id=4)
        #  dmt27 = DanhMucThuoc(thuoc_id=27, danh_muc_id=4)
        #  dmt28 = DanhMucThuoc(thuoc_id=28, danh_muc_id=4)
        #  dmt29 = DanhMucThuoc(thuoc_id=29, danh_muc_id=3)
        #  dmt30 = DanhMucThuoc(thuoc_id=29, danh_muc_id=4)
        #  dmt31 = DanhMucThuoc(thuoc_id=30, danh_muc_id=4)
        #  db.session.add(dmt1)
        #  db.session.add(dmt2)
        #  db.session.add(dmt3)
        #  db.session.add(dmt4)
        #  db.session.add(dmt5)
        #  db.session.add(dmt6)
        #  db.session.add(dmt7)
        #  db.session.add(dmt8)
        #  db.session.add(dmt9)
        #  db.session.add(dmt10)
        #  db.session.add(dmt11)
        #  db.session.add(dmt12)
        #  db.session.add(dmt13)
        #  db.session.add(dmt14)
        #  db.session.add(dmt15)
        #  db.session.add(dmt16)
        #  db.session.add(dmt17)
        #  db.session.add(dmt18)
        #  db.session.add(dmt19)
        #  db.session.add(dmt20)
        #  db.session.add(dmt21)
        #  db.session.add(dmt22)
        #  db.session.add(dmt23)
        #  db.session.add(dmt24)
        #  db.session.add(dmt25)
        #  db.session.add(dmt26)
        #  db.session.add(dmt27)
        #  db.session.add(dmt28)
        #  db.session.add(dmt29)
        #  db.session.add(dmt30)
        #  db.session.add(dmt31)
        # user1 = User(name='admin', username='admin', password='c4ca4238a0b923820dcc509a6f75849b',
        #              email='2051052030duc@ou.edu.vn',
        #              user_role='1')
        #
        # user2 = User(name='du', username='du', password='c20ad4d76fe97759aa27a0c99bff6710',
        #              email='dunguyen31122002@gmail.com',
        #              user_role='2')
        #
        # user3 = User(name='doctor', username='doctor', password='202cb962ac59075b964b07152d234b70',
        #              email='doctor@gmail.com',
        #              user_role='3')
        #
        # user4 = User(name='nurse', username='nurse', password='81dc9bdb52d04dc20036dbd8313ed055',
        #              email='nurse@gmail.com',
        #              user_role='4')
        #
        # user5 = User(name='staff', username='staff', password='827ccb0eea8a706c4c34a16891f84e7b',
        #              email='staff@gmail.com',
        #              user_role='5')
        #
        # db.session.add(user1)
        # db.session.add(user2)
        # db.session.add(user3)
        # db.session.add(user4)
        # db.session.add(user5)
        db.session.commit()
