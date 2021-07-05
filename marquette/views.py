
from django import forms
from django.template.defaulttags import register
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.db.models import Max, Count
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from weasyprint.urls import HTTP_HEADERS
from .models import hoso, marquette, nhacungcap, sanpham, phulieu, sudung, choghepmabfo, thongbao, thaydoi, sosanh, sosanhtext, sosanhimage, marquettedat, xuly, tongket
from .forms import AutocompleteSDK, AutocompleteSP, AutocompletePL, AutocompleteBFO
from .forms import HosoForm, SearchHosoForm, TCBForm, SearchSPForm, SearchPLForm, SearchBFOForm, NewPhulieuForm, PhulieuForm, MarquetteForm, SanphamForm
from .forms import SanphamPLForm, WaitForm, ThongbaoForm, PLthaydoiForm, SosanhForm, SolutionUpdateForm, StatusUpdateForm, ChotSDForm, EmailForm, SSTextForm, SSImageForm
from weasyprint import HTML,CSS
from django.core.mail import EmailMessage
from io import BytesIO
from django.conf import settings
import datetime
import xlwt
import os, mimetypes

# Create your views here.
@login_required (login_url='/login/')
def index(request):
    return render(request, 'marquette/index.html')

# Model hoso
@login_required (login_url='/login/')
def sdkindex(request):
    return render(request, 'marquette/sodangky/index.html')

@method_decorator(login_required, name='dispatch')
class DocCreateView(CreateView):
    model = hoso
    form_class = HosoForm
    template_name = 'marquette/sodangky/docinput.html'
    success_url ="/sdk"

@login_required (login_url='/login/')
def docfind(request,action):
    if request.method == "POST":
        thongtin = SearchHosoForm(request.POST)
        if thongtin.is_valid():
            sodk = thongtin.cleaned_data["sdk"]
            if action == 'view':
                return HttpResponseRedirect(reverse('docview',args=(sodk)))
            elif action == 'update':
                return HttpResponseRedirect(reverse('docupdate',args=(sodk)))
            elif action == 'change':
                return HttpResponseRedirect(reverse('tbcreate',args=(sodk)))
    return render(request, 'marquette/sodangky/docfind.html', {
        "form": SearchHosoForm()
    })

@method_decorator(login_required, name='dispatch')
class DocDetailView(DetailView):
    model = hoso
    template_name = 'marquette/sodangky/docview.html'
    slug_field = 'sodangky'

@method_decorator(login_required, name='dispatch')
class DocUpdateView(UpdateView):
    model = hoso
    form_class = HosoForm
    template_name = 'marquette/sodangky/docupdate.html'
    success_url ="/sdk"

@method_decorator(login_required, name='dispatch')
class DocExpiredView(ListView):
    model = hoso
    paginate_by = 10
    context_object_name = 'expiredlist'
    queryset = hoso.objects.filter(ngayhethan__lte=datetime.date.today())
    template_name = 'marquette/sodangky/docexpired.html'

@method_decorator(login_required, name='dispatch')
class DocTCBView(ListView):
    model = hoso
    paginate_by = 10
    context_object_name = 'tcblist'
    queryset = hoso.objects.all().exclude(sotucongbo=None).order_by('sotucongbo')
    template_name = 'marquette/sodangky/doctcb.html'
    
def TCBcreate(request):
    #Count số tự công bố
    sothutu = hoso.objects.aggregate(Count('sotucongbo'))
    index = sothutu['sotucongbo__count'] + 1
    if request.method == "POST":
        thongtin = TCBForm(request.POST)
        if thongtin.is_valid():
            sodk = thongtin.cleaned_data["sodk"]
            ngaychot = thongtin.cleaned_data["ngaychot"]
            #Create số tự công bố
            year = ngaychot.strftime("%y")
            month = ngaychot.strftime("%m")
            stt = f'{index:02d}'
            sotcb = stt+month+'/'+year+'/CPC1HN-TC'
            #Save số tự công bố
            doc = hoso.objects.get(sodangky=sodk[0])
            doc.sotucongbo = sotcb
            doc.save()
            return HttpResponseRedirect(reverse('doctcb'))
    return render(request, 'marquette/sodangky/tcbcreate.html', {
        "form": TCBForm(),
    })

