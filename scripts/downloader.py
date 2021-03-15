#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import inquirer
import os
import youtube_dl
import re

class results:
    def __init__(self, title, date, link, belongs_to = None):
        self.title = title
        self.date = date
        self.link = link
        self.belongs_to = belongs_to

def search(search_string):
    search_string = str(search_string).replace(" ","+")
    url = "https://www.zdf.de/suche?q="+search_string+"&synth=true&sender=Gesamtes+Angebot&from=&to=&attrs=&abName=ab-2021-02-22&abGroup=gruppe-a"

    page = requests.get(url)
    if page.status_code == 200:
        content = page.content
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find(id="aria-search-block")
    result_boxes = temp.findChildren(recursive=False)

    search_results = []
    for box in result_boxes:
        children = box.findChildren()
        belongs_to = None
        for child in children:
            if child.name == "a":
                title = child.text.replace("-","").replace("\n","").strip()
            if child.has_attr('class') and child['class'][0] == 'teaser-cat-brand-ellipsis':
                belongs_to = child.text.strip()
            if child.has_attr('class') and child['class'][0] == 'special-info':
                date = child.text.strip()
            if child.has_attr('class') and child['class'][0] == 'teaser-title-link':
                link = "https://www.zdf.de/"+child['href']
        search_results.append(results(title,date,link,belongs_to))
    return search_results

def prepare_selection_array(search_results):
    selections = []
    max_title = 0
    max_belongs_to = 0
    for result in search_results:
        if len(result.title) > max_title:
            max_title = len(result.title)
        if result.belongs_to is not None and len(result.belongs_to) > max_belongs_to:
            max_belongs_to = len(result.belongs_to)

    for result in search_results:
        result_type = ""
        if result.belongs_to == None:
            result_type = "Serie"
        else:
            result_type = "Sendung/film"

        selection = result.title + " "*(max_title-len(result.title)) + "|| " + result.date+" || "+ str(result.belongs_to).replace("None","    ") + " "*(max_belongs_to-len(str(result.belongs_to)))+" || "+result_type
        selections.append(selection)
    return selections

def get_download_links(search_item):
    page = requests.get(search_item.link)
    if page.status_code == 200:
        content = page.content
    soup = BeautifulSoup(content, "html.parser")

    #Requested download is a series
    if search_item.belongs_to == None:
        full_block = soup.find("div", {"class": "sb-page"})
        temp = full_block.findChildren(recursive=False)
        blocks = []

        for item in temp:
            if item.has_attr('class') and (item['class'][0] == 'b-content-teaser-list' or item['class'][0] == 'b-cluster'):
                blocks.append([item,""])

        for block in blocks:
            header = block[0].findChild("header", recursive=False)
            block[1] = header.text.strip()
        selection = []
        for item in blocks:
            selection.append(item[1])
        os.system("clear")
        questions = [inquirer.Checkbox('Results',message="Select",choices=selection,),
        ]
        answers = inquirer.prompt(questions)

        indexes = []
        temp = answers['Results']
        for item in temp:
            indexes.append(selection.index(item))

        for index in indexes:
            html = blocks[index][0]
            name = blocks[index][1]
            print("Searching in:",name)
            children = html.findChildren()
            for child in children:
                if child.has_attr('class') and 'teaser-title-link' in child['class']:
                    link = "https://www.zdf.de"+child["href"]

                    name_no_special = re.sub('\W',' ',name)
                    ydl_opts = {'outtmpl': "downloads/"+search_item.title+"/"+name_no_special+"/"+child.text.strip()+".mp4"}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link])

    #Requested download is NOT a series
    if search_item.belongs_to != None:
        print("This is NOT a series")

def add_automatic_download():

    while True:
        os.system("clear")
        search_string = input("Search for: ")
        if search_string == "exit" or search_string == "e" or search_string == "cancel" or search_string == "quit" or search_string == "break":
            break

        search_results = search(search_string)
        selection = ['Zurück']+prepare_selection_array(search_results)
        if len(search_results) == 0:
            os.system("clear")
            print("No Results")
            input("")
            os.system("clear")
            continue
        questions = [
          inquirer.List('Results', message="Results", choices=selection,
                    ),
        ]
        answers = inquirer.prompt(questions)

        if answers["Results"] == "Zurück":
            continue
        else:
            print(answers["Results"])
            search_item = search_results[selection.index(answers["Results"])-1]

            page = requests.get(search_item.link)
            if page.status_code == 200:
                content = page.content
            soup = BeautifulSoup(content, "html.parser")

            # Requested download is a series
            if search_item.belongs_to == None:
                full_block = soup.find("div", {"class": "sb-page"})
                temp = full_block.findChildren(recursive=False)
                blocks = []

                for item in temp:
                    if item.has_attr('class') and (
                            item['class'][0] == 'b-content-teaser-list' or item['class'][0] == 'b-cluster'):
                        blocks.append([item, ""])

                for block in blocks:
                    header = block[0].findChild("header", recursive=False)
                    block[1] = header.text.strip()
                selection = []
                for item in blocks:
                    selection.append(item[1])
                os.system("clear")
                questions = [inquirer.Checkbox('Results', message="Select", choices=selection, ),
                             ]
                answers2 = inquirer.prompt(questions)

                indexes = []
                temp = answers2['Results']
                for item in temp:
                    indexes.append(selection.index(item))

                for index in indexes:
                    name = blocks[index][1]
                    f = open("series.txt", "a")
                    f.write(search_item.link+";"+str(name)+"\n")
                    #f.write(str(answers["Results"]).split('  ')[0]+";"+str(name)+"\n")
                    f.close()

        input("Finished")

def manual_download():
    print("test")
    os.system("clear")
    search_string = input("Search for: ")
    if search_string == "exit" or search_string == "e" or search_string == "cancel" or search_string == "quit" or search_string == "break":
        return

    search_results = search(search_string)
    selection = ['Zurück']+prepare_selection_array(search_results)
    if len(search_results) == 0:
        os.system("clear")
        print("No Results")
        input("")
        os.system("clear")
        return
    questions = [
      inquirer.List('Results', message="Results", choices=selection,
                ),
    ]
    answers = inquirer.prompt(questions)

    if answers["Results"] == "Zurück":
        return
    else:
        links = get_download_links(search_results[selection.index(answers["Results"])-1])

    input("Finished")

if __name__ == '__main__':
    while True:
        os.system("clear")
        choices =["manual download", "Add automatic download","exit"]
        questions = [
            inquirer.List('Results', message="Results", choices=choices,
                          ),
        ]
        answers = inquirer.prompt(questions)

        if answers["Results"] == "manual download":
            manual_download()
        if answers["Results"] == "Add automatic download":
            add_automatic_download()

        if answers["Results"] == "exit":
            break
