# brainchain.py
Client library for Brainchain Core Services (+ SalesIntel)

```pip install -e .```

or 


```python setup.py install``` 

both seem to work!
Then you can import the clients needed as follows:

```
[0] from brainchain import Brainchain, SalesIntel, FactCheck
[1] bc = Brainchain()
[2] answer = bc.summon("What is the current temperature in New York City?")
[3] print(answer)
 ==> { 
      'question': 'What is the current temperature in New York City?', 
      'answer': 'The current temperature in New York City is 72 degrees Fahrenheit.'
     }

[4] wrong_statement = bc.fact_check("The current humidity in Rockville MD is 99%")
[5] print(wrong_statement)
 ==> {
  "statement": "The current humidity in Rockville MD is 99%",
  "verdict": "Based on the information provided, the current weather report for Rockville, MD states that it is currently 73°F with partly cloudy skies. The humidity is 69.01% and there is no mention of a 99% humidity level. Therefore, we can conclude that the statement 'The current humidity in Rockville MD is 99%' is not accurate.",
  "score": 0,
  "references": [
    "https://www.wunderground.com/weather/us/md/rockville",
    "https://weather.com/weather/hourbyhour/l/Rockville+MD?canonicalCityId=4078210cb35e3974fcdb3a0b0e63e5d930e3ae3d02c214d0983990396c2a349a",
    "https://www.accuweather.com/en/us/rockville/20850/current-weather/329305",
    "https://www.weatherforyou.com/weather/MD/Rockville.html",
    "https://world-weather.info/forecast/usa/rockville_1/",
    "https://www.localconditions.com/weather-rockville-maryland/20852/",
    "https://www.timeanddate.com/weather/@4367175/ext",
    "https://www.myforecast.com/15-day-forecast.php?cwid=19248&metric=false"
  ]
}
```
