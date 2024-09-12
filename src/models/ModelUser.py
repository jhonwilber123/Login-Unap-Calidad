from .entities.User import User

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            # Cambié 'user' por 'personal'
            sql = """SELECT id, username, password, fullname FROM personal 
                     WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row is not None:
                # Verificar si la tupla tiene los elementos esperados
                if len(row) == 4:
                    user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                    return user
                else:
                    print("Error: La consulta no devolvió los 4 elementos esperados.")
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            # Cambié 'user' por 'personal'
            sql = "SELECT id, username, fullname FROM personal WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row is not None:
                # Verificar si la tupla tiene los elementos esperados
                if len(row) == 3:
                    return User(row[0], row[1], None, row[2])
                else:
                    print("Error: La consulta no devolvió los 3 elementos esperados.")
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
