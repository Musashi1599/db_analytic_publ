import openpyxl
import os
import psycopg2 as ps
from datetime import date, datetime
import config

    
class Table_parser:   
    report_month = int(str(datetime.today())[5:7])-1 
    sro_names = [
    'Ассоциация арбитражных управляющих "СИБИРСКИЙ ЦЕНТР ЭКСПЕРТОВ АНТИКРИЗИСНОГО УПРАВЛЕНИЯ"',
    'Ассоциация "Национальная организация арбитражных управляющих"',
    'Ассоциация саморегулируемая организация арбитражных управляющих "Межрегиональный центр экспертов и профессиональных управляющих"',
    'Ассоциация "ДМСО" - Ассоциация "Дальневосточная межрегиональная саморегулируемая организация профессиональных арбитражных управляющих"',
    'Саморегулируемая организация "Ассоциация арбитражных управляющих "Паритет"',
    'Саморегулируемая межрегиональная общественная организация "Ассоциация антикризисных управляющих"',
    'СОЮЗ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ "ВОЗРОЖДЕНИЕ"',
    'Союз "МЦАУ" - Союз "Межрегиональный центр арбитражных управляющих"',
    'Союз "СОАУ "Альянс" - Союз "Саморегулируемая организация арбитражных управляющих "Альянс"',
    'Ассоциация "Саморегулируемая организация арбитражных управляющих "Южный Урал"',
    'Ассоциация ВАУ "Достояние" Ассоциация Ведущих Арбитражных Управляющих "Достояние"',
    'САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ СОЮЗ "АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ "ПРАВОСОЗНАНИЕ"',
    'Союз арбитражных управляющих "Саморегулируемая организация "ДЕЛО"',
    'ААУ "ЦФОП АПК" - Ассоциация арбитражных управляющих "Центр финансового оздоровления предприятий агропромышленного комплекса"',
    'НПС СОПАУ "Альянс управляющих" - Некоммерческое Партнёрство - Союз "Межрегиональная саморегулируемая организация профессиональных арбитражных управляющих "Альянс управляющих"',
    'АССОЦИАЦИЯ "САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ ЦЕНТРАЛЬНОГО ФЕДЕРАЛЬНОГО ОКРУГА"',
    'Ассоциация "КМ СРО АУ "Единство" - Ассоциация "Краснодарская межрегиональная саморегулируемая организация арбитражных управляющих "Единство"',
    'Ассоциация "Межрегиональная саморегулируемая организация арбитражных управляющих"',
    'Ассоциация арбитражных управляющих "СИРИУС"',
    'Союз арбитражных управляющих "Авангард"',
    'Ассоциация профессиональных арбитражных управляющих "Гарант"',
    'Ассоциация саморегулируемая организация "Объединение арбитражных управляющих "Лидер"',
    'Ассоциация "Саморегулируемая организация арбитражных управляющих "Лига"',
    'Ассоциация МСОПАУ - Ассоциация "Московская саморегулируемая организация профессиональных арбитражных управляющих"',
    'Некоммерческое партнерство Саморегулируемая организация арбитражных управляющих "РАЗВИТИЕ"',
    'Ассоциация "Региональная саморегулируемая организация профессиональных арбитражных управляющих"',
    'СОЮЗ «САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ «СТРАТЕГИЯ»',
    'Ассоциация арбитражных управляющих "Современные банкротные решения"',
    'Саморегулируемая организация "Союз менеджеров и арбитражных управляющих"',
    'СОЮЗ "САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ СЕВЕРО-ЗАПАДА"',
    'СРО ААУ "Синергия" - Саморегулируемая организация ассоциация арбитражных управляющих "Синергия"',
    'Ассоциация МСРО "Содействие" - Ассоциация "Межрегиональная саморегулируемая организация арбитражных управляющих "Содействие"',
    'ААУ "Содружество" - Ассоциация Арбитражных Управляющих "Содружество"',
    'Ассоциация "Межрегиональная Северо-Кавказская саморегулируемая организация профессиональных арбитражных управляющих "Содружество"',
    'Ассоциация арбитражных управляющих саморегулируемая организация "Центральное агентство арбитражных управляющих"',
    'Ассоциация саморегулируемая организация арбитражных управляющих "Эгида"'
]
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
        i = 2  # Начальное значение перед циклом
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

    def sro_au_info(self, sro_name):
        tb = Table_parser
        sql = f'''SELECT * FROM sro WHERE sro_name = '{sro_name}'
'''
        tb.db_connect(Table_parser)
        print(sro_name)
        cursor = tb.cursor
        cursor.execute(sql)
        sro_massiv = cursor.fetchall()
        name_set = set()
        name_etp_month_list = []
        name_etp_month_set = set()
        final_list = []
        for el in sro_massiv:
            name_set.add(el[1])
            date = el[7].replace(day=1)
            buffer_list = [el[1], el[6], el[9], date]
            name_etp_month_list.append(buffer_list)
            name_etp_month_set.add(tuple(buffer_list))

        for elem in name_etp_month_set:
            a = list(elem)
            a.append(name_etp_month_list.count(list(elem)))
            final_list.append(a)

        sorted_data = sorted(final_list, key=lambda x: x[0])

        report_list = []
        name_list = [element for element in name_set]

        for i in range(len(name_list)):
            list1 = []
            for j in range(len(final_list)):
                if name_list[i] in final_list[j]:
                    list1.append(final_list[j])

            list2 = sorted(list1, key=lambda x: x[2])    
            report_list.append(list2)


        file_path = os.getcwd()+'/report.xlsx'

        wb = openpyxl.Workbook()
        sheet = wb.active
        ws1 = wb.create_sheet('Падение')
        ws2 = wb.create_sheet('Уход')
        row_num = 2  # Начинаем со второй строки, чтобы в первую можно было врубить фильтры
        ws1_row_num = 2
        ws2_row_num = 2
        sheet.cell(row=1, column=1).value = 'ФИО АУ'
        sheet.cell(row=1, column=2).value = "ЭТП"
        sheet.cell(row=1, column=3).value = "Сумма"
        sheet.cell(row=1, column=3).value = 'Дата'  # Дата
        sheet.cell(row=1, column=4).value = 'Кол-во публикаций'
        message_list = [[], []]

        for org_data in report_list:  
            publish_all_last = []
            publish_cdt_last = []
            publish_all_now = []
            publish_cdt_now = []
            date_cdt_now = []
            date_cdt_last = []
            date_all_now = []
            etp_none_cdt_now = []
            etp_none_cdt_last = []
            etp_cdt_now = []
            etp_cdt_last = []
            sum_cdt_last = []
            sum_all_last = []
            sum_cdt_now = []
            sum_all_now = []
            for record in org_data:   
                sheet.cell(row=row_num, column=1).value = record[0]  # ФИО АУ
                sheet.cell(row=row_num, column=2).value = record[1]  # ETP
                sheet.cell(row=row_num, column=3).value = record[2] #сумма
                sheet.cell(row=row_num, column=3).value = record[3].strftime('%Y-%m-%d')  # Дата
                sheet.cell(row=row_num, column=4).value = record[4]  # Количество публикаций

                if 'ентр дистанционных торгов' in str(record[1]) and int(str(record[3])[5:7]) == tb.report_month:
                    publish_cdt_now.append(record[4])
                    date_cdt_now.append(str(record[3]))
                    sum_cdt_now.append(record[2])
                    etp_cdt_now.append(record[1])

                elif 'ентр дистанционных торгов' in str(record[1]) and tb.report_month - int(str(record[3])[5:7]) == 1:
                    publish_cdt_last.append(record[4])
                    date_cdt_last.append(str(record[3]))
                    sum_cdt_last.append(record[2])
                    etp_cdt_last.append(record[1])

                elif int(str(record[3])[5:7]) == tb.report_month:
                    etp_none_cdt_now.append(record[1])
                    publish_all_now.append(record[4])
                    date_all_now.append(str(record[3]))
                    sum_all_now.append(record[2])
                    
                elif tb.report_month - int(str(record[3])[5:7]) == 1:
                    publish_all_last.append(record[4])
                    etp_none_cdt_last.append(record[1])
                    
                row_num += 1



            if len(etp_none_cdt_now)>0 and len(etp_cdt_last) > 0 and len(etp_cdt_now) > 0:
                sum1 = sum(publish_cdt_last)+len(etp_none_cdt_last)
                sum2 = sum(publish_cdt_now)+len(etp_none_cdt_now)
                ratio_last = sum(publish_cdt_last) / sum1 if sum(publish_all_last) != 0 else 0
                ratio_now = sum(publish_cdt_now) / sum2 if sum(publish_all_now) != 0 else 0
                if ratio_last > ratio_now:
                    a = f'Прошлый месяц - ЦДТ - {sum(publish_cdt_last)}, всего - {sum1}, процент ЦДТ - {str(ratio_last*100)[0:5]}%'
                    b = f'Отчетный месяц - ЦДТ - {sum(publish_cdt_now)}, всего - {sum2}, процент ЦДТ - {str(ratio_now*100)[0:5]}%'
                    ws1.cell(row=1, column=1).value = 'ФИО АУ'
                    ws1.cell(row=1, column=2).value = 'Прошлый месяц'
                    ws1.cell(row=1, column=3).value = 'Отчётный месяц'
                    ws1.cell(row=ws1_row_num, column=1).value = org_data[0][0]
                    ws1.cell(row=ws1_row_num, column=2).value = a
                    ws1.cell(row=ws1_row_num, column=3).value = b
                    message_list[0].append(org_data[0][0])
                    message_list[0].append(a)
                    message_list[0].append(b)
                    
                    ws1_row_num += 1


            if len(date_cdt_last) > 0 and len(date_cdt_now) == 0 and len(date_all_now) > 0:
                ws2.cell(row=1, column=1).value = 'ФИО АУ'
                ws2.cell(row=1, column=2).value = 'ЭТП, куда перешел в этом месяце'
                ws2.cell(row=ws2_row_num, column=1).value = org_data[0][0]
                ws2.cell(row=ws2_row_num, column=2).value = ', '.join(etp_none_cdt_now)
                ws2_row_num += 1
                message_list[1].append(org_data[0][0]+':')
                etp_set = set()
                for i in range(len(etp_none_cdt_now)):
                    a = (etp_none_cdt_now[i], etp_none_cdt_now.count(etp_none_cdt_now[i]))
                    etp_set.add(a)
                etp_list = [list(el) for el in etp_set]

                for j in range(len(etp_list)):
                    message_list[1].append(f'{etp_list[j][0]}: {etp_list[j][1]}')

                message_list[1].append('\n')

        wb.save(file_path)
        return message_list

    def all_au_for_month(self):
        tb = Table_parser

        sql = f'''SELECT * FROM sro WHERE sro_name = ANY(%s)
'''
        tb.db_connect(Table_parser)
        
        cursor = tb.cursor
        cursor.execute(sql, (tb.sro_names,))
        sro_massiv = cursor.fetchall()
        name_set = set()
        name_etp_month_list = []
        name_etp_month_set = set()
        final_list = []
        for el in sro_massiv:
            name_set.add(el[1])
            date = el[7].replace(day=1)
            buffer_list = [el[1], el[6], el[9], date, el[5]]
            name_etp_month_list.append(buffer_list)
            name_etp_month_set.add(tuple(buffer_list))

        for elem in name_etp_month_set:
            a = list(elem)
            a.append(name_etp_month_list.count(list(elem)))
            final_list.append(a)

        sorted_data = sorted(final_list, key=lambda x: x[0])

        report_list = []
        name_list = [element for element in name_set]

        for i in range(len(name_list)):
            list1 = []
            for j in range(len(final_list)):
                if name_list[i] in final_list[j]:
                    list1.append(final_list[j])

            list2 = sorted(list1, key=lambda x: x[2])    
            report_list.append(list2)   

        message_list = [[], []]

        for org_data in report_list:  
            publish_all_last = []
            publish_cdt_last = []
            publish_all_now = []
            publish_cdt_now = []
            date_cdt_now = []
            date_cdt_last = []
            date_all_now = []
            etp_none_cdt_now = []
            etp_none_cdt_last = []
            etp_cdt_now = []
            etp_cdt_last = []
            sum_cdt_last = []
            sum_all_last = []
            sum_cdt_now = []
            sum_all_now = []
            for record in org_data:   
                if 'ентр дистанционных торгов' in str(record[1]) and int(str(record[3])[5:7]) == tb.report_month:
                    publish_cdt_now.append(record[5])
                    date_cdt_now.append(str(record[3]))
                    sum_cdt_now.append(record[2])
                    etp_cdt_now.append(record[1])

                elif 'ентр дистанционных торгов' in str(record[1]) and tb.report_month - int(str(record[3])[5:7]) == 1:
                    publish_cdt_last.append(record[5])
                    date_cdt_last.append(str(record[3]))
                    sum_cdt_last.append(record[2])
                    etp_cdt_last.append(record[1])

                elif int(str(record[3])[5:7]) == tb.report_month:
                    etp_none_cdt_now.append(record[1])
                    publish_all_now.append(record[5])
                    date_all_now.append(str(record[3]))
                    sum_all_now.append(record[2])
                    
                elif tb.report_month - int(str(record[3])[5:7]) == 1:
                    publish_all_last.append(record[5])
                    etp_none_cdt_last.append(record[1])
                    

            if len(etp_none_cdt_now)>0 and len(etp_cdt_last) > 0 and len(etp_cdt_now) > 0:
                ratio_last = sum(publish_cdt_last) / (sum(publish_cdt_last)+sum(publish_all_last)) if sum(publish_all_last) != 0 else 0
                ratio_now = sum(publish_cdt_now) / (sum(publish_cdt_now)+sum(publish_all_now)) if sum(publish_all_now) != 0 else 0
                if ratio_last > ratio_now:
                    message_list[0].append(org_data[0][0]+'\n'+ record[4])
                    message_list[0].append(f'Прошлый месяц - ЦДТ - {publish_cdt_last}, всего - {publish_all_last}, процент ЦДТ - {ratio_last}%')
                    message_list[0].append(f'Отчетный месяц - ЦДТ -{publish_cdt_now}, всего - {publish_all_now}, процент цдт - {ratio_now}%')
                    
            if len(date_cdt_last) > 0 and len(date_cdt_now) == 0 and len(date_all_now) > 0:
                message_list[1].append(org_data[0][0]+'\n'+record[4]+':')
                etp_set = set()
                for i in range(len(etp_none_cdt_now)):
                    a = (etp_none_cdt_now[i], etp_none_cdt_now.count(etp_none_cdt_now[i]))
                    etp_set.add(a)
                etp_list = [list(el) for el in etp_set]

                for j in range(len(etp_list)):
                    message_list[1].append(f'{etp_list[j][0]}: {etp_list[j][1]}')

                message_list[1].append('\n')

        return message_list

tb = Table_parser
reestr_path = os.getcwd()+'/reestr.xlsx'
sro_path = os.getcwd()+'/sro.xlsx'

#tb.table_reestr_pars(tb, reestr_path) #пока что прописывать вручную путь парса, а потом передавать его через интерфейс
# пока что выключил, чтобы не пересобирать её каждый раз

# tb.sro_pars(tb, sro_path)
# пропарсено с ноября по май, пока что не включать, с бд всё ок
