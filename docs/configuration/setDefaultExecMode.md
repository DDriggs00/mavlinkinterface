# setDefaultExecMode( mode )

Sets the queuing mode to use when the common parameter execMode is not given.  
This will only work if the queue is empty, and no commands are currently executing
The possible modes are as follows:

Synchronous mode:
> Commands will nor return a value or allow the entry of another command until completed or interrupted

Queue mode:
> If a movement command is currently executing and a new move command is initiated, the new move command will be placed in an execution queue.

Override mode:
> If a movement command is currently executing and a new move command is initiated, the currently executing movement command will be halted and discarded, and the new command will be executed.

Ignore mode:
> If a movement command is currently executing and a new move command is initiated, the new move command will be ignored and discarded.

For more information, see [here](../executionModes.md),

## Parameters

Mode (enum):  
> The queuing mode to use by default. Possible values are:  
> `synchronous`  
> `queue`  
> `override`  
> `ignore`

## Return Values

Returns void.  
If given an invalid mode, raises a ValueError.  
If there is an item in the queue or a currently executing command, raises a ResourceWarding

## Example

```py
MLI.setDefaultQueueMode('queue')
```
