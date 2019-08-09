# setLoggingLevel( level )

This function modifies the level of logging done by the program.  

## Parameters

level (string):
> The level of logging to perform. Possible levels are:  
> `Verbose`: Records All commands and their results, any status messages by the program, as well as any errors  
> `Standard`: Records results of returning commands only (and any errors)  
> `Error`: Records logs only upon receiving an error  
> `None`: Does not perform any level of logging

## Return Values

Returns void

## Examples

```py
MLI.setLoggingLevel('Verbose')
# Sets the logging mode to Verbose
```
