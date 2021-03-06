# KYCS
Know Your CodeForces Submissions.

## Introduction
I have created certain [CodeForces](https://codeforces.com/) submission visualization some days back (can be found [here](https://github.com/JeetKaria06/CF_Submissions/tree/master/Submission_Visualization)). And getting a really positive response, I thought of combining all of them at one place and make them easy to use which obviously needs deploying to web and needs nothing more than a good internet. So, I have come up with this small [Dash](https://dash.plotly.com/) python app which allows us to create really nice data analytics app and the main thing is its OpenSource.

## How to Use?
Just follow the instructions written in the top left corner of the [page](https://kycs.herokuapp.com/) when the app gets lauched from the web. 

The instructions look something like this:
<br>
<br>
![Output1](https://github.com/JeetKaria06/KYCS/blob/master/Images/learn.jpg) 
<br>
It's damn easy, don't you feel the same? Now go on and explore ;)
<br>
<br>
![Output2](https://github.com/JeetKaria06/KYCS/blob/master/Images/Enjoy.gif)

## Version 2

Added loading state animation and making it more user-friendly.
<br>
<br>
![Output3](https://github.com/JeetKaria06/KYCS/blob/master/Images/v2.gif)

And also bootstrapped the buttons' icons and making them look more pleasant than before.
<br>
<br>
![Output4](https://github.com/JeetKaria06/KYCS/blob/master/Images/buttons.png)

## Version 3
<h3>Average Submissions with date on the x-axis</h3>

One might want to analyze his/her own average number of submissions made per day in any given range of dates as shown below :
<br>
<br>
![Output4](https://github.com/JeetKaria06/KYCS/blob/master/Images/sd1.png)

A<br>
<br>nd can see the average submissions by hovering the mouse over the graph as shown :

![Output5](https://github.com/JeetKaria06/KYCS/blob/master/Images/sd2.png)

If one wants to see his/her only ```OK``` submissions then keep that checkbox selected and deselect the others will give you your desired graph.

<h3>Submissions Bifurcated based on Problem's Indices </h3>

Number of submissions of particular index with particular verdict and even the rate of submitting the particular verdict submission of some index, all in one. Below is shown how :
<br>
<br>
![Output6](https://github.com/JeetKaria06/KYCS/blob/master/Images/rate.png)

## Version 4 [ MAJOR UPDATE ]

The color combination is the thing which was taken care of in this version. Another thing that I have added is the learn more button and the Modal which is opened as shown
<br>
<br>
![Output6](https://github.com/JeetKaria06/KYCS/blob/master/Images/lmore.png)

This answers 2 major questions, ```What is this app about?``` and ```What makes it different from other apps/tools?```.

<h3> Submissions with Month on the x-axis </h3>

The reason behind getting converted from date to months is 30 times lesser iterations. In dates the code was iterating all 365 days and when converted to months then it will become 12 iterations for a year. And also it allows you to understand a bigger picture as one might skip for a day or two but months are more effective to analyse your situation.

Also there are 3 features added in it which are 
<li> Average Submissions </li>
<li> Cummulative Submissions </li>
<li> Individual Submissions </li>
<br>
<br>

![Output7](https://github.com/JeetKaria06/KYCS/blob/master/Images/selectavg.png)

<h5> Average Submissions </h5>
This averages the number of selected category submissions between the starting month selected and the ending month.
<br>
<br>

![Output8](https://github.com/JeetKaria06/KYCS/blob/master/Images/avgsubs.png)

<h5> Cummulative Submissions </h5>
Selected category submissions are added from starting to ending month i.e. ```x``` OK submissios in month1 then in month2 there will be month2 OK submissions + the submissions of all the previous months.
<br>
<br>

![Output9](https://github.com/JeetKaria06/KYCS/blob/master/Images/cumsubs.png)

<h5> Individual Submissions </h5>
Submissions of selected category are shown separately for all the months between starting month and ending month.
<br>
<br>

![Output10](https://github.com/JeetKaria06/KYCS/blob/master/Images/indisubs.png)

<h3> Bootstrapped Social Media Buttons </h3>

Credits for Social Media Buttons:    [ https://bootsnipp.com/snippets/3kQrB ] <br>
<br>
Credits for GitHub Repo Star Button: [ https://ghbtns.com/#star ]
<br>
<br>

![Output11](https://github.com/JeetKaria06/KYCS/blob/master/Images/bbutton.png)
