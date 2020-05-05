# GISAID_scrapper
This tool can be used to download the samples and metadata from GISAID provided you have an existing account with download privileges.

You also need to download chrome webdriver based on your operating system and place it in the directory.
Link: https://chromedriver.chromium.org

      - virtualenv virtual_env
      - source virtual_env/bin/activate
      - pip install -r requirements.txt
      - python main_scrapper.py
      
To run in headless mode use the following command:

      - python main_scrapper.py -q
      
      
or

      - python main_scrapper.py --headless
      
