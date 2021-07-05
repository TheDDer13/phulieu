from import_export import fields, resources
from .models import hoso, sanpham, nhacungcap, phulieu, marquette, choghepmabfo, sudung, thongbao, thaydoi, sosanh, sosanhtext, sosanhimage, marquettedat, xuly

class hosoResource(resources.ModelResource):
    class Meta:
        model = hoso
        import_id_fields = ('sodangky', )
        fields = ('sodangky','ngaycap','ngayhethan','sotucongbo','tensanpham','hansanpham','hoatchat','hamluong','dangbaoche','tieuchuan','nhadk','nhapp','quycach','phanloai')

class sanphamResource(resources.ModelResource):
    class Meta:
        model = sanpham
        import_id_fields = ('mabfo', )
        fields = ('mabfo','sodangky','quycach','vitri')

class nhacungcapResource(resources.ModelResource):
    class Meta:
        model = nhacungcap
        import_id_fields = ('ma', )
        fields = ('ma','ten')

class phulieuResource(resources.ModelResource):
    class Meta:
        model = phulieu
        import_id_fields = ('mabfomoi', )
        fields = ('mabfomoi','mabfocu','loai','lanbanhanh','ngaybanhanh','dauma','trangthaihoso','soluong','sudung')

class marquetteResource(resources.ModelResource):
    class Meta:
        model = marquette
        import_id_fields = ('phulieu','mancc','marquette' )
        fields = ('phulieu','mancc','marquette' )

class sudungResource(resources.ModelResource):
    class Meta:
        model = sudung
        import_id_fields = ('masp','mapl', )
        fields = ('masp','mapl')

class choghepmabfoResource(resources.ModelResource):
    class Meta:
        model = choghepmabfo
        import_id_fields = ('sodangky','quycach','vitri','phulieu', )
        fields = ('sodangky','quycach','vitri',)

class thongbaoResource(resources.ModelResource):
    class Meta:
        model = thongbao
        import_id_fields = ('congvan','ngayhethancv','ngayapdung','sodangky','loai','uutien','lydo','madadat')
        fields = ('congvan','ngayhethancv','ngayapdung','sodangky','loai','uutien','lydo','madadat')

class thaydoiResource(resources.ModelResource):
    class Meta:
        model = thaydoi
        import_id_fields = ('thongbao','sanpham','pltruoc','plsau')
        fields = ('thongbao','sanpham','pltruoc','plsau')

class sosanhResource(resources.ModelResource):
    class Meta:
        model = sosanh
        import_id_fields = ('thongbao','loai','noidung','matruoc','masau')
        fields = ('thongbao','loai','noidung','matruoc','masau')

class sosanhtextResource(resources.ModelResource):
    class Meta:
        model = sosanhtext
        import_id_fields = ('sosanh','noidung','chutruoc','chusau')
        fields = ('sosanh','noidung','chutruoc','chusau')

class sosanhimageResource(resources.ModelResource):
    class Meta:
        model = sosanhimage
        import_id_fields = ('sosanh','noidung','anhtruoc','anhsau')
        fields = ('sosanh','noidung','anhtruoc','anhsau')

class marquettedatResource(resources.ModelResource):
    class Meta:
        model = marquettedat
        import_id_fields = ('thongbao','marquettedat','tonkho','dathang')
        fields = ('thongbao','marquettedat','tonkho','dathang')

class xulyResource(resources.ModelResource):
    class Meta:
        model = xuly
        import_id_fields = ('sodangky','quycach','vitri','phulieu', )
        fields = ('thaydoi','xuly','chotxuly','thoihan','lenhsx','ngaysx','hansd','khsx','trangthai','ngaychot','chothuy')
