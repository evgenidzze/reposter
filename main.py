import re

from telethon import events, types
from telethon.sync import TelegramClient

api_id = 27746069
api_hash = '366b9ea354ea52be3b7c2485f710749f'
channel_name_get_post = 'REAL_REALMADRIDUZ_BELLINGEM'
channel_name_to_send = 'REALMADRID_REAL_MADRID_RMA'

client = TelegramClient('session_name', api_id, api_hash).start(password='2222')


@client.on(events.NewMessage(chats=channel_name_get_post))
async def event_handler(event):
    if event.message:
        message_dict: dict = event.message.to_dict()
        print(message_dict)
        if not message_dict.get('reply_markup'):
            for e in message_dict.get('entities'):
                e: dict
                if e.get('_') in ('MessageEntityUrl'):
                    return
                elif e.get('_') in ('MessageEntityMention'):
                    mention_pattern = r'(@[\w]+)'
                    event.message.text = re.sub(mention_pattern, '', event.message.text)
            if event.message.media:
                media: types.MessageMediaDocument = event.message.media
                if media.to_dict().get('photo'):
                    photo = event.message.media.photo
                    await client._send_album(channel_name_to_send, files=(photo,), caption=event.message.text)
                elif media.to_dict().get('document'):
                    document = event.message.media.document
                    await client.send_file(channel_name_to_send, file=document, caption=event.message.text)
            # Check if the message contains text
            elif not event.message.media and event.message.text:
                text = event.message.text
                await client.send_message(channel_name_to_send, text)


def main():
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
