# ![Alt text](/img/stf_logo.png?raw=true "Social ThreatFinder Framework")

Social ThreatFinder is an OSINT (Open source intelligence) tool which identifies new social engineering threats, such as phishing websites, that are reported on social media networks and provides additional reliable and feature-rich data about these attacks under an easily accessible blocklist. 

The creation of this tool was motivated by our findings in “Evaluating the Effectiveness of Phishing Reports on Twitter”, published at APWG eCrime 2021.[Link to the paper](https://ieeexplore.ieee.org/abstract/document/9738786?casa_token=FjAIF57PrIUAAAAA:timEgDLq87uH-jxlNFpAbrDjAxesCbdHV3Rg05ywazIEAkLi0Bb_JVNAfhNAOR0RrczqTwk3M_Y). 

**The contributions of this work are as follows:**

- We identified several security conscious individuals on Twitter who regularly shared reports about new phishing websites. These reports often contained more information regarding the attack, when compared to two of the most popular anti-phishing blocklists.

- Website takedown for the reported URLs was significantly slower than the attacks which were covered by popular blocklists. This resulted in these attacks staying online for an extended period of time.

- Consequently, a large volume of these URLs were not covered by prevalent anti-phishing tools and blocklists. 

Thus, Social ThreatFinder (STF) attempts to provide more visibility to these reports to enhance the anti-phishing and anti-scam ecosystem. 

## 1) Open-source code-base and our Framework

This repository includes all the core functionality which powers the Social ThreatFinder website, which is currently under development. By running this codebase, you can build your own URL database (from scratch) using phishing reports shared on Twitter. The full database can be accessed at anytime from the easy to use Social ThreatFinder website, and our STF REST API (both coming soon). For more information about the web interface and an early look, please check **Section 3** below.

Below is basic illustration of the Social ThreatFinder framework (in its current stable state). Note that we have several experimental features (non-stable) **(See Section 4)**, that have not been included in this framework.  

![Alt text](/img/stf_framework_basic.png?raw=true "Social ThreatFinder Framework")

## 2) Instructions for running Social ThreatFinder (STF)

**Updated: 09/12/2022, v0.19** 

**Step 1:** Install the necessary libraries from the requirements.txt file:

```
pip3 install -r requirements.txt
```

**Step 2:** To obtain new reports from Twitter, you will need a Twitter API access key. For full functionality, the Academic Track of the API is recommended, which can be obtained from here https://developer.twitter.com/en/products/twitter-api/academic-research

**Step 3:** After getting the API access key, configure your key with Twarc (The python library we use to collect the reports) by entering the following command in your console, and enter your Bearer Token in the resulting prompt.:

```
twarc2 configure
Please enter your Bearer Token (leave blank to skip to API key configuration): 
```

**Note:** STF also runs on regular Twitter API access (non-academic, 'Lite' mode) from stable v0.19 onwards. You can sign up for a regular API key on https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api. See how to run STF in 'Lite' mode in Step 5.2


**Step 4:** STF uses a CNN based classifier to identify if the reported URL is phishing or benign by analyzing the website screenshot. For this feature, you need to install and setup chromedriver on your system/environment. 

https://skolo.online/documents/webscrapping/

**Step 5:** You can now launch Social ThreatFinder by running:

5.1) In **Default** mode (using Twitter Academic API key access):

```
python3 run_stf.py
```
5.2) In **'Lite'** mode (using Regular Twitter API key access):

```
python3 run_stf.py lite
```

**WARNING:** Due to API limitations, running in *'Lite'* mode might **NOT** give you the most up-to-date reporter data. It is recomended that you run STF in **Default** mode only.  


**Step 6:** You can view the output under database/db.csv. 

## 3) Social ThreatFinder website (An early look)

The full Social ThreatFinder website is currently in development and is expected to be released in *mid November 2022*. 

Check out the three main features of the website, along with an early look below:

- **The blocklist:** A simple interface which shows all phishing reports that have been collected and analyzed by the STF instance on our server. This blocklist is currently updated every 5 mins.  

![Alt text](/img/stf_database.png?raw=true "Blocklist interface")
	
- **Interactive map:** An layout which points the location of the active and inactive phishing threats found by STF. 

![Alt text](/img/stf_map.gif?raw=true "Interactive Map")

- **STF API:** A REST API which can be used to obtain URLs from the STF instance running on our servers. The easiest way to access STF data without maintaining your own local instance. 
<p align="center">
<img src="/img/stf_api_demo.png" width="500" height="280"/>
</p>

## 4) Experimental features

Brief overview of some experimental features that we are under work and we are planning to release in future stable builds:

1) Identifying new social engineering attacks from narratives shared by users on Twitter, Facebook and Reddit. 
2) Checking the reliability of new phishing reporters (on Twitter) based on their account heuristics.
3) An ML based tool which provides better identification\* of whether the website is active/inactive/parked, when compared against other open-source anti-phishing implementations.
4) Focus on covering of smartphone specific social engineering attacks 

###### \*Preliminary comparison with URLLib, PhishTank and eCrimeX data.


If you like this work, please consider citing our publication:

```
@inproceedings{roy2021evaluating,
  title={Evaluating the effectiveness of Phishing Reports on Twitter},
  author={Roy, Sayak Saha and Karanjit, Unique and Nilizadeh, Shirin},
  booktitle={2021 APWG Symposium on Electronic Crime Research (eCrime)},
  pages={1--13},
  year={2021},
  organization={IEEE}
}
```
For any queries, feel free to reach out to Sayak Saha Roy (sayak.saharoy@mavs.uta.edu) and Shirin Nilizadeh (shirin.nilizadeh@uta.edu).
