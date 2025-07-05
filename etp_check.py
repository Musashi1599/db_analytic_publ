from pars import Table_parser
from datetime import datetime


def etp_month_rate(month, year):
        current_date = datetime.strptime(f'{year}-{month}-01', "%Y-%m-%d").date()
        tb = Table_parser
        sql = f'''SELECT * FROM sro'''
        tb.db_connect(Table_parser)
        cursor = tb.cursor
        cursor.execute(sql)
        sro_massiv = cursor.fetchall()

        final_list = []
        for el in sro_massiv:
            date = el[7].replace(day=1)
            if date == current_date:
                buffer_list = [el[6]] #ЭТП
                final_list.append(buffer_list)

        list1 = []

        for el in final_list:
             list1.append((tuple(el), final_list.count(el)))
            
        s1 = set(list1)
        a = [el for el in s1]
        list3 = sorted(a, key=lambda x: x[1], reverse=True)
        list4 = list3[0:10] 
        list5 = [f'{el[0][0]}: {el[1]}' for el in list4]
        mess = '\n'.join(list5)
        return mess