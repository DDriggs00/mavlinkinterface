# surface( execMode \<optional> )

This call brings the drone to the surface. It returns True upon success and False upon obstruction.  

## Parameters

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

Returns a string.  
Upon success, returns "Success"  
Upon Failure, returns the reason for failure and the new depth

## Example

```py
surface
# The drone ascends to the surface
```
