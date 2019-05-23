# armRelease( percent \<optional> )
Open the grabber arm by *percent*%

## Arguments
percent (integer, optional):  
: An integer from 1 to 100 representing the amount, as a percentage of the whole distance, the arm should close

## Return Values
Returns a string.  
Upon success, returns "Success"  
Upon failure, returns the reason for failure  
Note: If arm is overheating, or would overheat following the next action, no action will be taken and function will return "Overheating, No Action Taken".

## Examples
```py
armRelease
# The grabber arm opens completely

armRelease(10)
# The grabber arm opens by 10%
```