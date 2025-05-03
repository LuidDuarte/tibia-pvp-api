import requests
from datetime import datetime
from app.models import Injusted, LastDeath, Character
import threading

class CharacterSerializer:

    @classmethod
    def from_api(cls, name:str) -> Character:
        character_name = name.replace(' ', '%20')
        r = requests.get(f'https://api.tibiadata.com/v4/character/{character_name}')
        character = r.json()['character']['character']
        deaths = r.json()['character'].get('deaths', [])

        name = character['name'].split(' (traded)')[0]
        level = character['level']
        vocation = character['vocation']

        last_death = cls.get_lastdeath_from_api(deaths)

        return Character(name, level, vocation, last_death)

    @classmethod
    def get_lastdeath_from_api(cls, deaths) -> LastDeath:
        if deaths:
            death = deaths[0]
            death_time = datetime.strptime(death['time'], '%Y-%m-%dT%H:%M:%SZ' )
            killers = death.get('killers')
            # ignore monsters
            if killers:
                killers = [killer for killer in killers if killer.get('player', False)]

            return LastDeath(death_time, killers)

    @classmethod
    def object_to_dict(cls, char:Character) -> dict:
        dictionary = {}
        dictionary = vars(char).copy()
        dictionary['last_death'] = LastDeathSerializer.object_to_dict(char.last_death)
        return dictionary

    @classmethod
    def dict_to_object(cls, dictionary:dict) -> Character:
        last_death = LastDeath(**dictionary.pop('last_death'))
        return Character(**dictionary, last_death=last_death)

class InjustedSerializer:

    @classmethod
    def object_to_dict(cls, injusted:Injusted) -> dict:
        dictionary = {'char': None, 'skulls': [], 'already_lost': []}
        dictionary['char'] = CharacterSerializer.object_to_dict(injusted.char)

        if injusted.skulls:
            dictionary['skulls'] = [CharacterSerializer.object_to_dict(skull)
                                        for skull in injusted.skulls]
        if injusted.already_lost:
            dictionary['already_lost'] = [CharacterSerializer.object_to_dict(already_lost)
                                            for already_lost in injusted.already_lost]
        return dictionary

    @classmethod
    def dict_to_object(cls, dictionary) -> Injusted:
        char = CharacterSerializer.dict_to_object(dictionary.pop('char'))

        skulls = [ CharacterSerializer.dict_to_object(skull) for skull in dictionary['skulls']]
        already_lost = [ CharacterSerializer.dict_to_object(already_lost) for already_lost in dictionary['already_lost']]
        return Injusted(char=char, skulls=skulls, already_lost=already_lost)

    @classmethod
    def from_api(cls, char:Character) -> Injusted:
        skulls = []
        threads = [threading.Thread(target=cls.thread_skull_append_function,
                                    args=(char['name'], skulls)) for char in char.last_death.killers]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return Injusted(char=char, skulls=skulls)

    @classmethod
    def thread_skull_append_function(cls, name, skulls):
        skulls.append(CharacterSerializer.from_api(name))

    @classmethod
    def refresh_skull_from_api(cls, injusted:Injusted):
        skulls = []
        threads = [threading.Thread(target=cls.thread_skull_append_function,
                                    args=(char.name, skulls)) for char in injusted.skulls]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        injusted.skulls = skulls
        return injusted

class LastDeathSerializer:

    @classmethod
    def object_to_dict(cls, last_death:LastDeath) -> dict:
        dictionary = {'death_time': None, 'killers': []}
        if hasattr(last_death, 'death_time'):
            dictionary['death_time'] = last_death.death_time
        if hasattr(last_death, 'killers'):
            dictionary['killers'] = last_death.killers
        return dictionary