# setDefaultQueueMode( mode )
Sets the queuing mode to use when the universal parameter queueMode is not given.
The possible modes are as follows:

Queue mode:
> If a movement command is currently executing and a new move command is initiated, the new move command will be placed in a queue, which will be executed immediately following the existing command.

Override mode:
> If a movement command is currently executing and a new move command is initiated, the currently executing movement command will be halted and discarded, and the new command will be executed immediately. The *Override* causes any command to behave as though this mode were active.

Ignore mode:
> If a movement command is currently executing and a new move command is initiated, the new move command will be ignored.

The initial setting is Override

## Parameters
Mode (enum):  
> The queuing mode to use by default. Possible values are:  
> `queue`  
> `override`  
> `ignore`

## Return Values
Returns void

## Examples
```py
setDefaultQueueMode(Mode = queue)
setDefaultQueueMode(Mode = override)
setDefaultQueueMode(Mode = ignore)
```