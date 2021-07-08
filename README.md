# Project Website phụ liệu CPC1

## Giới thiệu
Website quản lý phụ liệu cho các phòng ban Quản lý Chất lượng, Nghiên cứu Phát triển sản phẩm, Kế hoạch và Kho của Công ty Cổ phần CPC1 Hà Nội.

## Nội dung
* [Kỹ thuật](#kythuat)
* [Tính năng công nghệ](#congnghe)
* [Tính năng sử dụng](#sudung)
* [Phát triển](#phattrien)

<a name="kythuat"/>
## Kỹ thuật
Trang web được viết bằng:
* Back-end Development:
  * python 3.9.5
  * Django 3.2.4
  * mysqlclient 2.0.3 (Kết nối với local MySQL qua MySQL Workbench)  
* Front-end Development:
  * HTML/CSS (Dùng template có sẵn tại https://www.free-css.com/free-css-templates/page9/the-green-house)
  * Bootstrap 4: Đang thử nghiệm để bổ sung modal dialog
  * Jquery 3.6: Đang thử nghiệm để bổ sung modal dialog
* Libraries:
  * django-autocomplete-light==3.8.2: Xử lý autocomplete cho thao tác điền form (Nhập/Tra cứu)
  * django-import-export==2.5.0: Xử lý import dữ liệu từ file excel tại admin site
  * xlwt==1.3.0: Xử lý export dữ liệu tại client site
  * WeasyPrint==52.5: Xử lý xuất file pdf (Cần install GTK+ và cairo đi kèm, chi tiết xem https://weasyprint.readthedocs.io/en/latest/install.html)
  * django-bootstrap-modal-forms==2.2.0: Đang thử nghiệm để bổ sung modal dialog
* Deploy Production (Hosted by Heroku):
  * django-heroku==0.3.1
  * gunicorn==20.1.0
  * dj-database-url==0.5.0
  * psycopg2==2.9.1
  * whitenoise==5.2.0
  * Kết nối với local PostgreSQL qua pgAdmin4
  * Kết nối với Amazon S3 Bucket để lưu trữ file static và media (Cài đặt django-storages và boto3): Chưa làm

<a name="congnghe"/>
## Tính năng công nghệ
1. CRUD dữ liệu (Create/Read/Update/Delete)
2. Xuất dữ liệu dưới dạng file .xls
3. Xuất file pdf
4. Gửi mail

<a name="sudung"/>
## Tính năng sử dụng
1. Với phòng Nghiên cứu Phát triển:
    *  Nhập/Tra cứu/Sửa thông tin hồ sơ số đăng ký
    *  Nhập/Tra cứu số tự công bố
    *  Tra cứu số đăng ký hết hạn
    *  Ban hành (Nhập) marquette cho sản phẩm mới đã có mã BFO sản phẩm
    *  Ban hành (Nhập) marquette cho sản phẩm mới chưa có mã BFO sản phẩm
    *  Ban hành (Nhập) marquette cho phụ liệu có sự thay đổi
    *  Ban hành (Nhập) marquette cho phụ liệu có bổ sung nhà cung cấp
    *  Nhập nhà cung cấp mới
    *  Ban hành (Nhập) thay đổi mới (Đi kèm xuất file pdf và gửi mail)
2. Với phòng Kế hoạch:
    * Bổ sung (Nhập) mã BFO cho sản phẩm đã có marquette phụ liệu
    * Tra cứu phụ liệu đang dùng cho sản phẩm (Kết quả trả ra theo lần ban hành và theo marquette)
3. Với phòng Kho vận:
    * Nhập/Tra cứu/Sửa tồn phụ liệu cho kế hoạch sản xuất hàng tuần
4. Với phòng Quản lý Chất lượng:
    * Tra cứu phụ liệu đang dùng cho sản phẩm
    * Tra cứu thông tin thay đổi chưa hoàn thành của sản phẩm
    * Tra cứu tồn kho của phụ liệu
    * Nhập/Tra cứu/Sửa hướng xử lý thay đổi
    * Nhập/Tra cứu thông tin lô sản xuất đầu tiên khi hoàn thành thay đổi
    * Chốt (Nhập) phụ liệu sử dụng cho kế hoạch sản xuất hàng tuần (Dựa vào 5 thông tin trên)

<a name="phattrien"/>
## Phát triển
* Các tính năng đang/dự định được phát triển:
  * Tạo modal form để cải thiện giao diện người dùng
  * Gửi mail liên tục vào một subject
  * Kết nối production environment với Amazon S3 Bucket
  * Thêm cronjob để cảnh báo khi có số đăng ký hết hạn/thay đổi chưa hoàn thành
* Các lỗi có thể gặp
  * Trong quá trình ban hành marquette nếu bị thoát ra sẽ không quay lại nhập tiếp được

