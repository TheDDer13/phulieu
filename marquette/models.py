from django.db import models
from django.core.validators import RegexValidator
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from django.db.models.fields import BooleanField

# Create your models here.
class hoso(models.Model):
    CLASS_CHOICES = [
        ('Thuốc','Thuốc'),
        ('Thực phẩm chức năng','Thực phẩm chức năng'),
        ('Mỹ phẩm','Mỹ phẩm'),
        ('Trang thiết bị','Trang thiết bị'),
        ('Sinh phẩm','Sinh phẩm'),
    ]
    sodangky = models.CharField(max_length=64,primary_key=True,verbose_name='Số đăng ký')
    ngaycap = models.DateField(verbose_name='Ngày cấp')
    ngayhethan = models.DateField(null=True,blank=True,verbose_name='Ngày hết hạn')
    sotucongbo = models.CharField(max_length=64,null=True,blank=True,verbose_name='Số tự công bố',unique=True)
    tensanpham = models.CharField(max_length=255,verbose_name='Tên sản phẩm')
    hansanpham = models.IntegerField(null=True,verbose_name='Hạn sử dụng')
    hoatchat = models.TextField(null=True,blank=True,verbose_name='Hoạt chất')
    hamluong = models.TextField(null=True,blank=True,verbose_name='Hàm lượng')
    dangbaoche = models.TextField(null=True,blank=True,verbose_name='Dạng bào chế')
    tieuchuan = models.CharField(max_length=64,null=True,blank=True,verbose_name='Tiêu chuẩn')
    nhadk = models.CharField(max_length=64,null=True,blank=True,verbose_name='Nhà đăng ký')
    nhapp = models.CharField(max_length=64,null=True,blank=True,verbose_name='Nhà phân phối')
    quycach = models.TextField(null=True,blank=True,verbose_name='Quy cách')
    phanloai = models.CharField(max_length=64,choices=CLASS_CHOICES,verbose_name='Phân loại')
    def __str__(self):
        return f"{self.tensanpham} (SDK: {self.sodangky})"

class nhacungcap(models.Model):
    ten = models.CharField(max_length=255,verbose_name='Nhà cung cấp')
    ma = models.CharField(max_length=6,verbose_name='Mã nhà cung cấp',primary_key=True)
    def __str__(self):
        return f"{self.ma}-{self.ten}"  

class phulieu(models.Model):
    PHULIEU_CHOICES = [
        ('Cầu','Cầu'),
        ('Hộp nhỏ','Hộp nhỏ'),
        ('Hộp trung gian','Hộp trung gian'),
        ('Khay cài','Khay cài'),
        ('Màng co','Màng co'),
        ('Màng nhôm','Màng nhôm'),
        ('Màng viên đặt','Màng viên đặt',),
        ('Tem chính','Tem chính'),
        ('Tem phụ','Tem phụ'),
        ('Toa','Toa'),
        ('Tuýp','Tuýp'),
        ('Túi','Túi'),
    ]
    TRANGTHAIHOSO_CHOICES = [
        ('Bản in','Bản in'),
        ('Hoàn thành','Hoàn thành'),
    ]
    mabfomoi = models.CharField(max_length=6,verbose_name='Mã BFO phụ liệu (Fast)')
    mabfocu = models.CharField(max_length=6,null=True,verbose_name='Mã BFO phụ liệu cũ')
    loai = models.CharField(max_length=64,choices=PHULIEU_CHOICES,verbose_name='Loại')
    lanbanhanh = models.IntegerField(verbose_name='Lần ban hành')
    dauma = models.CharField(max_length=6,verbose_name='Đầu mã')
    trangthaihoso = models.CharField(max_length=64,null=True,choices=TRANGTHAIHOSO_CHOICES,verbose_name='Trạng thái')
    soluong = models.IntegerField(null=True,verbose_name='Số lượng')
    class Meta:
        unique_together = (('mabfocu','loai','dauma'),) #Change
        unique_together = (('mabfomoi','lanbanhanh'),)
    def __str__(self):
        return f"{self.mabfomoi}"   

class marquette(models.Model):
    phulieu = models.ForeignKey(phulieu,on_delete=models.PROTECT,related_name='phulieu',verbose_name='Phụ liệu')
    manhacc = models.ForeignKey(nhacungcap,on_delete=models.PROTECT,related_name='nhacc',verbose_name='Nhà cung cấp')
    marquette = models.CharField(max_length=64,verbose_name='Mã marquette')
    def __str__(self):
        return f"{self.phulieu}: {self.marquette}"

