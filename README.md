# Social Threat Finder

Social ThreatFinder is an OSINT (Open source intelligence) tool which identifies new social engineering threats, such as phishing websites, that are reported on social media networks and provides additional reliable and feature-rich data about these attacks under an easily accessible blocklist. 

The creation of this tool was motivated by our findings in “Evaluating the Effectiveness of Phishing Reports on Twitter”, published at APWG eCrime 2021. [Link to the paper](https://ieeexplore.ieee.org/abstract/document/9738786?casa_token=FjAIF57PrIUAAAAA:timEgDLq87uH-jxlNFpAbrDjAxesCbdHV3Rg05ywazIEAkLi0Bb_JVNAfhNAOR0RrczqTwk3M_Y). 

**The contributions of this work were as follows:**

- We identified several security conscious individuals on Twitter who regularly shared reports about new phishing websites. These reports often contained more information regarding the attack, when compared to two of the most popular anti-phishing blocklists.

- Website takedown for the reported URLs was significantly slower than the attacks which were covered by popular blocklists. This resulted in these attacks staying online for an extended period of time.

- Consequently, a large volume of these URLs were not covered by prevalent anti-phishing tools and blocklists. 

Thus, Social ThreatFinder (STF) attempts to provide more visibility to these reports to enhance the anti-phishing and anti-scam ecosystem. 

## Our Framework

![Alt text](/img/stf_framework_basic.png?raw=true "Social ThreatFinder Framework")

## Instructions for running Social ThreatFinder (STF)

**Updated: 09/12/2022, v0.19** 

**Step 1:** Install the necessary libraries from the requirements.txt file:

*pip3 install -r requirements.txt*

**Step 2:** To obtain new reports from Twitter, you will need a Twitter API access key. For full functionality, the Academic Track of the API is recommended, which can be obtained from here https://developer.twitter.com/en/products/twitter-api/academic-research

Note: STF also runs on regular Twitter API access from v0.19 onwards

**Step 3:** After getting the API access key, configure your key with Twarc (The python library we use to collect the reports) by entering the following command in your console:

*twarc2 configure*

..and enter your Bearer Token in the resulting prompt.

**Step 4:** STF uses a CNN based classifier to identify if the reported URL is phishing or benign by analyzing the website screenshot. For this feature, you need to install and setup chromedriver on your system/environment. 

https://skolo.online/documents/webscrapping/

**Step 5:** You can now launch Social ThreatFinder by running:

python3 run_stf.py

**Step 6:** You can view the output under the generated db.csv file under 'database' folder.

## Social ThreatFinder website (An early look)

This repository includes all the core functionality which powers the Social ThreatFinder website, which is currently under development. 
The website contains three main features:

- **The blocklist:** A simple interface which shows all phishing reports that have been collected and analyzed by the STF instance on our server. This blocklist is currently updated every 5 mins.  

![Alt text](/img/stf_database.png?raw=true "Blocklist interface")
	
- **Interactive map:** An layout which points the location of the active and inactive phishing threats found by STF. 

![Alt text](/img/stf_map.gif?raw=true "Interactive Map")

- **STF API:** A REST API which can be used to obtain URLs from the STF instance running on our servers. The easiest way to access STF data without maintaining your own instance. 
<p align="center">
<img src="/img/stf_api_demo.png" width="500" height="280"/>
</p>

If you liked our word, please consider citing us:

```
@inproceedings{roy2021evaluating,
  title={Evaluating the effectiveness of Phishing Reports on Twitter},
  author={Roy, Sayak Saha and Karanjit, Unique and Nilizadeh, Shirin},
  booktitle={2021 APWG Symposium on Electronic Crime Research (eCrime)},
  pages={1--13},
  year={2021},
  organization={IEEE}
}
