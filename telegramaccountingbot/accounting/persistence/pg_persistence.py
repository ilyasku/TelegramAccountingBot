import psycopg2


class PGPersistence:

    def __init__(self, db_name, db_user):
        arg_str = "dbname={} user={}".format(db_name, db_user)
        self.connection = psycopg2.connect(arg_str)

    def get_dict_id_to_name(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        list_of_tuples = cursor.fetchall()
        cursor.close()
        dict_id_to_name = {}
        for t in list_of_tuples:
            dict_id_to_name[t[0]] = t[1]
        return dict_id_to_name

    def get_transactions(self, _id):
        cursor = self.connection.cursor()
        query_str = "SELECT * FROM transactions "
        query_str += "WHERE id = {}"
        query_str = query_str.format(_id)
        cursor.execute(query_str)        
        transactions = cursor.fetchall()
        cursor.close()
        l = []
        for trans in transactions:
            d_trans = {"id": trans[0], "value": trans[2],
                       "date": trans[1], "location": trans[3],
                       "comment": trans[4]}
            l.append(d_trans)
        return l

    def add_transaction(self, _id, value, date, location, comment=""):
        cursor = self.connection.cursor()
        insert_str = "INSERT INTO transactions VALUES ({}, '{}', {}, '{}', '{}');"
        insert_str = insert_str.format(_id, date, value, location, comment)
        cursor.execute(insert_str)
        self.connection.commit()
        cursor.close()

    def close_connection(self):
        self.connection.close()
        
