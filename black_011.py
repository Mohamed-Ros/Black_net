import base64
import xml.etree.ElementTree as ET
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import *

from asyncio import Queue
my_queue = Queue()
NUMBER, PASSWORD, EMAIL,CHOOSING, TYPING_REPLY  = range(5)

# Define a function to start the conversation
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    username = user.username if user.username else "Anonymous"

    keyboard = [
              [InlineKeyboardButton("نت مجاني ❤️", callback_data='net')
              ,InlineKeyboardButton("جروبي  ❤️ ", callback_data='group')
              ,InlineKeyboardButton("المطور ❤️", callback_data='developer')]
    
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f""" 🖤|مرحبا {username} 💫❤️

       🔥BLACK FOR FREE INTERNT🔥

🔰| المطور⚜️ @R7_60 ⚜️
       """, reply_markup=reply_markup)
def net(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="""للاستمتاع بهذا العرض 💫❤️‍🔥
 اشترك في عرض ☠️❤️‍🔥
 الاهلي فانز من هذا الكود *1907#
بعد الاشتراك سوف تحصل علي 100 ميجا هديه 💫❤️‍🔥
ثم اكمل بقيت الخطوات للحصول علي ساعتين نت مجاني  👇""")
    query.message.reply_text("الرجاء إدخال رقم اتصالات المكون من 11 رقمًا.")

    return NUMBER

def developer(update: Update, context: CallbackContext) -> int:
   query = update.callback_query
   query.answer()
   query.edit_message_text(text=f"""
    - ساعتين مجاني اتصالات يوميا ❤️.

- لشرح الاستخدم تحدث مع المالك 
 واتساب عبره هذا الرقم ❤️.
 
01150137726
- نلجرام : @R7_60
""")
   return ConversationHandler.END  
def group(update: Update, context: CallbackContext) -> int:
   query = update.callback_query
   query.answer()
   query.edit_message_text(text=f"يمكنك الانضمام للجروب الواتساب  عبر الرابط: https://chat.whatsapp.com/Hniz2EEd6PoEkVIuG53fqC")
   return ConversationHandler.END  
def handle_number(update: Update, context: CallbackContext) -> int:
    print("handle_number function is called!")  # Add this line for debugging
    context.user_data['number'] = update.message.text
    print("Number:", context.user_data['number'])  # Print the received number
    update.message.reply_text("من فضلك أدخل كلمة المرور الخاصة بتطبيق اتصالات: ")
    return PASSWORD
def handle_password(update: Update, context: CallbackContext) -> int:
    context.user_data['password'] = update.message.text
    update.message.reply_text("الرجاء ادخال البريد الالكتروني الخاص بك")
    return EMAIL
def handle_email(update: Update, context: CallbackContext) -> int:
    context.user_data['email'] = update.message.text

    if "011" in context.user_data['number']:
        num = context.user_data['number'][3:]
    else:
        num = context.user_data['number']

    code = context.user_data['email'] + ":" + context.user_data['password']
    ccode = code.encode("ascii")
    base64_bytes = base64.b64encode(ccode)
    auth = base64_bytes.decode("ascii")
    xauth = "Basic" + " " + auth

    urllog = "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan"
    headerslog = {
        "applicationVersion": "2",
        "applicationName": "MAB",
        "Accept": "text/xml",
        "Authorization": xauth,
        "APP-BuildNumber": "964",
        "APP-Version": "27.0.0",
        "OS-Type": "Android",
        "OS-Version": "12",
        "APP-STORE": "GOOGLE",
        "Is-Corporate": "false",
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": "1375",
        "Host": "mab.etisalat.com.eg:11003",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/5.0.0-alpha.11",
        "ADRUM_1": "isMobile:true",
        "ADRUM": "isAjax:true"
    }
    datalog = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId></deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType></modelType><osVersion></osVersion><platform>Android</platform><udid></udid></loginRequest>"
    log = requests.post(urllog, headers=headerslog, data=datalog)

    # Check if login was successful
    if "true" in log.text:
        # Extract necessary data for subsequent requests
        st = log.headers["Set-Cookie"]
        ck = st.split(";")[0]
        br = log.headers["auth"]

        # Prepare URL for offers request
        url = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/offersV3?req=<dialAndLanguageRequest><subscriberNumber>%s</subscriberNumber><language>1</language></dialAndLanguageRequest>" % (num)
        headers = {
        'applicationVersion': "2",
        'Content-Type': "text/xml",
        'applicationName': "MAB",
        'Accept': "text/xml",
        'Language': "ar",
        'APP-BuildNumber': "10459",
        'APP-Version': "29.9.0",
        'OS-Type': "Android",
        'OS-Version': "11",
        'APP-STORE': "GOOGLE",
        'auth': "Bearer " + br,
        'Host': "mab.etisalat.com.eg:11003",
        'Is-Corporate': "false",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'User-Agent': "okhttp/5.0.0-alpha.11",
        'Cookie': ck
    }

        # Perform offers request
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Extract offer ID from response
            root = ET.fromstring(response.text)
            offer_id = None
            for category in root.findall('.//mabCategory'):
                for product in category.findall('.//mabProduct'):
                    for parameter in product.findall('.//fulfilmentParameter'):
                        if parameter.find('name').text == 'Offer_ID':
                            offer_id = parameter.find('value').text
                            break
                    if offer_id:
                        break
                if offer_id:
                    break

            # Prepare URL for subscription request
            urlsub = "https://mab.etisalat.com.eg:11003/Saytar/rest/zero11/submitOrder"
            headerssub = {
             "applicationVersion": "2",
             "applicationName": "MAB",
             "Accept": "text/xml",
             "Cookie": ck,
             "Language": "ar",
             "APP-BuildNumber": "964",
             "APP-Version": "27.0.0",
             "OS-Type": "Android",
             "OS-Version": "12",
             "APP-STORE": "GOOGLE",
             "auth": "Bearer " + br + "",
             "Is-Corporate": "false",
             "Content-Type": "text/xml; charset=UTF-8",
             "Content-Length": "1375",
             "Host": "mab.etisalat.com.eg:11003",
             "Connection": "Keep-Alive",
             "User-Agent": "okhttp/5.0.0-alpha.11"
        }

            datasub = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>%s</msisdn><operation>ACTIVATE</operation><parameters><parameter><name>GIFT_FULLFILMENT_PARAMETERS</name><value>Offer_ID:%s;ACTIVATE:True;isRTIM:Y</value></parameter></parameters><productName>FAN_ZONE_HOURLY_BUNDLE</productName></submitOrderRequest>" % (num, offer_id)
            subs = requests.post(urlsub, headers=headerssub, data=datasub).text


            if "true" in subs:
                update.message.reply_text("تم الحصول علي الانترنت بنجاح")
            else:
                update.message.reply_text("راجع بياناتك وحاول مره اخري")
        else:
            update.message.reply_text("العرض غير متوافر")
    else:
        update.message.reply_text("رقمك او الباسورد غير صحيح")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("لقد الغيت العمليه")
    return ConversationHandler.END
def main() -> None:
    updater = Updater("6983628383:AAF9i1ZFwjDK0nPeDf88QJbZYsVHgNeAVaY")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),         
                      CallbackQueryHandler(net, pattern='^net$')


                      ],
        states={
            NUMBER: [MessageHandler(Filters.text & ~Filters.command, handle_number)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, handle_password)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, handle_email)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )


    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CallbackQueryHandler(developer, pattern='^developer$'))
    dispatcher.add_handler(CallbackQueryHandler(group, pattern='^group$'))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()