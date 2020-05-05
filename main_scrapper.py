import argparse, sys
from gisaid_scrapper import GisaidCoVScrapper
from gisaid_metadata_scrapper import GisaidCoVMetadataScrapper

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('--headless', '-q', help="Headless mode of scraping (experimental)", type=str2bool, nargs='?', default=False)

    args = parser.parse_args()
    args.headless = True if args.headless is None else args.headless 
    return args

def get_credentials():
    try:
        with open('credentials.txt') as f:
            login = f.readline()
            passwd = f.readline()
    except FileNotFoundError:
        print("File not found.")
        sys.exit(-1)

    return login, passwd

if __name__ == "__main__":
    args = parse_args()
    login, passwd = get_credentials()
    print("Downloading Metadata!!!!!")
    metadata_scrapper = GisaidCoVMetadataScrapper(args.headless)
    metadata_scrapper.login(login, passwd)
    metadata_scrapper.load_epicov()
    print("Downloading FASTA!!!!!")
    scrapper = GisaidCoVScrapper(args.headless)
    scrapper.login(login, passwd)
    scrapper.load_epicov()
    print("All Downloaded")