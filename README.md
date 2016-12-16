# ResearchFish

## Running the analysis

The code runs in a virtual environment which can be installed [following this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

The main directory contains:

1. research_fish_analysis.py: the analysis code itself
1. requirements.txt: a list of the libraries used by code
1. What questions do we want to answer with this data?: a list of questions I want to answer with the data

The data directory contains:

1. "softwareandtechnicalproductsearch-1481901871545.csv": A csv file downloaded by Simon Hettrick from Gateway to Research on 16 December 2016. This contains all "Software and Technical Products" research outputs
1. "Software&TechnicalProducts - ResearchFish.xlsx": around 1600 software outputs sent to us on 17 November 2016 by Louise Tillman from the EPSRC.
1. "researchfish_results.xlsx": results from the analysis
1. "impact.txt": all of the outputs' impact statements merged into a single text file for easy loading into a word frewquency counter

The charts directory contains png images of the charts produced by the analysis.
The venv directory is used by the virtual environment.

## About the data

Following a discussion about "software outputs" with Louise Tillman, I was offered all of the software outputs for EPSRC grants.

Louise describes the content as:

"These are self-reported outputs that PIs have submitted. We had a good submission rate overall (I think the 2016 report that is due to be published on our website in the next couple of weeks  says that we had 95% of PIs completed with 100% completion on current grants). However this does not tell you much about the quality of the data (software is not one of the mandatory boxes that must be filled in to comply). It is not the start date but the end date of the grants that controls whether PIs are asked to submit:

* Normally mandatory if current or <5 yrs since grant end date
* Either optional or not possible after that (most EP grants >6 yrs old ‘closed’, but could be re-opened on request).

So I think the earliest start date of the grants in the data set is 2006.The newest grants (i.e. those that have only just been funded / a year or so in) are not asked to submit outcomes immediately as that would not be realistic."
