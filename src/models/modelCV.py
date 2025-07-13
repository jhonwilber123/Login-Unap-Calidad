# src/models/ModelCV.py

import logging
import os
from MySQLdb.cursors import DictCursor

logging.basicConfig(filename='flask_app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class ModelCV:
    """
    Clase modelo para gestionar TODA la información del Currículum Vitae de los docentes.
    Utiliza métodos genéricos para reducir la duplicación de código y facilitar el mantenimiento.
    """

    # === MÉTODOS CRUD GENÉRICOS (LÓGICA CENTRAL) ===
    # (El código de los métodos _obtener_registros, _obtener_registro_por_id, _crear_registro, 
    # _actualizar_registro, y _eliminar_registro que te proporcioné anteriormente es correcto y va aquí)

    # === PEQUEÑA FUNCIÓN DE UTILIDAD INTERNA ===
    @staticmethod
    def _build_data_dict(form, **kwargs):
        """Construye un diccionario a partir de un objeto formulario y argumentos adicionales."""
        data = {key: getattr(form, key).data for key in form._fields if key not in ['csrf_token', 'submit']}
        # Eliminar campos que no son columnas de la BD si es necesario
        data.pop('archivo', None) 
        data.pop('archivo_sunedu', None)
        # Añadir o sobreescribir con kwargs
        data.update(kwargs)
        return data

    # ===============================================
    # === MÉTODOS PÚBLICOS COMPLETOS PARA CADA SECCIÓN ===
    # ===============================================

    # --- 1. Datos Personales ---
    @classmethod
    def obtener_datos_personales(cls, db, user_id):
        # ... (código que ya tienes)
        pass
    @classmethod
    def actualizar_datos_personales(cls, db, user_id, form, id_foto, id_constancia, datos_actuales):
        # ... (código que ya tienes)
        pass

    # --- 2. Grados y Títulos ---
    @classmethod
    def obtener_grados_por_usuario(cls, db, user_id):
        sql = "SELECT gt.*, ia.ruta_imagen, ias.ruta_imagen as ruta_imagen_sunedu FROM gradostitulos gt LEFT JOIN imagenesadjuntas ia ON gt.id_imagen = ia.id_imagen LEFT JOIN imagenesadjuntas ias ON gt.id_imagen_sunedu = ias.id_imagen WHERE gt.id_usuario = %s"
        return cls._obtener_registros(db, sql, user_id)
    @classmethod
    def crear_grado(cls, db, user_id, form, id_imagen, id_imagen_sunedu):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen, id_imagen_sunedu=id_imagen_sunedu)
        # Lógica especial para 'Otro'
        if data.get('pais') == 'Otro': data['pais'] = data.get('otro_pais')
        if data.get('universidad') == 'Otra': data['universidad'] = data.get('otro_universidad')
        data.pop('otro_pais', None); data.pop('otro_universidad', None)
        cls._crear_registro(db, 'gradostitulos', data)

    # --- 3. Experiencia Docente ---
    @classmethod
    def obtener_experiencias_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM experienciadocente WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_experiencia(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'experienciadocente', data)

    # --- 4. Investigaciones ---
    @classmethod
    def obtener_investigaciones_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM investigaciones WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_investigacion(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'investigaciones', data)

    # --- 5. Producción Intelectual ---
    @classmethod
    def obtener_producciones_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM produccionintelectual WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_produccion(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'produccionintelectual', data)

    # --- 6. Actualizaciones y Capacitaciones ---
    @classmethod
    def obtener_capacitaciones_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM actualizacionescapacitaciones WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_capacitacion(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'actualizacionescapacitaciones', data)

    # --- 7. Cargos Directivos ---
    @classmethod
    def obtener_cargos_directivos_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM cargosdirectivos WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_cargo_directivo(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'cargosdirectivos', data)

    # --- 8. Participación en Tesis ---
    @classmethod
    def obtener_participaciones_tesis_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM participaciontesis WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_participacion_tesis(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'participaciontesis', data)

    # --- 9. Reconocimientos y Distinciones ---
    @classmethod
    def obtener_reconocimientos_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM reconocimientos WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_reconocimiento(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'reconocimientos', data)

    # --- 10. Idiomas ---
    @classmethod
    def obtener_idiomas_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM idiomas WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_idioma(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        if data.get('idioma') == 'Otro': data['idioma'] = data.get('otro_idioma')
        data.pop('otro_idioma', None)
        cls._crear_registro(db, 'idiomas', data)

    # --- 11. Software Especializado ---
    @classmethod
    def obtener_softwares_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM softwareespecializado WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_software(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'softwareespecializado', data)

    # --- 12. Tutorías ---
    @classmethod
    def obtener_tutorias_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM tutorias WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_tutoria(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'tutorias', data)

    # --- 13. Carga Académica Lectiva ---
    @classmethod
    def obtener_cargas_academicas_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM carga_academica_lectiva WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_carga_academica(cls, db, user_id, form, id_memorandum):
        data = cls._build_data_dict(form, id_usuario=user_id, id_memorandum=id_memorandum)
        data.pop('archivo_memorandum', None)
        cls._crear_registro(db, 'carga_academica_lectiva', data)

    # --- 14. Participación en Gestión Universitaria ---
    @classmethod
    def obtener_gestiones_universitarias_por_usuario(cls, db, user_id):
        sql = "SELECT pgu.*, plan.ruta_imagen as ruta_plan, informe.ruta_imagen as ruta_informe, curso.ruta_imagen as ruta_curso FROM participaciongestionuniversitaria pgu LEFT JOIN imagenesadjuntas plan ON pgu.adjuntar_plan = plan.id_imagen LEFT JOIN imagenesadjuntas informe ON pgu.adjuntar_informe = informe.id_imagen LEFT JOIN imagenesadjuntas curso ON pgu.adjuntar_curso = curso.id_imagen WHERE pgu.id_usuario = %s"
        return cls._obtener_registros(db, sql, user_id)
    @classmethod
    def crear_gestion_universitaria(cls, db, user_id, form, id_plan, id_informe, id_curso):
        data = cls._build_data_dict(form, id_usuario=user_id, adjuntar_plan=id_plan, adjuntar_informe=id_informe, adjuntar_curso=id_curso)
        data.pop('adjuntar_plan', None); data.pop('adjuntar_informe', None); data.pop('adjuntar_curso', None)
        cls._crear_registro(db, 'participaciongestionuniversitaria', data)

    # --- 15. Acreditación y Licenciamiento ---
    @classmethod
    def obtener_acreditaciones_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM acreditacionlicenciamiento WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_acreditacion(cls, db, user_id, form, id_resolucion, id_evidencias):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_resolucion, id_imagen_evidencias=id_evidencias)
        data.pop('archivo_resolucion', None); data.pop('evidencias', None)
        cls._crear_registro(db, 'acreditacionlicenciamiento', data)

    # --- 16. Actividades de Proyección Social ---
    @classmethod
    def obtener_proyecciones_sociales_por_usuario(cls, db, user_id):
        return cls._obtener_registros(db, "SELECT * FROM actividadesproyeccionsocial WHERE id_usuario = %s", user_id)
    @classmethod
    def crear_proyeccion_social(cls, db, user_id, form, id_imagen):
        data = cls._build_data_dict(form, id_usuario=user_id, id_imagen=id_imagen)
        cls._crear_registro(db, 'actividadesproyeccionsocial', data)

    # --- MÉTODO PARA EL REPORTE DEL ADMIN (Asegúrate que esté completo) ---
    @classmethod
    def get_cv_completo_por_usuario(cls, db, user_id):
        cv_data = {}
        try:
            # Datos Personales
            cv_data['datos_personales'] = cls.obtener_datos_personales(db, user_id)
            
            # Datos de las demás tablas
            cv_data['grados_titulos'] = cls.obtener_grados_por_usuario(db, user_id)
            cv_data['experiencia_docente'] = cls.obtener_experiencias_por_usuario(db, user_id)
            cv_data['investigaciones'] = cls.obtener_investigaciones_por_usuario(db, user_id)
            cv_data['produccion_intelectual'] = cls.obtener_producciones_por_usuario(db, user_id)
            cv_data['actualizaciones_capacitaciones'] = cls.obtener_capacitaciones_por_usuario(db, user_id)
            cv_data['cargos_directivos'] = cls.obtener_cargos_directivos_por_usuario(db, user_id)
            cv_data['participacion_tesis'] = cls.obtener_participaciones_tesis_por_usuario(db, user_id)
            cv_data['reconocimientos'] = cls.obtener_reconocimientos_por_usuario(db, user_id)
            cv_data['idiomas'] = cls.obtener_idiomas_por_usuario(db, user_id)
            cv_data['software_especializado'] = cls.obtener_softwares_por_usuario(db, user_id)
            cv_data['tutorias'] = cls.obtener_tutorias_por_usuario(db, user_id)
            cv_data['carga_academica'] = cls.obtener_cargas_academicas_por_usuario(db, user_id)
            cv_data['participacion_gestion_universitaria'] = cls.obtener_gestiones_universitarias_por_usuario(db, user_id)
            cv_data['acreditacion_licenciamiento'] = cls.obtener_acreditaciones_por_usuario(db, user_id)
            cv_data['actividades_proyeccion_social'] = cls.obtener_proyecciones_sociales_por_usuario(db, user_id)
            
            return cv_data
        except Exception as ex:
            logging.error(f"Error al obtener CV completo para user_id {user_id}: {ex}")
            raise Exception("Error al recopilar los datos completos del docente.")