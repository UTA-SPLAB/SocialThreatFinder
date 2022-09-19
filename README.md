# ![Alt text](/img/stf_logo.png?raw=true "Social ThreatFinder Banner")

**Social ThreatFinder** is an OSINT (Open source intelligence) tool which identifies new social engineering threats, such as phishing websites, that are reported on social media networks and provides additional reliable and feature-rich data about these attacks in the form of an easily accessible blocklist. 

The creation of this tool was motivated by the findings in our work “Evaluating the Effectiveness of Phishing Reports on Twitter”, published at APWG eCrime 2021 ([Link to the paper](https://ieeexplore.ieee.org/abstract/document/9738786?casa_token=FjAIF57PrIUAAAAA:timEgDLq87uH-jxlNFpAbrDjAxesCbdHV3Rg05ywazIEAkLi0Bb_JVNAfhNAOR0RrczqTwk3M_Y)). 

**The contributions of this paper are as follows:**

- We identified several security conscious individuals on Twitter who regularly shared reports about new phishing websites. These reports often contained a lot of more contextual information regarding the attacks when compared to two of the most popular anti-phishing blocklists.

- Website takedown for the reported URLs was significantly slow, with nearly 31% of these attacks remaining online even a week after the report being shared. The tweets were very rarely interacted upon by hosting providers and targetted organizations, suggesting that they had a hard time *discovering* these attacks. 


- Also, a large volume of these reported URLs were not covered by prevalent anti-phishing tools and blocklists, with only less than 9% of the URLs shared on Twitter overlapping with these entities.  

Thus, the Social ThreatFinder framework (STF) attempts to provide more visibility to these reports by systematizing them under one consistent and easily accessible blocklist. Regularly sharing this information with antiphishing blocklists, hosting providers and other concerned security actors can help in enhancing the response towards these emerging attacks, and in turn, also boost the prevalent anti-phishing and anti-scam ecosystem. 

<p align="center">
<img src="/img/phishing_reports.png"/>
</p>

<p align="center">
  <b>Example of some phishing reports found on Twitter</b>
</p>

## 1) Open-source code-base and our Framework

This repository includes all the core functionality which powers the Social ThreatFinder website, which is currently under development. By running this codebase, you can build your own URL repository (from scratch) using phishing reports shared on Twitter. The full database can be accessed at anytime from the Social ThreatFinder website, and our STF REST API (both coming soon). For more information about the web interface and an early look, please check **Section 3** below.

The following is a basic illustration of the Social ThreatFinder framework (in its current stable state). Note that we have several experimental features (non-stable) **(See Section 4)**, that have not been included in this illustration.  

![Alt text](/img/stf_framework_basic.png?raw=true "Social ThreatFinder Framework")

## 2) Instructions for running Social ThreatFinder (STF)

**Updated: 09/18/2022, v0.19 stable release** 

**Step 1** Create a virtual environment with Python 3.8.10

**Step 2:** Install the necessary dependencies from the requirements.txt file:

```
pip3 install -r requirements.txt
```

**Step 3:** To obtain new reports from Twitter, you will need a Twitter API access key. For full functionality, the **Academic Track** of the API is recommended, which can be obtained from here: https://developer.twitter.com/en/products/twitter-api/academic-research

**Step 4:** After getting the API access key, configure your key with Twarc (The python library we use to collect the reports) by entering the following command in your console, and enter your Bearer Token in the resulting prompt:

```
twarc2 configure
Please enter your Bearer Token (leave blank to skip to API key configuration): 
```

**Note:** STF also runs on regular Twitter API access (non-academic, 'Lite' mode) from v0.19 stable onwards. You can sign up for a regular API key on https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api. See how to run STF in 'Lite' mode in Step 5.2


**Step 5:** STF uses a CNN based image classifier to identify if the reported URL is phishing or benign by analyzing the website screenshot. For this feature, you need to install and setup chromedriver on your system.

https://skolo.online/documents/webscrapping/

**Step 6:** You can now launch Social ThreatFinder by running:

5.1) In **Default** mode (using Twitter Academic API key access):

```
python3 run_stf.py
```
5.2) In **'Lite'** mode (using Regular Twitter API key access):

```
python3 run_stf.py lite
```

<p align="center">
<img src="/img/stf_running.png" width="500" height="280"/>
</p>

**WARNING:** Due to Twitter API limitations, running in *'Lite'* mode *might* not give you the most up-to-date reporter data. It is recomended that you run STF in **Default** mode only.  


**Step 7:** You can view the output under database/db.csv. 

## 3) Social ThreatFinder website (An early look)

The full Social ThreatFinder website is currently in development and is expected to be released in *mid November 2022*. 

Check out the three main features of the website, along with an early look below:

- **The blocklist:** A simple interface which shows all phishing reports that have been collected and analyzed by the STF instance on our server. This blocklist is updated in real-time.  

![Alt text](/img/stf_database.png?raw=true "Blocklist interface")
	
- **Interactive map:** An layout which points to the location of both active and inactive phishing threats found by STF. 

![Alt text](/img/stf_map.gif?raw=true "Interactive Map")

- **STF API:** A REST API which can be used to obtain metadata for all URLs collected by the STF instance running on our servers. It is the easiest way to access STF data without maintaining your own local instance. 
<p align="center">
<img src="/img/stf_api_demo.png" width="500" height="280"/>
</p>

## 4) Experimental features

Brief overview of some experimental features that are currently under construction, with plans for release in future stable builds:

1) Identifying new social engineering attacks from narratives shared by users on Twitter, Facebook and Reddit. 
2) Checking the reliability of new phishing reporters (on Twitter) based on their account heuristics.
3) An ML based tool which provides better identification\* of whether the website is active/inactive/parked, when compared against other open-source anti-phishing implementations.
4) Focus on covering smartphone specific social engineering attacks 

###### \*Preliminary comparison with URLLib, PhishTank and APWG eCrimeX data.


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
