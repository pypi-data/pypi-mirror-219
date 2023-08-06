
# AsreFaraErtebat

  

## Send

  

```python

from afeSMS import Send

  

result =  Send(username, password, number, mobile_list, message, checkingMessages)

```

**username** = afe username(string)

  

**password** = afe password(string)

  

**number** = sms number(string)

  

**mobile_list** = mobile(list)

  

**message** = message(string)

  

**checkingMessages** = refrenceid from checkingMessages(int)

  

## Send2

> no chacking message id

  

```python

from afeSMS import Send2

  

result =  Send2(username, password, number, mobile_list, message)

```

  

## SendMessagePeerToPeer

  

```python

from afeSMS import SendMessagePeerToPeer

  

result =  SendMessagePeerToPeer(username, password, number_list, mobile_list, message_list,type_list, checkingMessage_list)

```

  

**number_list** = sms number(list)

  

**mobile_list** = mobile(list)

  

**message_list** = message(list)

  

**checkingMessage_list** = refrenceid from checkingMessages(list)

  

## GetMessageID

```python

from afeSMS import GetMessageID

  

result =  GetMessageID(username, password, checkingMessages)

```

## GetMessagesStatus

```python

from afeSMS import GetMessagesStatus

  

result =  GetMessagesStatus(username, password, SmsId_list)

```

**SmsId_list** = messages id(list)

  

## GetRemainingCredit

```python

from afeSMS import GetRemainingCredit

  

result =  GetRemainingCredit(username, password)

```

## ListCredit

```python

from afeSMS import ListCredit

  

result =  ListCredit(username, password)

```

## GetInbox

```python

from afeSMS import GetInbox

  

result =  GetInbox(username, password, inbox_id)

```

**inbox_id** = inbox messages id(list)

  

## GetInbox

> A number between 0 and 100

```python

from afeSMS import InboxList

  

InboxList(username, password, to, inbox_id, count)

```

**count** = inbox messages id(int)

## GetInbox

```python

from afeSMS import GetCount

  

GetCount(username, password, to, inbox_id)

```

**to** = Recipient number (string)

  

> made by Morteza Sotoodeh
