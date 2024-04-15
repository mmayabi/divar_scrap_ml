import requests
from bs4 import BeautifulSoup
import mariadb
import sys
import time
from sklearn import tree
import mymodules

def main():
    # Connect DB
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="127.0.0.1",
            port=3306,
            database="divar"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    conn.autocommit = False
    cur = conn.cursor()

    print("This app gather data from divar and then predict price of apartment based extracted data from divar.")
    print("At first you should gather data from divar in DB. Then you can predict.")
    action = input("For gather data inter (IMPORT), and for predict inter (PREDICT) : ")

    # Web scapting
    if action.lower() == "import":
        print("Gather data takes times. More data, beter prediction.")
        pages = input("Number of pages for scroll: ")
        city = input("Enter city: ")
        # Get links
        links = []
        for i in range(1,int(pages)):
            time.sleep(20)
            request = requests.get("https://divar.ir/s/%s/buy-apartment?page=%i" % (city, i))
            soup = BeautifulSoup(request.text, "html.parser")
            body = soup.find_all("div", attrs={'id': 'post-list-container-id'})
            for link in body[0].find_all('a'):
                links.append(link.get('href'))

        # extract data form links and insert them to DB
        unique_links = mymodules.unique_list(links)
        for link in unique_links:
            print(link)
            home_attributes = mymodules.extract_ad_data(link)
            print(home_attributes)
            if bool(home_attributes):
                cur.execute("INSERT INTO buyapartment (price,location,metraj,sakht,otagh,asansor,parking,anbari,floor,link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (home_attributes['price'], 
                     home_attributes['location'], 
                     home_attributes['metraj'],
                     home_attributes['sakht'],
                     home_attributes['otagh'],
                     home_attributes['asansor'],
                     home_attributes['parking'],
                     home_attributes['anbari'],
                     home_attributes['floor'],
                     link))
        conn.commit()

    # ML
    elif action.lower() == "predict":
        x = []
        y = []
        cur.execute("SELECT price,location,metraj,sakht,otagh,asansor,parking,anbari,floor FROM buyapartment")
        for (price,location,metraj,sakht,otagh,asansor,parking,anbari,floor) in cur:
            x.append([mymodules.convert2int(location),metraj,sakht,otagh,asansor,parking,anbari,floor])
            y.append(price)
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(x, y)
        print("Inter your apartment featurs.")
        location = input("location: ")
        metraj = input("metraj(in meter): ")
        sakht = input("sakht(like 1402): ")
        otagh = input("otagh: ")
        floor = input("floor: ")
        asansor = input("asansor(1 if has else 0): ")
        parking = input("parking(1 if has else 0): ")
        anbari = input("anbari(1 if has else 0): ")

        new_apartment = [[mymodules.convert2int(location),int(metraj),int(sakht),int(otagh),bool(asansor),bool(parking),bool(anbari),int(floor)]]
        price_predict = clf.predict(new_apartment)
        print("Predicted price for your apartement is %i" % price_predict[0])

    else:
        print("You input is wrong. Try again")
    conn.close()

if __name__ == "__main__":
    main()
