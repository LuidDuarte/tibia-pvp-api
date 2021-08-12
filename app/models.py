from datetime import datetime

class LastDeath:
    def __init__(self, death_time=None, involveds=None):
        self.death_time = death_time
        self.involveds = involveds or []

    def lost_skull(self, injusted):
        if hasattr(self, 'death_time') and self.death_time:
            return  injusted.char.last_death.death_time < self.death_time 

    def __repr__(self):
        return f'<{self.death_time}>'


class Character:
    def __init__(self, name, level, vocation, last_death):
        self.name = name
        self.level = level
        self.vocation = vocation
        self.last_death = last_death

    def __repr__(self) -> str:
        return f'<{self.name} - {self.level} - {self.vocation}>'


class Injusted:
    def __init__(self,char:Character, skulls=None, already_lost=None):
        self.char = char
        self.skulls = skulls or []
        self.already_lost = already_lost or []

    def __repr__(self) -> str:
        return f'{self.char}'

    def verify_skulls(self):
        skulls_copy = self.skulls.copy() #remove inside loop
        for skull in self.skulls:
            if skull.last_death and skull.last_death.lost_skull(self):
                skulls_copy.remove(skull)
                self.already_lost.append(skull)
        self.skulls = sorted(skulls_copy, key=lambda player: player.level, reverse=True)
    
    def refresh_skull_from_api(self):
        from .serializer import CharacterSerializer
        new_skull = []
        for skull in self.skulls:
            new_skull.append(CharacterSerializer.from_api(skull.name))
        self.skulls = new_skull