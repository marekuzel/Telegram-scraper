# Hedon
### Telegram chat scrapper

Hedon is a simple script for scraping Telegram chat data which are publicly availible. It uses Telethon library for accessing Telegram API.

For Hedon to work you will need to create a Telegram API key (see [Use](#use) section for more information).

## State
Hedon is still in development

## Use
Before using Hedon you need to create a Telegram API key. You can find more information about creating Telegram API key [here](https://core.telegram.org/api/obtaining_api_id). After creating the key you need to create a file named `config.ini` in the same directory as `hedon.py` and add the following lines to it:
```ini
[Telegram]
api_id = #your api id
api_hash = #your api hash
username = #your username
```
After that you can run the script with the following commands:

```bash
./hedon.py
#runs the main script
./hedon.py -h
#shows help
./hedon.py -c
#generates channel list
./hedon.py -n
#runs the script with number of mentions for subjects
#this feature is just for estimating the number of mentions
#and is not accurate

```
## License
[GNU GPL](https://www.gnu.org/licenses/gpl-3.0.en.html)
