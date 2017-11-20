# Jeb Detector

## Setup

The actual corpus needs to be downloaded on local machines due to GitHub's repository size constraints. Download full corpus of emails from [here](https://americanbridgepac.org/jeb-bushs-gubernatorial-email-archive/). Create a folder in the main directory named JebBushEmails and extract the contents of the download into there.

Run `python3 EmailScraper.py` to prepare emails. The emails will be saved to numbered .json files in /output/

### N-gram analysis

Run `python3 TextAnalyzer.py`

### Simple Bayesian analysis

Run `python3 BayesianMethod.py`

### CNN analysis




Plans
- process emails, output a model
- try to see if it can distinguish between emails coming to Jeb vs emails Jeb sent
