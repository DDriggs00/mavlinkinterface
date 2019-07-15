# Execution Modes

There are multiple ways to define which execution mode to use for a file.

1. Set the default mode, and do not pass it with a function
   - `MLI = mavlinkinterface.mavlinkInterface(execMode="queue")`
   - `MLI.move(angle=0, time=3)`
1. Pass the mode with the function
   - `MLI.move(angle=0, time=3, execMode="queue")`
1. Change the default mode
   - `MLI.setDefaultExecutionMode(execMode="queue")`

## Synchronous

In this mode, each movement command will return only once it is completed. An example is below:

```py
# Assuming default execMode is Synchronous
MLI.move(angle=0, time=3)
MLI.move(angle=90, time=3)
MLI.move(angle=180, time=3)
MLI.move(angle=270, time=3)
print(MLI.getTemperature())   # getTemperature is not a movement command
```

In this example, the first 4 commands will be executed in series, following the completion of the prior command, then the print command will be executed  

Output:
> time=0:  Move Command 1 started
>
> time=3:  Move Command 1 Finished  
> time=3:  Move Command 2 started
>
> time=6:  Move Command 2 Finished  
> time=6:  Move Command 3 started
>
> time=9:  Move Command 3 Finished  
> time=9:  Move Command 4 started
>
> time=12: Move Command 4 Finished  
> time=12: 26 # Temperature in degrees Celsius

## Queuing

In this asynchronous mode, a command returns directly after initiating.  If, upon entering a movement command, there is not currently a movement command executing, this movement command will be immediately executed.  If a movement command is currently executing, this movement command will be added to the command queue.  The command queue will automatically execute the contained commands in the order added.  An example is below.

```py
# Assuming default execMode is queuing
MLI.move(angle=0, time=3)
MLI.move(angle=90, time=3)
MLI.move(angle=180, time=3)
MLI.move(angle=270, time=3)
print(MLI.getTemperature()  # getTemperature is not a movement command
```

In this example, upon running this series of commands, the first command will be called, immediately start executing, and return.  The second command will then be added to the queue, and then cease blocking, as will the third and fourth. Then, while the first move command is still executing, the temperature will be printed out. After the first command ends, the next three will execute in sequence.

Output:
> time=0:  Move Command 1 started  
> time=0:  Move Command 2 Queued  
> time=0:  Move Command 3 Queued  
> time=0:  Move Command 4 Queued  
> time=0:  26 # Temperature in degrees Celsius
>
> time=3:  Move Command 1 Finished  
> time=3:  Move Command 2 started
>
> time=6:  Move Command 2 Finished  
> time=6:  Move Command 3 started
>
> time=9:  Move Command 3 Finished  
> time=9:  Move Command 4 started
>
> time=12: Move Command 4 Finished  

## Ignore

In this asynchronous mode, a command returns directly after initiating.  If, upon entering a movement command, there is not currently a movement command executing, this movement command will be immediately executed.  If a movement command is currently executing, this movement command will be ignored.  An example is below.

```py
# Assuming default execMode is ignore
move(angle=0, time=3)
move(angle=90, time=3)
move(angle=180, time=3)
move(angle=270, time=3)
print( getTemperature() ) # getTemperature is not a movement command
```

In this example, upon running this series of commands, the first command will be called, immediately start executing, and return.  The Second, third, and fourth commands will be ignored, as a movement command is already executing. Then, while the first move command is still executing, the temperature will be printed out.  The only movement to be taken will be the first.

Output:
> time=0:  Move Command 1 started  
> time=0:  Move Command 2 ignored  
> time=0:  Move Command 3 ignored  
> time=0:  Move Command 4 ignored  
> time=0:  26 # Temperature in degrees Celsius
>
> time=3:  Move Command 1 Finished  


## Override

In this asynchronous mode, a command returns directly after initiating.  If, upon entering a movement command, there is not currently a movement command executing, this movement command will be immediately executed.  If a movement command is currently executing, the currently executing movement command will be immediately terminated, and this command will be executed.  An example is below.

```py
# Assuming default execMode is override
MLI.move(angle=0, time=3)
MLI.move(angle=90, time=3)
MLI.move(angle=180, time=3)
MLI.move(angle=270, time=3)
print(MLI.getTemperature()) # getTemperature is not a movement command
```

In this example, upon running this series of commands, the first command will be called, immediately start executing, and return.  The second command will then be called, terminating the first and executing itself. The second and third commands will do likewise. Then, while the last movement command is still executing, the temperature will be printed out.  The only movement command to be completed will be the last one, while the first three would be only partially executed (move only until the next command was able to terminate it).

Output:
> time=0:  Move Command 1 started  
> time=0:  Move Command 1 Killed  
> time=0:  Move Command 2 started  
> time=0:  Move Command 2 Killed  
> time=0:  Move Command 3 started  
> time=0:  Move Command 3 Killed  
> time=0:  Move Command 4 started  
> time=12: 26 # Temperature in degrees Celsius
>
> time=3:  Move Command 4 Finished  

## Interactions between modes

Below are some Examples:

### Example 1: Queue + Synchronous

```py
# Add Items to the queue
MLI.move(angle=0, time=10, execMode="queue")
MLI.move(angle=180, time=10, execMode="queue")
MLI.move(angle=0, time=10, execMode="queue")
for i in range(3):
    print("Print statement " + str(i))
    sleep(1)
MLI.move(angle=180, time=10, execMode="synchronous")
print("Last Line")
```

Output:
> time=0:  Move Command 1 started  
> time=0:  Move Command 2 queued  
> time=0:  Move Command 3 queued
> time=0:  Print statement 1
> time=1:  Print statement 2
> time=2:  Print statement 3
> time=3:  Move command 4 called, waiting to execute
>
> time=10: Move Command 1 Finished  
> time=10: Move Command 2 started
>
> time=20: Move Command 2 Finished  
> time=20: Move Command 3 started
>
> time=30: Move Command 3 Finished  
> time=20: Move Command 4 started
>
> time=30: Move Command 4 Finished  
> time=30: Last Line

In this example, the first move command will executed, and the next 2 put in the queue.  The print loop will be started and will finish. When the 4th move command is called, it will wait until the CPU is free (until the entire queue has finished execution) to execute, blocking the entire time.

### Example 2: Queue + Override

```py
MLI.move(0, 10, execMode="queue")
MLI.move(180, 10, execMode="queue")
MLI.move(90, 10, execMode="override")
```

Output:
> time=0:  Move Command 1 Started  
> time=0:  Move Command 2 Queued  
> 
> time=0:  Move Command 3 Called  
> time=0:  Queue Cleared  
> time=0:  Move Command 1 Killed  
> time=0:  Move Command 3 Started
>  
> time=10:  Move Command 3 Finished  

In this example, the first command immediately executes and the second is added to the queue. The third will (1): Clear the Queue, (2): stop the currently executing command, and (3) execute.
