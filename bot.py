import telebot
import pars
import os
from telebot import types
from telebot.util import split_string
from config import token

bot = telebot.TeleBot(token)

last_message_id = None
last_message_text =''
zad_mess = ''
running = True
first_name = ''


def bot_start():
    while running:
        bot.infinity_polling(timeout=10, long_polling_timeout = 5)

def send_mess(chat_id, message, markup) -> None:
    global last_message_id
    global last_message_text

    mess = bot.send_message(chat_id=chat_id, text=message, reply_markup=markup)
    last_message_id = mess.message_id
    last_message_text = message

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


def create_buttons(*args):
    markup = types.InlineKeyboardMarkup()
    half_len = int(len(args)/2)
    for i in range(half_len):
        if 'http' in args[i+half_len]:
            markup.add(types.InlineKeyboardButton(args[i], url=args[i+half_len]))
        else:    
            markup.add(types.InlineKeyboardButton(args[i],callback_data=args[(i+half_len)]))

    return markup

def sro_send(mess_list, message, name):
    mess = 'Падение за месяц: \n'+'\n'.join(mess_list[0])+'\n\n'+'Уход на другие ЭТП:'+'\n'+'\n'.join(mess_list[1])
    bot.send_message(message.chat.id, mess)
    sro_path = os.getcwd()+'/report.xlsx'
    with open(f'{sro_path}',"rb") as file:
        f=file.read()
        bot.send_document(message.chat.id, f, visible_file_name=f"{name}.xlsx")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Тенденция по участникам СРО")
    btn2 = types.KeyboardButton("Тенденция по всем АУ за месяц")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types='text')
