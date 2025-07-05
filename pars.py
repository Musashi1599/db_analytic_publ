import openpyxl
import os
import psycopg2 as ps
from datetime import date, datetime
import config
import re
    
class Table_parser:   
    report_month = int(str(datetime.today())[5:7])-1  #очень внимательно к этому быть, тк как только следующий месяц наступает, код может начинать сбоить там, где есть сравнение по месяцам, не сразу эту ошибку заметил, да и заметил случайно
    
    connection = ''
    cursor = ''
    def db_connect(self):
        self.connection = ps.connect(
            host = 'localhost',
            database = 'db1',
            user = 'postgres',
            password = '1234'
    )
        
        self.cursor = self.connection.cursor()

    def clear_and_create_table(self, path, column_names, column_type):
        Table_parser.db_connect(Table_parser)
        cursor = Table_parser.cursor
        wb = openpyxl.load_workbook(path)
        sheet = wb.active
        t1 = path.find('/')
        t2 = path.find('.')
        table_name = path[t1+1:t2]
        column_types = ', \n'.join(column_type)

        create_table = f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL,
{column_types}
        
)'''
         
        clear_table =  f'''TRUNCATE TABLE {table_name}'''
        cursor.execute(create_table)
        cursor.execute(clear_table)

        a1 = True
        i = 2  # Начальное значение перед циклом, потому что парс идет со 2 строки, не с первой(чтобы фильтрым можно было впихнуть при необходимости в экселе)
        while a1:
            counter = i - 1
            insert_list = []
            
            for j in range(1, len(column_names)+1):
                value = sheet.cell(row=i, column=j).value
                
                if value == 'stop':
                    a1 = False
                    break  # Выход из цикла for и while
                elif value is None or value == ' ':
                    insert_list.append(None)  # NULL в БД
                elif type(value) == str:
                    result = value.replace('  ', ' ')
                    insert_list.append(result)
                else:
                    insert_list.append(value)
            
            if not a1:
                break  
            
            # Одной командой INSERT
            columns = ', '.join(column_names)
            placeholders = ', '.join(['%s'] * len(column_names))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, insert_list)
            
            Table_parser.connection.commit()
            i += 1

    def add_to_table_without_clear(self):
        pass


    def table_reestr_pars(self, path):
        col_n = config.reestr_column_names
        col_t = config.reestr_column_types
        Table_parser.clear_and_create_table(Table_parser, path, col_n, col_t)
       

        
    def sro_pars(self, path):
        col_n = config.sro_column_names
        col_t = config.sro_column_types
        Table_parser.clear_and_create_table(Table_parser, path, col_n, col_t)

    


tb = Table_parser
reestr_path = os.getcwd()+'/reestr.xlsx'
sro_path = os.getcwd()+'/sro.xlsx'

#tb.table_reestr_pars(tb, reestr_path) #пока что прописывать вручную путь парса, а потом передавать его через интерфейс
# пока что выключил, чтобы не пересобирать её каждый раз

#tb.sro_pars(tb, sro_path)
# пропарсено с ноября по май, пока что не включать, с бд всё ок
#05/07 пропарсил с компа снова, тк были двойные пробелы и пришлось пересобрать БД через регулярки