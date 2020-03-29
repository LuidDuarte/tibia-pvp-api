import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime


class Last_Death():
    
    def __init__(self, date=None, names=None, dictionary=None):
        if dictionary:
            self.date = dictionary['date']
            self.already_lost = dictionary['already_lost']
            self.still_skull = dictionary['still_skull']

        else:
            print(date)
            self.date = datetime.strptime(date,'%b %d %Y, %H:%M:%S')
            if 'Assisted ' in names:
                self.assisted_by = names.split('Assisted ')[1].split(',')
                self.names = names.split('Assisted ')[0].split(',')
            else:
                self.assisted_by = None
                self.names = names.split(', ')

    @property
    def verify_skull(self):
        self.already_lost = []
        still_skull = []
        for name in self.names:
            skull = return_character(name)
            if skull:
                if skull.last_death and skull.last_death.date > self.date:
                    self.already_lost.append(skull.name)
                else:
                    skull_dict = {}
                    skull_dict['name'] = skull.name
                    skull_dict['level'] = skull.level
                    still_skull.append(skull_dict)
        self.still_skull = sorted(still_skull, key = lambda i: int(i['level']), reverse=True)

    @property
    def refresh(self):
        still_skull = []
        for skull in self.still_skull:
            skull = return_character(skull['name'])
            if skull:
                if skull.last_death and skull.last_death.date > self.date:
                    self.already_lost.append(skull.name)
                else:
                    skull_dict = {}
                    skull_dict['name'] = skull.name
                    skull_dict['level'] = skull.level
                    still_skull.append(skull_dict)
        self.still_skull = still_skull 


class Character():
    
    def __init__(self, tables):
        table_death = tables[2].findAll('td')
        character_information = tables[0].findAll('td')
        self.name = character_information[2].text[:-1]
        if 'Former' in character_information[3].text:
            self.vocation = character_information[10].text
            self.level = character_information[12].text
            self.world = character_information[16].text
        else:      
            self.vocation = character_information[8].text
            self.level = character_information[10].text
            self.world = character_information[14].text
        if table_death[0].text == 'Character Deaths':
            date = table_death[1].text.replace('\xa0', ' ').split(' CEST')[0]
            names = table_death[2].text.split('by ')[1].replace(' and', ',').replace('\xa0', ' ').replace('.', '')
            self.last_death = Last_Death(date, names)
        elif tables[3].findAll('td')[0].text == 'Character Deaths':
            table_death = tables[3].findAll('td')
            date = table_death[1].text.replace('\xa0', ' ').split(' CEST')[0]
            names = table_death[2].text.split('by ')[1].replace(' and', ',').replace('\xa0', ' ')
            self.last_death = Last_Death(date, names)
        else:
            self.last_death = None

    def __str__(self):
        return self.name + ', ' + self.level
    
    def __repr__(self):
        return self.name + ', ' + self.level

def return_character(name):
    url = 'https://www.tibia.com/community/?subtopic=characters&name=' + name.replace(' ', '+')
    uClient = requests.get(url)
    page_html = uClient.content
    uClient.close()

    page_soup = soup(page_html, 'html.parser')
    tables = page_soup.findAll('table')
    
    if tables[0].find('td').text == 'Could not find character':
        return None

    c = Character(tables)

    return c

def verify_by_name(name):
    character = return_character(name)
    character.last_death.verify_skull
    return character.last_death

def verify_by_text(text):
    date, names = text.split(' CEST')
    names = names.split('by ')[1].replace(' and', ',').replace('.', '')
    last_death = Last_Death(date, names)
    last_death.verify_skull
    return last_death

