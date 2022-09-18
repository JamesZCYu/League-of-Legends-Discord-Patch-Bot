import random
import requests
import re
from colorama import Fore
from bs4 import BeautifulSoup

def ScrapePatchNotes():
    patch_notes_url = "https://na.leagueoflegends.com/en-us/news/tags/patch-notes/"
    patch_notes_prefix = "https://na.leagueoflegends.com"

    found_patches = []

    print("Pulling latest patch notes ... ",end="")

    try:
        patch_notes_page = requests.get(patch_notes_url,timeout = 60)
    except Exception as error:
        print(Fore.RED + "! Unable to connect ({}).".format(error.__class__.__name__) + Fore.WHITE)
        # We can just return an empty list if we cannot connect, as the program should proceed as if nothing new has been found
        return found_patches

    if patch_notes_page.status_code == 200: #OK
        # Find all 'a' elements with a href attribute held within (Any patch note entries currently listed)
        patch_entry_classes = BeautifulSoup(patch_notes_page.text,"html.parser").find_all("a", href=True)
    
        for entry in patch_entry_classes:
            # Grab Patch notes title in plaintext from the first h2 element found.
            entry_title = entry.find("h2").contents[0]
            # Grab the suffix for the Patch notes' URL to append to the original request URL.
            entry_link = patch_notes_prefix + entry["href"]
            found_patches.insert(0,(entry_title,entry_link))    
        
    print(Fore.GREEN + "Done." + Fore.WHITE)

    return found_patches

def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == '$hello':
        return 'Hello!'

    if p_message == '$roll':
        return str(random.randint(1, 6))

    if p_message == '$help':
        return "`This is a help message that you can modify.`"

    if p_message == '$patch':
        return '@everyone \n The latest League of Legends patch is now available, ' + re.sub('notes', '', ScrapePatchNotes()[-1][0]) + ': \n\n' + ScrapePatchNotes()[-1][-1]

    if p_message == '$allpatches':
        links = []
        for link in ScrapePatchNotes():
            links.insert(0,link[-1])
        return '@everyone \n List of the most recent League of Legends patches: \n\n' + ',\n'.join(links)
