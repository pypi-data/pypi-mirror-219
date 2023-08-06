.. Buckaroo documentation master file, created by
   sphinx-quickstart on Wed Apr 19 14:07:15 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Comparison of jupyter table widgets
===================================


* **Criteria**

** **Styling**

Silicon Valley or Wall St Trader.

A bit tongue in cheek, but you will notice two seaprate styles.  Tables that come out of finance are tightly packed with data, mono space fonts and no rounded corners.

Tables that come out of venture backed firms tend to look good on landing pages with drop shadows, rounded corners, and nicely kerned fonts that don't properly line up.

If you haven't noticed I prefer the trader styling.  You might prefer the VC styling if you are making glossy reports and dashboards for executives.

** **Is it a framework for building apps on top of**

There are some widgets that want to be just that.  They have an opinionated design and are customizeable, but gneearlly are not expected to be packaged into an app.

Others are intended to have an app built around them.  They are much more configurable, but they aren't as useful out of box

** **Core JS Library**


** **Cells in 1 second**
What's the largest table size that could be thrown at the table and displayed in 1 second

** **Cells in 5 seconds**
...

** **Supports Streaming**

Does this work for live data in a sane way.  Note for every table here you can rerender 1000 cells in less than 100ms (verify).  By streaming I mean accumulating slices on top of 50k + cells where you aren't just rerendering the whole table each time

** **Pagination**

Is there a sane bexperience for only having a subset of cells resident in the browser with additional calls to the backend to receive different sections of the full dataframe.

** **Builtin summary stats**

** **Pluggable summary stats**

** **Requires JS for customization**

** **Commerical support available**
Always the case if the price is right.  More the case of is it currently offered by a known consulting company.

** **Data Frames supported**

Pandas? Numpy? pd.Series? Polars? Dask? SparkDF? Modin?

** **Builtin charting**

** **Auto sizing**



Here is my draft.
https://buckaroo-data--30.org.readthedocs.build/en/30/articles/dont-use-df-head-buckaroo-instead.html

I think I have one more revision for wording.

The big thing I'm working on is an animated gif that shows opening buckaroo, and toggling through the different views.

Do you think I should just make a gif showing buckaroo, show df.head() side-by-side, or something else.

Not sure how to make a side-by-side gif.  I'm trying not to let perfect be the enemy of good.  Decided to publish on the Read-the-docs site for that reason.

What I wrote is more salesy about Buckaroo than something I'd expect you to publish under your name. We could do it as a guest-post, you write a synopsis and link, or you re-write in your own voice and I also publish the roadmap bits.

What makes sense to you?






