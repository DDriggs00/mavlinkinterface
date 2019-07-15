# setSurfacePressure( pressure \<optional> )

Sets the surface pressure (used in depth calculations) to the given value.

## Parameters

pressure (int):
> The pressure in pascals to set as default.  
> If no value is given, uses the current external pressure of the drone  
> Sea Level is 101325

## Return Values

Returns void

## Examples

```py
MLI.setSurfacePressure()    # While on surface
# Sets the surfacePressure value to the current exterior pressure

MLI.setSurfacePressure(101000)
# Sets the surfacePressure value to 101000 pascals
```
