import requests
from datetime import datetime


class LastDeath:
    def __init__(self, deaths=None, view_involveds=False):
        if deaths:
            self.datetime = datetime.strptime(deaths[0]['date']['date'].split('.')[0], '%Y-%m-%d %H:%M:%S')
            if view_involveds:
                self.involveds = [Character(involved['name']) for involved in deaths[0]['involved']]
                self.skulls = self.involveds.copy()
                self.already_lost = []
                self.verify_skulls()

    def is_skull(self, pk):
        return self.datetime > pk.last_death.datetime if pk.last_death else True
    
    def verify_skulls(self):
        for index, pk in enumerate(self.skulls):
            if not self.is_skull(pk):
                self.skulls.remove(pk)
                self.already_lost.append(pk)
        self.skulls = sorted(self.skulls, key=lambda player: player.level, reverse=True )
    
    def __repr__(self):
        if hasattr(self, 'involveds'):
            return f'{self.datetime} {self.involveds}'
        return f'{self.datetime}'

    

class Character:
    def __init__(self, name, view_involveds=False):
        character_name = name.replace(' ', '+')
        r = requests.get(f'https://api.tibiadata.com/v2/characters/{character_name}.json')
        character = r.json()['characters']

        self.name = character['data']['name']
        self.level = character['data']['level']
        self.vocation = character['data']['vocation']
        self.last_death = LastDeath(character['deaths'], view_involveds=view_involveds)
    
    def __repr__(self):
        return f'{self.name}, {self.level}, {self.vocation}'
