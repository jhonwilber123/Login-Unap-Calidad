# src/models/ModelCV.py

import logging
import os
from MySQLdb.cursors import DictCursor # ¡IMPORTANTE! Para obtener resultados como diccionarios.

# Configuración del logging
logging.basicConfig(filename='flask_app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class ModelCV:
    """
    Clase modelo para gestionar toda la información del Currículum Vitae de los docentes.
    Centraliza todas las consultas a la base de datos relacionadas con el CV.
    """

    @classmethod
    def get_cv_completo_por_usuario(cls, db, user_id):
        """
        Recopila TODA la información de un docente desde todas las tablas relacionadas
        y la devuelve en un único diccionario estructurado.
        
        Este es el método principal para los reportes del administrador.
        """
        cv_data = {}
        try:
            # Usamos DictCursor para que los resultados sean diccionarios (row['columna'])
            # en lugar de tuplas (row[0]). ¡Es mucho más legible!
            cursor = db.connection.cursor(DictCursor)

            # 1. Datos Personales (es un solo registro)
            sql_dp = """
                SELECT dp.*, u.usuario as email_usuario, u.rol
                FROM datospersonales dp
                JOIN usuarios u ON dp.id_usuario = u.id_usuario
                WHERE dp.id_usuario = %s
            """
            cursor.execute(sql_dp, (user_id,))
            cv_data['datos_personales'] = cursor.fetchone()

            # Diccionario de tablas y sus consultas (Principio DRY)
            # Cada consulta hace un LEFT JOIN para traer la ruta del archivo adjunto.
            tablas_a_consultar = {
                'grados_titulos': "SELECT gt.*, ia.ruta_imagen, ias.ruta_imagen as ruta_imagen_sunedu FROM gradostitulos gt LEFT JOIN imagenesadjuntas ia ON gt.id_imagen = ia.id_imagen LEFT JOIN imagenesadjuntas ias ON gt.id_imagen_sunedu = ias.id_imagen WHERE gt.id_usuario = %s",
                'experiencia_docente': "SELECT ed.*, ia.ruta_imagen FROM experienciadocente ed LEFT JOIN imagenesadjuntas ia ON ed.id_imagen = ia.id_imagen WHERE ed.id_usuario = %s",
                'actualizaciones_capacitaciones': "SELECT ac.*, ia.ruta_imagen FROM actualizacionescapacitaciones ac LEFT JOIN imagenesadjuntas ia ON ac.id_imagen = ia.id_imagen WHERE ac.id_usuario = %s",
                'investigaciones': "SELECT i.*, ia.ruta_imagen FROM investigaciones i LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen WHERE i.id_usuario = %s",
                'produccion_intelectual': "SELECT pi.*, ia.ruta_imagen FROM produccionintelectual pi LEFT JOIN imagenesadjuntas ia ON pi.id_imagen = ia.id_imagen WHERE pi.id_usuario = %s",
                'cargos_directivos': "SELECT cd.*, ia.ruta_imagen FROM cargosdirectivos cd LEFT JOIN imagenesadjuntas ia ON cd.id_imagen = ia.id_imagen WHERE cd.id_usuario = %s",
                'participacion_tesis': "SELECT pt.*, ia.ruta_imagen FROM participaciontesis pt LEFT JOIN imagenesadjuntas ia ON pt.id_imagen = ia.id_imagen WHERE pt.id_usuario = %s",
                'reconocimientos': "SELECT r.*, ia.ruta_imagen FROM reconocimientos r LEFT JOIN imagenesadjuntas ia ON r.id_imagen = ia.id_imagen WHERE r.id_usuario = %s",
                'idiomas': "SELECT i.*, ia.ruta_imagen FROM idiomas i LEFT JOIN imagenesadjuntas ia ON i.id_imagen = ia.id_imagen WHERE i.id_usuario = %s",
                'software_especializado': "SELECT se.*, ia.ruta_imagen FROM softwareespecializado se LEFT JOIN imagenesadjuntas ia ON se.id_imagen = ia.id_imagen WHERE se.id_usuario = %s",
                'tutorias': "SELECT t.*, ia.ruta_imagen FROM tutorias t LEFT JOIN imagenesadjuntas ia ON t.id_imagen = ia.id_imagen WHERE t.id_usuario = %s",
                'carga_academica': "SELECT cal.*, ia.ruta_imagen as ruta_memorandum FROM carga_academica_lectiva cal LEFT JOIN imagenesadjuntas ia ON cal.id_memorandum = ia.id_imagen WHERE cal.id_usuario = %s",
                'participacion_gestion_universitaria': "SELECT pgu.*, plan.ruta_imagen as ruta_plan, informe.ruta_imagen as ruta_informe, curso.ruta_imagen as ruta_curso FROM participaciongestionuniversitaria pgu LEFT JOIN imagenesadjuntas plan ON pgu.adjuntar_plan = plan.id_imagen LEFT JOIN imagenesadjuntas informe ON pgu.adjuntar_informe = informe.id_imagen LEFT JOIN imagenesadjuntas curso ON pgu.adjuntar_curso = curso.id_imagen WHERE pgu.id_usuario = %s",
                'evaluacion_desempeno': "SELECT * FROM evaluacion_desempeno_docente WHERE id_usuario = %s",
                'acreditacion_licenciamiento': "SELECT al.*, res.ruta_imagen as ruta_resolucion, evi.ruta_imagen as ruta_evidencias FROM acreditacionlicenciamiento al LEFT JOIN imagenesadjuntas res ON al.id_imagen = res.id_imagen LEFT JOIN imagenesadjuntas evi ON al.id_imagen_evidencias = evi.id_imagen WHERE al.id_usuario = %s",
                'actividades_proyeccion_social': "SELECT aps.*, ia.ruta_imagen FROM actividadesproyeccionsocial aps LEFT JOIN imagenesadjuntas ia ON aps.id_imagen = ia.id_imagen WHERE aps.id_usuario = %s",
            }

            # 2. Consultar el resto de las tablas (que son registros múltiples)
            for nombre_tabla, sql in tablas_a_consultar.items():
                cursor.execute(sql, (user_id,))
                cv_data[nombre_tabla] = cursor.fetchall()
            
            cursor.close()
            return cv_data

        except Exception as ex:
            logging.error(f"Error en ModelCV.get_cv_completo_por_usuario para user_id {user_id}: {ex}")
            raise Exception("Error al recopilar los datos completos del docente.")

    # --- FUTUROS MÉTODOS CRUD ---
    # Aquí irían los métodos para que el DOCENTE gestione su propia información.
    # Por ejemplo, para la tabla 'gradostitulos'.
    
    @classmethod
    def crear_grado(cls, db, user_id, form_data):
        """
        Crea un nuevo registro de grado o título.
        (Este es un ejemplo, necesitará manejar la subida de archivos)
        """
        # ... Lógica para insertar en la tabla gradostitulos ...
        pass

    @classmethod
    def actualizar_grado(cls, db, grado_id, user_id, form_data):
        # ... Lógica para actualizar un registro en gradostitulos ...
        pass

    @classmethod
    def eliminar_grado(cls, db, upload_folder, grado_id, user_id):
        """
        Elimina un registro de grado y su archivo físico asociado.
        """
        try:
            cursor = db.connection.cursor(DictCursor)
            
            # 1. Obtener la ruta del archivo para poder borrarlo
            cursor.execute("SELECT id_imagen, id_imagen_sunedu FROM gradostitulos WHERE id_grado = %s AND id_usuario = %s", (grado_id, user_id))
            registro = cursor.fetchone()
            
            if not registro:
                raise Exception("Registro de grado no encontrado o no pertenece al usuario.")

            # Lógica para eliminar los archivos físicos asociados
            for key in ['id_imagen', 'id_imagen_sunedu']:
                if registro[key]:
                    cursor.execute("SELECT ruta_imagen FROM imagenesadjuntas WHERE id_imagen = %s", (registro[key],))
                    archivo = cursor.fetchone()
                    if archivo and archivo['ruta_imagen']:
                        try:
                            os.remove(os.path.join(upload_folder, archivo['ruta_imagen']))
                        except OSError as e:
                            logging.warning(f"No se pudo eliminar el archivo {archivo['ruta_imagen']}: {e}")
                    # Eliminar la entrada de la tabla de imágenes
                    cursor.execute("DELETE FROM imagenesadjuntas WHERE id_imagen = %s", (registro[key],))
            
            # 2. Eliminar el registro de la tabla principal
            cursor.execute("DELETE FROM gradostitulos WHERE id_grado = %s", (grado_id,))
            
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            db.connection.rollback()
            logging.error(f"Error al eliminar grado {grado_id}: {ex}")
            raise Exception("Error al eliminar el grado o título.")
            
    # Deberás crear métodos similares (crear_experiencia, obtener_experiencias, etc.)
    # para cada una de las secciones del CV a medida que refactorices el blueprint 'docente'.