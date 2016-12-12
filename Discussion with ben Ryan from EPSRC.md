# Discussion with Ben Ryan about changes to first draft

I completed the first draft of the article about the ResearchFish data and sent it to Louise on 8 December 2016. Louise passed it around the office and Ben Ryan (EPSRC Snr. Mgr, Research Outcomes) said that he would like to discuss the details with me.

Ben identified some issues with the data I had been given, and a couple of issues with the methodology. I agreed to adapt and repeat the analysis, edit the post and send it to him for review. His comments were:

1. Some of the 'Type of Tech Product' (TOTP) included in the original data set do not relate to software!

  * The original data contained the TOTPs: Detection Devices, e-Business Platform, Grid Application, New Material/Compound, New/Improved Technique/Technology, Physical Model/Kit, Software, Systems, Materials & Instrumental Engineering, Systems, Materials &amp; Instrumental Engineering, and Webtool/Application

  * The only TOTPs that related to software are: e-Business Platform, Grid Application, Software, and Webtool/Application

1. The question about open source licensing is asked only for the 'Software' TOTP. Consequently, the field 'Open Source?' can only be assessed in relation to 'Software' TOTPs (and not e-Business Platform, Grid Application, or Webtool/Application).

1. We'll open the article with a “Let us know” call to arms. The point of doing this work is the get people talking about recording their software in ResearchFish. We want people to get back to us and the EPSRC about their experiences, why they're recording software and any problems they might have.

1. Change the language from "register an output" to "record an output" to ensure that people don't think that EPSRC are endorsing a particular bit of software.

1. There is a possibility that some of the outputs are duplicates, because Investigators occassionally re-use an output against different grants. There's no easy way to search for these. Probably the most effective way to find them is to look for duplicates in the 'Impact' and 'Product' fields, which are both verbose and hence unlikely to coincidentally match another entry.

1. We need to be careful with the date range. ResearchFish only began to be used by the EPSRC in 2014, data from earlier will have been retrofitted from data that was in earlier systems the EPSRC used to store research outputs. However, Ben believes that the data over the years 2012-2014 is reliable enough to be included in this study. Consequently, we're going to limit the date range to 2012-2016. I'll add a section into the proviso section of the article about why this change has been made.

1. There has only been one data collection so far in 2016, and that took place early in the year. This explains why there are so few outputs recorded in 2016.

1. The research outcomes in general can be found in the ("Research outputs 2016 report")[https://www.epsrc.ac.uk/newsevents/pubs/researchoutputs2016/]. There were around 100k publications registered! I can use this to provide a nice comparator for the software outputs. Many publications are entered automatically, because they can be harvested from publishers if the researcher has included the grant number. These automatic outputs are passed by the researcher for confirmation, which is far easier than having to enter them manually oneself.

1. All the ResearchFish data is available in Gateway to Research (GtR). It would be easier to point people there than re-licence the data I was given. Following a conversation with Neil (Chue Hong), it might be possible to write an interface to the GtR API which automatically downloads all software-related outputs.
