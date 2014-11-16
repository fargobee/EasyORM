import sys
sys.path.append('path\to\your\EasyORM')

from easyORM import Orm
    
class Teman(Orm):
    nama=["str",20,"not null"]
    alamat=["text",50,"null"]
    telpon=["str",15,"not null"]
    umur=["int",3,'null']
