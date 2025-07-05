from sro_check import sro_au_info, sro_send, sro_without_accr
from telebot import types
from telebot.util import split_string
from etp_check import etp_month_rate
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

def send_long_message(bot, chat_id, text, max_length=4096, **kwargs):
    """
    Отправляет длинное сообщение, разбивая его на части
    :param bot: объект TeleBot
    :param chat_id: ID чата
    :param text: текст сообщения
    :param max_length: максимальная длина части (по умолчанию 4096)
    :param kwargs: дополнительные параметры для send_message
    """
    for part in split_string(text, max_length):
        bot.send_message(chat_id, part, **kwargs)


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

        elif pre_pre_last_mess == 'Без аккредитации':
            long_mess = sro_without_accr(month_num, pre_last_mess)
            send_long_message(bot, message.chat.id, long_mess)

        elif pre_pre_last_mess == 'Статистика по ЭТП':
            mess = etp_month_rate(month_num, pre_last_mess)
            bot.send_message(message.chat.id, mess)

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
                date_select(bot, message, 'ассоциация арбитражных управляющих "сибирский центр экспертов антикризисного управления"', 'СЦЭАУ')
                
            case "НацАрбитр":
                date_select(bot, message, 'ассоциация "национальная организация арбитражных управляющих"', "НацАрбитр")
                
            case 'МЦПУ':
                date_select(bot, message, 'ассоциация саморегулируемая организация арбитражных управляющих "межрегиональный центр экспертов и профессиональных управляющих"', 'МЦПУ')

            case 'ДМСО':
                date_select(bot, message, 'ассоциация "дмсо" - ассоциация "дальневосточная межрегиональная саморегулируемая организация профессиональных арбитражных управляющих"', 'ДМСО')

            case 'Паритет':
                date_select(bot, message, 'саморегулируемая организация "ассоциация арбитражных управляющих "паритет"', 'Паритет')

            case 'САМРО':
                date_select(bot, message, 'саморегулируемая межрегиональная общественная организация "ассоциация антикризисных управляющих"', 'САМРО')

            case 'ВОЗРОЖДЕНИЕ':
                date_select(bot, message, 'союз арбитражных управляющих "возрождение"', 'ВОЗРОЖДЕНИЕ')

            case 'МЦАУ':
                date_select(bot, message, 'союз "мцау" - союз "межрегиональный центр арбитражных управляющих"', 'МЦАУ')

            case 'Альянс':
                date_select(bot, message, 'союз "соау "альянс" - союз "саморегулируемая организация арбитражных управляющих "альянс"', 'Альянс')

            case 'Южный Урал':
                date_select(bot, message, 'ассоциация "саморегулируемая организация арбитражных управляющих "южный урал"', 'Южный Урал')
                
            case 'Достояние':
                date_select(bot, message, 
                        'ассоциация вау "достояние" ассоциация ведущих арбитражных управляющих "достояние"',
                        'Достояние')

            case 'ПРАВОСОЗНАНИЕ':
                date_select(bot, message, 
                        'саморегулируемая организация союз "арбитражных управляющих "правосознание"',
                        'ПРАВОСОЗНАНИЕ')

            case 'ДЕЛО':
                date_select(bot, message, 
                        'союз арбитражных управляющих "саморегулируемая организация "дело"',
                        'ДЕЛО')

            case 'ЦФОП АПК':
                date_select(bot, message, 
                        'аау "цфоп апк" - ассоциация арбитражных управляющих "центр финансового оздоровления предприятий агропромышленного комплекса"',
                        'ЦФОП АПК')

            case 'Альянс управляющих':
                date_select(bot, message, 
                        'нпс сопау "альянс управляющих" - некоммерческое партнёрство - союз "межрегиональная саморегулируемая организация профессиональных арбитражных управляющих "альянс управляющих"',
                        'Альянс управляющих')

            case 'СРО ПАУ ЦФО':
                date_select(bot, message, 
                        'ассоциация "саморегулируемая организация арбитражных управляющих центрального федерального округа"',
                        'СРО ПАУ ЦФО')

            case 'Единство':
                date_select(bot, message, 
                        'ассоциация "км сро ау "единство" - ассоциация "краснодарская межрегиональная саморегулируемая организация арбитражных управляющих "единство"',
                        'Единство')

            case 'МСО ПАУ':
                date_select(bot, message, 
                        'ассоциация "межрегиональная саморегулируемая организация профессиональных арбитражных управляющих"',
                        'МСО ПАУ')

            case 'СИРИУС':
                date_select(bot, message, 
                        'ассоциация арбитражных управляющих "сириус"',
                        'СИРИУС')

            case 'Авангард':
                date_select(bot, message, 
                        'союз арбитражных управляющих "авангард"',
                        'Авангард')

            case 'Гарант':
                date_select(bot, message, 
                        'ассоциация профессиональных арбитражных управляющих "гарант"',
                        'Гарант')

            case 'Лидер':
                date_select(bot, message, 
                        'ассоциация саморегулируемая организация "объединение арбитражных управляющих "лидер"',
                        'Лидер')

            case 'Лига':
                date_select(bot, message, 
                        'ассоциация "саморегулируемая организация арбитражных управляющих "лига"',
                        'Лига')

            case 'Мск СОПАУ':
                date_select(bot, message, 
                        'ассоциация мсопау - ассоциация "московская саморегулируемая организация профессиональных арбитражных управляющих"',
                        'Мск СОПАУ')

            case 'Развитие':
                date_select(bot, message, 
                        'некоммерческое партнерство саморегулируемая организация арбитражных управляющих "развитие"',
                        'Развитие')

            case 'РСОПАУ':
                date_select(bot, message, 
                        'ассоциация "региональная саморегулируемая организация профессиональных арбитражных управляющих"',
                        'РСОПАУ')

            case 'Стратегия':
                date_select(bot, message, 
                        'союз «саморегулируемая организация арбитражных управляющих «стратегия»',
                        'Стратегия')

            case 'СоБР':
                date_select(bot, message, 
                        'ассоциация арбитражных управляющих "современные банкротные решения"',
                        'СоБР')

            case 'МЦПУ':
                date_select(bot, message, 
                        'ассоциация саморегулируемая организация арбитражных управляющих "межрегиональный центр экспертов и профессиональных управляющих"',
                        'МЦПУ')

            case 'СМиАУ':
                date_select(bot, message, 
                        'саморегулируемая организация "союз менеджеров и арбитражных управляющих"',
                        'СМиАУ')

            case 'СРО АУ СЗ':
                date_select(bot, message, 
                        'союз "саморегулируемая организация арбитражных управляющих северо-запада"',
                        'СРО АУ СЗ')

            case 'Синергия':
                date_select(bot, message, 
                        'сро аау "синергия" - саморегулируемая организация ассоциация арбитражных управляющих "синергия"',
                        'Синергия')

            case 'Содействие':
                date_select(bot, message, 
                        'ассоциация мсро "содействие" - ассоциация "межрегиональная саморегулируемая организация арбитражных управляющих "содействие"',
                        'Содействие')

            case 'ААУ Содружество':
                date_select(bot, message, 
                        'аау "содружество" - ассоциация арбитражных управляющих "содружество"',
                        'ААУ Содружество')

            case 'МСК ПАУ Содружество':
                date_select(bot, message, 
                        'ассоциация "межрегиональная северо-кавказская саморегулируемая организация профессиональных арбитражных управляющих "содружество"',
                        'МСК ПАУ Содружество')

            case 'ЦААУ':
                date_select(bot, message, 
                        'ассоциация арбитражных управляющих саморегулируемая организация "центральное агентство арбитражных управляющих"',
                        'ЦААУ')

            case 'Эгида':
                date_select(bot, message, 
                        'ассоциация саморегулируемая организация арбитражных управляющих "эгида"',
                        'Эгида')
                        
            case "Без аккредитации":
                date_select(bot, message)

            case 'Статистика по ЭТП':
                date_select(bot, message)



            #case "Тенденция по всем АУ за месяц":  пока что убрал и вырезал из кода в отдельный файл, много места занимает, а пользоваться не будут .скорее всего
                #mess_list = pars.tb.all_au_for_month(pars.tb)
                #print('отработала функция большая')
                #mess = 'Падение по сумме за месяц: \n'+'\n'.join(mess_list[0])+'\n\n'+'Уход на другие ЭТП:'+'\n'+'\n'.join(mess_list[1])
                #send_long_message(bot, message.chat.id, mess)