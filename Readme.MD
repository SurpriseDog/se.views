I wrote a simple python script which I run every day to keep track of the views on Stack Exchange questions:

![Example image](example.png)


It uses the StackAPI which you can install with: `pip3 install StackAPI`

To run it on a single question just copy paste the url:


````
./se.views.py https://meta.stackexchange.com/questions/92554/is-there-a-possibility

````

Or can use it to watch ALL of you Questions and Answes across the StackExchange Network:

Copy paste your userpage url from each website. For example, to get all of my questions and answes on Arquade stack exchange, I would type:

````
./se.views.py https://gaming.stackexchange.com/users/234411/surprisedog
````

Or more compactly you can just specify `site_name.user_id`

Note that some sites like `Arquade` have different url names than display names.

````
./se.views.py gaming.234411

````

You can also mix and match to run multiple sites and questions at once like this:

````
./se.views.py askubuntu.951756 superuser.1023751 worldbuilding.63172 https://meta.stackexchange.com/questions/92554/is-there-a-possibility

````


Set it up as cron script to run everyday or if you are running this from a laptop you can use [LazyCron](https://github.com/SurpriseDog/LazyCron) to make sure it runs everyday even if the laptop isn't always on (or connected to the internet) at the same time of day.

----

## Graphing

After you have built up several weeks of data on StackExchange views, you can graph it by running:

./se.plot.py se.views.out question_url


For example to get the number of views on my popular Lifehacks question I would run:

```
./se.plot.py se.views.out https://lifehacks.stackexchange.com/questions/22791/how-can-i
```

Raw view data is printed to the terminal if you want to make your own fun graphs in applications such as LibreOffice Calc


#### FAQ:

**How do weekly views have a fractional number of views? **

If the script didn't run at the same time every day, the numbers are being adjusted. For example if the time between the first to last data point in a week is actually 7.3 days, then the number of views is being divided down by 7.3/7  to normalize the numbers.
