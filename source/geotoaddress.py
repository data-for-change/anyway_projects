from urllib.request import urlopen
import psycopg2
import json
import sys
import csv

'''
Connect to googles geocode api  and converts lat,lon to location name
'''
def getplace(lat, lon, api_key):
    components = ''
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json?key=%s" % (api_key)
        url += "latlng=%s,%s&sensor=false" % (lat, lon)
        v = urlopen(url).read()
        j = json.loads(v)

        if (j['status'] == 'OVER_QUERY_LIMIT'):
            print("GOOGLE: OVER_QUERY_LIMIT...\n")

        if j['results']:
            components = j['results'][0]['formatted_address']
    except Exception as e:
        print(e)
    return components

'''
Reads coordinates from the database and try to match lat,lon to google location
'''
def writePlaceToCvs(cvsFile, api_key,db_password):
    try:
        connStr = "dbname='anyway' user='postgres' host='localhost' password='%s'" % (db_password)
        conn = psycopg2.connect(connStr)
        cur = conn.cursor()
        try:
            cur.execute("""select lat,lon from research.junction_50m_accurate_2015_2018""")

        except:
            print("Can't find database!\n")

        rows = cur.fetchall()
        print("\nRows: \n")

        f = open(cvsFile, 'wt')
        try:
            writer = csv.writer(f)
            writer.writerow(('lon', 'lat', 'google_info'))

            for row in rows:
                try:

                    place = getplace(row[0],row[1],api_key)
                    print(row[0], row[1],place)
                    writer.writerow((row[0], row[1], place))
                except Exception as e:
                    print(row[0],row[1],e);
        finally:
            f.close()
    except Exception as ex:
        print(ex)

    return

def isBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return False
    #myString is None OR myString is empty or blank
    return True

'''
Used to re-run on existing csv file against original csv results
'''
def readWritePlaceCsv(csvRead,csvWrite,api_key):
    fin = open(csvRead, 'rt')
    fout = open(csvWrite,'wt')
    try:
        writer = csv.writer(fout)
        reader = csv.reader(fin)
        isHeader = True
        for row in reader:
            if(isHeader):
                isHeader = False
                continue

            if len(row) != 3:
                continue

            if not isBlank(row[2]):
                writer.writerow((row[0],row[1],row[2]))
            else:
                place = getplace(row[0], row[1],api_key)
                print(row[0], row[1], place)
                writer.writerow((row[0], row[1], place))

    except Exception as e:
        print(e)

    try:
        fin.close()
    except:
        pass

    try:
        fout.close()
    except:
        pass

    return

csv_file = "results.csv"
api_key = '<Enter Google key for geocode>'
db_password = '<Enter postgres password>'
writePlaceToCvs(csv_file,api_key,db_password)

#readWritePlaceCsv('processedRes.csv','processedRes2.csv')

