
import mongoengine as me
import re

def solo_letras(value):
    if not re.fullmatch(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+', value):
        raise me.ValidationError("El nombre solo debe contener letras y espacios.")

class Producto(me.Document):
    nombre = me.StringField(
        required=True,
        max_length=100,
        validation=solo_letras
    )
    descripcion = me.StringField(
        required=True,
        min_length=5,
        max_length=10
    )
    stock = me.IntField(
        required=True,
        min_value=1
    )

    def __str__(self):
        return self.nombre

    meta = {
        'collection': 'productos'
    }
