from django import forms
from django.db import models
from django.forms import widgets
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput, SelectDateWidget, Textarea
from django.core.validators import RegexValidator
from .models import hoso, marquette, nhacungcap, sanpham, phulieu, choghepmabfo, thongbao, thaydoi, sosanh, sosanhtext, sosanhimage, marquettedat, xuly, tongket
from dal import autocomplete

# Model hoso
class HosoForm(forms.ModelForm):
    class Meta:
        model = hoso
        fields = ['sodangky','ngaycap','ngayhethan','sotucongbo','tensanpham','hansanpham','hoatchat','hamluong','dangbaoche','tieuchuan','nhadk','nhapp','quycach','phanloai']
        help_texts ={"hansanpham": "Nhập số (Đơn vị: tháng)",}
        widgets = {'ngaycap': forms.SelectDateWidget(years=range(2010, 2050)),
                'ngayhethan': forms.SelectDateWidget(),}

class AutocompleteSDK(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = hoso.objects.all()
        if self.q:
            qs = qs.filter(sodangky__istartswith=self.q)
        return qs

class SearchHosoForm(forms.Form):
    sdk = forms.ModelChoiceField(
        label='Số đăng ký', 
        queryset=hoso.objects.values_list('sodangky'),
        widget=autocomplete.ModelSelect2(
            url='autocompletesdk', 
            attrs={'data-placeholder':'Nhập số đăng ký',
                'data-minimum-input-length': 3,}
        ))

class TCBForm(forms.Form):
    sodk = forms.ModelChoiceField(
        label='Số đăng ký', 
        queryset=hoso.objects.values_list('sodangky'),
        widget=autocomplete.ModelSelect2(
            url='autocompletesdk', 
            attrs={'data-placeholder':'Nhập số đăng ký',
                'data-minimum-input-length': 3,}
        ))
    ngaychot = forms.DateField(label='Ngày chốt số tự công bố',
                            widget=forms.SelectDateWidget(years=range(2000, 2050)),)

# Model sanpham
class AutocompleteSP(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = hoso.objects.all()
        if self.q:
            qs = qs.filter(tensanpham__icontains=self.q)
        return qs

class SearchSPForm(forms.Form):
    sp = forms.ModelChoiceField(
        label='Sản phẩm sử dụng', 
        queryset=hoso.objects.values_list('sodangky'),
        widget=autocomplete.ModelSelect2(
            url='autocompletesp', 
            attrs={'data-placeholder':'Nhập tên sản phẩm',
                'data-minimum-input-length': 3,}
        ))

class AutocompleteBFO(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = sanpham.objects.all()
        if self.q:
            qs = qs.filter(sodangky__tensanpham__icontains=self.q)
        return qs

class SearchBFOForm(forms.Form):
    mabfo = forms.ModelChoiceField(
        label='Sản phẩm', 
        queryset=sanpham.objects.values_list('mabfo'),
        widget=autocomplete.ModelSelect2(
            url='autocompletebfo', 
            attrs={'data-placeholder':'Nhập tên sản phẩm',
                'data-minimum-input-length': 3,}
        ))

class SanphamForm(forms.ModelForm):
    sodangky = forms.ModelChoiceField(
        label='Tên sản phẩm', 
        queryset=hoso.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='autocompletesp', 
            attrs={'data-placeholder':'Nhập tên sản phẩm',
                'data-minimum-input-length': 3,}
        ))
    class Meta:
        model = sanpham
        fields = ['mabfo','sodangky','quycach','vitri']

class SanphamPLForm(forms.ModelForm):
    class Meta:
        model = phulieu
        fields = ['mabfomoi','loai','lanbanhanh','dauma','trangthaihoso']

class WaitForm(forms.ModelForm):
    sodangky = forms.ModelChoiceField(
        label='Số đăng ký', 
        queryset=hoso.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='autocompletesdk', 
            attrs={'data-placeholder':'Nhập số đăng ký',
                'data-minimum-input-length': 3,}
        ))
    class Meta:
        model = choghepmabfo
        fields = ['sodangky','quycach','vitri']

# Model phulieu
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

class AutocompletePL(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = phulieu.objects.all()
        if self.q:
            qs = qs.filter(mabfomoi__istartswith=self.q)
        return qs

class SearchPLForm(forms.Form):
    mabfomoi =  forms.ModelChoiceField(
        label='Mã BFO (Fast)',
        queryset=phulieu.objects.values_list('mabfomoi'),
        widget=autocomplete.ModelSelect2(
            url='autocompletepl', 
            attrs={'data-placeholder':'Nhập mã BFO (Fast)',}
        ))
    lanbanhanh = forms.IntegerField(label='Lần ban hành')

class NewPhulieuForm(forms.Form):
    sp = forms.ModelChoiceField(
        label='Sản phẩm sử dụng', 
        queryset=hoso.objects.values_list('sodangky'),
        widget=autocomplete.ModelSelect2(
            url='autocompletesp', 
            attrs={'data-placeholder':'Nhập tên sản phẩm',
                'data-minimum-input-length': 3,}
        ))
    mabfomoi = forms.CharField(label='Mã BFO mới')
    loai = forms.ChoiceField(label='Loại phụ liệu',choices=PHULIEU_CHOICES)
    trangthaihoso = forms.ChoiceField(label='Trạng thái hồ sơ',choices=TRANGTHAIHOSO_CHOICES)

class PhulieuForm(forms.Form):
    sp = forms.ModelChoiceField(
        label='Sản phẩm sử dụng', 
        queryset=hoso.objects.values_list('sodangky'),
        widget=autocomplete.ModelSelect2(
            url='autocompletesp', 
            attrs={'data-placeholder':'Nhập tên sản phẩm',
                'data-minimum-input-length': 3,}
        ))
    mabfomoi =  forms.ModelChoiceField(
        label='Mã BFO (Fast)',
        queryset=phulieu.objects.values_list('mabfomoi'),
        widget=autocomplete.ModelSelect2(
            url='autocompletepl', 
            attrs={'data-placeholder':'Nhập mã BFO phụ liệu',}
        ))
    lanbanhanh = forms.IntegerField(label='Lần ban hành')
    trangthaihoso = forms.ChoiceField(label='Trạng thái hồ sơ',choices=TRANGTHAIHOSO_CHOICES)

class MarquetteForm(forms.Form):
    nhacc =  forms.ModelMultipleChoiceField(label='Mã nhà cung cấp',
                                            queryset=nhacungcap.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            )

# Model thaydoi
class ThongbaoForm(forms.ModelForm):
    class Meta:
        model = thongbao
        fields = ['congvan','ngayhethancv','ngayapdung','sodangky','loai','uutien','lydo']
        widgets = {'ngayhethancv': forms.SelectDateWidget(),
                'ngayapdung': forms.SelectDateWidget(),
                'sodangky': forms.HiddenInput()}

class PLthaydoiForm(forms.Form):
    mabfomoi =  forms.ModelChoiceField(
        label='Mã BFO (Fast)',
        queryset=phulieu.objects.values_list('mabfomoi'),
        widget=autocomplete.ModelSelect2(
            url='autocompletepl', 
            attrs={'data-placeholder':'Nhập mã BFO phụ liệu',}
        ))
    lbhtruoc = forms.IntegerField(label='Lần ban hành trước')
    lbhsau = forms.IntegerField(label='Lần ban hành sau')

class SosanhForm(forms.ModelForm):
    class Meta:
        model = sosanh
        fields = ['loai','noidung','matruoc','masau']

class SSTextForm(forms.ModelForm):
    class Meta:
        model = sosanhtext
        fields = ['sosanh','noidung','chutruoc','chusau']
        widgets = {'sosanh': forms.HiddenInput,}

class SSImageForm(forms.ModelForm):
    class Meta:
        model = sosanhimage
        fields = ['noidung','anhtruoc','anhsau']
       # widgets = {'sosanh': forms.HiddenInput,}

class SolutionUpdateForm(forms.ModelForm):
    class Meta:
        model = xuly
        fields = ['xuly','chotxuly','ngaychot','thoihan','chothuy','trangthai']
        widgets = {'ngaychot': forms.SelectDateWidget(),
                'thoihan': forms.SelectDateWidget(years=range(2000, 2050)),
                'trangthai': forms.HiddenInput,}

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = xuly
        fields = ['lenhsx','ngaysx','hansd','khsx','trangthai']
        widgets = {'ngaysx': forms.SelectDateWidget(),
                'hansd': forms.SelectDateWidget(),
                'trangthai': forms.HiddenInput,}

class ChotSDForm(forms.ModelForm):
    class Meta:
        model = tongket
        fields = ['chotsudung','tinhtrang','ghichu']

class EmailForm(forms.Form):
    attach = forms.FileField(label='Tệp đính kèm',widget=forms.ClearableFileInput)
    message = forms.CharField(label='Nội dung mail',widget=forms.Textarea)
    huongxutri = forms.CharField(label='Hướng xử trí',widget=forms.Textarea)
    noidungthaydoi = forms.CharField(label='Nội dung thay đổi',widget=forms.Textarea)
    link = forms.URLField(label='Link bản mềm')