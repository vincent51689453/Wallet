'''
@@@ Author: Vincent
@@@ Date  : 8 Sep 2022
@@@ About : System Core
'''
from datetime import datetime
import MQTT
import codebook
import wallet

def main():
    # Set Up MQTT
    node_red = MQTT.MQTTManager("localhost",codebook.topics_lib)
    node_red.mqtt_client_setup()

    # Set Up Wallet
    vincent_wallet = wallet.MyWallet('2022') 

    # Publish Monthly Expense (based on system datetime)
    currentMonth = list(codebook.months.keys())[list(codebook.months.values()).index(datetime.now().month)]
    monthly_json = vincent_wallet.get_monthly_expense(currentMonth,True)
    node_red.publish_mqtt_message(1,monthly_json)

    # Publish Money Flow (monthly & annual)
    vincent_wallet.calculate_monthly_remain()
    vincent_wallet.calculate_annual_remain()
    message = "{\"monthly_remain\":\""+str(vincent_wallet.monthly_remain)+"\",\"annual_remain\":\""+str(vincent_wallet.annual_remain)+"\"}"
    node_red.publish_mqtt_message(2,message)
    
    # Publish General Info
    owner_name = 'Vincent'
    annual_pretax_income = 65000
    owner_position = 'Test Engineer'
    vincent_wallet.get_monthly_salary()
    message = "{\"owner\":\""+owner_name+"\",\"position\":\""+owner_position+"\",\"annual_pretax_income\":\""+ '$' + str(annual_pretax_income)+"\",\"month_aftertax_income\":\""+ '$'+str(vincent_wallet.monthly_salary)+"\"}"
    node_red.publish_mqtt_message(0,message)

    # Publish Other Bank Info


if __name__ == '__main__':
    main()




