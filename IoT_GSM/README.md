# IoT_Graphical_Security_Model

Created by Mengmeng Ge

Modified by Moyang Feng to adapt to the CREST#9 project

Further updated by Xuanyu Duan.

This project builds a graphical security model for IoT networks and performs security assessments on impact, risk, probability of attack and CVSS base score. 
Vulnerabilities are based on CVSS V2 metrics from the National Vulnerability Database. 

The entry point of the project is NetGen.py. 
Input vulnerabilities are formated in csv files stored in ./data/
./data/original/ contains csv files of original vulnerabilities
./data/predicted/ contains csv files of predicted vulnerabilities
Sample outputs are stored in ./output/

When evaluating sample IoT networks, you would need to choose the corresponding file names and networks in the main function. 

### Requirements
* At least Python 3.6+