class sanpham(models.Model):
    mabfo = models.CharField(max_length=6,primary_key=True,verbose_name='Mã BFO sản phẩm')
    sodangky = models.ForeignKey(hoso, on_delete=models.PROTECT, related_name='hososdk',verbose_name='Số đăng ký')
    quycach = models.TextField(verbose_name='Quy cách')
    vitri = models.CharField(max_length=6,null=True,blank=True,verbose_name='Vị trí')
    # vitri = models.CharField(max_length=6,verbose_name='Vị trí',validators=[RegexValidator(regex='[0-9]-[0-9]-[0-10]',
    #                                                                         message='Vị trí nhập theo dạng 1-1-1',
    #                                                                         ),])
    phulieu = models.ManyToManyField(phulieu,through='sudung',verbose_name='Phụ liệu')
    def __str__(self):
        return f"{self.mabfo}: {self.sodangky} - {self.quycach}"

class sudung(models.Model):
    sp = models.ForeignKey(sanpham,on_delete=models.PROTECT,related_name='spusing',verbose_name='Sản phẩm')
    pl = models.ForeignKey(phulieu,on_delete=models.PROTECT,related_name='plusing',verbose_name='Phụ liệu')
    use = BooleanField(verbose_name="Hiệu lực sử dụng")

class choghepmabfo(models.Model):
    sodangky = models.ForeignKey(hoso,on_delete=models.PROTECT,related_name='sanphamcho',verbose_name='Số đăng ký')
    quycach = models.CharField(max_length=64,verbose_name='Quy cách')
    vitri = models.CharField(max_length=16,null=True,verbose_name='Vị trí',validators=[RegexValidator(regex='[0-9]-[0-9]-*',
                                                                                    message='Vị trí nhập theo dạng 1-1-1',
                                                                                    ),])
    phulieu = models.ManyToManyField(phulieu,related_name='phulieucho',verbose_name='Phụ liệu')
    def __str__(self):
        return f"{self.sodangky}-{self.quycach}"

class thongbao(models.Model):
    THAYDOI_CHOICES = [
        ('BB','Bắt buộc'),
        ('THT','Tự hoàn thiện'),
    ]
    UUTIEN_CHOICES = [
        ('G','Gấp'),
        ('T','Thông thường'),
    ]
    LYDO_CHOICES = [
        ('CPC1','Công ty cổ phần dược phẩm CPC1 Hà Nội'),
        ('NPP','Nhà phân phối'),
    ]
    congvan = models.CharField(max_length=20,null=True,verbose_name='Số công văn thay đổi')
    ngayhethancv = models.DateField(null=True,verbose_name='Ngày hết hạn hiệu lực công văn')
    ngayapdung = models.DateField(verbose_name='Ngày áp dụng thay đổi')
    sodangky = models.ForeignKey(hoso,on_delete=models.PROTECT,related_name='sdkthaydoi',verbose_name='Số đăng ký')
    loai = models.CharField(max_length=6,choices=THAYDOI_CHOICES,verbose_name='Loại thay đổi')
    uutien = models.CharField(max_length=6,choices=UUTIEN_CHOICES,verbose_name='Mức độ ưu tiên')
    lydo = models.CharField(max_length=6,choices=LYDO_CHOICES,verbose_name='Lý do thay đổi')
    mahangdat = models.ManyToManyField(marquette,through='marquettedat',verbose_name='Mã hàng đã đặt')
    link = models.URLField(verbose_name='Link bản mềm')

class thaydoi(models.Model):
    thongbao = models.ForeignKey(thongbao,on_delete=models.PROTECT,related_name='thongbao',verbose_name='Thông báo')
    sanpham = models.ForeignKey(sanpham,on_delete=models.PROTECT,related_name='spthaydoi',verbose_name='Sản phẩm')
    pltruoc = models.ForeignKey(phulieu,on_delete=models.PROTECT,related_name='pltruoc',verbose_name='Phụ liệu trước')
    plsau = models.ForeignKey(phulieu,on_delete=models.PROTECT,related_name='plsau',verbose_name='Phụ liệu sau')

class sosanh(models.Model):
    PHULIEU_CHOICES = [
        ('Cầu','Cầu'),
        ('Hộp nhỏ','Hộp nhỏ'),
        ('Hộp trung gian','Hộp trung gian'),
        ('Khay cài','Khay cài'),
        ('Màng co','Màng co'),
        ('Màng nhôm','Màng nhôm'),
        ('Màng viên đặt','Màng viên đặt',),
        ('Tem chính','Tem chính'),
        ('Tem phụ','Tem phụ'),
        ('Toa','Toa'),
        ('Tuýp','Tuýp'),
        ('Túi','Túi'),
    ]
    thongbao = models.ForeignKey(thongbao,on_delete=models.PROTECT,related_name='thongbaochitiet',verbose_name='Thay đổi')
    loai = models.CharField(max_length=64,choices=PHULIEU_CHOICES,verbose_name='Loại')
    noidung = models.TextField(null=True,verbose_name='Nội dung so sánh')
    matruoc = models.CharField(max_length=64,verbose_name='Marquette trước')
    masau = models.CharField(max_length=64,verbose_name='Marquette sau')

