from bs4 import BeautifulSoup
import requests
import json
import csv
from datetime import date

html=requests.get("http://theverge.com")
html=html.text
soup= BeautifulSoup(html,"html.parser")

today=date.today()
d=today.strftime("%d%m%y")

def main():
    print("scrapping started!")
    def obj(Id,Headline,Url,Author,Date):
        return [Id,Headline,Url,Author,Date]

    id=list()
    headline=list()
    author=list()
    curr_date=list()
    url=list()

    #id
    for ids in soup.find_all(class_="z-10 flex h-5 w-5 items-center justify-center rounded-full bg-gray-31/90 font-polysans text-11 text-franklin"):
        id.append(ids.contents[0])

    # headline and url
    for i in soup.find_all(class_="group-hover:shadow-underline-franklin",href=True):
        url.append("https://www.theverge.com"+i['href'])
        headline.append(i.contents[0])

    # author
    for i in soup.find_all(class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8"):
        author.append(i.contents[0])

    # date
    for i in soup.find_all(class_="text-gray-63 dark:text-gray-94"):
        curr_date.append(i.contents[0])


    rows=["Id", "Headline", "Url", "Author", "Date"]
    store=list()
    for i in range(len(id)):
        data=obj(id[i],headline[i],url[i],author[i],d+" " +curr_date[i])
        store.append(data)

    # print(store)
    # print(d)
    with open(f"./JSON_Data/{d}_verge.json",'w') as file:
        json.dump(store,file,indent=4)

    with open(f"./ScrappedData/{d}_verge", 'w') as file:
        write = csv.writer(file,delimiter=",")
        write.writerow(rows)
        write.writerows(store)


if __name__=='__main__':
    main()