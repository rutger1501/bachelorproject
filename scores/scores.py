import json
import os
import sys
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from bs4 import BeautifulSoup as Soup
import codecs


#open excel sheet containing allele information
#convert excel sheet to pandas dataframe, leaving only the first two columns (star alleles and acitivity score)
#replace NaN scores with 0
excel = 'scores/CYP2D6_allele_functionality_reference.xlsx'
df = pd.read_excel(excel, engine='openpyxl')
df = df.iloc[:, 0:2]
df.columns = ['allele', 'score']
df = df.drop(0)
df['allele'] = df.allele.astype(str)
df['score'] = df['score'].fillna(0)

#variables used to store information

variations = []
fn = sys.argv[1]


#opening report.json file, when using shellscript this will loop through all the files in the pharmcat output  folder
if os.path.exists(fn):
    f = open(fn)
data = json.load(f)

act_scores = []
#compare all available calls in the report for the CYP2D6 gene with scores from the excel sheet. Sum all the acitivity scores from all the variants together for a total acitivity score
for j in data['genotypes'][5]['calls']:
    score = 0
    variations.append(j)
    call = j.split('/', 1)[-1]
    call1 = j.split('/', 1)[0]
    select = df.loc[df['allele'] == call]
    select1 = df.loc[df['allele'] == call1]
    select['score'] = select['score'].astype(float)
    select1['score'] = select1['score'].astype(float)
    if select.size != 0 and select1.size != 0:
        score += select.iat[0,1]
        score += select1.iat[0,1]
        act_scores.append(score)
        

highest = 0
for item in act_scores:
        if item > highest:
                highest = item

tot = highest
print(highest)

f.close()

#print which file contains which variants and display the total calculated acitivity score
print("File: ", fn)
print("For star alleles: ", ', '.join(variations))
print("Highest activity score = ", tot)
print(" ")




#comparing acitivity scores to metabolizer scores based on the CYP2D6 table
metabolizer = " "

#scores are only saved if they are called. Not Called scores of 0 are not considerd
if any("not called" in s for s in variations):
        metabolizer = "Not Called"
else:
        with open ("scores.txt", "a") as file:
                file.write("\n")
                file.write(str(tot))
                file.close()
                
                
if float(tot) >= float(0) and float(tot) < float(0.5):
    metabolizer = "Poor metabolizer"
if float(tot) >= float(0.5) and float(tot) < float(1.0):
    metabolizer = "Intermediate metabolizer"
if float(tot) >= float(1.0) and float(tot) <= float(2.0):
    metabolizer = "Extensive metabolizer"
if float(tot) > float(2.0):
    metabolizer = "Ultra-rapid metabolizer"


######################
#writing to html file#
######################

#getting the right files from the right folder
sample = fn.split("/")[-1].split(".")[0]
html_file_folder = "/home/rutger/Desktop/PharmCAT-0.8.0/output/trimmed_canada/"
html_file = html_file_folder + sample + ".report.html"

html=codecs.open(html_file, 'r')
content = html.read()

#reading the html file and putting it into the soup constructor
soup = Soup(content, features="lxml")
table = soup.find("section", {"id": "genotypes"})
head = soup.find("head")

#getting the metabolizer score based on the activity table for CYP2D6
metabolizer_score = metabolizer + " (Activity score: " + str(tot) + ")"

#clean up the report.html genotype summary table and insert metabolizer_score
#in the CYP2D6 row
for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    cells[2].extract()
    cells[3].extract()
    phenotypes = []
    for word in cells[4].text.strip().split("\n"):
        if word not in phenotypes:
            phenotypes.append(word)

    if cells[1].text.strip()[:-1] == 'CYP2D6':
        new_td = soup.new_tag('td')
        new_td.append(metabolizer_score)
        cells[4].replace_with(new_td)
    else:
        clean_td = soup.new_tag('td')
        for entry in phenotypes:
            clean_td.append("\n")
            clean_td.append(entry)
        cells[4].replace_with(clean_td)

#remove headers
for header in table.find_all("th"):
    if header.text == "Genotype" or header.text == "Allele Functionalitya":
        header.extract()

#generating the output file and folder and writing the table to a new html file
outputfolder = "summary_tables/"
output_file = outputfolder + sample + "_table.html"


with open(output_file, "w") as file:
        file.write(str(head))
        file.write(str(table))
        file.close()
