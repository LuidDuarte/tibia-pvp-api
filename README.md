Tibia PVP Api
===

This is a project to help pvp tibia players know which players that killed him had already died and which ones are waiting a revenge.

Were useds:
   
- [Flask](https://pypi.org/project/Flask/)

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)


HOW TO USE
===
https://tibia-skull.herokuapp.com 
### There are two ways to check:
- By a character name, his last death will be used
- By a Death Text that tibia shows in their site

Those ways will show you a same page, it will compare the datetime of the death that want to be check with the last death of all murderers, if they died after, they will no longer be skull.

There is a `Refresh` button on the bottom that will only verify the `still skull` list.