def text(message):
    match message.text:
        case 'Тенденция по участникам СРО':
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
            name = 'СЦЭАУ'
            message_list = message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация арбитражных управляющих "СИБИРСКИЙ ЦЕНТР ЭКСПЕРТОВ АНТИКРИЗИСНОГО УПРАВЛЕНИЯ"')
            sro_send(message_list, message, name)

        case "НацАрбитр":
            name = 'НацАрбитр'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "Национальная организация арбитражных управляющих"')
            sro_send(message_list, message, name)

        case 'МЦПУ':
            name = 'МЦПУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация саморегулируемая организация арбитражных управляющих "Межрегиональный центр экспертов и профессиональных управляющих"')
            sro_send(message_list, message, name)

        case 'ДМСО':
            name = 'ДМСО'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "ДМСО" - Ассоциация "Дальневосточная межрегиональная саморегулируемая организация профессиональных арбитражных управляющих"')
            sro_send(message_list, message, name)


        case 'Паритет':
            name = 'Паритет'
            message_list = pars.tb.sro_au_info(pars.tb, 'Саморегулируемая организация "Ассоциация арбитражных управляющих "Паритет"')
            sro_send(message_list, message, name)


        case 'САМРО':
            name = 'САМРО'
            message_list = pars.tb.sro_au_info(pars.tb, 'Саморегулируемая межрегиональная общественная организация "Ассоциация антикризисных управляющих"')
            sro_send(message_list, message, name)

        case 'ВОЗРОЖДЕНИЕ':
            name = 'ВОЗРОЖДЕНИЕ'
            message_list = pars.tb.sro_au_info(pars.tb, 'СОЮЗ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ "ВОЗРОЖДЕНИЕ"')
            sro_send(message_list, message, name)

        case 'МЦАУ':
            name = 'МЦАУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Союз "МЦАУ" - Союз "Межрегиональный центр арбитражных управляющих"')
            sro_send(message_list, message, name)
  

        case 'Альянс':
            name = 'Альянс'
            message_list = pars.tb.sro_au_info(pars.tb, 'Союз "СОАУ "Альянс" - Союз "Саморегулируемая организация арбитражных управляющих "Альянс"')
            sro_send(message_list, message, name)
 
        case 'Южный Урал':
            name = 'Южный Урал'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "Саморегулируемая организация арбитражных управляющих "Южный Урал"')
            sro_send(message_list, message, name)
  

        case 'Достояние':
            name = 'Достояние'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация ВАУ "Достояние" Ассоциация Ведущих Арбитражных Управляющих "Достояние"')
            sro_send(message_list, message, name)


        case 'ПРАВОСОЗНАНИЕ':
            name = 'ПРАВОСОЗНАНИЕ'
            message_list = pars.tb.sro_au_info(pars.tb, 'САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ СОЮЗ "АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ "ПРАВОСОЗНАНИЕ"')
            sro_send(message_list, message, name)

        case 'ДЕЛО':
            name = 'ДЕЛО'
            message_list = pars.tb.sro_au_info(pars.tb, 'Союз арбитражных управляющих "Саморегулируемая организация "ДЕЛО"')
            sro_send(message_list, message, name)

        case 'ЦФОП АПК':
            name = 'ЦФОП АПК'
            message_list = pars.tb.sro_au_info(pars.tb, 'ААУ "ЦФОП АПК" - Ассоциация арбитражных управляющих "Центр финансового оздоровления предприятий агропромышленного комплекса"')
            sro_send(message_list, message, name)

        case 'Альянс управляющих':
            name = 'Альянс управляющих'
            message_list = pars.tb.sro_au_info(pars.tb, 'НПС СОПАУ "Альянс управляющих" - Некоммерческое Партнёрство - Союз "Межрегиональная саморегулируемая организация профессиональных арбитражных управляющих "Альянс управляющих"')
            sro_send(message_list, message, name) 

        case 'СРО ПАУ ЦФО':
            name = 'СРО ПАУ ЦФО'
            message_list = pars.tb.sro_au_info(pars.tb, 'АССОЦИАЦИЯ "САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ ЦЕНТРАЛЬНОГО ФЕДЕРАЛЬНОГО ОКРУГА"')
            sro_send(message_list, message, name)

        case 'Единство':
            name = 'Единство'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "КМ СРО АУ "Единство" - Ассоциация "Краснодарская межрегиональная саморегулируемая организация арбитражных управляющих "Единство"')
            sro_send(message_list, message, name)   

        case 'МСО ПАУ':
            name = 'МСО ПАУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "Межрегиональная саморегулируемая организация арбитражных управляющих"')
            sro_send(message_list, message, name)
   
        case 'СИРИУС':
            name = 'СИРИУС'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация арбитражных управляющих "СИРИУС"')
            sro_send(message_list, message, name)

        case 'Авангард':
            name = 'СИРИУС'
            message_list = pars.tb.sro_au_info(pars.tb, 'Союз арбитражных управляющих "Авангард"')
            sro_send(message_list, message, name)

        case 'Гарант':
            name = 'Гарант'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация профессиональных арбитражных управляющих "Гарант"')
            sro_send(message_list, message, name)

        case 'Лидер':
            name = 'Лидер'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация саморегулируемая организация "Объединение арбитражных управляющих "Лидер"')
            sro_send(message_list, message, name)

        case 'Лига':
            name = 'Лига'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "Саморегулируемая организация арбитражных управляющих "Лига"')
            sro_send(message_list, message, name)

        case 'Мск СОПАУ':
            name = 'Мск СОПАУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация МСОПАУ - Ассоциация "Московская саморегулируемая организация профессиональных арбитражных управляющих"')
            sro_send(message_list, message, name)

        case 'Развитие':
            name = 'Развитие'
            message_list = pars.tb.sro_au_info(pars.tb, 'Некоммерческое партнерство Саморегулируемая организация арбитражных управляющих "РАЗВИТИЕ"')
            sro_send(message_list, message, name)

        case 'РСОПАУ':
            name = 'РСОПАУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "Региональная саморегулируемая организация профессиональных арбитражных управляющих"')
            sro_send(message_list, message, name)

        case 'Стратегия':
            name = 'Стратегия'
            message_list = pars.tb.sro_au_info(pars.tb, 'СОЮЗ «САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ «СТРАТЕГИЯ»')
            sro_send(message_list, message, name)

        case 'СоБР':
            name = 'СоБР'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация арбитражных управляющих "Современные банкротные решения"')
            sro_send(message_list, message, name)

        case 'МЦПУ':
            name = 'МЦПУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация саморегулируемая организация арбитражных управляющих "Межрегиональный центр экспертов и профессиональных управляющих"')
            sro_send(message_list, message, name)

        case 'СМиАУ':
            name = 'СМиАУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Саморегулируемая организация "Союз менеджеров и арбитражных управляющих"')
            sro_send(message_list, message, name)

        case 'СРО АУ СЗ':
            name = 'СРО АУ СЗ'
            message_list = pars.tb.sro_au_info(pars.tb, 'СОЮЗ "САМОРЕГУЛИРУЕМАЯ ОРГАНИЗАЦИЯ АРБИТРАЖНЫХ УПРАВЛЯЮЩИХ СЕВЕРО-ЗАПАДА"')
            sro_send(message_list, message, name)

        case 'Синергия':
            name = 'Синергия'
            message_list = pars.tb.sro_au_info(pars.tb, 'СРО ААУ "Синергия" - Саморегулируемая организация ассоциация арбитражных управляющих "Синергия"')
            sro_send(message_list, message, name)

        case 'Содействие':
            name = 'Содействие'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация МСРО "Содействие" - Ассоциация "Межрегиональная саморегулируемая организация арбитражных управляющих "Содействие"')
            sro_send(message_list, message, name)

        case 'ААУ Содружество':
            name = 'ААУ Содружество'
            message_list = pars.tb.sro_au_info(pars.tb, 'ААУ "Содружество" - Ассоциация Арбитражных Управляющих "Содружество"')
            sro_send(message_list, message, name)

        case 'МСК ПАУ Содружество':
            name = 'МСК ПАУ Содружество'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация "Межрегиональная Северо-Кавказская саморегулируемая организация профессиональных арбитражных управляющих "Содружество"')
            sro_send(message_list, message, name)

        case 'ЦААУ':
            name = 'ЦААУ'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация арбитражных управляющих саморегулируемая организация "Центральное агентство арбитражных управляющих"')
            sro_send(message_list, message, name)

        case 'Эгида':
            name = 'Эгида'
            message_list = pars.tb.sro_au_info(pars.tb, 'Ассоциация саморегулируемая организация арбитражных управляющих "Эгида"')
            sro_send(message_list, message, name)


        case "Тенденция по всем АУ за месяц":
            mess_list = pars.tb.all_au_for_month(pars.tb)
            print('отработала функция большая')
            mess = 'Падение по сумме за месяц: \n'+'\n'.join(mess_list[0])+'\n\n'+'Уход на другие ЭТП:'+'\n'+'\n'.join(mess_list[1])
            send_long_message(bot, message.chat.id, mess)

        case "Без аккредитации":
            pass


bot_start()