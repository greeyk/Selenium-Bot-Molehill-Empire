from imperium.imperium import Imperium
import time

''' 2 - salat, 6 - carrot, 12 -ogorek, 14 - rzodkiewa, 3 - strawberry, 5 - tomato, 9 - onion, 36 - spinat,
 32 - kalafior, 49 - nagietek, 22 - ziemniak, 35 - czosnek, 15 - papryka, 33 - brokul '''

login = "selen123"
password = 'kuba1234'
plant = [2]

with Imperium() as bot:

    bot.land_first_page()
    bot.try_login(login, password)
    try:
        bot.accept_cookies()
    except:
        print("Can't accept cookies")
    time.sleep(2)

    while True:
        try:
            bot.closing_windows()
            print("Popups closing")
        except:
            pass

        try:
            bot.harvesting()
        except Exception as e:
            print('Harvesting error -----' + str(e))

        try:
            bot.planting(*plant)
        except Exception as e:
            print('Planting Error -----' + str(e))

        try:
            bot.watering()
        except Exception as e:
            print('Watering error -----' + str(e))

        try:
            bot.selling()
        except Exception as e:
            print('Selling error -----' + str(e))

        time.sleep(2)
        bot.refreshing()
        time.sleep(60)

        try:
            bot.try_login_again(login, password)
            print("Logged again")
        except:
            pass
