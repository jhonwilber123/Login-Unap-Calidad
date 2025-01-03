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
import requests
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
    area_gestion = SelectField(
        'Área de Gestión',
        choices=[
            ('Administración Académica', 'Administración Académica'),
            ('Administración Financiera', 'Administración Financiera'),
            ('Desarrollo de Infraestructura', 'Desarrollo de Infraestructura'),
            ('Innovación y Tecnología', 'Innovación y Tecnología'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired()]
    )
    otro_area_gestion = StringField(
        'Otra Área de Gestión',
        validators=[Optional(), Length(max=255)]
    )
    rol_gestion = SelectField(
        'Rol de Gestión',
        choices=[
            ('Coordinador', 'Coordinador'),
            ('Secretario', 'Secretario'),
            ('Miembro del Comité', 'Miembro del Comité'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired()]
    )
    otro_rol_gestion = StringField(
        'Otro Rol de Gestión',
        validators=[Optional(), Length(max=255)]
    )
    descripcion_responsabilidades = TextAreaField(
        'Descripción de Responsabilidades',
        validators=[DataRequired()]
    )
    fecha_inicio = DateField(
        'Fecha de Inicio',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )
    fecha_fin = DateField(
        'Fecha de Fin',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )
    logros_contribuciones = TextAreaField(
        'Logros y Contribuciones',
        validators=[Optional()]
    )
    adjuntar_documentacion = FileField(
        'Adjuntar Documentación',
        validators=[
            Optional(),
            FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo se permiten archivos PDF o imágenes.')
        ]
    )
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
    foto_docente = FileField('Foto del Docente', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes.')
    ])
    constancia_habilitacion = FileField('Constancia de Habilitación', validators=[
        FileAllowed(['pdf'], 'Solo se permiten archivos PDF.')
    ])
    # Personal Information
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(), Length(max=50)])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired(), Length(max=50)])
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()], format='%Y-%m-%d')
    lugar_nacimiento_departamento = StringField('Departamento de Nacimiento', validators=[DataRequired(), Length(max=50)])
    lugar_nacimiento_provincia = StringField('Provincia de Nacimiento', validators=[DataRequired(), Length(max=50)])
    lugar_nacimiento_distrito = StringField('Distrito de Nacimiento', validators=[DataRequired(), Length(max=50)])
    dni = StringField('DNI', validators=[DataRequired(), Regexp(r'^\d{8}$', message="El DNI debe tener 8 dígitos.")])
    
    # Professional Information
    numero_colegiatura = StringField('Número de Colegiatura', validators=[Optional(), Length(max=20)])
    codigo = StringField('Código UNAP', validators=[DataRequired(), Length(max=20)])
    condicion = SelectField(
        'Condición', 
        choices=[
            ('', 'Seleccione...'),
            ('Nombrado', 'Nombrado'),
            ('Contratado', 'Contratado')
        ], 
        validators=[DataRequired()]
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
        validators=[DataRequired()]
    )
    dedicacion = SelectField(
        'Dedicación', 
        choices=[
            ('', 'Seleccione...'),
            # Opcion solo para 'Nombrado'
            ('Exclusiva', 'Exclusiva'),
            # Opciones para 'Contratado y Nombrado'
            ('Tiempo completo', 'Tiempo completo'),
            ('Tiempo parcial', 'Tiempo parcial')
        ], 
        validators=[DataRequired()]
    )
    
    # Academic Information
    ID_CTI = StringField('ID CTI', validators=[DataRequired(), Length(max=50)])
    ID_Scopus = StringField('ID Scopus', validators=[DataRequired(), Length(max=50)])
    ID_ORCID = StringField('ID ORCID', validators=[DataRequired(), Length(max=50)])
    # Contact Information
    telefono_fijo = TelField('Teléfono Fijo', validators=[DataRequired(), Regexp(r'^\d{6,15}$', message="Ingrese un número de teléfono válido.")])
    movil = TelField('Teléfono Móvil', validators=[DataRequired(), Regexp(r'^\d{6,15}$', message="Ingrese un número de teléfono válido.")])
    correo_personal = EmailField('Correo Personal', validators=[DataRequired(), Email()])
    correo_institucional = EmailField('Correo Institucional', validators=[DataRequired(), Email()])
    domicilio_actual = StringField('Domicilio Actual', validators=[DataRequired(), Length(max=200)])
    referencia = StringField('Referencia', validators=[Optional(), Length(max=200)])
    
    # Image Uploads
    foto_docente = FileField('Foto de Docente', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo se permiten imágenes'),
        Optional()
    ])
    constancia_habilitacion = FileField('Constancia de Habilitación', validators=[
        FileAllowed(['pdf'], 'Solo se permiten PDF'),
        Optional()
    ])
    
    submit = SubmitField('Guardar Cambios')


