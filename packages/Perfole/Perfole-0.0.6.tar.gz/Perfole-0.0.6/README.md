
Package for measuring software performance. Measuring is done by defining start and end point to measure. 
Start and end point is called action. Action should have meaningful name. Multiple actions can exist.

## Import
```
from Perfole.Perfole import PERFORMANCE_TEST
```

## Set start/end points
```
    PERFORMANCE_TEST.StartAction(name...)
    ...
    PERFORMANCE_TEST.EndAction(name...)
```


## Start/stop measurement
```
    PERFORMANCE_TEST.Start()
    ...
    PERFORMANCE_TEST.Stop()
```


## Expected methods order
```
PERFORMANCE_TEST.Start()  // before action points


PERFORMANCE_TEST.StartAction() // anywhere beetwen start/stop measurement
...
PERFORMANCE_TEST.EndAction() // anywhere beetwen start/stop measurement


PERFORMANCE_TEST.Stop() // after all action points
```

## Results
Stop() method will return list of caught actions. For cloud reporting functionality visit https://perfole.com


## UniqueIdentifier parameter
UniqueIdentifier parameter must be given when start/end points are in different threads:
```
PERFORMANCE_TEST.StartAction(name="myAction", uniqueIdentifier= "myIdentifier")
...
PERFORMANCE_TEST.EndAction(name="myAction", uniqueIdentifier= "myIdentifier")
```









