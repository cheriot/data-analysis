
# Results
**y = -27.4772x + 75.8890** where y is the respondent's rating of President Obama and x is the categorization of their anger.

The results of the linear regression model indicate that anger in politics is significantly and negatively associated
with ratings of President Obama. Specifically, this model indicates that increased anger in politics is associated with
a 27 point drop in the respondent's rating of the President.

# Background
All data is from the Outlook on Life survey, 2012.

* **W1_B4** Generally speaking, how angry do you feel about the way things are going in the country these days?
  * -1 Refused
  * 1  Extremely angry
  * 2  Very angry
  * 3  Somewhat angry
  * 4  A little angry
  * 5  Not angry at all
* **MOST_ANGRY** Divides **W1_B4** into two groups.
  * The **explanatory variable**.
  * 0 for Not agnry at all, A little angry, and Somewhat angry
  * 1 for Extremely angry and Very angry
* **W1_D1** [Barack Obama] How would you rate
  * The *response variable*.
  * Scale from 0 to 100.
