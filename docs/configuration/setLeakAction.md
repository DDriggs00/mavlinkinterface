# setLeakAction( action )

This function sets the action to be taken on encountering a leak.

## Parameters

action (string)
> There are several default options as well as a custom option (all listed below)  
> `surface` - This causes the drone to surface and cease other actions upon detecting a leak  
> `home` - This causes the drone to surface, wait for gps signal, and return to the designated home point, ignoring other non-override commands  
> `<Path to python file>` - This will execute the function customLeakAction from the given file. A template to use for that file is below.

## Return Data

Returns void

## Examples

```py
try:
    MLI.setLeakAction( '~/myFile.py')
except:
    print("There was a crash when executing code in myFile.py that was not caught by the internal try/except block")
```

`~/myFile.py`

```py
# Not yet Implemented
```