def exporthoso(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="hoso.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Hoso')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Số đăng ký','Tên sản phẩm','Ngày cấp','Ngày hết hạn','Số tự công bố','Hạn sản phẩm','Quy cách','Phân loại']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = hoso.objects.all().values_list('sodangky','tensanpham','ngaycap','ngayhethan','sotucongbo','hansanpham','quycach','phanloai')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# Model sanpham
@login_required (login_url='/login/')
def spindex(request):
    return render(request, 'marquette/sanpham/index.html')

@login_required (login_url='/login/')
def spfind(request,action):
    if request.method == "POST":
        thongtin = SearchBFOForm(request.POST)
        if thongtin.is_valid():
            mabfo = thongtin.cleaned_data["mabfo"]
            if action == 'stock':
                return HttpResponseRedirect(reverse('stockview',kwargs={'ma': mabfo[0], }))
            if action == 'recall':
                return HttpResponseRedirect(reverse('recallview',kwargs={'ma': mabfo[0], }))
            if action == 'view':
                return HttpResponseRedirect(reverse('plview',kwargs={'ma': mabfo[0], }))
            if action == 'change':
                return HttpResponseRedirect(reverse('tdview',kwargs={'ma': mabfo[0], }))
            if action == 'complete':
                return HttpResponseRedirect(reverse('htview',kwargs={'ma': mabfo[0], }))
    return render(request, 'marquette/sanpham/spfind.html', {
        "form": SearchBFOForm,
    })

@method_decorator(login_required, name='dispatch')
class SPCreateView(CreateView):
    model = sanpham
    form_class = SanphamForm
    template_name = 'marquette/sanpham/spcreate.html'
    def form_valid(self, form):
        self.object = form.save()
        pk = self.object.pk
        return HttpResponseRedirect(reverse('spcreatepl', kwargs={'pk': pk, }))

@method_decorator(login_required, name='dispatch')
class PLCreateView(CreateView):
    model = phulieu
    form_class = SanphamPLForm
    template_name = 'marquette/sanpham/spcreatepl.html'
    def get_context_data(self):
        context = super().get_context_data()
        context['sp'] = sanpham.objects.get(pk=self.kwargs['pk'])
        return context
    def form_valid(self, form):
        self.object = form.save()
        sp = sanpham.objects.get(pk=self.kwargs['pk'])
        sudung.objects.create(sp=sp,pl=self.object,use=True)
        pk = self.object.pk 
        return HttpResponseRedirect(reverse('marquettecreate', kwargs={"pk": pk, "sp": sp.mabfo, }))

@login_required (login_url='/login/')
def spaddpl(request,ma):
    if request.method == "POST":
        thongtin = SearchPLForm(request.POST)
        if thongtin.is_valid():
            mapl = thongtin.cleaned_data["mabfomoi"]
            lbh = thongtin.cleaned_data["lanbanhanh"]
            pl = phulieu.objects.get(mabfomoi=mapl[0],lanbanhanh=lbh)
            sp = sanpham.objects.get(mabfo=ma)
            sudung.objects.create(sp=sp,pl=pl,use=True)
            return HttpResponseRedirect(reverse('spcreatepl', kwargs={'pk': ma, }))
    return render(request, 'marquette/sanpham/spaddpl.html',{
        "form": SearchPLForm,
    })

@method_decorator(login_required, name='dispatch')
class PLListView(ListView):
    model = sanpham
    template_name = 'marquette/sanpham/plview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp = sanpham.objects.get(mabfo=self.kwargs['ma'])
        context['sp'] = sp
        context['list'] = sudung.objects.filter(sp=sp,use=True)
        return context

@login_required (login_url='/login/')
def sample(request,pk,ma):
    sample = request.GET.get('sample')
    plieu = phulieu.objects.get(pk=pk)
    plieu.trangthaihoso = sample
    plieu.save()
    return HttpResponseRedirect(reverse('plview', kwargs={'ma': ma, })) 

@login_required (login_url='/login/')
def vitriupdate(request,ma):
    vtri = request.GET.get('vitri')
    sp = sanpham.objects.get(mabfo=ma)
    sp.vitri = vtri
    sp.save()
    return HttpResponseRedirect(reverse('plview', kwargs={'ma': ma, })) 

def exportsanpham(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sanpham.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sanpham')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Mã BFO','Số đăng ký','Tên sản phẩm','Quy cách','Vị trí hồ sơ']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = sanpham.objects.all().values_list('mabfo','sodangky','sodangky__tensanpham','quycach','vitri')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# Model choghepma
@method_decorator(login_required, name='dispatch')
class WaitCreateView(CreateView):
    model = choghepmabfo
    form_class = WaitForm
    template_name = 'marquette/sanpham/waitcreate.html'
    def form_valid(self, form):
        self.object = form.save()
        pk = self.object.pk
        return HttpResponseRedirect(reverse('waitcreatepl', kwargs={'pk': pk, }))

@method_decorator(login_required, name='dispatch')
class WaitPLCreateView(CreateView):
    model = phulieu
    form_class = SanphamPLForm
    template_name = 'marquette/sanpham/waitcreatepl.html'
    def get_context_data(self):
        context = super().get_context_data()
        context['waitsp'] = choghepmabfo.objects.get(pk=self.kwargs['pk'])
        return context
    def form_valid(self, form):
        self.object = form.save()
        waitsp = choghepmabfo.objects.get(pk=self.kwargs['pk'])
        waitsp.phulieu.add(self.object)
        pk = self.object.pk 
        return HttpResponseRedirect(reverse('marquettecreate', kwargs={"pk": pk, "sp": waitsp.pk, }))

@login_required (login_url='/login/')
def waitaddpl(request,ma):
    if request.method == "POST":
        thongtin = SearchPLForm(request.POST)
        if thongtin.is_valid():
            mapl = thongtin.cleaned_data["mabfomoi"]
            lbh = thongtin.cleaned_data["lanbanhanh"]
            pl = phulieu.objects.get(mabfomoi=mapl[0],lanbanhanh=lbh)
            waitsp = choghepmabfo.objects.get(pk=ma)
            waitsp.phulieu.add(pl)
            return HttpResponseRedirect(reverse('waitcreatepl', kwargs={'pk': ma, }))
    return render(request, 'marquette/sanpham/waitaddpl.html',{
        "form": SearchPLForm,
    })

@method_decorator(login_required, name='dispatch')
class WaitView(ListView):
    model = choghepmabfo
    template_name = 'marquette/sanpham/waitview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        waitsp = choghepmabfo.objects.get(pk=self.kwargs['ma'])
        context['waitsp'] = waitsp
        return context

@method_decorator(login_required, name='dispatch')
class WaitListView(ListView):
    model = choghepmabfo
    context_object_name = 'waitlist'
    queryset = choghepmabfo.objects.all()
    template_name = 'marquette/sanpham/waitlistview.html'

@login_required (login_url='/login/')
def addbfo(request,pk):
    bfo = request.POST.get('ma')
    waitsp = choghepmabfo.objects.get(pk=pk)
    sp = sanpham(mabfo=bfo,sodangky=waitsp.sodangky,quycach=waitsp.quycach,vitri=waitsp.vitri)
    sp.save()
    for pl in waitsp.phulieu.all():
        sudung.objects.create(sp=sp,pl=pl,use=True)
    waitsp.delete()
    return HttpResponseRedirect(reverse('waitlistview'))

def exportwaiting(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="thieuBFO.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ThieuBFO')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Số đăng ký','Tên sản phẩm','Quy cách','Vị trí hồ sơ','Mã phụ liệu (Fast)','Mã phụ liệu cũ','Loại phụ liệu','Lần ban hành','Đầu mã']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = sanpham.objects.all().values_list('sodangky','sodangky__tensanpham','quycach','vitri','phulieu__mabfomoi','phulieu__mabfocu','phulieu__loai','phulieu__lanbanhanh','phulieu__dauma')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# Model phulieu
code = {'Cầu': 'C',
        'Hộp nhỏ': 'H',
        'Hộp trung gian': 'H',
        'Khay cài': 'K',
        'Màng co': 'MC',
        'Màng nhôm': 'M',
        'Màng viên đặt': 'MV',
        'Tem chính': 'E',
        'Tem phụ': 'E',
        'Toa': 'T',
        'Tuýp': 'T',
        'Túi': 'TU',
} 
@login_required (login_url='/login/')
def plindex(request):
    return render(request, 'marquette/phulieu/index.html')

@login_required (login_url='/login/')
def plcreate(request):
    if request.method == "POST":
        thongtin = NewPhulieuForm(request.POST)
        if thongtin.is_valid():
            sp = thongtin.cleaned_data["sp"]
            mabfomoi = thongtin.cleaned_data["mabfomoi"]
            loai = thongtin.cleaned_data["loai"]
            trangthaihoso = thongtin.cleaned_data["trangthaihoso"]
            dauma = code[loai] + "1"
            newphulieu = phulieu(mabfomoi=mabfomoi,mabfocu='',loai=loai,lanbanhanh=1,dauma=dauma,trangthaihoso=trangthaihoso)
            newphulieu.save()
            return HttpResponseRedirect(reverse('ghepmapl', kwargs={'sdk': sp[0], 'pk':newphulieu.pk}))
    return render(request, 'marquette/phulieu/plcreate.html',{
        "form": NewPhulieuForm,
    })

@login_required (login_url='/login/')
def plinput(request):       
    if request.method == "POST":
        thongtin = PhulieuForm(request.POST)
        if thongtin.is_valid():
            sp = thongtin.cleaned_data["sp"]
            mabfomoi = thongtin.cleaned_data["mabfomoi"]
            lanbanhanh = thongtin.cleaned_data["lanbanhanh"]
            trangthaihoso = thongtin.cleaned_data["trangthaihoso"]
            pl = phulieu.objects.filter(mabfomoi=mabfomoi[0]).first()
            mabfo = pl.mabfomoi
            #Check lanbanhanh
            max = phulieu.objects.filter(mabfomoi=mabfo).aggregate(Max('lanbanhanh'))['lanbanhanh__max']
            if lanbanhanh <= max:
                return render(request, 'marquette/phulieu/plinput.html',{
                    "form": PhulieuForm,
                    "notice": "Note: Lần ban hành gần nhất là lần " + str(max),
                })
            else:
                #Create dauma
                loai = pl.loai
                dauma = code[loai] + str(lanbanhanh)
                newbanhanh = phulieu(mabfomoi=mabfo,loai=loai,lanbanhanh=lanbanhanh,dauma=dauma,trangthaihoso=trangthaihoso)
                newbanhanh.save()
                return HttpResponseRedirect(reverse('ghepmapl', kwargs={'sdk': sp[0], 'pk':newbanhanh.pk}))
    return render(request, 'marquette/phulieu/plinput.html',{
        "form": PhulieuForm,
    })

@login_required (login_url='/login/')
def ghepmapl(request,sdk,pk):
    class GhepmaForm(forms.Form):
        sanpham = forms.ModelMultipleChoiceField(label="Sản phẩm áp dụng",
                                                queryset=sanpham.objects.filter(sodangky=sdk),
                                                widget=forms.CheckboxSelectMultiple,)
    if request.method == "POST":
        thongtin = GhepmaForm(request.POST)
        bosung = SearchSPForm(request.POST)
        if thongtin.is_valid():
            splist = thongtin.cleaned_data["sanpham"]
            pl = phulieu.objects.get(pk=pk)
            for sp in splist:
                sudung.objects.create(sp=sp,pl=pl,use=True)
            return render(request, 'marquette/phulieu/ghepmapl2.html',{
                "form": SearchSPForm,
                "pk": pk,
            })
        if bosung.is_valid():
            sdk = bosung.cleaned_data["sp"]
            return HttpResponseRedirect(reverse('ghepmapl', kwargs={'sdk': sdk[0], 'pk': pk}))
    return render(request, 'marquette/phulieu/ghepmapl1.html',{
        "form": GhepmaForm,
    })

@login_required (login_url='/login/')
def marquettecreate(request,pk,sp):
    pl = phulieu.objects.get(pk=pk)
    #Info for marquette
    dauma = pl.dauma
    year = datetime.date.today().strftime("%y")
    date = datetime.date.today().strftime("%d%m%y")
    bfo = pl.mabfomoi
    #Info for ncc
    listncc = marquette.objects.filter(phulieu__mabfomoi=bfo).values('manhacc__ten').distinct()
    if request.method == "POST":
        thongtin = MarquetteForm(request.POST)
        if thongtin.is_valid():
            ncclist = thongtin.cleaned_data["nhacc"]
            for ncc in ncclist:
                #Create marquette
                manhain = ncc.ma
                ma = dauma+"-"+year+"-"+date+"-"+bfo+"-"+manhain
                new = marquette(phulieu=pl,marquette=ma,manhacc=ncc)
                new.save()
            if sp == 'x':
                return HttpResponseRedirect(reverse('marquetteview', args=(pk, )))
            elif sp[0].isdigit():
                return HttpResponseRedirect(reverse('waitcreatepl', kwargs={'pk': sp, }))
            else:
                return HttpResponseRedirect(reverse('spcreatepl', kwargs={'pk': sp, }))
    return render(request, 'marquette/phulieu/marquettecreate.html',{
        "form": MarquetteForm,
        "listncc": listncc,
    })

@login_required (login_url='/login/')
def marquetteadd(request):
    if request.method == "POST":
        thongtinpl = SearchPLForm(request.POST)
        thongtinma = MarquetteForm(request.POST)
        if thongtinpl.is_valid() and thongtinma.is_valid():
            mapl = thongtinpl.cleaned_data["mabfomoi"]
            lbh = thongtinpl.cleaned_data["lanbanhanh"]
            ncclist = thongtinma.cleaned_data["nhacc"]
            #Info for marquette
            pl = phulieu.objects.get(mabfomoi=mapl[0],lanbanhanh=lbh)
            dauma = pl.dauma
            year = datetime.date.today().strftime("%y")
            date = datetime.date.today().strftime("%d%m%y")
            bfo = pl.mabfomoi
            for ncc in ncclist:
                #Create marquette
                manhain = ncc.ma
                ma = dauma+"-"+year+"-"+date+"-"+bfo+"-"+manhain
                new = marquette(phulieu=pl,marquette=ma,manhacc=ncc)
                new.save()
            return HttpResponseRedirect(reverse('marquetteview', args=(pl.pk, )))
    return render(request, 'marquette/phulieu/marquetteadd.html',{
        "form": SearchPLForm,
        "maform": MarquetteForm,
    })

@method_decorator(login_required, name='dispatch')
class MarquetteListView(ListView):
    model = marquette
    template_name = 'marquette/phulieu/marquetteview.html'
    context_object_name = 'marquettelist'
    def get_queryset(self):
        pl = phulieu.objects.get(pk=self.kwargs['pk'])
        return marquette.objects.filter(phulieu=pl).order_by('marquette')

@method_decorator(login_required, name='dispatch')
class StockListView(ListView):
    model = sudung
    template_name = 'marquette/phulieu/stockview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp = sanpham.objects.get(mabfo=self.kwargs['ma'])
        context['sp'] = sp
        context['list'] = sudung.objects.filter(sp=sp,use=True)
        return context

@login_required (login_url='/login/')
def stockupdate(request,pk,ma):
    stock = request.GET.get('stock')
    pl = phulieu.objects.get(pk=pk)
    pl.soluong = stock
    pl.save()
    return HttpResponseRedirect(reverse('stockview', kwargs={'ma': ma, })) 

@method_decorator(login_required, name='dispatch')
class RecallListView(ListView):
    model = sudung
    template_name = 'marquette/phulieu/recallview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp = sanpham.objects.get(mabfo=self.kwargs['ma'])
        context['sp'] = sp
        context['list'] = sudung.objects.filter(sp=sp,use=False)
        return context

@login_required (login_url='/login/')
def recall(request,pl,sp):
    spham = sanpham.objects.get(mabfo=sp)
    plieu = phulieu.objects.get(pk=pl)
    recall = sudung.objects.get(sp=spham,pl=plieu)
    recall.use = True
    recall.save()
    return HttpResponseRedirect(reverse('recallview', kwargs={'ma': sp, })) 

@method_decorator(login_required, name='dispatch')
class NCCCreateView(CreateView):
    model = nhacungcap
    fields = ['ten','ma']
    template_name = 'marquette/phulieu/ncccreate.html'
    success_url ="/pl"

def exportghepma(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ghepma.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Ghepma')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Mã BFO sản phẩm', 'Tên sản phẩm','Quy cách','Mã BFO phụ liệu (Fast)','Mã BFO phụ liệu cũ','Loại phụ liệu','Lần ban hành']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = sudung.objects.all().values_list('sp__mabfo','sp__sodangky__tensanpham','sp__quycach','pl__mabfomoi','pl__mabfocu','pl__loai','pl__dauma')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def exportmarquette(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="marquette.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Marquette')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Mã BFO phụ liệu (Fast)','Mã BFO phụ liệu cũ','Loại phụ liệu','Lần ban hành','Mã marquette']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = marquette.objects.all().values_list('phulieu__mabfomoi','phulieu__mabfocu','phulieu__loai','phulieu__lanbanhanh','marquette')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# Model thaydoi
@login_required (login_url='/login/')
def tdindex(request):
    return render(request, 'marquette/thaydoi/index.html')

@method_decorator(login_required, name='dispatch')
class TBCreateView(CreateView):
    model = thongbao
    form_class = ThongbaoForm
    template_name = 'marquette/thaydoi/tbcreate.html'
    def get_initial(self):
        initial = super(TBCreateView,self).get_initial()
        initial['sodangky'] = hoso.objects.get(sodangky=self.kwargs['sdk'])
        return initial
    def form_valid(self, form):
        self.object = form.save()
        pk = self.object.pk
        sdk = self.kwargs['sdk']
        return HttpResponseRedirect(reverse('tdcreate', kwargs={'pk': pk, 'sdk':sdk, }))

@login_required (login_url='/login/')
def tdcreate(request,pk,sdk):
    class SPForm(forms.Form):
        sp = forms.ModelMultipleChoiceField(label='SẢN PHẨM ÁP DỤNG',
                                            queryset=sanpham.objects.filter(sodangky=sdk),
                                            widget=forms.CheckboxSelectMultiple,
                                            )
    if request.method == "POST":
        pl = PLthaydoiForm(request.POST)
        splist = SPForm(request.POST)
        if pl.is_valid() and splist.is_valid():
            mabfomoi = pl.cleaned_data["mabfomoi"]
            lbhtruoc = pl.cleaned_data["lbhtruoc"]
            lbhsau = pl.cleaned_data["lbhsau"]
            splist = splist.cleaned_data["sp"]
            pltruoc = phulieu.objects.get(mabfomoi=mabfomoi[0],lanbanhanh=lbhtruoc)
            plsau = phulieu.objects.get(mabfomoi=mabfomoi[0],lanbanhanh=lbhsau)
            tbao = thongbao.objects.get(pk=pk)
            #Input sosanh model
            matruoc = marquette.objects.filter(phulieu=pltruoc).order_by('manhacc').first()
            masau = marquette.objects.filter(phulieu=plsau).order_by('manhacc').first()
            loai = pltruoc.loai
            newss = sosanh(thongbao=tbao,loai=loai,noidung="Mã nhà in",matruoc=matruoc.marquette,masau=masau.marquette)
            newss.save()
            #Input thaydoi model
            for sp in splist:
                newtd = thaydoi(thongbao=tbao,sanpham=sp,pltruoc=pltruoc,plsau=plsau)
                newtd.save()
                newxl = xuly(thaydoi=newtd)
                newxl.save()
            return render(request, 'marquette/thaydoi/tdcreate.html', {
                    "pllist": sosanh.objects.filter(thongbao=tbao).values('loai').distinct(),
                    "spform": SPForm,
                    "form": PLthaydoiForm,
                    "pk": pk,
            })
    return render(request, 'marquette/thaydoi/tdcreate.html', {
            "spform": SPForm,
            "form": PLthaydoiForm,
            "pk": pk,
    })

@method_decorator(login_required, name='dispatch')
class SosanhListView(ListView):
    model = sosanh
    template_name = 'marquette/thaydoi/ssview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tbao = thongbao.objects.get(pk=self.kwargs['pk'])
        context['thongbao'] = tbao
        context['list'] = sosanh.objects.filter(thongbao=tbao)
        return context

@method_decorator(login_required, name='dispatch')
class SosanhUpdateView(UpdateView):
    model = sosanh
    form_class = SosanhForm
    template_name = 'marquette/thaydoi/ssupdate.html'
    def get_success_url(self):
        pk = self.kwargs['tb']
        return reverse('sosanhview', kwargs={"pk": pk,})

@method_decorator(login_required, name='dispatch')
class SSTextCreateView(CreateView):
    model = sosanhtext
    form_class = SSTextForm
    template_name = 'marquette/thaydoi/sstextcreate.html'
    def get_initial(self):
        initial = super(SSTextCreateView,self).get_initial()
        initial['sosanh'] = sosanh.objects.get(pk=self.kwargs['pk'])
        return initial
    def get_context_data(self):
        context = super().get_context_data()
        ss = sosanh.objects.get(pk=self.kwargs['pk'])
        context['ndlist'] = sosanhtext.objects.filter(sosanh=ss)
        return context
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('sstextcreate', kwargs={"pk": pk, })

@login_required (login_url='/login/')
def SSImageCreateView(request,pk):
    ss = sosanh.objects.get(pk=pk)
    ndlist = sosanhimage.objects.filter(sosanh=ss)
    if request.method == "POST":
        thongtin = SSImageForm(request.POST, request.FILES)
        if thongtin.is_valid():
            noidung = thongtin.cleaned_data["noidung"]
            anhtruoc = thongtin.cleaned_data["anhtruoc"]
            anhsau = thongtin.cleaned_data["anhsau"]
            ssimg = sosanhimage(sosanh=ss,noidung=noidung,anhtruoc=anhtruoc,anhsau=anhsau)
            ssimg.save()
            return HttpResponseRedirect(reverse('ssimagecreate', kwargs={"pk": pk, }))
    return render(request, 'marquette/thaydoi/ssimagecreate.html', {
            "form": SSImageForm,
            "ndlist": ndlist,
    })

@method_decorator(login_required, name='dispatch')
class TBListDTView(ListView):
    model = thongbao
    queryset = thongbao.objects.all()
    context_object_name = 'tblist'
    template_name = 'marquette/thaydoi/tbviewdt.html'

@method_decorator(login_required, name='dispatch')
class TBListPLView(ListView):
    model = thongbao
    queryset = thongbao.objects.all()
    context_object_name = 'tblist'
    template_name = 'marquette/thaydoi/tbviewpl.html'

@method_decorator(login_required, name='dispatch')
class TBListDLView(ListView):
    model = thongbao
    queryset = thongbao.objects.all()
    context_object_name = 'tblist'
    template_name = 'marquette/thaydoi/tbviewdl.html'

@method_decorator(login_required, name='dispatch')
class TBListSMView(ListView):
    model = thongbao
    queryset = thongbao.objects.all()
    context_object_name = 'tblist'
    template_name = 'marquette/thaydoi/tbviewsm.html'

@login_required (login_url='/login/')
def mahangdat(request,pk):
    listpl = []
    tbao = thongbao.objects.get(pk=pk)
    listtd = thaydoi.objects.filter(thongbao=tbao)
    for td in listtd:
        pl = td.pltruoc
        if pl not in listpl:
            listpl.append(pl)
    class MadatForm(forms.Form):
        ma = forms.ModelMultipleChoiceField(label='Mã hàng đã đặt',
                                            queryset=marquette.objects.filter(phulieu__in=listpl),
                                            widget=forms.CheckboxSelectMultiple,
                                            )
    if request.method == "POST":
        listma = MadatForm(request.POST)
        if listma.is_valid():
            listma = listma.cleaned_data["ma"]
            for ma in listma:
                marquettedat.objects.create(thongbao=tbao,marquettedat=ma)
            return HttpResponseRedirect(reverse('soluongdat', kwargs={'pk': pk, }))
    return render(request, 'marquette/thaydoi/marquettedat.html', {
            "form": MadatForm,
    })

@login_required (login_url='/login/')
def soluongdat(request,pk):
    tbao = thongbao.objects.get(pk=pk)
    listma = marquettedat.objects.filter(thongbao=tbao)
    return render(request, 'marquette/thaydoi/soluongdat.html', {
            "listma": listma,
            "tb": pk,
    })

@login_required (login_url='/login/')
def tonkhoupdate(request,pk,tb):
    tonkho = request.GET.get('tonkho')
    ma = marquettedat.objects.get(pk=pk)
    ma.tonkho = tonkho
    ma.save()
    return HttpResponseRedirect(reverse('soluongdat', kwargs={'pk': tb, }))

@login_required (login_url='/login/')
def dathangupdate(request,pk,tb):
    dathang = request.GET.get('dathang')
    ma = marquettedat.objects.get(pk=pk)
    ma.dathang = dathang
    ma.save()
    return HttpResponseRedirect(reverse('soluongdat', kwargs={'pk': tb, })) 

@register.filter
def filterss(qs, ss):
    return qs.filter(sosanh=ss)

@login_required (login_url='/login/')
def xuatfile(request,pk):
    tbao = thongbao.objects.get(pk=pk)
    tdoi = thaydoi.objects.filter(thongbao=tbao).values('sanpham__quycach').distinct()
    ssanh = sosanh.objects.filter(thongbao=tbao)
    madat = marquettedat.objects.filter(thongbao=tbao)
    today = datetime.datetime.today()
    html_template = render_to_string('marquette/thaydoi/pdf.html', {
            "tbao": tbao,
            "tdoi": tdoi,
            "ssanh": ssanh,
            "madat": madat,
            "today": today,
    })
    pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri('')).write_pdf(
       stylesheets=[CSS(settings.STATIC_ROOT +  '/marquette/pdf.css')])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="TBTD.pdf"'
    ##Download the pdf
    #response['Content-Disposition'] = 'attachment; filename="TBTD.pdf"'
    return response

def mailthongbao(request,pk):
    if request.method == "POST":
        thongtin = EmailForm(request.POST,request.FILES)
        if thongtin.is_valid():
            notice = thongtin.cleaned_data['message']
            huongxl = thongtin.cleaned_data['huongxutri']
            noidungtd = thongtin.cleaned_data['noidungthaydoi']
            link = thongtin.cleaned_data['link']
            attach = request.FILES['attach']
            tbao = thongbao.objects.get(pk=pk)
            tbao.link = link
            tbao.save()
            subject = ('[KyThuatVien][TBTĐ],%s,%s' %(tbao.sodangky.tensanpham, tbao.sodangky.sodangky))
            message = get_template('marquette/thaydoi/mailcontent.html').render({
                        'tbao': tbao,
                        'notice': notice,
                        'huongxl': huongxl,
                        'noidungtd': noidungtd,
                        'link': link,
            })
            mail = EmailMessage(subject,
                                message,
                                #'Thông Báo Thay ĐổI',
                                'ha.tranphuong22@gmail.com',
                                ['tranphuongha1234@gmail.com'],
                                reply_to=['tranphuongha1234@gmail.com'],)
            mail.attach(attach.name, attach.read(), attach.content_type)
            mail.content_subtype = "html"
            mail.send()
            return HttpResponse('Mail successfully sent')
    return render(request, 'marquette/thaydoi/tbmail.html',{
        "form": EmailForm,
    })

@method_decorator(login_required, name='dispatch')
class TDListView(ListView):
    model = thaydoi
    template_name = 'marquette/thaydoi/tdview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp = sanpham.objects.get(mabfo=self.kwargs['ma'])
        context['sp'] = sp
        context['list'] = xuly.objects.filter(thaydoi__sanpham=sp).exclude(trangthai='Hoàn thành') #Thêm filter chưa hoàn thành
        return context

@method_decorator(login_required, name='dispatch')
class SolutionUpdateView(UpdateView):
    model = xuly
    form_class = SolutionUpdateForm
    template_name = 'marquette/thaydoi/solutionupdate.html'
    def get_initial(self):
        initial = super(SolutionUpdateView,self).get_initial()
        initial['trangthai'] = "Chưa hoàn thành"
        return initial
    def get_success_url(self):
        ma = self.kwargs['ma']
        return reverse('tdview', kwargs={"ma": ma, })
    def form_valid(self, form):
        self.object = form.save()
        tdoi = thaydoi.objects.get(pk=self.kwargs['pk'])
        if tongket.objects.filter(thaydoi=tdoi).exists():
            tk = tongket.objects.get(thaydoi=tdoi)
            tk.huongxuly = xuly.objects.get(thaydoi=tdoi)
            tk.save(update_fields=['huongxuly'])
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class StatusUpdateView(UpdateView):
    model = xuly
    form_class = StatusUpdateForm
    template_name = 'marquette/thaydoi/statusupdate.html'
    def get_initial(self):
        initial = super(StatusUpdateView,self).get_initial()
        initial['trangthai'] = "Hoàn thành"
        return initial
    def get_success_url(self):
        ma = self.kwargs['ma']
        return reverse('tdview', kwargs={"ma": ma, })
    def form_valid(self, form):
        self.object = form.save()
        sp = sanpham.objects.get(mabfo=self.kwargs['ma'])
        pl = thaydoi.objects.get(pk=self.kwargs['pk'])
        recall = sudung.objects.get(sp=sp,pl=pl.pltruoc)
        recall.use = False
        recall.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class HTListView(ListView):
    model = thaydoi
    template_name = 'marquette/thaydoi/htview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp = sanpham.objects.get(mabfo=self.kwargs['ma'])
        context['sp'] = sp
        context['list'] = xuly.objects.filter(thaydoi__sanpham=sp, trangthai='Hoàn thành')
        return context

def exportthaydoi(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="thaydoi.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Thaydoi')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Link bản mềm','Mã BFO sản phẩm','Mã BFO phụ liệu (Fast)','Mã BFO phụ liệu (cũ)','Lần ban hành cũ','Lần ban hành mới','Hướng xử lý','Chốt hướng xử lý','Thời hạn','Lệnh sản xuất','Ngày sản xuất','Hạn sử dụng','Kế hoạch sản xuất','Trạng thái','Ngày chốt','Chốt hủy']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = xuly.objects.all().values_list('thaydoi__thongbao__link','thaydoi__sanpham__mabfo','thaydoi__pltruoc__mabfomoi','thaydoi__pltruoc__mabfocu','thaydoi__pltruoc__lanbanhanh','thaydoi__plsau__lanbanhanh','xuly','chotxuly','thoihan','lenhsx','ngaysx','hansd','khsx','trangthai','ngaychot','chothuy')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# Model tongket
@login_required (login_url='/login/')
def tongkettuan(request):
    if request.method == 'POST':
        thongtin = SearchBFOForm(request.POST)
        if thongtin.is_valid():
            mabfo = thongtin.cleaned_data["mabfo"]
            sp = sanpham.objects.get(mabfo=mabfo[0])
            #Check duplicate any sanpham
            if not tongket.objects.filter(sanpham=sp).exists():
                pllist = sudung.objects.filter(sp=sp,use=True)
                #sanpham has change
                if thaydoi.objects.filter(sanpham=sp).exists():
                    for pl in pllist:
                        #phulieu has change
                        if thaydoi.objects.filter(pltruoc=pl.pl).exists():
                            try:
                                tdoi = thaydoi.objects.get(sanpham=sp,pltruoc=pl.pl)
                                hxuly = xuly.objects.get(pk=tdoi.pk)
                            except thaydoi.DoesNotExist:
                                tdoi = None
                                hxuly = None
                            tk = tongket(sanpham=sp,dauma=pl.pl,trangthai="Mã cũ",thaydoi=tdoi,huongxuly=hxuly)
                            tk.save()
                        #phulieu doesn't have change
                        else:
                            tk = tongket(sanpham=sp,dauma=pl.pl,trangthai="Mã mới")
                            tk.save()
                #sanpham doesn't have change
                else:
                    for pl in pllist:
                        tk = tongket(sanpham=sp,dauma=pl.pl,trangthai="Mã mới")
                        tk.save()
        return render(request, 'marquette/tongket.html', {
            "form": thongtin,
            "listtk": tongket.objects.all().order_by('sanpham','dauma__loai'),
        })
    return render(request, 'marquette/tongket.html', {
        "form": SearchBFOForm(),
        "listtk": tongket.objects.all().order_by('sanpham','dauma__loai'),
    })

@login_required (login_url='/login/')
def stocktkupdate(request,pk,ma):
    stock = request.GET.get('stock')
    pl = phulieu.objects.get(pk=pk)
    pl.soluong = stock
    pl.save()
    return HttpResponseRedirect(reverse('tongket'))

@method_decorator(login_required, name='dispatch')
class TKUpdateView(UpdateView):
    model = tongket
    form_class = ChotSDForm
    template_name = 'marquette/tkupdate.html'
    success_url = "/tongket"

@login_required (login_url='/login/')
def tongketclear(request): 
    tongket.objects.all().delete()
    return HttpResponseRedirect(reverse('tongket')) 

def mailkhsx(request):
    weeknum = datetime.date.today().isocalendar()[1],
    subject = ('Chốt phụ liệu cho KHSX tuần %d' % weeknum)
    message = get_template('marquette/khsx.html').render({
        'list': tongket.objects.all(),
        })
    email = EmailMessage(subject,
                        message,
                        'ha.tranphuong22@gmail.com',
                        ['tranphuongha1234@gmail.com'],)
    email.content_subtype = "html"
    email.send()
    return HttpResponse('Mail successfully sent')

# def mailthongbao(request,pk):
#     tbao = thongbao.objects.get(pk=pk)
#     tdoi = thaydoi.objects.filter(thongbao=tbao).values('sanpham__quycach').distinct()
#     ssanh = sosanh.objects.filter(thongbao=tbao)
#     madat = marquettedat.objects.filter(thongbao=tbao)
#     today = datetime.datetime.today()
#     #Mail content
#     subject = ('Thông báo thay đổi cho SĐK %s' % tbao.sodangky.sodangky)
#     message = render_to_string('marquette/thaydoi/pdf.html')  #Đổi lại sau
#     email = EmailMessage(subject,
#                         message,
#                         'ha.tranphuong22@gmail.com',
#                         ['tranphuongha1234@gmail.com'],)
#     #Generation PDF
#     html_template = render_to_string('marquette/thaydoi/pdf.html',{
#             "tbao": tbao,
#             "tdoi": tdoi,
#             "ssanh": ssanh,
#             "madat": madat,
#             "today": today,
#     })
#     out = BytesIO()
#     HTML(string=html_template, base_url=request.build_absolute_uri('')).write_pdf(out,
#        stylesheets=[CSS(settings.STATIC_ROOT +  '/marquette/pdf.css')])
#     #Attach PDF
#     email.attach('TBTD_SĐK {}.pdf'.format(tbao.sodangky.sodangky),
#                  out.getvalue(),
#                 'application/pdf')
#     #Attach file
#     file = ssanh[0].anhtruoc #Get the FileField of model
#     file.open()
#     email.attach('Ảnh trước.jpg', 
#                 file.read(), 
#                 mimetypes.guess_type(file.name)[0])
#     file.close()
#     #Send mail
#     email.content_subtype = "html"
#     email.send()
#     return HttpResponse('Mail successfully sent')