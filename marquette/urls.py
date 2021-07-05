from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import DocCreateView, DocDetailView, DocUpdateView, DocExpiredView, DocTCBView 
from .views import SPCreateView, PLCreateView, PLListView, MarquetteListView, StockListView 
from .views import RecallListView, NCCCreateView, WaitCreateView, WaitPLCreateView, WaitView
from .views import WaitListView, TBCreateView, SosanhListView, SosanhUpdateView, TDListView
from .views import TBListDTView, TBListPLView, TBListDLView, TBListSMView
from .views import SolutionUpdateView, StatusUpdateView, HTListView, TKUpdateView, SSTextCreateView
from .views import AutocompleteSDK, AutocompleteSP, AutocompletePL, AutocompleteBFO
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.index, name='mainindex'),
    path('sdk', views.sdkindex, name='sdkindex'),
    path('sdk/docinput', DocCreateView.as_view(), name='docinput'),
    path('sdk/docfind/<str:action>', views.docfind, name='docfind'),
    re_path(r'^autocompletesdk/$', AutocompleteSDK.as_view(), name='autocompletesdk'),
    path('sdk/docview/<path:pk>', DocDetailView.as_view(), name='docview'),
    path('sdk/docupdate/<path:pk>', DocUpdateView.as_view(), name='docupdate'),
    path('sdk/docexpired', DocExpiredView.as_view(), name='docexpired'),
    path('sdk/doctcb', DocTCBView.as_view(), name='doctcb'),
    path('sdk/doctucb', views.TCBcreate, name='tucbcreate'),
    path('sdk/export', views.exporthoso, name='exporthoso'),
    path('sp', views.spindex, name='spindex'),
    re_path(r'^autocompletebfo/$', AutocompleteBFO.as_view(), name='autocompletebfo'),
    path('sp/spfind/<str:action>', views.spfind, name='spfind'),
    re_path(r'^autocompletesp/$', AutocompleteSP.as_view(), name='autocompletesp'),
    path('sp/spcreate', SPCreateView.as_view(), name='spcreate'),
    path('sp/spcreatepl/<path:pk>', PLCreateView.as_view(), name='spcreatepl'),
    path('sp/spaddpl/<str:ma>', views.spaddpl, name='spaddpl'),
    path('sp/plview/<str:ma>', PLListView.as_view(), name='plview'),
    path('sp/sample/<int:pk>/<str:ma>', views.sample, name='sample'),
    path('sp/vitri/<str:ma>', views.vitriupdate, name='vitriupdate'),
    path('sp/waitcreate', WaitCreateView.as_view(), name='waitcreate'),
    path('sp/waitcreatepl/<path:pk>', WaitPLCreateView.as_view(), name='waitcreatepl'),
    path('sp/waitaddpl/<str:ma>', views.waitaddpl, name='waitaddpl'),
    path('sp/waitview/<str:ma>', WaitView.as_view(), name='waitview'),
    path('sp/waitlistview', WaitListView.as_view(), name='waitlistview'),
    path('sp/addbfo/<int:pk>', views.addbfo, name='addbfo'),
    path('sp/exportsanpham', views.exportsanpham, name='exportsanpham'),
    path('sp/exportwaiting', views.exportwaiting, name='exportwaiting'),
    path('pl', views.plindex, name='plindex'),
    re_path(r'^autocompletepl/$', AutocompletePL.as_view(), name='autocompletepl'),
    path('pl/plcreate', views.plcreate, name='plcreate'),
    path('pl/plinput', views.plinput, name='plinput'),
    path('pl/ghepma/<path:sdk>/<int:pk>', views.ghepmapl, name='ghepmapl'),
    path('pl/marquettecreate/<str:sp>/<int:pk>', views.marquettecreate, name='marquettecreate'),
    path('pl/marquetteview/<path:pk>', MarquetteListView.as_view(), name='marquetteview'),
    path('pl/marquetteadd', views.marquetteadd, name='marquetteadd'),
    path('pl/stockview/<str:ma>', StockListView.as_view(), name='stockview'),
    path('pl/stockupdate/<int:pk>/<str:ma>', views.stockupdate, name='stockupdate'),
    path('pl/recallview/<str:ma>', RecallListView.as_view(), name='recallview'),
    path('pl/recall/<int:pl>/<str:sp>', views.recall, name='recall'),
    path('pl/ncccreate', NCCCreateView.as_view(), name='ncccreate'),
    path('pl/exportghepma', views.exportghepma, name='exportghepma'),
    path('pl/exportmarquette', views.exportmarquette, name='exportmarquette'),
    path('td', views.tdindex, name='tdindex'),
    path('td/tbcreate/<path:sdk>', TBCreateView.as_view(), name='tbcreate'),
    path('td/tdcreate/<int:pk>/<path:sdk>', views.tdcreate, name='tdcreate'),
    path('td/sosanhview/<int:pk>', SosanhListView.as_view(), name='sosanhview'),
    path('td/sosanhupdate/<int:tb>/<int:pk>', SosanhUpdateView.as_view(), name='sosanhupdate'),
    path('td/sstextcreate/<int:pk>', SSTextCreateView.as_view(), name='sstextcreate'),
    path('td/ssimagecreate/<int:pk>', views.SSImageCreateView, name='ssimagecreate'),
    path('td/marquettedat/<int:pk>', views.mahangdat, name='marquettedat'),
    path('td/soluongdat/<int:pk>', views.soluongdat, name='soluongdat'),
    path('td/tonkhoupdate/<int:tb>/<int:pk>', views.tonkhoupdate, name='tonkhoupdate'),
    path('td/dathangupdate/<int:tb>/<int:pk>', views.dathangupdate, name='dathangupdate'),
    path('td/tbviewdt', TBListDTView.as_view(), name='tbviewdetail'),
    path('td/tbviewpl', TBListPLView.as_view(), name='tbviewphulieu'),
    path('td/tbviewdl', TBListDLView.as_view(), name='tbviewdownload'),
    path('td/tbviewsm', TBListSMView.as_view(), name='tbviewsendmail'),
    path('td/xuatfile/<int:pk>', views.xuatfile, name='xuatfile'),
    path('td/mailthongbao/<int:pk>', views.mailthongbao, name='mailthongbao'),
    path('td/tdview/<str:ma>', TDListView.as_view(), name='tdview'),
    path('td/solutionupdate/<str:ma>/<int:pk>', SolutionUpdateView.as_view(), name='solutionupdate'),
    path('td/statusupdate/<str:ma>/<int:pk>', StatusUpdateView.as_view(), name='statusupdate'),
    path('td/htview/<str:ma>', HTListView.as_view(), name='htview'),
    path('td/exportthaydoi', views.exportthaydoi, name='exportthaydoi'),
    path('tongket',views.tongkettuan, name='tongket'),
    path('stocktkupdate/<int:pk>/<str:ma>', views.stocktkupdate, name='stocktkupdate'),
    path('tkupdate/<int:pk>', TKUpdateView.as_view(), name='tkupdate'),
    path('tongketclear',views.tongketclear, name='tongketclear'),
    path('mailkhsx', views.mailkhsx, name='mailkhsx'),
    path('xuatfile', views.xuatfile, name='xuatfile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
