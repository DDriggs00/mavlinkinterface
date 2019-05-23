# armGrab( strength \<optional>, percent \<optional> )
Close the grabber arm by *percent*% or until gripping an object with *strength*% strength

## Parameters
strength (integer, optional):  
> An integer from 1 to 100 representing the percentage of motor strength to use in gripping.  
> Defaults to 100%

percent (integer, optional):  
> An integer from 1 to 100 representing the amount, as a percentage of the whole distance, the arm should close

## Return Values
Returns a string.  
Upon success, returns "Success"  
Upon failure, returns the reason for failure  
Note: If arm is overheating, or would overheat following the next action, no action will be taken and function will return "Overheating, No Action Taken".

## Examples
```py
armGrab()
# The grabber arm closes until either closed or gripping an object with 100% strength

armGrab(strength = 50)
# The grabber arm closes until either closed or gripping an object with 50% strength

armGrab(strength = 100, percent = 50)
# The grabber arm closes by 50% or until closed or gripping an object with full strength
```
