# src/forms.py
from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField, 
    IntegerField, 
    SelectField, 
    StringField,  # Asegúrate de importar StringField
    DateField, 
    FileField, 
    SubmitField,
    BooleanField,

)
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError, Length
from flask_wtf.file import FileAllowed
from datetime import datetime
from datetime import date



def file_size_limit(max_size):
    """Validador personalizado para limitar el tamaño del archivo."""
    def _file_size_limit(form, field):
        if field.data:
            field.data.stream.seek(0, 2)  # Mover al final del archivo
            file_size = field.data.stream.tell()
            field.data.stream.seek(0)  # Volver al inicio del archivo
            if file_size > max_size:
                raise ValidationError(f"El archivo no puede exceder los {max_size / (1024 * 1024)} MB.")
    return _file_size_limit

class TutoriaForm(FlaskForm):
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    anio = IntegerField('Año', validators=[
        DataRequired(),
        NumberRange(min=2020, max=datetime.now().year, message=f"El año no puede ser mayor a {datetime.now().year}.")
    ])
    archivo = FileField('Adjuntar Archivo (Imagen o PDF)', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
        file_size_limit(10 * 1024 * 1024)  # 10 MB
    ])
    submit = SubmitField('Guardar')

class SoftwareEspecializadoForm(FlaskForm):
    nombre_curso = StringField(
        'Nombre del Curso', 
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    modalidad = SelectField(
        'Modalidad', 
        choices=[
            ('', 'Seleccione una opción'),
            ('Presencial', 'Presencial'), 
            ('Virtual', 'Virtual')
        ], 
        validators=[
            DataRequired(message='Debe seleccionar una modalidad.')
        ]
    )
    horas = IntegerField(
        'Horas', 
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=1, max=1000, message="Debe ser entre 1 y 1000 horas.")
        ]
    )
    institucion = SelectField(
        'Tipo de Institución', 
        choices=[
            ('', 'Seleccione una opción'),
            ('Universidad', 'Universidad'), 
            ('Instituto', 'Instituto'), 
            ('Otra', 'Otra')
        ], 
        validators=[
            DataRequired(message='Debe seleccionar un tipo de institución.')
        ]
    )
    nombre_institucion = StringField(
        'Nombre de la Institución',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    top_1000 = BooleanField(
        '¿Fue en una de las 1000 mejores universidades del mundo?',
        default=False
    )
    fecha = DateField(
        'Fecha', 
        format='%Y-%m-%d', 
        validators=[
            DataRequired(message='Este campo es obligatorio.')
        ]
    )
    archivo = FileField(
        'Adjuntar Archivo (Imagen o PDF)', 
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')
    
class ReconocimientosForm(FlaskForm):
    tipo = SelectField(
        'Tipo de Reconocimiento',
        choices=[
            ('', 'Seleccione una opción'),
            ('Docente Visitante', 'Docente Visitante'),
            ('Premio Internacional', 'Premio Internacional'),
            ('Premio Nacional', 'Premio Nacional'),
            ('Miembro de Sociedad Científica Internacional', 'Miembro de Sociedad Científica Internacional'),
            ('Miembro de Sociedad Científica Nacional', 'Miembro de Sociedad Científica Nacional'),
            ('Distinción Académica', 'Distinción Académica'),
            ('Resolución Rectoral', 'Resolución Rectoral'),
            ('Resolución Decanal', 'Resolución Decanal')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de reconocimiento.')]
    )
    tipo_institucion = SelectField(
        'Tipo de Institución',
        choices=[
            ('', 'Seleccione una opción'),
            ('Universidad', 'Universidad'),
            ('Sociedad Científica', 'Sociedad Científica'),
            ('Organización Internacional', 'Organización Internacional'),
            ('Organización Nacional', 'Organización Nacional'),
            ('Gobierno', 'Gobierno'),
            ('Empresa Privada', 'Empresa Privada'),
            ('Otra', 'Otra')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de institución.')]
    )
    descripcion = StringField(
        'Descripción',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    institucion = StringField(
        'Nombre de la Institución',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    fecha = DateField(
        'Fecha',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Este campo es obligatorio.')
        ]
    )
    archivo = FileField(
        'Adjuntar Archivo (Imagen o PDF)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')


    # Validadores personalizados
    def validate_top_1000(self, field):
        if field.data:
            if self.institucion.data != 'Universidad':
                raise ValidationError('Solo las universidades pueden estar en el top 1000.')

    def validate_nombre_institucion(self, field):
        if self.institucion.data == 'Otra' and not field.data.strip():
            raise ValidationError('Debe ingresar el nombre de la institución.')
        if len(field.data.strip()) > 100:
            raise ValidationError('El nombre de la institución debe tener máximo 100 caracteres.')

    def validate_fecha(self, field):
        if field.data > date.today():
            raise ValidationError('La fecha no puede ser en el futuro.')