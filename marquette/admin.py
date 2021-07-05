from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import hoso, sanpham, nhacungcap, phulieu, marquette, choghepmabfo, sudung, thongbao, thaydoi, sosanh, sosanhtext, sosanhimage, marquettedat, xuly
from .resources import hosoResource, sanphamResource, nhacungcapResource, phulieuResource, marquetteResource, sudungResource, choghepmabfoResource, thongbaoResource, thaydoiResource, sosanhResource, sosanhtextResource, sosanhimageResource, marquettedatResource, xulyResource

class hosoAdmin(ImportExportModelAdmin):
    resource_class = hosoResource

class sanphamAdmin(ImportExportModelAdmin):
    resource_class = sanphamResource

class nhacungcapAdmin(ImportExportModelAdmin):
    resource_class = nhacungcapResource

class phulieuAdmin(ImportExportModelAdmin):
    resource_class = phulieuResource

class marquetteAdmin(ImportExportModelAdmin):
    resource_class = marquetteResource

class sudungAdmin(ImportExportModelAdmin):
    resource_class = sudungResource

class choghepmabfoAdmin(ImportExportModelAdmin):
    resource_class = choghepmabfoResource

class thongbaoAdmin(ImportExportModelAdmin):
    resource_class = thongbaoResource

class thaydoiAdmin(ImportExportModelAdmin):
    resource_class = thaydoiResource

class sosanhAdmin(ImportExportModelAdmin):
    resource_class = sosanhResource

class sosanhtextAdmin(ImportExportModelAdmin):
    resource_class = sosanhtextResource

class sosanhimageAdmin(ImportExportModelAdmin):
    resource_class = sosanhimageResource

class marquettedatAdmin(ImportExportModelAdmin):
    resource_class = marquettedatResource

class xulyAdmin(ImportExportModelAdmin):
    resource_class = xulyResource

# Register your models here.
admin.site.register(hoso,hosoAdmin)
admin.site.register(sanpham,sanphamAdmin)
admin.site.register(nhacungcap,nhacungcapAdmin)
admin.site.register(phulieu,phulieuAdmin)
admin.site.register(marquette,marquetteAdmin)
admin.site.register(sudung,sudungAdmin)
admin.site.register(choghepmabfo,choghepmabfoAdmin)
admin.site.register(thongbao,thongbaoAdmin)
admin.site.register(thaydoi,thaydoiAdmin)
admin.site.register(marquettedat,marquettedatAdmin)
admin.site.register(sosanh,sosanhAdmin)
admin.site.register(sosanhtext,sosanhtextAdmin)
admin.site.register(sosanhimage,sosanhimageAdmin)
admin.site.register(xuly,xulyAdmin)