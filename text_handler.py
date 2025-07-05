from sro_check import sro_au_info, sro_send, sro_without_accr
from telebot import types
import config
import pars

pre_pre_last_mess = ''
pre_last_mess = ''
last_mess = ''
sro_name = ''
full_sro_name = ''
#Контекст запроса обрабатываю сохранением тремя сообщений последних. Почему не аппенд в один список? Чтобы ОЗУ на ровном месте и без особого смысла не загружать
years = ['2023', '2024', '2025']
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

def last_mess_foo(message):
    global pre_pre_last_mess, pre_last_mess, last_mess
    pre_pre_last_mess = pre_last_mess
    pre_last_mess = last_mess
    last_mess = message

def date_select(bot, message, f_sro_name=' ', s_name=' '):
    global full_sro_name, sro_name
    sro_name = s_name
    full_sro_name = f_sro_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('2024')
    btn2 = types.KeyboardButton('2025')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выбор года:", reply_markup=markup)

def text(bot, message):   
    last_mess_foo(message.text)
    
    if message.text in years:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [types.KeyboardButton(month) for month in months]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Выберите месяц:", reply_markup=markup)
    
    elif message.text in months:
        month_num = months.index(message.text)+1
        #сюда потом добавить проверку, если пре_пре_ласт сообщение в сро неймс, то этот запрос по сро отчету и что выполнялось это, тк я потом это буду юзать и для других функций
        print(pre_pre_last_mess)
        print
        if pre_pre_last_mess == sro_name: 
            message_list = sro_au_info(full_sro_name, month_num, pre_last_mess)
            sro_send(bot, message_list, message, sro_name)
        else:
            sro_without_accr(month_num, pre_last_mess)


    else:
        match message.text:
            case 'Статистика по СРО':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("С аккредитацией")
                btn2 = types.KeyboardButton("Без аккредитации")
                markup.add(btn1, btn2)
                bot.send_message(message.chat.id, "Наличие аккредитации у ЦДТ в СРО:", reply_markup=markup)

            case 'С аккредитацией':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn0 = types.KeyboardButton("Авангард")
                btn1 = types.KeyboardButton("Альянс")
                btn2 = types.KeyboardButton("Альянс управляющих")
                btn3 = types.KeyboardButton("ВОЗРОЖДЕНИЕ")
                btn4 = types.KeyboardButton("Гарант")
                btn5 = types.KeyboardButton("ДЕЛО")
                btn6 = types.KeyboardButton("ДМСО")
                btn7 = types.KeyboardButton("Достояние")
                btn8 = types.KeyboardButton("Единство")
                btn9 = types.KeyboardButton("Континент")
                btn10 = types.KeyboardButton("Лидер")
                btn11 = types.KeyboardButton("Лига")
                btn12 = types.KeyboardButton("Мск СОПАУ")
                btn13 = types.KeyboardButton("МСО ПАУ")
                btn14 = types.KeyboardButton("МЦАУ")
                btn15 = types.KeyboardButton("НацАрбитр")
                btn16 = types.KeyboardButton("Паритет")
                btn17 = types.KeyboardButton("ПРАВОСОЗНАНИЕ")
                btn18 = types.KeyboardButton("Развитие")
                btn19 = types.KeyboardButton("РСОПАУ")
                btn20 = types.KeyboardButton("Стратегия")
                btn21 = types.KeyboardButton("СоБР")
                btn22 = types.KeyboardButton("МЦПУ")
                btn23 = types.KeyboardButton("СМиАУ")
                btn24 = types.KeyboardButton("СРО АУ СЗ")
                btn25 = types.KeyboardButton("Синергия")
                btn26 = types.KeyboardButton("Содействие")
                btn27 = types.KeyboardButton("ААУ Содружество")
                btn28 = types.KeyboardButton("МСК ПАУ Содружество")
                btn29 = types.KeyboardButton("САМРО")
                btn30 = types.KeyboardButton("СИРИУС")
                btn31 = types.KeyboardButton("СРО ПАУ ЦФО")
                btn32 = types.KeyboardButton("СЦЭАУ")   
                btn33 = types.KeyboardButton("ЦФОП АПК")
                btn34 = types.KeyboardButton("ЦААУ")
                btn35 = types.KeyboardButton("Южный Урал")
                btn36 = types.KeyboardButton("Эгида")
                
                
                markup.add(btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18, btn19, btn20, btn21, btn22, btn23, btn24, btn25, btn26, btn27, btn28, btn29, btn30, btn31, btn32, btn33, btn34, btn35, btn36)
        
                bot.send_message(message.chat.id, "Выберите СРО:", reply_markup=markup)

            
            case "СЦЭАУ":
                date_select(bot, message, 'Ассоциация арбитражных управляющих "СИБИРСКИЙ ЦЕНТР ЭКСПЕРТОВ АНТИКРИЗИСНОГО УПРАВЛЕНИЯ"', 'СЦЭАУ')
                
            case "НацАрбитр":
                date_select(bot, message, 'Ассоциация "Национальная организация арбитражных управляющих"', "НацАрбитр")
                
            case 'МЦПУ':
                date_select(bot, message, 'Ассоциация саморегулируемая организация арбитражных управляющих "Межрегиональный центр экспертов и профессиональных управляющих"', 'МЦПУ')

            case 'ДМСО':
                date_select(bot, message, 'Ассоциация "ДМСО" - Ассоциация "Дальневосточная межрегиональная саморегулируемая организация профессиональных арбитражных управляющих"', 'ДМСО')
            
            case 'Паритет':
                date_select(bot, message, 'Саморегулируемая организация "Ассоциация арбитражных управляющих "Паритет"', 'Паритет')

            case 'САМРО':
                date_select(bot, message, 'Саморегулируемая межрегиональная общественная организация "Ассоциация антикризисных управляющих"', 'САМРО')

            case 'ВОЗРОЖДЕНИЕ':
                date_select(bot, message, 'СОЮЗ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ "ВОЗРОЖДЕНИЕ"', 'ВОЗРОЖДЕНИЕ')

            case 'МЦАУ':
                date_select(bot, message, 'Союз "МЦАУ" - Союз "Межрегиональный центр арбитражных управляющих"', 'МЦАУ')
    
            case 'Альянс':
                date_select(bot, message, 'Союз "СОАУ "Альянс" - Союз "Саморегулируемая организация арбитражных управляющих "Альянс"', 'Альянс')

            case 'Южный Урал':
                date_select(bot, message, 'Ассоциация "Саморегулируемая организация арбитражных управляющих "Южный Урал"', 'Южный Урал')
                
            case 'Достояние':
                date_select(bot, message, 
                        'Ассоциация ВАУ "Достояние" Ассоциация Ведущих Арбитражных Управляющих "Достояние"',
                        'Достояние')

            case 'ПРАВОСОЗНАНИЕ':
                date_select(bot, message, 
                        'САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ СОЮЗ "АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ "ПРАВОСОЗНАНИЕ"',
                        'ПРАВОСОЗНАНИЕ')

            case 'ДЕЛО':
                date_select(bot, message, 
                        'Союз арбитражных управляющих "Саморегулируемая организация "ДЕЛО"',
                        'ДЕЛО')

            case 'ЦФОП АПК':
                date_select(bot, message, 
                        'ААУ "ЦФОП АПК" - Ассоциация арбитражных управляющих "Центр финансового оздоровления предприятий агропромышленного комплекса"',
                        'ЦФОП АПК')

            case 'Альянс управляющих':
                date_select(bot, message, 
                        'НПС СОПАУ "Альянс управляющих" - Некоммерческое Партнёрство - Союз "Межрегиональная саморегулируемая организация профессиональных арбитражных управляющих "Альянс управляющих"',
                        'Альянс управляющих')

            case 'СРО ПАУ ЦФО':
                date_select(bot, message, 
                        'АССОЦИАЦИЯ "САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ ЦЕНТРАЛЬНОГО ФЕДЕРАЛЬНОГО ОКРУГА"',
                        'СРО ПАУ ЦФО')

            case 'Единство':
                date_select(bot, message, 
                        'Ассоциация "КМ СРО АУ "Единство" - Ассоциация "Краснодарская межрегиональная саморегулируемая организация арбитражных управляющих "Единство"',
                        'Единство')

            case 'МСО ПАУ':
                date_select(bot, message, 
                        'Ассоциация "Межрегиональная саморегулируемая организация арбитражных управляющих"',
                        'МСО ПАУ')

            case 'СИРИУС':
                date_select(bot, message, 
                        'Ассоциация арбитражных управляющих "СИРИУС"',
                        'СИРИУС')

            case 'Авангард':
                date_select(bot, message, 
                        'Союз арбитражных управляющих "Авангард"',
                        'Авангард')

            case 'Гарант':
                date_select(bot, message, 
                        'Ассоциация профессиональных арбитражных управляющих "Гарант"',
                        'Гарант')

            case 'Лидер':
                date_select(bot, message, 
                        'Ассоциация саморегулируемая организация "Объединение арбитражных управляющих "Лидер"',
                        'Лидер')

            case 'Лига':
                date_select(bot, message, 
                        'Ассоциация "Саморегулируемая организация арбитражных управляющих "Лига"',
                        'Лига')

            case 'Мск СОПАУ':
                date_select(bot, message, 
                        'Ассоциация МСОПАУ - Ассоциация "Московская саморегулируемая организация профессиональных арбитражных управляющих"',
                        'Мск СОПАУ')

            case 'Развитие':
                date_select(bot, message, 
                        'Некоммерческое партнерство Саморегулируемая организация арбитражных управляющих "РАЗВИТИЕ"',
                        'Развитие')

            case 'РСОПАУ':
                date_select(bot, message, 
                        'Ассоциация "Региональная саморегулируемая организация профессиональных арбитражных управляющих"',
                        'РСОПАУ')

            case 'Стратегия':
                date_select(bot, message, 
                        'СОЮЗ «САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ «СТРАТЕГИЯ»',
                        'Стратегия')

            case 'СоБР':
                date_select(bot, message, 
                        'Ассоциация арбитражных управляющих "Современные банкротные решения"',
                        'СоБР')

            case 'МЦПУ':
                date_select(bot, message, 
                        'Ассоциация саморегулируемая организация арбитражных управляющих "Межрегиональный центр экспертов и профессиональных управляющих"',
                        'МЦПУ')

            case 'СМиАУ':
                date_select(bot, message, 
                        'Саморегулируемая организация "Союз менеджеров и арбитражных управляющих"',
                        'СМиАУ')

            case 'СРО АУ СЗ':
                date_select(bot, message, 
                        'СОЮЗ "САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ СЕВЕРО-ЗАПАДА"',
                        'СРО АУ СЗ')

            case 'Синергия':
                date_select(bot, message, 
                        'СРО ААУ "Синергия" - Саморегулируемая организация ассоциация арбитражных управляющих "Синергия"',
                        'Синергия')

            case 'Содействие':
                date_select(bot, message, 
                        'Ассоциация МСРО "Содействие" - Ассоциация "Межрегиональная саморегулируемая организация арбитражных управляющих "Содействие"',
                        'Содействие')

            case 'ААУ Содружество':
                date_select(bot, message, 
                        'ААУ "Содружество" - Ассоциация Арбитражных Управляющих "Содружество"',
                        'ААУ Содружество')

            case 'МСК ПАУ Содружество':
                date_select(bot, message, 
                        'Ассоциация "Межрегиональная Северо-Кавказская саморегулируемая организация профессиональных арбитражных управляющих "Содружество"',
                        'МСК ПАУ Содружество')

            case 'ЦААУ':
                date_select(bot, message, 
                        'Ассоциация арбитражных управляющих саморегулируемая организация "Центральное агентство арбитражных управляющих"',
                        'ЦААУ')

            case 'Эгида':
                date_select(bot, message, 
                        'Ассоциация саморегулируемая организация арбитражных управляющих "Эгида"',
                        'Эгида')

            #case "Тенденция по всем АУ за месяц":  пока что убрал и вырезал из кода в отдельный файл, много места занимает, а пользоваться не будут .скорее всего
            #    mess_list = pars.tb.all_au_for_month(pars.tb)
            #   print('отработала функция большая')
            #  mess = 'Падение по сумме за месяц: \n'+'\n'.join(mess_list[0])+'\n\n'+'Уход на другие ЭТП:'+'\n'+'\n'.join(mess_list[1])
            #    send_long_message(bot, message.chat.id, mess)

            case "Без аккредитации":
                date_select(bot, message)
