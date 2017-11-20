# Jeb Detector

## Setup
You must use Python3.

Note: several parts of the analysis use multiprocessing to speed up the runtime. All of the listed commands *up to but not including* Simple Bayesian analysis commands work quickly on Carleton's mirage server, which has 72 cpus available. If fewer cpus are available, it can take significantly more time.

The actual corpus needs to be downloaded on local machines due to GitHub's repository size constraints. Download full corpus of emails from [here](https://americanbridgepac.org/jeb-bushs-gubernatorial-email-archive/). Create a folder in the main directory named JebBushEmails and extract the contents of the download into there.

Create an 'output' directory.

Run `python3 EmailScraper.py` to prepare emails. The emails will be saved to numbered .json files in /output/

### N-gram analysis

`python3 TextAnalyzer.py`

To analyze the upspeak and downspeak MLE of a specific phrase:

`python3 TextAnalyzer.py "<phrase>"`

If runtime is a concern, set `makeFromScratch = False` in the first line of TextAnalyzer's main function if it has already been run at least once. (If you are running on mirage, re-running is trivial)

### Simple Bayesian analysis

*Note: this cannot run on mirage.mathcs.carleton.edu without installing simplebayes. We could not install the package due to ownership restrictions, so we ran it on a local Linux machine instead.*

`sudo pip install simplebayes`

`python3 BayesianMethod.py`


### Libraries and packages

- Python Standard Library

- NLTK

- SimpleBayesian
