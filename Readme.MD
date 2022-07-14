I wrote a simple python script which I run every day to keep track of the views across all of my Questions and Answes on the StackExchange Network.

![Example image](example.png)


It uses the StackAPI which you can install with: `pip3 install StackAPI`


To run it you just need to copy paste you userpage url from each website. For example, to get all of my questions and answes on Arquade stackexchange, I would type:

````
./se.views.py https://gaming.stackexchange.com/users/234411/surprisedog
````

or alternatively you can just specify `site_name.user_id`

````
./se.views.py gaming.234411

````

You can also run it on multiple sites at once like this:

````
./se.views.py askubuntu.951756 superuser.1023751 worldbuilding.63172

````

Set it up as cron script to run everyday or if you are running this from a laptop you can use [LazyCron](https://github.com/SurpriseDog/LazyCron) to make sure it runs everyday even if the laptop isn't always on at the same time of day.

----

## Graphing

After you have built up several weeks of data on StackExchange views, you can graph it by running:

./se.plot.py se.views.out question_url


For example to get the number of views on my popular Lifehacks question I would run:

```
./se.plot.py se.views.out https://lifehacks.stackexchange.com/questions/22791/how-can-i
```

Weekly view data is printed to the terminal if you want to make your own fun graphs in LibreOffice Calc
