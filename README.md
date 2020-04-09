<h5>This project has been created to download the district level data for COVID19 cases in India and then create a json data set as follows:</h5>

```
{
  "STATE1" : {
                "latitude" : xx
                "longitude" : xx
                "total_count" : xx
                "districts" : {
                                "DISTRICT1" : {
                                                "count": xx,
                                                "latitude" : xx,
                                                "longitude" : xx,
                                              },
                                "DISTRICT2" " {
                                                "count": xx
                                                "latitude" : xx,
                                                "longitude" : xx,
                                              }
                            }
              },
  "STATE2" : {
                "latitude" : xx
                "longitude" : xx
                "total_count" : xx
                "districts" : {
                                "DISTRICT1" : {
                                                "count": xx,
                                                "latitude" : xx,
                                                "longitude" : xx,
                                              },
                                "DISTRICT2" " {
                                                "count": xx
                                                "latitude" : xx,
                                                "longitude" : xx,
                                              }
                            }
              },
}
```

<h5>To work on this project you will need to install python3 and it's corresponding virtual environment package.</h5
<p>Step 1: Setup and activate virtual environment</p>

```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

<p>Step 2: run main.py </p>

```
python main.py
```
             
                                
Location of Datasets:
```
https://s3.console.aws.amazon.com/s3/buckets/covid19-india-datasets/
```