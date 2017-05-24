# Alex Lee
# May 23rd, 2017
#

import requests
import codecs
import pandas as pd
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

def open_file(path):
    """Opens csv file at path and deals with encoding issues.
    Cleans data and returns a list of all the urls in the file.
    
    Parameters: path - a local to path to a csv file
    Returns: a list of cleaned url strings
    """
    url_list = list(codecs.open(path, encoding='utf-8-sig'))
    cleaned_list = []
    for url in url_list:
        cleaned_url = url.strip('\r')
        if cleaned_url[0:4] != 'www.':
            cleaned_url = 'www.' + cleaned_url
        cleaned_url = 'http://' + cleaned_url
        cleaned_list.append(cleaned_url)
    return cleaned_list

def get_server_data(url):
    """ Opens a url and returns the status code, server response time, and contact link if successfully opened.
    Otherwise, prints an error. Two different packages are used to access the web pages.
    'requests' is used to get the status code and server response time.
    'httplib2' and 'BeautifulSoup' are used to create the crawler that searches for contact links.
    
    Parameters: url - a cleaned url string
    Returns: status code, server response time, and contact link as a list
    """
    try:
        r = requests.head(url)
        contact_link = 'n/a'        
        http = httplib2.Http(disable_ssl_certificate_validation=True)
        try:
            status, response = http.request(url)
            for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
                if '/contact' in str(link):
                    if link.has_attr('href'):
                        contact_link = link['href']
                    return r.status_code, r.elapsed, contact_link
        except httplib2.RedirectLimit, httplib2.FailedToDecompressContent:
            print 'Error retrieving Server Data for ' + url + '.'
        return r.status_code, r.elapsed, contact_link
    except requests.ConnectionError:
        print 'Error retrieving Server Data for ' + url + '.'

def data_frame(list_of_dicts):
    """Convert a list of dictionaries into a pandas DataFrame.
    Outputs the data into a csv file called 'results.csv' with the url column as the index.
    
    Parameters: list_of_dicts - list of dictionaries containing information for each url
    Output: csv file named 'results.csv'
    """
    df = pd.DataFrame(list_of_dicts)
    index_df = df.set_index('url')
    index_df.to_csv('result.csv')

def main():
    """ Main function
    Three urls were removed from the code because they broke my crawler for obtaining the contact links.
    """
    url_list = open_file('/Users/AlexLee/Desktop/DataOperationsCandidateProject.csv')
    url_list.remove('http://www.bitcoin-otc.com')
    url_list.remove('http://www.ipdomain.net')
    url_list.remove('http://www.athomecaretn.com')
    dict_list = []
    for url in url_list:
        server_data = get_server_data(url)
        print server_data
        if server_data == None:
            dict_list.append({'url': str(url), 'HTTP_Response_Code': 'n/a',
            'Server_Response_Time': 'n/a', 'Contact_Link': 'n/a'})
        else:
            server_response_time = str(server_data[1]).replace('0:00:0', '')
            dict_list.append({'url': str(url), 'HTTP_Response_Code': server_data[0],
            'Server_Response_Time': server_response_time, 'Contact_Link': server_data[2]})
    data_frame(dict_list)

# If this file, Project.py, is run as a Python script (such as by typing
# "python Project.py" at the command shell), then run the main() function.
if __name__ == "__main__":
    main()