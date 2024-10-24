# forms.py

from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField, 
    IntegerField, 
    SelectField, 
    StringField, 
    DateField, 
    FileField, 
    SubmitField,
    BooleanField,
)
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError, Length
from flask_wtf.file import FileAllowed
from datetime import datetime, date
import re

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
    descripcion = TextAreaField('Descripción', validators=[DataRequired(message='Este campo es obligatorio.')])
    anio = IntegerField('Año', validators=[
        DataRequired(message='Este campo es obligatorio.'),
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
        'Título',
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
        'Título',
        validators=[
            DataRequired(message='Este campo es obligatorio.'),
            Length(max=255, message='Máximo 255 caracteres.')
        ]
    )
    tipo = SelectField(
        'Tipo de Título',
        choices=[
            ('', '--- Seleccione una opción ---'),
            ('Título Profesional', 'Título Profesional (Adjuntar certificado de habilidad en el colegio profesional correspondiente)'),
            ('Título de Segunda Especialidad Profesional', 'Título de Segunda Especialidad Profesional'),
            ('Especialidad Médica', 'Especialidad Médica (Adjuntar Registro Nacional de especialista)'),
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
            ('Universidad Peruana Cayetano Heredia', 'Universidad Peruana Cayetano Heredia'),
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
            ('', 'Seleccione una opción'),
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
    archivo = FileField(
        'Adjuntar Archivo (Imagen o PDF)',
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Solo se permiten imágenes y archivos PDF.'),
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
            ('Segunda Especialidad', 'Segunda Especialidad'),
            ('Maestría', 'Maestría'),
            ('Doctorado', 'Doctorado'),
            ('Especialización en Docencia Universitaria', 'Especialización en Docencia Universitaria')
        ],
        validators=[DataRequired(message='Debe seleccionar un tipo de capacitación.')]
    )
    descripcion = StringField(
        'Descripción',
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
    archivo = FileField(
        'Adjuntar Archivo (Imagen o PDF)',
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
        'Adjuntar Archivo (Imagen o PDF)',
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