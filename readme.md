# Zabbiz Hetzner Storagebox Template

This is a Zabbix template used for monitoring used space on Hetzner Storage Box. 

The python script uses Hetzner's Web Services to get all data needed. You can get your webservice account on hetzner.com.

It automatically finds all active storageboxes and calculate the used space percentage.

## Warning
Hetzner web services have limits on how many requests you can do in a certain period of time. Please check their docs before choosing how often Zabbix should update his data.

## Installation

- Place zabbix-hetzner-storagebox.py and storagebox-user-parameters.conf in a Zabbix Agent conf.d folder.
- Edit the conf file and fix the path, the username and the password.
- Import the template on Zabbix Server.

## Usage
- Add the template to the desired host.
- Edit the template only Discovery Rule Update interval. Default is 60 minutes.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)