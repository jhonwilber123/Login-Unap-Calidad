# src/forms.py (Versión Final Refactorizada)

import os
from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (StringField, DateField, SelectField, TelField, EmailField, 
                     SubmitField, TextAreaField, IntegerField, BooleanField, 
                     PasswordField, DecimalField)
from wtforms.validators import (DataRequired, Length, Optional, Regexp, Email, 
                                NumberRange, ValidationError, EqualTo)

# ===============================================
# === FUNCIÓN DE UTILIDAD Y CLASE BASE ===
# ===============================================

def file_size_limit(max_size_mb):
    """Validador personalizado para limitar el tamaño del archivo en MB."""
    max_bytes = max_size_mb * 1024 * 1024
    def _file_size_limit(form, field):
        if field.data:
            # Nos aseguramos de leer el archivo una sola vez
            field.data.seek(0, os.SEEK_END)
            file_length = field.data.tell()
            field.data.seek(0)
            if file_length > max_bytes:
                raise ValidationError(f'El archivo no debe exceder los {max_size_mb} MB.')
    return _file_size_limit

class BaseCVForm(FlaskForm):
    """
    Clase base para todos los formularios del CV.
    Contiene campos comunes como el de subir archivos y el botón de envío.
    """
    archivo = FileField('Adjuntar Archivo de Constancia (PDF o Imagen)', validators=[
        Optional(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], '¡Solo se permiten archivos PDF o de imagen!'),
        file_size_limit(10) # Límite de 10 MB
    ])
    submit = SubmitField('Guardar Registro')


# ===============================================
# === FORMULARIOS DE GESTIÓN DE USUARIOS ===
# ===============================================

class EditUserForm(FlaskForm):
    """Formulario para que el administrador edite los datos de un usuario."""
    username = StringField('Correo Electrónico (Usuario)', validators=[DataRequired(), Email()])
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired()])
    password = PasswordField('Nueva Contraseña (dejar en blanco para no cambiar)', validators=[
        Optional(),
        EqualTo('confirm_password', message='Las contraseñas deben coincidir.')
    ])
    confirm_password = PasswordField('Confirmar Nueva Contraseña')
    submit = SubmitField('Guardar Cambios')


# ===============================================
# === FORMULARIOS DEL CV DEL DOCENTE ===
# ===============================================

# --- Cada formulario hereda de BaseCVForm para reutilizar campos ---

