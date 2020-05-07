# GISAID_scrapper
This tool can be used to download the samples and metadata from GISAID provided you have an existing account with download privileges.

You also need to download chrome webdriver based on your operating system and place it in the directory (for Windows).

For Linux, you need to place the chrome webdriver in usr/bin or in PATH after executing:

       chmod a+x chromedriver

You also need to make sure that the credentials.txt has your username and password exactly as given in the file.

       <username>
       <password>

Link: https://chromedriver.chromium.org

       virtualenv virtual_env
       source virtual_env/bin/activate
       pip install -r requirements.txt
       python main_scrapper.py

To run in headless mode use the following command:

       python main_scrapper.py -q
      
or

       python main_scrapper.py --headless
      
