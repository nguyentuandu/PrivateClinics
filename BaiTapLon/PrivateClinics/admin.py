from PrivateClinics import admin, db, app, dao
from PrivateClinics.models import UserRole, User, DanhMuc,Thuoc, DonViThuoc, DanhSachDatLich
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_login import current_user, logout_user
from datetime import datetime
from flask import request,redirect,url_for


class AuthenticatedModelView(ModelView):
    column_display_pk = False
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role==UserRole.ADMIN


class UserView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_exclude_list = ['password','ngayThamGia']
    column_filters = ['username']
    column_searchable_list = ['username']
    column_labels = {
        'name':'Họ và tên',
        'username': 'Tên đăng nhập',
        'active': 'Hoạt động',
        'user_role': 'Quyền người dùng',
        'ngayThamGia':'Ngày tham gia'
    }


class MedicineView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    column_filters = ['name','giaThuoc']
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Tên thuốc ',
        'giaThuoc': 'Giá',
        'CachSD': 'Cách sử dụng',
        'DonViThuoc': 'Đơn vị thuốc',
    }


class CateView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    column_filters = ['name']
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Tên loại thuốc '
    }


class UnitView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    column_filters = ['name']
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Tên đơn vị '
    }


class ScheduleListView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    create_modal = True
    details_modal = True
    edit_modal = True
    column_filters = ['tenBN','SDT']
    column_searchable_list = ['tenBN','SDT']
    column_labels = {
        'tenBN': 'Tên BN',
        'gioiTinh': 'Giới tính ',
        'namSinh': 'Năm sinh',
        'SDT': 'SĐT',
        'diaChi':'Địa chỉ',
    }


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin/')

    def is_accessible(self):
        return current_user.is_authenticated


class Stats(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month', datetime.now().month)
        kw = request.args.get('kw')
        id = request.args.get('id')
        return self.render('admin/stats.html',
                           medi_month_stats=dao.medicine_month_stats(kw=kw, id=id, month=month)
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role==UserRole.ADMIN


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        total = 0
        month = request.args.get('month', datetime.now().month)
        return self.render('admin/index.html', month_stats=dao.bill_stats(month), total=dao.total_bill(month))


admin = Admin(app=app, name='QUẢN LÝ PHÒNG MẠCH', template_mode='bootstrap4', index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session, name='Quản lý người dùng'))
admin.add_sub_category(name='medicine_manager ', parent_name='Quản lý thuốc')
admin.add_view(MedicineView(Thuoc, db.session, name='Thuốc', category='Quản lý thuốc'))
admin.add_view(CateView(DanhMuc, db.session, name='Loại thuốc',category='Quản lý thuốc'))
admin.add_view(UnitView(DonViThuoc, db.session,name='Đơn vị thuốc',category='Quản lý thuốc'))
# admin.add_view(ModelView(Thuoc,db.session, name='Thuốc'))
admin.add_view(ScheduleListView(DanhSachDatLich, db.session, name='Quản lý đặt lịch'))
admin.add_view(Stats(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))