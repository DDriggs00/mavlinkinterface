# Missions

In order to use advanced GPS-Related functionality, it is necessary to create and use missions.

Missions work differently from normal commands in that they must be created, planned, and uploaded. Only then can they be executed.

## Mission Creation

```py
# Assuming you have initiated a mavlinkInterface class "mli"
myMission = mavlinkinterface.mission(mli)
```

## Mission Planning

```py
# Add some waypoints to the mission
myMission.goToCoordinates(33.810561, -118.394265)
myMission.goToCoordinates(33.811006, -118.394265)
myMission.goToCoordinates(33.811006, -118.394749)
myMission.goToCoordinates(33.810561, -118.394749)
myMission.goToCoordinates(33.810561, -118.394265)
```
