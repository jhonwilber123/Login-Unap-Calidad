# forms.py
from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    PasswordField,
    TextAreaField, 
    IntegerField, 
    SelectField, 
    StringField, 
    DateField, 
    FileField, 
    SubmitField,
    BooleanField,
)

from wtforms import StringField, DateField, SelectField, TelField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, Regexp, Email
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError, Length, EqualTo
from flask_wtf.file import FileAllowed, FileRequired
from datetime import datetime, date
import re
import os

def file_size_limit(max_size):
    """Validador personalizado para limitar el tamaño del archivo."""
    def _file_size_limit(form, field):
        if field.data:
            field.data.stream.seek(0, os.SEEK_END)  # Mover al final del archivo
            file_size = field.data.stream.tell()
            field.data.stream.seek(0)  # Volver al inicio del archivo
            if file_size > max_size:
                raise ValidationError(f"El archivo no puede exceder los {max_size / (1024 * 1024)} MB.")
    return _file_size_limit

class EditUserForm(FlaskForm):
    username = StringField('Nuevo Usuario', validators=[Optional()])
    password = PasswordField('Nueva Contraseña', validators=[Optional()])
    confirm_password = PasswordField('Confirma Contraseña', validators=[
        Optional(),
        EqualTo('password', message='Las contraseñas deben coincidir.')
    ])
    submit = SubmitField('Guardar Cambios')

