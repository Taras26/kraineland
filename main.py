import telebot
from telebot import types

from aternosapi import AternosAPI

headers_cookie = "ATERNOS_SEC_vittvols29m00000=8hcue12at8n00000; _ga=GA1.2.286329612.1673391127; _gid=GA1.2.2113513319.1673391127; ATERNOS_LANGUAGE=uk; ATERNOS_GA=286329612.1673391127; ATERNOS_SESSION=V3oX6f1jNTIdjKl5kphK0NiXo1i4JcChDp45Ye16czujhS9PbydIec7oxp8fSiugK0H0mFUhCSDh02joSt8H2FYylyyJ3sGfsz8r; _pbjs_userid_consent_data=3524755945110770; __gads=ID=fd836f19202a752f:T=1673391135:S=ALNI_MZ5oIJE3CvYnLlef7-ERQrey9XEIQ; __gpi=UID=00000ba0d6af9f26:T=1673391135:RT=1673521918:S=ALNI_MZtTmNuMQpPFASroJwv-EFCvnqLxg; _pubcid=83740…MwOUJGQlhaMUN2czRRMGZRNEFyb1RTQ3hEQklGY2ROV0JRdGNVS2FoVjltVEthQ2lBUEtmSW4; pbjs-unifiedid=%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-01-10T22%3A57%3A02%22%7D; _cc_id=4a4c136daf792e42a48fb732877127f4; __cf_bm=JU0.7qK6OwDvPvV8TUBdW92i9bgQ3MSiy1Zx3yBEvxo-1673521914-0-AdKPcxG57Udb0ns+rvMrB0IwNE6A3MlQTXKbcEue1/6GMPENPKLwdJeE5i48vYTaV0WL3T0Z+ajLjktulJx0dos4rZtyi8j8nLu4ibcw9oyOYF8SaSn8zG8+8piQNL4kp/6CVXmbnOC4CjFzmEo3ijo=; ATERNOS_SERVER=IvTDogGMZ9q8aK6T; _ublock=1; _lr_retry_request=true"
TOKEN = "ZFL6ZGjSsYMlBc3o5WrZ"
server = AternosAPI(headers_cookie, TOKEN, timeout=10)
admin_id = [853380216, 1055097059, 1530841839, 1279202423]
admin_log = "True"
sep = ',\n'
playerinfo = server.GetPlayerInfo()

API_TOKEN = '5843974512:AAEyGMp6bkhGR4c0Xa0SxKFIB-S5kYCM86Y'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    global admin_log

    for i in admin_id:
        if str(i) == str(message.from_user.id):
            admin_log = "True"
            break
        else:
            admin_log = "False"

    if admin_log == "False":
        bot.send_message(message.chat.id, f'Ви не адміністратор. Для надання прав писати: <i>@kinakht</i> ',
                         parse_mode="html")
    elif admin_log == "True":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        button1 = types.KeyboardButton('Увімкнути сервер')
        button2 = types.KeyboardButton('Вимкнути сервер')
        button3 = types.KeyboardButton('Статус сервера')
        button4 = types.KeyboardButton('Список гравців')
        markup.add(button1, button2, button3, button4)
        send_mes = (
            f'Вхід виконано, Ви Адміністратор сервера майнкрафт KraineLand.\nServer ip: KraineLand.aternos.me')
        bot.send_message(message.chat.id, send_mes, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Щось пішло не так, можливо ви не адміністратор.')


@bot.message_handler(content_types=['text'])
def get_text(message):
    get_message_text = message.text.strip().lower()
    if get_message_text == 'id':
        bot.send_message(message.chat.id, f'Твій ID: {message.from_user.id}', parse_mode='html')
    elif get_message_text == 'статус сервера' and admin_log == "True":
        bot.send_message(message.chat.id, f'Статус сервера: {server.GetStatus()}', parse_mode='html')
    elif get_message_text == 'увімкнути сервер' and admin_log == "True":
        bot.send_message(message.chat.id, f'Зачекайте, будь ласка, сервер запускається...', parse_mode='html')
        bot.send_message(message.chat.id, f'{server.StartServer()}', parse_mode='html')
    elif get_message_text == 'вимкнути сервер' and admin_log == "True":
        bot.send_message(message.chat.id, f'Зачекайте, будь ласка, сервер вимикається...', parse_mode='html')
        bot.send_message(message.chat.id, f'{server.StopServer()}', parse_mode='html')
    elif get_message_text == 'список гравців' and admin_log == "True":
        if len(playerinfo) > 0:
            bot.send_message(message.chat.id, f'На сервері {len(playerinfo)}/25 гравців.\nСписок гравців:\n{sep.join(playerinfo)}')
        else:
            bot.send_message(message.chat.id, f'На сервері немає гравців.')
    else:
        bot.send_message(message.chat.id, f'Ви не адміністратор.', parse_mode='html')


bot.polling(none_stop=True)