class sosanhtext(models.Model):
    sosanh = models.ForeignKey(sosanh,on_delete=models.PROTECT,related_name='sstext')
    noidung = models.TextField(null=True,verbose_name='Nội dung so sánh')
    chutruoc = models.TextField(null=True,verbose_name='Nội dung trước')
    chusau = models.TextField(null=True,verbose_name='Nội dung hiện tại')

class sosanhimage(models.Model):
    sosanh = models.ForeignKey(sosanh,on_delete=models.PROTECT,related_name='ssimage')
    noidung = models.TextField(null=True,verbose_name='Nội dung so sánh')
    anhtruoc = models.ImageField(null=True,verbose_name='Hình ảnh trước',upload_to='images')
    anhsau = models.ImageField(null=True,verbose_name='Hình ảnh hiện tại',upload_to='images')

class marquettedat(models.Model):
    thongbao = models.ForeignKey(thongbao,on_delete=models.PROTECT,related_name='tbao',verbose_name='Thông báo thay đổi')
    marquettedat = models.ForeignKey(marquette,on_delete=models.PROTECT,related_name='madat',verbose_name='Mã hàng đã đặt')
    tonkho = models.IntegerField(null=True,verbose_name='Tồn kho thực tế')
    dathang = models.IntegerField(null=True,verbose_name='Số lượng đặt')

class xuly(models.Model):
    CHOTXULY_CHOICES = [
        ('Đã chốt','Đã chốt'),
        ('Chưa chốt','Chưa chốt'),
    ]
    CHOTHUY_CHOICES = [
        ('H','Hủy'),
        ('K','Không hủy'),
    ]
    TRANGTHAIXULY_CHOICES = [
        ('Hoàn thành','Hoàn thành'),
        ('Chưa hoàn thành','Chưa hoàn thành'),
    ]
    thaydoi = models.OneToOneField(thaydoi,on_delete=models.PROTECT,primary_key=True,related_name='xulythaydoi',verbose_name='Thay đổi')
    xuly = models.TextField(null=True,verbose_name='Hướng xử lý')
    chotxuly = models.CharField(max_length=64,null=True,choices=CHOTXULY_CHOICES,verbose_name='Tình trạng chốt')
    thoihan = models.DateField(null=True,verbose_name='Thời hạn thực hiện')
    lenhsx =  models.CharField(max_length=255,null=True,verbose_name='Lệnh sản xuất')
    ngaysx = models.DateField(null=True,verbose_name='Ngày sản xuất')
    hansd = models.DateField(null=True,verbose_name='Hạn sử dụng')
    khsx = models.CharField(max_length=255,null=True,verbose_name='Kế hoạch sản xuất')
    trangthai = models.CharField(max_length=64,choices=TRANGTHAIXULY_CHOICES,verbose_name='Trạng thái')
    ngaychot = models.DateField(blank=True,null=True,verbose_name='Ngày chốt')
    chothuy = models.CharField(max_length=64,choices=CHOTHUY_CHOICES,verbose_name='Chốt hủy',null=True)

class tongket(models.Model):
    TRANGTHAIMA_CHOICES = [
        ('Mã cũ','Mã cũ'),
        ('Mã mới','Mã mới'),
    ]
    SUDUNG_CHOICES = [
        ('Có','Có'),
        ('Không','Không'),
    ]
    TINHTRANG_CHOICES = [
        ('Đủ','Đủ'),
        ('Không đủ','Không đủ'),
    ]
    sanpham = models.ForeignKey(sanpham, on_delete=models.PROTECT, related_name='sanpham')
    dauma = models.ForeignKey(phulieu, on_delete=models.PROTECT, related_name='daumabanhanh')
    trangthai = models.CharField(max_length=64,choices=TRANGTHAIMA_CHOICES)
    thaydoi = models.ForeignKey(thaydoi,on_delete=models.PROTECT,related_name='thaydoipending',blank=True,null=True)
    huongxuly = models.ForeignKey(xuly,on_delete=models.PROTECT,related_name='xulypending',blank=True,null=True)
    chotsudung = models.CharField(max_length=64,choices=SUDUNG_CHOICES,null=True,verbose_name='Chốt sử dụng')
    tinhtrang = models.CharField(max_length=64,choices=TINHTRANG_CHOICES,null=True,verbose_name='Tình trạng')
    ghichu = models.TextField(null=True,verbose_name='Ghi chú')