import mysql.connector


class BancoDeDados:
    def __init__(self):
        self.host = 'sql812.main-hosting.eu'
        self.user = 'u274908554_710A'
        self.password = 'INbd710A'
        self.database = 'u274908554_710A'
        self.connection = None
        self.cursor = None
    
    def conectar(self):
        
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("Conexão bem-sucedida!")
        
    
    def criar_cursor(self):
        if self.connection:
            self.cursor = self.connection.cursor()
            print("Cursor criado com sucesso!")
        else:
            print("Conexão não estabelecida. Não é possível criar o cursor.")
    
    # def fechar_cursor(self):
    #     if self.cursor:
    #         self.cursor.close()
    #         print("Cursor fechado com sucesso!")
    
    def commit(self): # Persistir os dados no banco de dados
        if self.connection:
            try: 
                self.connection.commit()
                print("Alterações confirmadas com sucesso!")
            except mysql.connector.Error as err:
                print(f"Erro ao tentar confirmar alterações: {err}")
        else:
            print("Conexão não estabelecida. Não é possível confirmar alterações.")
    
    
    def fechar_conexao(self):
        if self.connection:
            self.connection.close()
            print("Conexão fechada com sucesso!")
