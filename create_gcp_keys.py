from os import environ

import dotenv


def main():
    dotenv.load_dotenv()
    gcp_json_plain = environ.get('GCP_KEYS_JSON')
    with open('gcp-keys.json', 'w', encoding='utf-8') as f:
        if gcp_json_plain is None:
            print('GCP_KEYS_JSON is not set')
            return
        f.write(gcp_json_plain)

if __name__ == '__main__':
    main()
