import pandas as pd
from bs4 import BeautifulSoup
import requests

dept = ["ACCT", "ADMJ", "AFAM", "ANTH", "APRN", "ARTS", "ASAM",
        "ASTR", "AUTO", "BIOL", "BUS", "CD", "CETH", "CHLX", "CIS",
        "CLP", "COMM", "COUN", "DANC", "DMT", "ECON", "EDAC", "EDUC",
        "ELIT", "ENGR", "ES", "ESCI", "ESL", "EWRT", "F/TV", "FREN",
        "GEO", "GEOL", "GERM", "GUID", "HIST", "HLTH", "HNDI", "HTEC",
        "HUMA", "HUMI", "ICS", "INTL", "ITAL", "JAPN", "JOUR", "KNES",
        "KORE", "LART", "LIB", "LING", "LRNA", "LS", "MAND", "MASG",
        "MATH", "MET", "MUSI", "NAIS", "NURS", "NUTR", "PARA", "PE",
        "PEA", "PERS", "PHIL", "PHTG", "PHYS", "POLI", "PSYC", "READ",
        "REST", "RUSS", "SIGN", "SKIL", "SOC", "SOSC", "SPAN", "SPED",
        "THEA", "VIET", "WMST"]

term = "F2023"
for i in dept:
    print(i)
    try:
        val = "https://www.deanza.edu/schedule/listings.html?dept="+i+"&t="+term

        page = requests.get(val).text

        soup = BeautifulSoup(page, "html.parser")

        tables = soup.find_all('table')

        table = soup.find('table', class_='table table-schedule table-hover mix-container')

        df = pd.DataFrame(columns=['CRN', 'COURSE', 'SECTION', 'DAY', 'START TIME', 'END TIME', 'NAME', 'LOCATION'])

        # Collecting data
        for row in table.tbody.find_all('tr'):
            # Find all data for each column
            columns = row.find_all('td')

            if columns:
                try:
                    crn = columns[0].text.strip()
                    course = columns[1].text.strip()
                    section = columns[2].text.strip()
                    days = columns[5].text.strip()
                    days = ''.join([i for i in days if i.isalpha()])
                    time = columns[6].text.strip()
                    startTime = ""
                    endTime = ""
                    if time != "TBA-TBA":
                        x = 0
                        while x < 2:
                            startTime += time[x]
                            endTime += time[x + 9]
                            x += 1
                        x += 1  # skip ':'

                        while x < 5:
                            startTime += time[x]
                            endTime += time[x + 9]
                            x += 1

                        startTime = int(startTime)
                        endTime = int(endTime)
                        if time[6] == 'P':
                            if startTime < 1200:
                                startTime += 1200

                        if time[15] == 'P':
                            if endTime < 1200:
                                endTime += 1200

                    name = columns[7].text.strip()
                    location = columns[8].text.strip()
                except:
                    continue

                df = df._append({'CRN': crn, 'COURSE': course, 'SECTION': section,'DAY': days,
                                 'START TIME': startTime, 'END TIME': endTime, 'NAME': name,
                                 'LOCATION': location}, ignore_index=True)
        if i == "F/TV":
            filename = "FTV_" + term + "_data.csv"
        else:
            filename = i + '_' + term + '_data.csv'

        df.to_csv(filename, index = False)
    except:
        continue
