from bs4 import BeautifulSoup
from os.path import basename
import urllib.request
import requests
import time
import csv
import os

issue_csv = os.path.join('../'+'Data', 'issue.csv')

# Testing part number will add aditional parts in loop. 
# test_batch = ['D333MU@-UL', '07-t-002', 'D333MU@-UL', '07-t-002','D333MU@-UL', '07-t-002','D333MU@-UL', '07-t-002',]
# temp_part = 'D333MU@-UL'
# temp_part = '07-t-002'
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

def image_fix(url):
    ''' Takes image thumbnail URL and Updates the URL to a full image
        example:
            https://ktperformance.net/images/T143863006.jpg
                                to
            https://ktperformance.net/images/F143863006.jpg                    
     '''
    
    parsed_url = url.split('/')[4].split('.')[0]
    image_list = list(parsed_url)
    del image_list[0]
    image_list.insert(0,'F')
    corrected_image =''.join(image_list)
    corrected_url = f'https://ktperformance.net/images/{corrected_image}.jpg'
    return corrected_url

def scrape(url):
    ''' Initialize and scrape KTPerformance.net for images by part_number '''
    part_link = []
    image_source = []
    
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    image_tags = soup.findAll('img', attrs = {'class':'lazyload'})
    for image in image_tags:
        image_source.append(image['src'])
    if len(image_source) > 1:
        return image_fix(image_source[1])
    else:
        return image_fix(image_source[0])

def run():    
    log_list = []
    part_numbers = get_part_numbers(issue_csv)
    print('''
    --------------------Begining Data Retrieval.--------------------------
    ''')
    for part in part_numbers:
        try:
            time.sleep(1)
            scrape_url=f'https://ktperformance.net/search.html?q={part}' 
            print(f'Scraping {scrape_url}.')
            urllib.request.urlretrieve(scrape(scrape_url), os.path.join('../' + 'Images', f'{part}.jpg'))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print('Image or part not found, skipping.')
            log_list.append(f'Part number:{part}--{scrape_url}\n')
    
    log_file = open(os.path.join('../' +'Logs', 'error_log.txt'), 'w+')
    for log in log_list:
        log_file.write(log)
    log_file.close()
    print('''
    --------------------Data Retrieval Complete.--------------------------
    ------------See error_log.txt for parts that failed scrape.-----------
    ''')

if __name__ == '__main__':
    run()