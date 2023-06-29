import vk_api
from config import access_token
import datetime
from datetime import datetime


class VkTools():
    def __init__(self, access_token):
        self.api = vk_api.VkApi(token=access_token)

    def get_profile_info(self, user_id):

        info = self.api.method('users.get',
                            {'user_id': user_id, 'fields': 'first_name, last_name, city, bdate, sex,relation, home_town'
                            }
                               )

        user_info = {'name': info[0]['first_name'] + info[0]['last_name'],
                         'id': info['id'],
                         'bdate': info['bdate'] if 'bdate' in info else None,
                         'home_town': info['home_town'],
                         'sex': info['sex'],
                         'city': info['city'][id]
                         }

        return user_info

    def serch_users(self, params):
        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        current_year = datetime.now().year
        user_year = int(params['bdate'].split('.')[2])
        age = current_year-user_year
        age_from = age - 5
        age_to = age + 5

        users  = self.api.method('users.search',
                                 {'count': 10,
                                  'offset': 0,
                                  'age_from': age_from,
                                  'age_to' : age_to,
                                  'sex': sex,
                                  'city': city,
                                  'status': 6,
                                  'is_closed': False
                                  })

        try:
            users = users['items']
        except KeyError:
            return []

        result = []

        for user in users:
            if user['is_closed'] == False:
                result.append({'id': user['id'], 'name': user[0]['first_name'] + user[0]['last_name']})
        return result

    def get_photos(self, user_id):

        photos = self.api.method('photos.get',
                                 {'user_id':user_id,
                                  'album_id': 'profile',
                                  'extended': 1})
        try:
            photos = photos['items']
        except KeyError:
            return []

        result = []
        for photo in photos:
            result.append({'owner_id': photo['owner_id'],
                           'id': photo['id'],
                           'likes': photo['likes']['count'],
                            'comments': photo['comments']['count']
                           })

        result.sort(key=lambda x: x['likes'] + x['comments']*10, reverse=True)

        return result


if __name__ == '__main__':
    bot = VkTools(access_token)
    params = bot.get_profile_info(801748008)
    users = bot.serch_users(params)
    print(bot.get_photos(users[2][id]))
