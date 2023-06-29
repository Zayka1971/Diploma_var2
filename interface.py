import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import community_token, access_token

from core import VkTools


class BotInterface():

    def __init__(self, community_token, access_token):
        self.interface = vk_api.VkApi(token=community_token)
        self.api = VkTools(access_token)
        self.params = None

    def message_send(self, user_id, message=None, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'random_id': get_random_id(),
                               'attachment': attachment
                               }
                              )

    def event_handler(self):
        longpull = VkLongPoll(self.interface)

        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    self.message_send(event.user_id, 'Добрый день! Хочешь познакомиться?')
                elif event.text.lower() == 'поиск':
                    users = self.api.serch_users(self.params)
                    user = users.pop()
#здесь надо как-то проверить нету ли этого юзера уже в базе
                    photos_user = self.api.get_photos(user['id'])

                    attachment = ''
                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{["ouner_id"]}_{photo["id"]}'
                        if num == 3:
                            break
                    self.message_send(event.user_id, f'Мне кажется,тебе подходит {user["name"]}', attachment=attachment)
#здесь надо юзера и того, кого он просмотрел вставить в базу
                elif event.text.lower() == 'Пока!':
                    self.message_send(event.user_id, 'Пока!')
                else:
                    self.message_send(event.user_id, 'Не понимаю, о чем ты!')


if __name__ == '__main__':
    bot = BotInterface(community_token, access_token)
    bot.event_handler()
