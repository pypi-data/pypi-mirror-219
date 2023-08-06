from zeep import Client



#######################
WEBSERVICE_URL_V8 = 'https://www.afe.ir/webservice/v8/BoxService.asmx?WSDL'
WEBSERVICE_URL_V5 = 'https://www.afe.ir/webservice/v5/BoxService.asmx?WSDL'
INBOXSERVICE = 'http://www.afe.ir/WebService/Inboxservice.asmx?WSDL'
#######################




###### Sending methods ######

# Send message
def Send(username, password, number, mobile_list, message, checkingMessages):
    client = Client(WEBSERVICE_URL_V8)

    Username = username
    Password = password
    Number = number

    Mobiles = client.get_type('ns0:ArrayOfString')()
    for mobile in mobile_list:
        Mobiles['string'].append(mobile)

    Message = message
    Type = '1'

    CheckingMessageID = client.get_type('ns0:ArrayOfLong')(checkingMessages)

    result = client.service.SendMessage(Username, Password, Number, Mobiles, Message, Type, CheckingMessageID)
    return result

# Send message - no chacking message id
def Send2(username, password, number, mobile_list, message):
    client = Client(WEBSERVICE_URL_V5)

    Username = username
    Password = password
    Number = number

    Mobiles = client.get_type('ns0:ArrayOfString')()
    for mobile in mobile_list:
        Mobiles['string'].append(mobile)

    Message = message
    Type = '1'

    result = client.service.SendMessage(Username, Password, Number, Mobiles, Message, Type)
    return result


# Send Message PeerToPeer 
def SendMessagePeerToPeer(username, password, number_list, mobile_list, message_list,type_list, checkingMessage_list):
    client = Client(WEBSERVICE_URL_V8)

    Username = username
    Password = password

    Numbers = client.get_type('ns0:ArrayOfString')()
    for number in number_list:
        Numbers['string'].append(number)

    Mobiles = client.get_type('ns0:ArrayOfString')()
    for mobile in mobile_list:
        Mobiles['string'].append(mobile)

    Messages = client.get_type('ns0:ArrayOfString')()
    for message in message_list:
        Messages['string'].append(message)


    Types = client.get_type('ns0:ArrayOfString')()
    for typ in type_list:
        Types['string'].append(typ)


    CheckingMessageID = client.get_type('ns0:ArrayOfLong')(checkingMessage_list)


    result = client.service.SendMessagePeerToPeer(Username, Password, Numbers, Mobiles, Messages, Types, CheckingMessageID)

    return result


# get message id
def GetMessageID(username, password, checkingMessages):
    client = Client(WEBSERVICE_URL_V8)

    Username = username
    Password = password

    CheckingMessageID = client.get_type('ns0:ArrayOfLong')()

    CheckingMessageID['long'].extend(checkingMessages)

    SmsId = client.service.GetMessageID(Username, Password, CheckingMessageID)
    return SmsId


# Get Messages Status
def GetMessagesStatus(username, password, SmsId_list):
    client = Client(WEBSERVICE_URL_V8)


    Username = username
    Password = password

    SmsID = client.get_type('ns0:ArrayOfString')()
    for messageId in SmsId_list:
        SmsID['string'].append(messageId)

    result = client.service.GetMessagesStatus(Username, Password, SmsID)
    return result

################# end ###############

###### Account Credit methods ######

# Get Remaining Credit
def GetRemainingCredit(username, password):

    client = Client(WEBSERVICE_URL_V8)
    Username = username
    Password = password
    result = client.service.GetRemainingCredit(Username, Password)
    return result

# Get credit list
def ListCredit(username, password):
    client = Client(WEBSERVICE_URL_V8)
    Username = username
    Password = password
    result = client.service.ListCredit(Username, Password)
    return result

###### inbox methods ######

# Get inbox message with ID
def GetInbox(username, password, inbox_id):
    client = Client(INBOXSERVICE)
    Username = username
    Password = password
    ID = inbox_id
    result = client.service.Get(Username, Password,ID)
    return result

# Get  count inbox message with ID
def GetCount(username, password, to, inbox_id):
    client = Client(INBOXSERVICE)
    Username = username
    Password = password
    To = to
    ID = inbox_id
    result = client.service.GetCount(Username, Password, To, ID)
    return result

# Get  list inbox message with ID 0 - 100
def InboxList(username, password, to, inbox_id, count):
    client = Client(INBOXSERVICE)
    Username = username
    Password = password
    To = to
    ID = inbox_id
    Count = count
    result = client.service.List(Username, Password, To, ID, Count)
    return result

################# end ###############