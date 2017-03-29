# ResearchFish investigation

# Purpose

This code analyses research outcomes provided by the EPSRC (but also available on Gateway to Research) to investigate some aspects of the outcomes: the number, the universities who register them, where the software is stored, whether it's stored under an open licence, and whether the URL linked to the storage is live.

The results of the investigation will be published on the Software Sustainability Institute's website under the title: "[Researchfish®: what can it tell us about software in research?](https://www.software.ac.uk/blog/2017-01-18-researchfishr-what-can-it-tell-us-about-software-research)".

# Files

The main directory contains:

1. research_fish_analysis.py: the analysis code itself
1. requirements.txt: a list of the libraries used by code
1. What questions do we want to answer with this data?: a list of questions I want to answer with the data

The data directory contains:

1. softwareandtechnicalproductsearch-1490799160221.csv: a csv file downloaded on 29 March 2017 from [Gateway to Research from the outcomes page](http://gtr.rcuk.ac.uk/search/outcomes?term=*&page=1&fetchSize=25&fields=pro.gr,pro.t,pro.a,pro.orcidId,per.fn,per.on,per.sn,per.fnsn,per.orcidId,per.org.n,per.pro.t,per.pro.abs,pub.t,pub.a,pub.orcidId,org.n,org.orcidId,acp.t,acp.d,acp.i,acp.oid,kf.d,kf.oid,is.t,is.d,is.oid,col.i,col.d,col.c,col.dept,col.org,col.pc,col.pic,col.oid,ip.t,ip.d,ip.i,ip.oid,pol.i,pol.gt,pol.in,pol.oid,prod.t,prod.d,prod.i,prod.oid,rtp.t,rtp.d,rtp.i,rtp.oid,rdm.t,rdm.d,rdm.i,rdm.oid,stp.t,stp.d,stp.i,stp.oid,so.t,so.d,so.cn,so.i,so.oid,ff.t,ff.d,ff.c,ff.org,ff.dept,ff.oid,dis.t,dis.d,dis.i,dis.oid&type=softwareandtechnicalproduct&selectedFacets=#). This includes all outcomes registered on the site within the "software" categories: E-business platform, Grid application, Software and Webtool/application.
1. "researchfish_results.xlsx": results from the analysis
1. "impact.txt": all of the outputs' impact statements merged into a single text file for easy loading into a word frequency counter

Where is the data?

I was asked not to release the data that I used in this study. There are two options if you would like to reproduce the analysis. The first is to go to Gateway to Research and download the appropriate research outcomes for yourself, the second is to wait for my second post on this subject which will include the data relating to research outcomes from all Research Councils.

The charts directory contains png images of the charts produced by the analysis.
The venv directory is used by the virtual environment.

## Requirements

The code runs on Python 3.5.

The code runs in a virtual environment which can be installed [following this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Inside the virtual environment, install the libraries by running the command:

    pip install -r requirements.txt

Once they're installed, run the code with the command:

    python research_fish_analysis.py

## About the data

Following a discussion about "software outputs" with Louise Tillman, I was offered all of the software outputs for EPSRC grants.

Louise describes the content as:

"These are self-reported outputs that PIs have submitted. We had a good submission rate overall (I think the 2016 report that is due to be published on our website in the next couple of weeks  says that we had 95% of PIs completed with 100% completion on current grants). However this does not tell you much about the quality of the data (software is not one of the mandatory boxes that must be filled in to comply). It is not the start date but the end date of the grants that controls whether PIs are asked to submit:

* Normally mandatory if current or <5 yrs since grant end date
* Either optional or not possible after that (most EP grants >6 yrs old ‘closed’, but could be re-opened on request).

So I think the earliest start date of the grants in the data set is 2006.The newest grants (i.e. those that have only just been funded / a year or so in) are not asked to submit outcomes immediately as that would not be realistic."

## Troubleshooting

Sometimes the URL checker hangs on a URL. Hit ctrl+ c to skip the URL.
