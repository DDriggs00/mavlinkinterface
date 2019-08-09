# setLeakAction( action )

This function sets the action to be taken on encountering a leak.

## Parameters

action (string)
> There are several default options as well as a custom option (all listed below)  
> `nothing` - No action, other than warning the user and noting the leak in the log, will be taken
> `surface` - This causes the drone to surface and cease other actions upon detecting a leak  
> ***Not yet Implemented***: `home` - This causes the drone to surface, wait for gps signal, and return to the designated home point, ignoring other non-override commands.  If no gps is present, or drone is unable to get a GPS lock, just surfaces  
> ***Not yet Implemented***: `<Path to python file>` - This will execute the function customLeakAction from the given file. A template to use for that file is below.

## Return Data

Returns void

## Examples

```py
try:
    MLI.setLeakAction( '~/myFile.py')
except:
    print("There was an issue with the file")
    MLI.setLeakAction('surface')
```

`~/myFile.py`

```py
from mavlinkinterface.logger import getLogger
# User imports go here

# Do NOT alter this line \/
def customLeakAction(mli) -> None:
    log = getLogger('leakAction')
    log.trace('Entered custom leak action function')
    # User code starts here

    # Example, delete before inserting your code
    mli.surface()

    try:
        if mli.gpsEnabled:
            c = mli.gps.getCoordinates()
        log.warn('surfaced at ' + c + ' upon detecting leak')
    except ConnectionError:
        log.error('Failed to get GPS')

    # User code ends here
    log.trace('Custom leak action completed')
```
