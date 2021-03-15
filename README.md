# ZDF-Scraper
 A simple python script to automatically download tv shows from the ZDF media library. 
 
 
# Usage
## downloader
![First Selection](https://i.imgur.com/nh3vCzc.png)

In the first selection, you can decide, wether you want to 
1. manually download series from the ZDF media library by selecting "manual download"
2. Search and add a tv-show, which should be added to the series.txt, so it will be automatically downloaded when executing the "auto_downloader.py" script by selecting "Add automatic download"
3. exit the program

![Search result](https://i.imgur.com/4JEso4V.png)

After searching the desired tv-show, you get some basic information about the show and can select the the right show.

![video types](https://i.imgur.com/lh87bN0.png?1)

Once you selected the desired tv-show, you can select the videos of the show, which you want to download.

The next step depends on wether you selected "Manual download" or "Add automatic download" in the beginning.
If you selected Manual download the script will start downloading  the selected tv-show which then can be found in the downloads folder.

If you selected "Add automatic download" the show is added to a list of series that will be downloaded when the auto_downloader script is being executed.
 
## auto_downloader.py
Once you added a series for automatic download with the downloader script, this script can be executed to automatically download **all** series which you wanted to be downloaded. If the video is already downloaded, the script will skip the video and move to the next one. That way this script can be executed frequently (e.g. with a cron job) so it will only download new videos

# Installation Linux
## 1. Clone Github repository

`git clone https://github.com/BastianLo/ZDF_Scraper`

## 2. Install Dependencies

ZDF_Scraper depends on certain python libraries, which can be installed with the following commands:

Installation of Beatifulsoup4:

`pip3 install bs4`

Installation of Inquirer:

`pip3 install inquirer`

Installation of youtube-dl:

`pip3 install youtube-dl`

## 3. make scripts executable:
`chmod +x ZDF_Scraper/scripts/downloader.py && chmod +x ZDF_Scraper/scripts/auto_downloader.py`

## 4. Execute Scripts
Scripts can be executed with `./downloader.py` & `./auto_downloader.py`
