# stopAllTasks()

This function clears the queue and kills the currently executing task.

## Return Values

Returns void

## Examples

```py
MLI.move(direction=0, time=1000, execMode='queue')
MLI.move(direction=180, time=1000, execMode='queue')
MLI.stopAllTasks()
# The drone will stop moving
```