class ParticipacionGestionUniversitariaForm(FlaskForm):
    cargo = StringField('Cargo', validators=[DataRequired(), Length(max=255)])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()], format='%Y-%m-%d')
    fecha_fin = DateField('Fecha de Fin', validators=[DataRequired()], format='%Y-%m-%d')
    curso_relevante = StringField('Curso Relevante', validators=[Optional(), Length(max=255)])
    adjuntar_plan = FileField('Adjuntar Plan', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo se permiten archivos PDF.')])
    adjuntar_informe = FileField('Adjuntar Informe', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo se permiten archivos PDF.')])
    adjuntar_curso = FileField('Adjuntar Certificado o Constancia de Curso Relevante', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo se permiten archivos PDF.')])
    submit = SubmitField('Guardar')


class EvaluacionDesempenoDocenteForm(FlaskForm):
    periodo_academico_evaluado = StringField(
        'Período Académico Evaluado',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    categoria_docente = StringField(
        'Categoría Docente',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    promedio_evaluacion_general = DecimalField(
        'Promedio de Evaluación General',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=0, max=100, message='El valor debe estar entre 0 y 100.')
        ],
        places=2
    )
    promedio_evaluacion_autoridades = DecimalField(
        'Promedio de Evaluación por Autoridades',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=0, max=100, message='El valor debe estar entre 0 y 100.')
        ],
        places=2
    )
    promedio_evaluacion_estudiantes = DecimalField(
        'Promedio de Evaluación por Estudiantes',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=0, max=100, message='El valor debe estar entre 0 y 100.')
        ],
        places=2
    )
    informes_evaluacion = FileField(
        'Adjuntar Resultados de Evaluación (PDF)',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')

class InformacionPersonalForm(FlaskForm):
    # Subida de Imágenes y Archivos
    foto_docente = FileField('Foto del Docente', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes.'),
        Optional()
    ])
    constancia_habilitacion = FileField('Constancia de Habilitación', validators=[
        FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
        Optional()
    ])
    
    # Información Personal
    apellido_paterno = StringField('Apellido Paterno', validators=[Optional(), Length(max=50)])
    apellido_materno = StringField('Apellido Materno', validators=[Optional(), Length(max=50)])
    nombres = StringField('Nombres', validators=[Optional(), Length(max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[Optional()], format='%Y-%m-%d')
    lugar_nacimiento_departamento = StringField('Departamento de Nacimiento', validators=[Optional(), Length(max=50)])
    lugar_nacimiento_provincia = StringField('Provincia de Nacimiento', validators=[Optional(), Length(max=50)])
    lugar_nacimiento_distrito = StringField('Distrito de Nacimiento', validators=[Optional(), Length(max=50)])
    dni = StringField('DNI', validators=[
        Optional(), 
        Regexp(r'^\d{8}$', message="El DNI debe tener 8 dígitos.")
    ])
    
    # Información Profesional
    colegio_profesional = StringField('Colegio Profesional', validators=[Optional(), Length(max=100)])
    numero_colegiatura = StringField('Número de Colegiatura', validators=[Optional(), Length(max=20)])
    codigo = StringField('Código UNAP', validators=[Optional(), Length(max=20)])
    condicion = SelectField(
        'Condición', 
        choices=[
            ('', 'Seleccione...'),
            ('Nombrado', 'Nombrado'),
            ('Contratado', 'Contratado')
        ], 
        validators=[Optional()]
    )
    categoria = SelectField(
        'Categoría', 
        choices=[
            ('', 'Seleccione...'),
            # Opciones para 'Nombrado'
            ('Principal', 'Principal'),
            ('Asociado', 'Asociado'),
            ('Auxiliar', 'Auxiliar'),
            # Opciones para 'Contratado'
            ('A1', 'A1'),
            ('B1', 'B1'),
            ('B2', 'B2'),
            ('B3', 'B3')
        ], 
        validators=[Optional()]
    )
    dedicacion = SelectField(
        'Dedicación', 
        choices=[
            ('', 'Seleccione...'),
            # Opción solo para 'Nombrado'
            ('Exclusiva', 'Exclusiva'),
            # Opciones para 'Contratado y Nombrado'
            ('Tiempo completo', 'Tiempo completo'),
            ('Tiempo parcial', 'Tiempo parcial')
        ], 
        validators=[Optional()]
    )
    
    # Información Académica
    ID_CTI = StringField('ID CTI', validators=[Optional(), Length(max=50)])
    ID_Scopus = StringField('ID Scopus', validators=[Optional(), Length(max=50)])
    ID_ORCID = StringField('ID ORCID', validators=[Optional(), Length(max=50)])
    
    # Información de Contacto
    telefono_fijo = TelField('Teléfono Fijo', validators=[
        Optional(), 
        Regexp(r'^\d{6,15}$', message="Ingrese un número de teléfono válido.")
    ])
    movil = TelField('Teléfono Móvil', validators=[
        Optional(), 
        Regexp(r'^\d{6,15}$', message="Ingrese un número de teléfono válido.")
    ])
    correo_personal = EmailField('Correo Personal', validators=[Optional(), Email()])
    correo_institucional = EmailField('Correo Institucional', validators=[Optional(), Email()])
    domicilio_actual = StringField('Domicilio Actual', validators=[Optional(), Length(max=200)])
    referencia = StringField('Referencia', validators=[Optional(), Length(max=200)])
    
    submit = SubmitField('Guardar Cambios')



# Suponiendo que file_size_limit ya está definido en alguna parte de tu código
def file_size_limit(max_size):
    # Implementación de una función personalizada para limitar el tamaño de archivos
    from wtforms import ValidationError
    def _file_size_limit(form, field):
        if field.data:
            if len(field.data.read()) > max_size:
                raise ValidationError(f'El archivo no debe exceder los {max_size / (1024 * 1024)} MB.')
            field.data.seek(0)  # Resetear el puntero del archivo después de leer
    return _file_size_limit

class CargaAcademicaLectivaForm(FlaskForm): 
    periodo_academico = SelectField(
        'Período Académico',
        choices=[
            ('', '--- Seleccione una opción ---'), 
            ('2023-I', '2023-I'), 
            ('2023-II', '2023-II'), 
            ('2024-I', '2024-I'), 
            ('2024-II', '2024-II'),
            ('2025-I', '2025-I'), 
            ('2025-II', '2025-II')
        ],
        validators=[DataRequired(message='Este campo es obligatorio.')]
    )
    
    numero_memorandum = StringField(
        'Número de Memorándum de Carga Académica', 
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=50, message='Máximo 50 caracteres.')
        ]
    )
    
    archivo_memorandum = FileField(
        'Archivo PDF del Memorándum de Carga Académica', 
        validators=[
            Optional(),  # Cambiado de DataRequired a Optional
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
      
    horas_asignadas = IntegerField(
        'Horas Lectivas Asignadas durante el Período Académico', 
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=1, max=30, message='Las horas asignadas deben estar entre 1 y 30.')
        ]
    )
    
    submit = SubmitField('Guardar')

    
    def __init__(self, *args, **kwargs):
        super(CargaAcademicaLectivaForm, self).__init__(*args, **kwargs)
        # Si tienes lógica adicional para inicializar campos, colócala aquí
        # Por ejemplo, cargar opciones dinámicas desde una API

