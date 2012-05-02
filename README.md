Command-Line Wikipedia Querier
=======
Another 20-minute script built purely to make my life easier.

Offered because I find it useful, so you might too.

Usage
-----
./wq.py <search terms>

Description
------
Queries Wikipedia to find the most relevant page to your query, retrieves that page, and prints the first paragraph (the quick info).

Works very well with aliases and DTerm - when set up properly, you can find information on anything by pressing cmd-shift-enter, entering "wq That Thing You Wanted", and hitting enter.

Known Bugs
------
Doesn't always return the right thing: the script relies on Wikipedia's opensearch API, which usually returns the right results, but it will fall back to title searches, which is extremely unlikely to return the best result.

Fixing this would take longer than 20min.

Requirements
------
Uses Requests and BeautifulSoup.