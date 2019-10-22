from bs4 import BeautifulSoup
from os.path import basename
import urllib.request
import requests
import time
import csv
import os

issue_csv = os.path.join('.'+'/Data', 'issue.csv')

# Testing part number will add aditional parts in loop. 
# temp_part = 'RT-WARRIOR-30-10-14'
# scrape_url = f'https://ktperformance.net/search.html?q={temp_part}'

def get_part_numbers(csv_input):
    '''reads csv and pulls part numbers to search in scrape'''
    
    with open(csv_input) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        next(read_csv)
        part_numbers = []
        for row in read_csv:
            part = row[0]
            part_numbers.append(part)
    return part_numbers

def image_fix(url_to_fix):
    ''' Takes image thumbnail URL and Updates the URL to a full image
        example:
            https://ktperformance.net/images/T143863006.jpg
                                to
            https://ktperformance.net/images/F143863006.jpg                    
     '''
    
    parsed_url = url_to_fix.split('/')[4].split('.')[0]
    image_list = list(parsed_url)
    del image_list[0]
    image_list.insert(0,'F')
    corrected_image =''.join(image_list)
    corrected_url = f'https://ktperformance.net/images/{corrected_image}.jpg'
    
    return corrected_url

def scrape(url_to_scrape):
    ''' Initialize and scrape KTPerformance.net for images by part_number '''
    
    content = requests.get(scrape_url).content

    soup = BeautifulSoup(content, 'html.parser')
    image_tags = soup.findAll('img', attrs = {'class':'lazyload'})
    image_source=[]
    for image in image_tags:
        image_source.append(image['src'])
    return image_fix(image_source[1])

if __name__ == "__main__":
    part_numbers = get_part_numbers(issue_csv)
    print('''
    --------------------Begining Data Retrieval---------------------------
    ''')
    for part in part_numbers:
        try:
            time.sleep(0)
            scrape_url=f"https://ktperformance.net/search.html?q={part}" 
            print(scrape_url)
            urllib.request.urlretrieve(scrape(scrape_url), f"./Images/{part}.jpg")
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print('Image or part not found skipping')
            log_file = open("error_log.txt", 'w+')
            log_file.write(f'Part number:{part}')
            log_file.close()

    print('''
    --------------------Data Retrieval Complete---------------------------
    ''')

