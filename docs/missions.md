# Missions

In order to use advanced GPS-Related functionality, it is necessary to create and use missions.

Missions work differently from normal commands in that they must be created, planned, and uploaded. Only then can they be executed.

For more information on missions, refer to the links at the bottom of this page.

## Mission Creation

```py
# Assuming you have initiated a mavlinkInterface class "mli"
myMission = mavlinkinterface.mission(mli)
```

## Mission Planning

By adding waypoints here, they will be executed in order once the mission is started.

```py
# Add some waypoints to the mission, this does a small square
myMission.goToCoordinates(33.810561, -118.394265)
myMission.goToCoordinates(33.811006, -118.394265)
myMission.goToCoordinates(33.811006, -118.394749)
myMission.goToCoordinates(33.810561, -118.394749)
myMission.goToCoordinates(33.810561, -118.394265)
```

## Valid Mission Commands

### goToCoordinates(lat, lon)

> This command causes the drone to move to a specific set of coordinates

### setHome(lat \<optional>, lon \<optional>)

> This command sets the drone's home location to a specific set of coordinates.  
> If no coordinates are given, uses the drone's current location

## Uploading Mission

This uploads the mission to the drone. The SITL Simulator appears to retain missions between reboots, so actual drones may do that as well.

```py
myMission.upload()
```

## Running mission

This sends the signal to the drone to run the currently uploaded mission.  Note that it cannot differentiate between uploaded missions, so if another mission is on the drone, that one will be run, sometimes failing.

If the Wait parameter is present, blocks until the mission is completed.

```py
myMission.start(wait=True)
```

To see this in action, run the mission example with SITL.

## Additional Documentation

- [Mavlink mission protocol](https://mavlink.io/en/services/mission.html)
- [Mission Planner documentation](https://mavlink.io/en/services/mission.html)
