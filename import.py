import json
import sqlite3
from usefulFunctions import dubApos

conn = sqlite3.connect('radioGarden.db')
c = conn.cursor()

with open("./results/radio.garden.mp3s.json","r",encoding="UTF-8") as jsonFile:
    allRadioStations = json.load(jsonFile)
    # print(json.dumps(allRadioStations[0], indent=4))

try:
    c.execute('DROP TABLE RadioStations;')
except:
    print("No RadioStations Table")

#Probably should be making multiple tables 
# Id int PRIMARY KEY NOT NULL AUTOINCREMENT, 
c.execute( """
    CREATE TABLE RadioStations (
        Id varchar(50),
        Name nvarchar(255),
        Slug nvarchar(255),
        Website nvarchar(255),
        PlaceName nvarchar(255),
        PlaceX real,
        PlaceY real,
        Functioning TINYINT,
        Secure TINYINT,
        CountryName nvarchar(255),
        CountryCode varchar(3),
        Mp3 nvarchar(255)
    )  
    """)

# print(allRadioStations[0]["mp3"])
for radioStation in range(len(allRadioStations)):
    #print(allRadioStations[radioStation]) 
    # hyperlink = hyperlink if (isinstance(hyperlink,str)) else ("NULL")
    functioning = ('1' if (allRadioStations[radioStation]["functioning"] == 'true') else '0')
    secure = ('1' if (allRadioStations[radioStation]["secure"] == 'true') else '0')
    # print(functioning)
    # print(secure)
    
    # nothing from Mautitiana since the json files dont have a country code for it
    try:
        sql = "INSERT INTO RadioStations VALUES ( " 
        sql = sql + "'" + allRadioStations[radioStation]["id"] + "'," 
        sql = sql + "'" + dubApos(allRadioStations[radioStation]["name"]) + "'," 
        sql = sql + "'" + dubApos(allRadioStations[radioStation]["slug"]) + "'," 
        sql = sql + "'" + dubApos(allRadioStations[radioStation]["website"]) + "'," 
        sql = sql + "'" + dubApos(allRadioStations[radioStation]["place"]["name"]) + "'," 
        sql = sql + " " + str(allRadioStations[radioStation]["place"]["geo"][0]) + " ," 
        sql = sql + " " + str(allRadioStations[radioStation]["place"]["geo"][1]) + " ," 
        sql = sql + " " + functioning + " ," 
        sql = sql + " " + secure + " ," 
        sql = sql + "'" + dubApos(allRadioStations[radioStation]["country"]["name"]) + "'," 
        sql = sql + "'" + allRadioStations[radioStation]["country"]["code"] + "'," 
        sql = sql + "'" + str(allRadioStations[radioStation]["mp3"]) + "' " 
        sql = sql + ");"
        conn.execute(sql)
    except:
        print(sql)
    
conn.commit()

c.execute("SELECT * FROM RadioStations LIMIT 5;")
print(c.fetchall())

# sql =   "INSERT INTO RadioStations VALUES ( " 
#            sql = sql + "'" + allRadioStations[radioStation]["id"] + "'," 
#            sql = sql + "'" + dubApos(allRadioStations[radioStation]["name"]) + "'," 
#            sql = sql + "'" + dubApos(allRadioStations[radioStation]["slug"]) + "'," 
#            sql = sql + "'" + dubApos(allRadioStations[radioStation]["website"]) + "'," 
#            sql = sql + "'" + dubApos(allRadioStations[radioStation]["place"]["name"]) + "'," 
#             sql = sql + "'" + str(allRadioStations[radioStation]["place"]["geo"][0]) + " ," 
#             sql = sql + "'" + str(allRadioStations[radioStation]["place"]["geo"][1]) + " ," 
#             sql = sql + "'" + '1' if (allRadioStations[radioStation]["functioning"] == 'true') else '0' + " ," 
#             sql = sql + "'" + '1' if (allRadioStations[radioStation]["secure"] == 'true') else '0' + " ," 
#            sql = sql + "'" + dubApos(allRadioStations[radioStation]["country"]["name"]) + "'," 
#            sql = sql + "'" + allRadioStations[radioStation]["country"]["code"] + "'," 
#            sql = sql + "'" + str(allRadioStations[radioStation]["mp3"]) + "' " + ");"