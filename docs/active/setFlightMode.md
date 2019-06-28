# setFlightMode( flightMode, execMode \<optional> )

Sets the drone's flight mode to the given value.

## Flight Modes

MANUAL
> Manual mode passes the pilot inputs directly to the motors, with no stabilization. ArduSub always boots in Manual mode.

STABILIZE
> Stabilize mode is like Manual mode, with heading and attitude stabilization.

ALT_HOLD
> Depth Hold is like Stabilize mode with the addition of depth stabilization when the pilot throttle input is zero. A depth sensor is required to use depth hold mode.

### Position Enabled Modes

> These modes require an under water positioning system. A GPS antenna will not work under water.

POS_HOLD
> Position Hold mode will stabilize the vehicle's absolute position, attitude, and heading when the pilot control inputs are neutral. The vehicle can be maneuvered and repositioned by the pilot.

AUTO
> Auto mode executes the mission stored on the autopilot autonomously. Pilot control inputs are ignored in most cases. The vehicle may be disarmed, or the mode can be changed to abort the mission.

CIRCLE
> Circle mode navigates in circles with the front of the vehicle facing the center point.

GUIDED
> Guided mode allows the vehicle's target position to be set dynamically by a ground control station or companion computer. This allows 'Click to Navigate Here' interactions with a map.

### Secret Menu

ACRO
> Acro (Acrobatic) mode performs angular rate stabilization.

## Parameters

mode (string):  
> The mode to use

execMode (string, optional):
> The execution mode to use for this command. Possible execution modes are:
>
> 1. Synchronous
> 1. Queue
> 1. Ignore
> 1. Override
>
> If not given, defaults to the execution mode given on class initiation.  
> For details on how these modes work, see [Here](../executionModes.md)

## Return Values

Returns void

## Example

```py
setFlightMode(ALT_HOLD)
# sets the drone to depth hold mode
```