class TutoriaForm(FlaskForm):
    descripcion = TextAreaField('Descripción', validators=[DataRequired(message='Este campo es obligatorio.')])
    anio = IntegerField('Año', validators=[
        DataRequired(message='Este campo es obligatorio.'),
        NumberRange(min=2020, max=datetime.now().year, message=f"El año no puede ser mayor a {datetime.now().year}.")
    ])
    archivo = FileField('Adjuntar Archivo (Imagen o PDF)', validators=[
        Optional(),
        FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
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
            ('', '--- Seleccione una opción ---'),
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
            Optional(),
            NumberRange(min=1, max=1000, message="Debe ser entre 1 y 1000 horas.")
        ]
    )
    creditos = IntegerField(
        'Créditos',
        validators=[
            Optional(),
            NumberRange(min=0, message='Debe ingresar un número válido de créditos.')
        ]
    )
    institucion = SelectField(
        'Tipo de Institución', 
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Universidad', 'Universidad'),
            ('Sociedad Científica', 'Sociedad Científica'),
            ('Organización Internacional', 'Organización Internacional'),
            ('Organización Nacional', 'Organización Nacional'),
            ('Gobierno', 'Gobierno'),
            ('Empresa Privada', 'Empresa Privada'),
            ('Otra', 'Otra')
        ], 
        validators=[
            DataRequired(message='Debe seleccionar un tipo de institución.')
        ]
    )
    nombre_institucion = StringField(
        'Nombre de la Institución',
        validators=[
            Optional(),
            Length(max=100, message='Máximo 100 caracteres.')
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

    def validate_nombre_institucion(self, field):
        if self.institucion.data == 'Otra' and (not field.data or not field.data.strip()):
            raise ValidationError('Debe ingresar el nombre de la institución.')


class ReconocimientosForm(FlaskForm):
    tipo = SelectField(
        'Tipo de Reconocimiento',
        choices=[
            ('', '--- Seleccione una opción ---'),
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
            ('', '--- Seleccione una opción ---'),
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
            Optional(),
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

    def validate_institucion(self, field):
        if self.tipo_institucion.data == 'Otra' and (not field.data or not field.data.strip()):
            raise ValidationError('Debe ingresar el nombre de la institución.')


class ProduccionIntelectualForm(FlaskForm):
    tipo = SelectField(
        'Tipo de Producción Intelectual',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Texto Universitario', 'Texto Universitario'),
            ('Traducción de Libro', 'Traducción de Libro'),
            ('Capítulo de Libro', 'Capítulo de Libro'),
            ('Obra Literaria', 'Obra Literaria'),
            ('Manual de Prácticas', 'Manual de Prácticas'),
            ('Guía de Enseñanza', 'Guía de Enseñanza'),
            ('Monografía', 'Monografía')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de producción intelectual.')]
    )
    titulo = StringField(
        'Título',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    isbn = StringField(
        'ISBN',
        validators=[
            Optional(),
            Length(max=50, message='Máximo 50 caracteres.')
        ]
    )
    deposito_legal = BooleanField('Depósito Legal')
    fecha_publicacion = DateField(
        'Fecha de Publicación',
        format='%Y-%m-%d',
        validators=[Optional()]
    )
    autor = BooleanField('Autor')
    coautor = BooleanField('Coautor')
    archivo = FileField(
        'Adjuntar Archivo PDF',
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)
        ]
    )
    submit = SubmitField('Guardar')

    def validate_isbn(self, field):
        if field.data:
            isbn_clean = field.data.replace('-', '').replace(' ', '')
            if not (re.match(r'^\d{8}$', isbn_clean) or re.match(r'^\d{13}$', isbn_clean)):
                raise ValidationError('ISBN inválido. Debe tener 10 o 13 dígitos.')

    def validate_fecha_publicacion(self, field):
        if field.data and field.data > date.today():
            raise ValidationError('La fecha de publicación no puede ser en el futuro.')


class ParticipacionTesisForm(FlaskForm):
    tipo = SelectField(
        'Tipo de Participación',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Director', 'Director'),
            ('Asesor', 'Asesor'),
            ('Jurado', 'Jurado')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de participación.')]
    )
    nivel = SelectField(
        'Nivel',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Pregrado', 'Pregrado'),
            ('Posgrado', 'Posgrado'),
            ('Otra', 'Otra')  # Añadido 'Otra' si se requiere
        ],
        validators=[DataRequired(message='Debe seleccionar el nivel.')]
    )
    otro_nivel = StringField(
        'Otro Nivel',
        validators=[Optional(), Length(max=255, message='Máximo 255 caracteres.')]
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    universidad = StringField(
        'Universidad',
        validators=[
            Optional(),
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

    def validate_otro_nivel(self, field):
        if self.nivel.data == 'Otra' and (not field.data or not field.data.strip()):
            raise ValidationError('Debe ingresar el nombre del nivel.')

    def validate_fecha(self, field):
        if field.data > date.today():
            raise ValidationError('La fecha no puede ser en el futuro.')


# --- Clase de Formulario (InvestigacionesForm) ---
class InvestigacionesForm(FlaskForm):
    tipo = SelectField(
        'Tipo de Investigación',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Artículo Científico', 'Artículo Científico'),
            ('Artículo Aceptado', 'Artículo Aceptado'),
            ('Artículo en Congreso', 'Artículo en Congreso'),
            ('Registro de Patente', 'Registro de Patente'),
            ('Informe de Investigación', 'Informe de Investigación'),
            ('Participación en Publicación Científica', 'Participación en Publicación Científica')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de investigación.')]
    )
    titulo = StringField(
        'Denominación',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    revista = StringField(
        'Revista',
        validators=[DataRequired(message='Este campo es obligatorio.'), Length(max=255, message='Máximo 255 caracteres.')]
    )
    indice = SelectField(
        'Índice',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Thomson Reuters', 'Thomson Reuters'),
            ('Scopus', 'Scopus'),
            ('Web of Science', 'Web of Science'),
            ('Scielo', 'Scielo'),
            ('Latin Index', 'Latin Index'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired(message='Debe seleccionar un índice.')]
    )
    fecha_publicacion = DateField(
        'Fecha de Publicación',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Este campo es obligatorio.')]
    )
    autor = BooleanField('Autor')
    coautor = BooleanField('Coautor')
    archivo = FileField(
        'Adjuntar Archivo (Solo PDF)',
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # 10 MB máximo
        ]
    )
    submit = SubmitField('Guardar')
    
    def validate_otro_indice(self, field):
        if self.indice.data == 'Otro' and (not field.data or not field.data.strip()):
            raise ValidationError('Debe ingresar el nombre del índice.')

    def validate_fecha_inicio(self, field):
        if field.data > date.today():
            raise ValidationError('La fecha de inicio no puede ser en el futuro.')

    def validate_fecha_fin(self, field):
        if field.data and field.data > date.today():
            raise ValidationError('La fecha de fin no puede ser en el futuro.')
        if field.data and self.fecha_inicio.data and field.data < self.fecha_inicio.data:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

    def validate_fecha_publicacion(self, field):
        if field.data and field.data > date.today():
            raise ValidationError('La fecha de publicación no puede ser en el futuro.')


class IdiomasForm(FlaskForm):
    idioma = SelectField(
        'Idioma',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Inglés', 'Inglés'),
            ('Francés', 'Francés'),
            ('Alemán', 'Alemán'),
            ('Italiano', 'Italiano'),
            ('Portugués', 'Portugués'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired(message='Debe seleccionar un idioma.')]
    )
    otro_idioma = StringField(
        'Otro Idioma',
        validators=[
            Optional(),
            Length(max=50, message='Máximo 50 caracteres.')
        ]
    )
    nivel = SelectField(
        'Nivel',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Básico', 'Básico'),
            ('Intermedio', 'Intermedio'),
            ('Avanzado', 'Avanzado')
        ],
        validators=[DataRequired(message='Debe seleccionar un nivel.')]
    )
    certificado = BooleanField(
        '¿Posee Certificado?'
    )
    archivo = FileField(
        'Adjuntar Certificado (Imagen o PDF)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')

    def validate_otro_idioma(self, field):
        if self.idioma.data == 'Otro' and (not field.data or not field.data.strip()):
            raise ValidationError('Debe ingresar el otro idioma.')


class GradostitulosForm(FlaskForm):
    titulo = StringField(
        'Denominación del Grado o Título',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    tipo = SelectField(
        'Tipo de Grado o Título',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Grado de Bachiller', 'Grado de Bachiller'),
            ('Título Profesional', 'Título Profesional (Adjuntar certificado de habilidad)'),
            ('Título de Segunda Especialidad Profesional', 'Título de Segunda Especialidad Profesional'),
            ('Maestría (un año de duración)', 'Maestría (un año de duración)'),
            ('Maestría (dos años de duración)', 'Maestría (dos años de duración)'),
            ('Doctorado o Ph.D.', 'Doctorado o Ph.D.')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de título.')]
    )
    pais = SelectField(
        'País',
        choices=[],  # Se actualizará dinámicamente desde app.py
        validators=[DataRequired(message='Debe seleccionar un país.')]
    )
    universidad = SelectField(
        'Universidad',
        choices=[('', '--- Seleccione un país primero ---')],
        validators=[DataRequired(message='Debe seleccionar una universidad.')]
    )
    otro_universidad = StringField(
        'Otra Universidad',
        validators=[
            Optional(),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    otro_pais = StringField(
        'Otro País',
        validators=[Optional(), Length(max=255, message='Máximo 255 caracteres.')]
    )
    fecha_expedicion = DateField(
        'Fecha de Expedición',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Este campo es obligatorio.')
        ]
    )
    archivo = FileField(
        'Adjuntar grado o título (PDF)',
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    archivo_sunedu = FileField(
        'Adjuntar Constancia SUNEDU',
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')

    def validate_otro_universidad(self, field):
        if self.universidad.data == 'Otra' and (not field.data or not field.data.strip()):
            raise ValidationError('Por favor, especifique la otra universidad.')

    def validate_otro_pais(self, field):
        if self.pais.data == 'Otro' and (not field.data or not field.data.strip()):
            raise ValidationError('Por favor, especifique el otro país.')

    def validate_fecha_expedicion(self, field):
        if field.data > date.today():
            raise ValidationError('La fecha de expedición no puede ser en el futuro.')


class ActividadesProyeccionSocialForm(FlaskForm):
    fecha = DateField(
        'Fecha',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Este campo es obligatorio.')]
    )
    Emitido_por = StringField(
        'Emitido por',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    archivo = FileField(
        'Adjuntar Archivo (PDF)',
        validators=[
            Optional(),
            # Solo se permite la extensión 'pdf'
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')


    def validate_fecha(self, field):
        if field.data > date.today():
            raise ValidationError('La fecha no puede ser en el futuro.')


class ActualizacionesCapacitacionesForm(FlaskForm):
    tipo = SelectField(
        'Tipo de Capacitación',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Curso Presencial', 'Curso Presencial'),
            ('Curso Virtual', 'Curso Virtual'),
            ('Curso taller', 'Curso taller'),
            ('Diplomado Presencial', 'Diplomado Presencial'),
            ('Diplomado Virtual', 'Diplomado Virtual'),
            ('Segunda Especialidad', 'Estudios de Segunda Especialidad'),
            ('Maestría', 'Estudios de Maestría'),
            ('Doctorado', 'Estudios de Doctorado'),
            ('Especialización en Docencia Universitaria', 'Estudios de Especialización en Docencia Universitaria'),
            ('otro tipo de capacitación', 'otro tipo de capacitación')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de capacitación.')]
    )
    
    fecha = DateField(
        'Fecha',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Este campo es obligatorio.')
        ]
    )

    def validate_fecha(self, field):
        min_date = date.today().replace(year=date.today().year - 4)
        if field.data < min_date:
            raise ValidationError('La fecha debe ser de los últimos 3 años.')
    
    descripcion = StringField(
        'Denominación de la Actualización Profesional o Los Estudios',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    horas = IntegerField(
        'Horas',
        validators=[
            Optional(),
            NumberRange(min=1, message='Debe ingresar un número válido de horas.')
        ]
    )
    creditos = IntegerField(
        'Créditos',
        validators=[
            Optional(),
            NumberRange(min=0, message='Debe ingresar un número válido de créditos.')
        ]
    )
    semestres_concluidos = IntegerField(
        'Semestres Concluidos',
        validators=[
            Optional(),
            NumberRange(min=0, message='Debe ingresar un número válido de semestres concluidos.')
        ]
    )
    institucion_otorga = StringField(
        'Institución que Otorga',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )

    archivo = FileField(
        'Adjuntar Constancia o Certificado (PDF)',
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')

    def validate(self, *args, **kwargs):
        # Llamar al método validate de la clase base con los argumentos
        rv = super(ActualizacionesCapacitacionesForm, self).validate(*args, **kwargs)
        if not rv:
            return False

        # Definir los tipos que se miden por semestres
        tipos_por_semestres = [
            'Segunda Especialidad',
            'Maestría',
            'Doctorado',
            'Especialización en Docencia Universitaria'
        ]

        # Definir los tipos que se miden por horas y créditos
        tipos_por_horas_creditos = [
            'Curso Presencial',
            'Curso Virtual',
            'Diplomado Presencial',
            'Diplomado Virtual',
            'Curso taller',
            'otro tipo de capacitación'
        ]

        tipo_seleccionado = self.tipo.data

        if tipo_seleccionado in tipos_por_semestres:
            if not self.semestres_concluidos.data:
                self.semestres_concluidos.errors.append('Este campo es obligatorio para el tipo seleccionado.')
                return False
            # Opcionalmente, puedes limpiar horas y créditos si no son relevantes
            self.horas.data = None
            self.creditos.data = None
        elif tipo_seleccionado in tipos_por_horas_creditos:
            if not self.horas.data:
                self.horas.errors.append('Este campo es obligatorio para el tipo seleccionado.')
                return False
            # Opcionalmente, puedes limpiar semestres_concluidos si no son relevantes
            self.semestres_concluidos.data = None
        else:
            # Tipo no reconocido
            self.tipo.errors.append('Tipo de capacitación no reconocido.')
            return False

        return True
    
class CargosDirectivosForm(FlaskForm):
    cargo = StringField(
        'Cargo',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    anios = IntegerField(
        'Años en el Cargo',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=0, message='Debe ser un número positivo.')
        ]
    )
    descripcion = StringField(
        'Descripción',
        validators=[
            Optional(),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    archivo = FileField(
        'Adjuntar resolucion o memorandum (PDF)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')

class ExperienciaDocenteForm(FlaskForm):
    tipo = SelectField(
        'Tipo de Experiencia',
        choices=[
            ('', 'Seleccione una opción'),
            ('Movilidad Docente', 'Movilidad Docente'),
            ('Posgrado', 'Posgrado'),
            ('Docencia en Categoría', 'Docencia en Categoría')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de experiencia.')]
    )
    descripcion = StringField(
        'Descripción',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    anios = IntegerField(
        'Años de Experiencia',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=0, message='Debe ser un número positivo.')
        ]
    )
    cursos = IntegerField(
        'Cantidad de Cursos',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=0, message='Debe ser un número positivo.')
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

    def validate_fecha_expedicion(self, field):
        if hasattr(self, 'fecha_expedicion') and field.data > date.today():
            raise ValidationError('La fecha de expedición no puede ser en el futuro.')


class AcreditacionLicenciamientoForm(FlaskForm):
    numero_resolucion = StringField(
        'Número de Resolución', 
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    
    fecha_resolucion = DateField(
        'Fecha de Resolución',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Este campo es obligatorio.')]
    )
    
    fecha_inicio = DateField(
        'Fecha de Inicio',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Este campo es obligatorio.')]
    )
    
    fecha_fin = DateField(
        'Fecha de Fin',
        format='%Y-%m-%d',
        validators=[DataRequired(message='Este campo es obligatorio.')]
    )
    
    cargo_comite = SelectField(
        'Cargo en el Comité', 
        choices=[
            ('', '--- Seleccione una opción ---'),            
            ('PRESIDENTE DE COMITE', 'PRESIDENTE DE COMITE'),
            ('MIEMBRO DE COMITE', 'MIEMBRO DE COMITE')
        ],
        validators=[DataRequired(message='Este campo es obligatorio.')]
    )
    
    archivo_resolucion = FileField(
        'Archivo PDF de la Resolución', 
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    
    evidencias = FileField(
        'Archivo de Evidencias (opcional)', 
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    
    submit = SubmitField('Guardar')
