# Telegram Scraper
### Telegram chat scraper

Telegram Scraper is a simple script for scraping Telegram chat data which are publicly available. It uses the Telethon library for accessing Telegram API. The scraper runs from a UNIX terminal and is written in Python 3.

For scraper to work you will need to create a Telegram API key (see [Use](#use) section for more information).

## State
This project is still in development. 

## Use
Before using  you need to create a Telegram API key. You can find more information about creating Telegram API key [here](https://core.telegram.org/api/obtaining_api_id). After creating the key you need to create a file named `config.ini` in the same directory as `scrap.py` and add the following lines to it:
```ini
[Telegram]
api_id = #your api id
api_hash = #your api hash
username = #your username
```
After that you can run the script with the following commands:

```bash
./scrap.py
#runs the main script
./scrap.py -h
#shows help
./scrap.py -c
#generates channel list

```
## License
[GNU GPL](https://www.gnu.org/licenses/gpl-3.0.en.html)