class InformacionPersonalForm(FlaskForm):
    # Este formulario es especial y no necesita los campos base.
    foto_docente = FileField('Foto del Docente', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Solo imágenes.')])
    constancia_habilitacion = FileField('Constancia de Habilitación (PDF)', validators=[Optional(), FileAllowed(['pdf'], 'Solo PDFs.')])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(), Length(max=50)])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired(), Length(max=50)])
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[Optional()])
    lugar_nacimiento_departamento = StringField('Departamento de Nacimiento', validators=[Optional(), Length(max=50)])
    lugar_nacimiento_provincia = StringField('Provincia de Nacimiento', validators=[Optional(), Length(max=50)])
    lugar_nacimiento_distrito = StringField('Distrito de Nacimiento', validators=[Optional(), Length(max=50)])
    dni = StringField('DNI', validators=[DataRequired(), Regexp(r'^\d{8}$', message="El DNI debe tener 8 dígitos.")])
    colegio_profesional = StringField('Colegio Profesional', validators=[Optional(), Length(max=100)])
    numero_colegiatura = StringField('Nº de Colegiatura', validators=[Optional(), Length(max=20)])
    codigo = StringField('Código UNAP', validators=[Optional(), Length(max=20)])
    condicion = SelectField('Condición', choices=[('', 'Seleccione...'), ('Nombrado', 'Nombrado'), ('Contratado', 'Contratado')], validators=[Optional()])
    categoria = SelectField('Categoría', choices=[('', 'Seleccione...'), ('Principal', 'Principal'), ('Asociado', 'Asociado'), ('Auxiliar', 'Auxiliar'), ('A1', 'A1'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3')], validators=[Optional()])
    dedicacion = SelectField('Dedicación', choices=[('', 'Seleccione...'), ('Exclusiva', 'Exclusiva'), ('Tiempo completo', 'Tiempo completo'), ('Tiempo parcial', 'Tiempo parcial')], validators=[Optional()])
    ID_CTI = StringField('ID CTI Vitae', validators=[Optional(), Length(max=50)])
    ID_Scopus = StringField('ID Scopus', validators=[Optional(), Length(max=50)])
    ID_ORCID = StringField('ID ORCID', validators=[Optional(), Length(max=50)])
    telefono_fijo = TelField('Teléfono Fijo', validators=[Optional(), Regexp(r'^\d{6,15}$', message="Número de teléfono inválido.")])
    movil = TelField('Teléfono Móvil', validators=[Optional(), Regexp(r'^\d{9}$', message="El móvil debe tener 9 dígitos.")])
    correo_personal = EmailField('Correo Personal', validators=[DataRequired(), Email()])
    correo_institucional = EmailField('Correo Institucional', validators=[Optional(), Email()])
    domicilio_actual = StringField('Domicilio Actual', validators=[Optional(), Length(max=200)])
    referencia = StringField('Referencia', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Guardar Cambios')

class GradostitulosForm(BaseCVForm):
    titulo = StringField('Denominación del Grado o Título', validators=[DataRequired(), Length(max=255)])
    tipo = SelectField('Tipo de Grado o Título', validators=[DataRequired()], choices=[...]) # Añade tus choices aquí
    pais = SelectField('País', validators=[DataRequired()])
    universidad = SelectField('Universidad', validators=[DataRequired()])
    otro_universidad = StringField('Otra Universidad', validators=[Optional(), Length(max=255)])
    otro_pais = StringField('Otro País', validators=[Optional(), Length(max=255)])
    fecha_expedicion = DateField('Fecha de Expedición', validators=[DataRequired()])
    # Campo de archivo extra para SUNEDU
    archivo_sunedu = FileField('Adjuntar Constancia SUNEDU (PDF)', validators=[Optional(), FileAllowed(['pdf'], 'Solo PDFs.')])

class ExperienciaDocenteForm(BaseCVForm):
    tipo = SelectField('Tipo de Experiencia', validators=[DataRequired()], choices=[('', 'Seleccione'), ('Movilidad Docente', 'Movilidad Docente'), ('Posgrado', 'Posgrado'), ('Docencia en Categoría', 'Docencia en Categoría')])
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(max=255)])
    anios = IntegerField('Años de Experiencia', validators=[DataRequired(), NumberRange(min=0)])
    cursos = IntegerField('Cantidad de Cursos', validators=[DataRequired(), NumberRange(min=0)])

class InvestigacionesForm(BaseCVForm):
    tipo = SelectField('Tipo de Investigación', validators=[DataRequired()], choices=[...])
    titulo = StringField('Denominación', validators=[DataRequired(), Length(max=255)])
    revista = StringField('Revista', validators=[DataRequired(), Length(max=255)])
    indice = SelectField('Índice', validators=[DataRequired()], choices=[...])
    fecha_publicacion = DateField('Fecha de Publicación', validators=[DataRequired()])
    autor = BooleanField('Autor')
    coautor = BooleanField('Coautor')

class ProduccionIntelectualForm(BaseCVForm):
    tipo = SelectField('Tipo de Producción', validators=[DataRequired()], choices=[...])
    titulo = StringField('Título', validators=[DataRequired(), Length(max=255)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=50)])
    deposito_legal = BooleanField('Depósito Legal')
    fecha_publicacion = DateField('Fecha de Publicación', validators=[Optional()])
    autor = BooleanField('Autor')
    coautor = BooleanField('Coautor')
    editorial_prestigiosa = SelectField('Editorial Prestigiosa', choices=[('No', 'No'), ('Scopus', 'Scopus'), ('Web of Science', 'Web of Science'), ('SciELO', 'SciELO')], default='No')

class ActualizacionesCapacitacionesForm(BaseCVForm):
    tipo = SelectField('Tipo de Capacitación', validators=[DataRequired()], choices=[...])
    descripcion = StringField('Denominación', validators=[DataRequired(), Length(max=255)])
    horas = IntegerField('Horas', validators=[Optional(), NumberRange(min=1)])
    creditos = IntegerField('Créditos', validators=[Optional(), NumberRange(min=0)])
    semestres_concluidos = IntegerField('Semestres Concluidos', validators=[Optional(), NumberRange(min=0)])
    institucion_otorga = StringField('Institución que Otorga', validators=[DataRequired(), Length(max=255)])
    fecha = DateField('Fecha', validators=[DataRequired()])

class CargosDirectivosForm(BaseCVForm):
    cargo = StringField('Cargo', validators=[DataRequired(), Length(max=100)])
    anios = IntegerField('Años en el Cargo', validators=[DataRequired(), NumberRange(min=0)])
    descripcion = StringField('Descripción', validators=[Optional(), Length(max=255)])

class ParticipacionTesisForm(BaseCVForm):
    tipo = SelectField('Tipo de Participación', validators=[DataRequired()], choices=[('Director', 'Director'), ('Asesor', 'Asesor'), ('Jurado', 'Jurado')])
    nivel = SelectField('Nivel', validators=[DataRequired()], choices=[('Pregrado', 'Pregrado'), ('Posgrado', 'Posgrado'), ('Otra', 'Otra')])
    descripcion = TextAreaField('Descripción (Título de la tesis, nombre del tesista)', validators=[DataRequired(), Length(max=255)])
    universidad = StringField('Universidad', validators=[Optional(), Length(max=255)])
    fecha = DateField('Fecha', validators=[DataRequired()])

class ReconocimientosForm(BaseCVForm):
    tipo = SelectField('Tipo de Reconocimiento', validators=[DataRequired()], choices=[...])
    descripcion = StringField('Descripción del Reconocimiento', validators=[DataRequired(), Length(max=255)])
    institucion = StringField('Nombre de la Institución', validators=[DataRequired(), Length(max=255)])
    tipo_institucion = SelectField('Tipo de Institución', validators=[DataRequired()], choices=[...])
    fecha = DateField('Fecha', validators=[DataRequired()])

class IdiomasForm(BaseCVForm):
    idioma = SelectField('Idioma', validators=[DataRequired()], choices=[...])
    otro_idioma = StringField('Otro Idioma', validators=[Optional(), Length(max=50)])
    nivel = SelectField('Nivel', validators=[DataRequired()], choices=[('Básico', 'Básico'), ('Intermedio', 'Intermedio'), ('Avanzado', 'Avanzado')])
    certificado = BooleanField('¿Posee Certificado?')

class SoftwareEspecializadoForm(BaseCVForm):
    nombre_curso = StringField('Nombre del Curso o Software', validators=[DataRequired(), Length(max=100)])
    modalidad = SelectField('Modalidad', choices=[('Presencial', 'Presencial'), ('Virtual', 'Virtual')])
    horas = IntegerField('Horas', validators=[Optional(), NumberRange(min=1)])
    institucion = StringField('Institución', validators=[Optional(), Length(max=100)])
    fecha = DateField('Fecha', validators=[DataRequired()])

class TutoriaForm(BaseCVForm):
    semestre = SelectField('Semestre', validators=[DataRequired()], choices=[...])
    # El campo 'archivo' ya está en la clase base

class CargaAcademicaLectivaForm(BaseCVForm):
    periodo_academico = SelectField('Período Académico', validators=[DataRequired()], choices=[...])
    numero_memorandum = StringField('Número de Memorándum', validators=[DataRequired(), Length(max=50)])
    horas_asignadas = IntegerField('Horas Asignadas', validators=[DataRequired(), NumberRange(min=1)])
    # Renombramos el campo de archivo para que sea más específico
    archivo_memorandum = FileField('Adjuntar Memorándum (PDF)', validators=[Optional(), FileAllowed(['pdf'], 'Solo PDFs.')])

class ParticipacionGestionUniversitariaForm(BaseCVForm):
    cargo = StringField('Cargo', validators=[DataRequired(), Length(max=255)])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', validators=[DataRequired()])
    # Aquí tenemos múltiples archivos, por lo que los definimos explícitamente
    adjuntar_plan = FileField('Adjuntar Plan', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'])])
    adjuntar_informe = FileField('Adjuntar Informe', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'])])
    adjuntar_curso = FileField('Adjuntar Certificado de Curso', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'])])

class AcreditacionLicenciamientoForm(BaseCVForm):
    numero_resolucion = StringField('Número de Resolución', validators=[DataRequired(), Length(max=100)])
    fecha_resolucion = DateField('Fecha de Resolución', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', validators=[DataRequired()])
    cargo_comite = SelectField('Cargo en Comité', validators=[DataRequired()], choices=[...])
    archivo_resolucion = FileField('Adjuntar Resolución (PDF)', validators=[Optional(), FileAllowed(['pdf'], 'Solo PDFs.')])
    evidencias = FileField('Adjuntar Evidencias (PDF)', validators=[Optional(), FileAllowed(['pdf'], 'Solo PDFs.')])

class ActividadesProyeccionSocialForm(BaseCVForm):
    Emitido_por = StringField('Emitido por', validators=[DataRequired(), Length(max=100)])
    fecha = DateField('Fecha', validators=[DataRequired()])

class EvaluacionDesempenoDocenteForm(BaseCVForm):
    periodo_academico_evaluado = StringField('Período Académico Evaluado', validators=[DataRequired(), Length(max=100)])
    categoria_docente = StringField('Categoría Docente', validators=[DataRequired(), Length(max=100)])
    promedio_evaluacion_general = DecimalField('Promedio General', validators=[DataRequired(), NumberRange(min=0, max=100)])
    promedio_evaluacion_autoridades = DecimalField('Promedio Autoridades', validators=[DataRequired(), NumberRange(min=0, max=100)])
    promedio_evaluacion_estudiantes = DecimalField('Promedio Estudiantes', validators=[DataRequired(), NumberRange(min=0, max=100)])
    informes_evaluacion = FileField('Adjuntar Resultados (PDF)', validators=[DataRequired(), FileAllowed(['pdf'], 'Solo PDFs.')])