class CargaAcademicaLectivaForm(FlaskForm):
    periodo_academico = SelectField(
        'Período Académico',
        choices=[('', '--- Seleccione una opción ---'), ('2023-I', '2023-I'), ('2023-II', '2023-II'), ('2024-I', '2024-I'), ('2024-II', '2024-II')],
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
            DataRequired(message='Este campo es obligatorio.'),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    categoria_docente = SelectField(
        'Categoría Docente durante el Período Académico', 
        choices=[('', 'Seleccione una opción'), ('Auxiliar', 'Auxiliar'), ('Asociado', 'Asociado'), ('Principal', 'Principal')], 
        validators=[DataRequired(message='Debe seleccionar una categoría.')]
    )
    horas_asignadas = IntegerField(
        'Horas Asignadas durante el Período Académico', 
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            NumberRange(min=1, max=30, message='Las horas asignadas deben estar entre 1 y 30.')
        ]
    )
    observaciones = TextAreaField(
        'Observaciones',
        validators=[Optional(), Length(max=500, message='Máximo 500 caracteres.')]
    )
    submit = SubmitField('Guardar')

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
        validators=[
            Optional()
        ]
    )
    autor = BooleanField('Autor')
    coautor = BooleanField('Coautor')
    archivo = FileField(
        'Adjuntar Archivo (Imagen o PDF)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    editorial_prestigiosa = SelectField(
        'Editorial de Reconocido Prestigio',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('No', 'Otro'),
            ('Scopus', 'Scopus'),
            ('Web of Science', 'Web of Science'),
            ('SciELO', 'SciELO')
        ],
        validators=[DataRequired(message='Debe seleccionar una opción para la editorial.')]
    )
    submit = SubmitField('Guardar')

    def validate_isbn(self, field):
        if field.data:
            isbn_clean = field.data.replace('-', '').replace(' ', '')
            if not (re.match(r'^\d{10}$', isbn_clean) or re.match(r'^\d{13}$', isbn_clean)):
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
    descripcion = TextAreaField(
        'Descripción',
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
        validators=[Optional()]
    )
    revista = StringField(
        'Revista',
        validators=[Optional(), Length(max=255, message='Máximo 255 caracteres.')]
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
        validators=[Optional()]
    )
    otro_indice = StringField(
        'Otro Índice',
        validators=[Optional(), Length(max=255, message='Máximo 255 caracteres.')]
    )
    fecha_publicacion = DateField(
        'Fecha de Publicación',
        format='%Y-%m-%d',
        validators=[Optional()]
    )
    autor = BooleanField('Autor')
    coautor = BooleanField('Coautor')
    archivo = FileField(
        'Adjuntar Archivo (Imagen o PDF)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
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
    universidad = SelectField(
        'Universidad',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Universidad Nacional Del Altiplano', 'Universidad Nacional Del Altiplano'),
            ('Otra', 'Otra')
        ],
        validators=[DataRequired(message='Debe seleccionar una universidad.')]
    )
    otro_universidad = StringField(
        'Otra Universidad',
        validators=[
            Optional(),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    pais = SelectField(
        'País',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Afganistán', 'Afganistán'),
            ('Albania', 'Albania'),
            ('Alemania', 'Alemania'),
            ('Andorra', 'Andorra'),
            ('Angola', 'Angola'),
            ('Antigua y Barbuda', 'Antigua y Barbuda'),
            ('Arabia Saudita', 'Arabia Saudita'),
            ('Argelia', 'Argelia'),
            ('Argentina', 'Argentina'),
            ('Armenia', 'Armenia'),
            ('Australia', 'Australia'),
            ('Austria', 'Austria'),
            ('Azerbaiyán', 'Azerbaiyán'),
            ('Bahamas', 'Bahamas'),
            ('Bangladés', 'Bangladés'),
            ('Barbados', 'Barbados'),
            ('Baréin', 'Baréin'),
            ('Bélgica', 'Bélgica'),
            ('Belice', 'Belice'),
            ('Benín', 'Benín'),
            ('Bielorrusia', 'Bielorrusia'),
            ('Birmania', 'Birmania'),
            ('Bolivia', 'Bolivia'),
            ('Bosnia y Herzegovina', 'Bosnia y Herzegovina'),
            ('Botsuana', 'Botsuana'),
            ('Brasil', 'Brasil'),
            ('Brunéi', 'Brunéi'),
            ('Bulgaria', 'Bulgaria'),
            ('Burkina Faso', 'Burkina Faso'),
            ('Burundi', 'Burundi'),
            ('Bután', 'Bután'),
            ('Cabo Verde', 'Cabo Verde'),
            ('Camboya', 'Camboya'),
            ('Camerún', 'Camerún'),
            ('Canadá', 'Canadá'),
            ('Centroafricana', 'Centroafricana'),
            ('Chad', 'Chad'),
            ('Chile', 'Chile'),
            ('China', 'China'),
            ('Chipre', 'Chipre'),
            ('Colombia', 'Colombia'),
            ('Comoras', 'Comoras'),
            ('Corea del Norte', 'Corea del Norte'),
            ('Corea del Sur', 'Corea del Sur'),
            ('Costa de Marfil', 'Costa de Marfil'),
            ('Costa Rica', 'Costa Rica'),
            ('Croacia', 'Croacia'),
            ('Cuba', 'Cuba'),
            ('Dinamarca', 'Dinamarca'),
            ('Dominica', 'Dominica'),
            ('Ecuador', 'Ecuador'),
            ('Egipto', 'Egipto'),
            ('El Salvador', 'El Salvador'),
            ('Emiratos Árabes Unidos', 'Emiratos Árabes Unidos'),
            ('Eritrea', 'Eritrea'),
            ('Eslovaquia', 'Eslovaquia'),
            ('Eslovenia', 'Eslovenia'),
            ('España', 'España'),
            ('Estados Unidos', 'Estados Unidos'),
            ('Estonia', 'Estonia'),
            ('Etiopía', 'Etiopía'),
            ('Filipinas', 'Filipinas'),
            ('Finlandia', 'Finlandia'),
            ('Fiyi', 'Fiyi'),
            ('Francia', 'Francia'),
            ('Gabón', 'Gabón'),
            ('Gambia', 'Gambia'),
            ('Georgia', 'Georgia'),
            ('Ghana', 'Ghana'),
            ('Granada', 'Granada'),
            ('Grecia', 'Grecia'),
            ('Guatemala', 'Guatemala'),
            ('Guinea', 'Guinea'),
            ('Guinea-Bisáu', 'Guinea-Bisáu'),
            ('Guinea Ecuatorial', 'Guinea Ecuatorial'),
            ('Guyana', 'Guyana'),
            ('Haití', 'Haití'),
            ('Honduras', 'Honduras'),
            ('Hungría', 'Hungría'),
            ('India', 'India'),
            ('Indonesia', 'Indonesia'),
            ('Irán', 'Irán'),
            ('Iraq', 'Iraq'),
            ('Irlanda', 'Irlanda'),
            ('Islandia', 'Islandia'),
            ('Islas Marshall', 'Islas Marshall'),
            ('Islas Salomón', 'Islas Salomón'),
            ('Israel', 'Israel'),
            ('Italia', 'Italia'),
            ('Jamaica', 'Jamaica'),
            ('Japón', 'Japón'),
            ('Jordania', 'Jordania'),
            ('Kazajistán', 'Kazajistán'),
            ('Kenia', 'Kenia'),
            ('Kirguistán', 'Kirguistán'),
            ('Kiribati', 'Kiribati'),
            ('Kuwait', 'Kuwait'),
            ('Laos', 'Laos'),
            ('Lesoto', 'Lesoto'),
            ('Letonia', 'Letonia'),
            ('Líbano', 'Líbano'),
            ('Liberia', 'Liberia'),
            ('Libia', 'Libia'),
            ('Liechtenstein', 'Liechtenstein'),
            ('Lituania', 'Lituania'),
            ('Luxemburgo', 'Luxemburgo'),
            ('Madagascar', 'Madagascar'),
            ('Malasia', 'Malasia'),
            ('Malaui', 'Malaui'),
            ('Maldivas', 'Maldivas'),
            ('Malí', 'Malí'),
            ('Malta', 'Malta'),
            ('Marruecos', 'Marruecos'),
            ('Mauricio', 'Mauricio'),
            ('Mauritania', 'Mauritania'),
            ('México', 'México'),
            ('Micronesia', 'Micronesia'),
            ('Moldavia', 'Moldavia'),
            ('Mónaco', 'Mónaco'),
            ('Mongolia', 'Mongolia'),
            ('Montenegro', 'Montenegro'),
            ('Mozambique', 'Mozambique'),
            ('Namibia', 'Namibia'),
            ('Nauru', 'Nauru'),
            ('Nepal', 'Nepal'),
            ('Nicaragua', 'Nicaragua'),
            ('Níger', 'Níger'),
            ('Nigeria', 'Nigeria'),
            ('Noruega', 'Noruega'),
            ('Nueva Zelanda', 'Nueva Zelanda'),
            ('Omán', 'Omán'),
            ('Pakistán', 'Pakistán'),
            ('Palaos', 'Palaos'),
            ('Palestina', 'Palestina'),
            ('Panamá', 'Panamá'),
            ('Papúa Nueva Guinea', 'Papúa Nueva Guinea'),
            ('Paraguay', 'Paraguay'),
            ('Perú', 'Perú'),
            ('Polonia', 'Polonia'),
            ('Portugal', 'Portugal'),
            ('Reino Unido', 'Reino Unido'),
            ('República Centroafricana', 'República Centroafricana'),
            ('República Checa', 'República Checa'),
            ('República Dominicana', 'República Dominicana'),
            ('Ruanda', 'Ruanda'),
            ('Rumania', 'Rumania'),
            ('Rusia', 'Rusia'),
            ('Samoa', 'Samoa'),
            ('San Cristóbal y Nieves', 'San Cristóbal y Nieves'),
            ('San Marino', 'San Marino'),
            ('San Vicente y las Granadinas', 'San Vicente y las Granadinas'),
            ('Santa Lucía', 'Santa Lucía'),
            ('Santo Tomé y Príncipe', 'Santo Tomé y Príncipe'),
            ('Senegal', 'Senegal'),
            ('Serbia', 'Serbia'),
            ('Seychelles', 'Seychelles'),
            ('Sierra Leona', 'Sierra Leona'),
            ('Singapur', 'Singapur'),
            ('Siria', 'Siria'),
            ('Somalia', 'Somalia'),
            ('Sri Lanka', 'Sri Lanka'),
            ('Sudáfrica', 'Sudáfrica'),
            ('Sudán', 'Sudán'),
            ('Sudán del Sur', 'Sudán del Sur'),
            ('Suecia', 'Suecia'),
            ('Suiza', 'Suiza'),
            ('Surinam', 'Surinam'),
            ('Tailandia', 'Tailandia'),
            ('Tanzania', 'Tanzania'),
            ('Tayikistán', 'Tayikistán'),
            ('Timor Oriental', 'Timor Oriental'),
            ('Togo', 'Togo'),
            ('Tonga', 'Tonga'),
            ('Trinidad y Tobago', 'Trinidad y Tobago'),
            ('Túnez', 'Túnez'),
            ('Turkmenistán', 'Turkmenistán'),
            ('Turquía', 'Turquía'),
            ('Tuvalu', 'Tuvalu'),
            ('Ucrania', 'Ucrania'),
            ('Uganda', 'Uganda'),
            ('Uruguay', 'Uruguay'),
            ('Uzbekistán', 'Uzbekistán'),
            ('Vanuatu', 'Vanuatu'),
            ('Venezuela', 'Venezuela'),
            ('Vietnam', 'Vietnam'),
            ('Yemen', 'Yemen'),
            ('Yibuti', 'Yibuti'),
            ('Zambia', 'Zambia'),
            ('Zimbabue', 'Zimbabue'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired(message='Debe seleccionar un país.')]
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
    def __init__(self, *args, **kwargs):
        super(GradostitulosForm, self).__init__(*args, **kwargs)
        try:
            response = requests.get('https://restcountries.com/v3.1/all')
            response.raise_for_status()
            countries = response.json()
            country_choices = [('', '--- Seleccione una opción ---')]
            for country in countries:
                country_name = country.get('translations', {}).get('spa', {}).get('common')
                if country_name:
                    country_choices.append((country_name, country_name))
            self.pais.choices = sorted(country_choices, key=lambda x: x[1])
        except Exception:
            self.pais.choices = [('', '--- Seleccione una opción ---')]
    archivo = FileField(
        'Adjuntar grado o título (PDF)',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    archivo_sunedu = FileField(
        'Adjuntar Constancia SUNEDU',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            FileAllowed(['pdf'], 'Solo se permiten Archivos PDF.'),
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
    tipo = SelectField(
        'Tipo de Actividad',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Organización', 'Organización'),
            ('Expositor', 'Expositor'),
            ('Asistencia', 'Asistencia')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de actividad.')]
    )
    evento = SelectField(
        'Evento',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Congreso', 'Congreso'),
            ('Convención', 'Convención'),
            ('Simposio', 'Simposio'),
            ('Foro', 'Foro'),
            ('Seminario', 'Seminario'),
            ('Curso Taller', 'Curso Taller'),
            ('Charla', 'Charla')
        ],
        validators=[DataRequired(message='Debe seleccionar un evento.')]
    )
    descripcion = StringField(
        'Descripción',
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

    Emitido_por = StringField(
        'Emitido por',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=100, message='Máximo 100 caracteres.')
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
            ('Diplomado Presencial', 'Diplomado Presencial'),
            ('Diplomado Virtual', 'Diplomado Virtual'),
            ('Segunda Especialidad', 'Estudios de Segunda Especialidad'),
            ('Maestría', 'Estudios de Maestría'),
            ('Doctorado', 'Estudios de Doctorado'),
            ('Especialización en Docencia Universitaria', 'Estudios de Especialización en Docencia Universitaria')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de capacitación.')]
    )
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
        'Adjuntar Archivo (PDF)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
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
            'Diplomado Virtual'
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
    cargo = StringField(
        'Cargo en el Comité de Calidad, Licenciamiento y Acreditación',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    nombre_comite = StringField(
        'Nombre del Comité o Proyecto',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    tipo_participacion = SelectField(
        'Tipo de Participación',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Acreditación', 'Acreditación'),
            ('Licenciamiento', 'Licenciamiento'),
            ('Otro', 'Otro')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de participación.')]
    )
    otro_tipo_participacion = StringField(
        'Especificar Otro Tipo de Participación',
        validators=[
            Optional(),
            Length(max=100, message='Máximo 100 caracteres.')
        ]
    )
    fecha_inicio = DateField(
        'Fecha de Inicio',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Este campo es obligatorio.')
        ]
    )
    fecha_fin = DateField(
        'Fecha de Fin',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Este campo es obligatorio.')
        ]
    )
    numero_resolucion = StringField(
        'Número de Resolución de Nombramiento',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=50, message='Máximo 50 caracteres.')
        ]
    )
    fecha_resolucion = DateField(
        'Fecha de Resolución de Nombramiento',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message='Este campo es obligatorio.')
        ]
    )
    resolucion_nombramiento = FileField(
        'Adjuntar Resolución (archivo PDF)',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    logros = TextAreaField(
        'Logros Alcanzados',
        validators=[
            Optional(),
            Length(max=2000, message='Máximo 2000 caracteres.')
        ]
    )
    evidencias = FileField(
        'Adjuntar Informe de las Comisiones y/o Subcomisiones (PDF)',
        validators=[
            Optional(),
            FileAllowed(['pdf'], 'Solo se permiten archivos PDF.'),
            file_size_limit(10 * 1024 * 1024)  # Límite de 10 MB
        ]
    )
    submit = SubmitField('Guardar')