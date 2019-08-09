# waitQueue()

This function blocks until:

1. The queue has completed and the current task has ended
2. a Keyboard Interrupt (Ctrl+C) has been received

## Return Values

Returns void

## Examples

```py
MLI.move(direction=0, time=10, execMode='queue')
MLI.move(direction=180, time=10, execMode='queue')
MLI.waitQueue()
# the waitQueue function will block for 20 seconds, returning once the last function has been completed.
```
