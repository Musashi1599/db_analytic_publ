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
                sum1 = sum(publish_cdt_last)+len(etp_none_cdt_last)
                sum2 = sum(publish_cdt_now)+len(etp_none_cdt_now)
                ratio_last = sum(publish_cdt_last) / sum1 if sum(publish_all_last) != 0 else 0
                ratio_now = sum(publish_cdt_now) / sum2 if sum(publish_all_now) != 0 else 0
                a = f'Прошлый месяц - ЦДТ - {sum(publish_cdt_last)}, всего - {sum1}, процент ЦДТ - {str(ratio_last*100)[0:5]}%'
                b = f'Отчетный месяц - ЦДТ - {sum(publish_cdt_now)}, всего - {sum2}, процент ЦДТ - {str(ratio_now*100)[0:5]}%'
                if ratio_last > ratio_now:
                    message_list[0].append(org_data[0][0]+'\n'+ record[4])
                    message_list[0].append(a)
                    message_list[0].append(b)
                    
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