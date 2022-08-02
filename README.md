# improvement-devops-scratch

## Background

This repo contains two AWS Lambda functions intended to help with QA/QC of data coming
from a UV-Vis spectrophotometer. Data from the spectrometer lands in an SQS and
subsequently triggers the data check Lambda function. If a data issue is
identified, another Lambda is triggered to send a notification to lab staff.

## Operational Observations

Here are some observations that a developer has noticed regarding the system:

* Runtimes for both Lambdas are about 200 ms. 
* The quality check Lambda reports using 108 MB of memory on average.
* The notification Lambda reports using 90 MB on memory of average.
* The quality check Lambda works 99.9 % of the time.
* The notification Lambda fails 10 % of the time. No one is notified after the 
failure, and there's no record of the erroneous data.
* It is difficult to figure out which sample's data might have caused a failure.


## Prompt

Questions to consider:

* What other pieces of information would you want to see? How might that information be acquired?
* What are your thoughts on code quality and tests within the repo? What tools could be used to improve it?
* Are there improvements that you would like to make to the code to improve behavior or performance?
* Are there optimizations within the configuration that could potentially reduce operational costs?
* How could the data loss from the failures be addressed? 
* Are there different tools and/or different ways of putting things together that would be more effective?
* Are there any other improvements that you can think of?
