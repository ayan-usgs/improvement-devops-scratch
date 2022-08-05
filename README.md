# improvement-devops-scratch

This exercise will present you with application code and an ongoing operational issue.
You will be provided with a brief background regarding the purpose of the application,
some details regarding the operational issues, and then questions for you to consider.
You need not answer all the questions nor be constrained by them--the goal of this
exercise for you to get a sense of the domain and for us to understand how you think 
and problem-solve.

## Background

This repo contains two AWS Lambda functions intended to help with QA/QC of data coming
from a UV-Vis spectrophotometer. Data from the spectrophotometer lands in an SQS queue and
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


## Prompts

Please submit you exercise responses to eread@usgs.gov either in the body of an email or in an attachment. Each 
question maybe addressed with a few sentences or a short paragraph.

Questions to consider:

1. What is the purpose of the serverless.yml file?
2. What is the purpose of the pyproject.toml file?
3. What other pieces of information would you want to see to help investigate the operational issues? 
How might that information be acquired?
4. What are your thoughts on code quality and tests within the repo? 
What tools and techniques could be used to improve it?
5. Are there improvements that you would make to the application code to address the operational issues?
6. Are there improvements that you would make to the infrastructure-as-code to address the operational issues?
7. Are there optimizations within the infrastructure-as-code that could potentially reduce operational costs?
8. Are there different tools and/or different ways of putting things together that would be more effective?
9. Are there any other improvements that you can think of?
