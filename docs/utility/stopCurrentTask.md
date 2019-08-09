# stopCurrentTask()

This function kills the currently executing task.

## Return Values

Returns void

## Examples

```py
MLI.move(direction=0, time=1000, execMode='queue')      # task A
MLI.move(direction=180, time=1000, execMode='queue')    # task B
MLI.stopCurrentTask()
# The drone stop executing task a, and continue executing the queue (executing task B)
```
