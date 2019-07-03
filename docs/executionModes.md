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
move(angle=0, time=3)
move(angle=90, time=3)
move(angle=180, time=3)
move(angle=270, time=3)
print(getTemperature())   # getTemperature is not a movement command
```

In this example, the first 4 commands will be executed in series, following the completion of the prior command, then the print command will be executed  

Output:
> t=0:  Move Command 1 started
>
> t=3:  Move Command 1 Finished  
> t=3:  Move Command 2 started
>
> t=6:  Move Command 2 Finished  
> t=6:  Move Command 3 started
>
> t=9:  Move Command 3 Finished  
> t=9:  Move Command 4 started
>
> t=12: Move Command 4 Finished  
> t=12: 26 # Temperature in degrees Celsius

## Queuing

In this asynchronous mode, a command returns directly after initiating.  If, upon entering a movement command, there is not currently a movement command executing, this movement command will be immediately executed.  If a movement command is currently executing, this movement command will be added to the command queue.  The command queue will automatically execute the contained commands in the order added.  An example is below.

```py
# Assuming default execMode is queuing
move(angle=0, time=3)
move(angle=90, time=3)
move(angle=180, time=3)
move(angle=270, time=3)
print(getTemperature()  # getTemperature is not a movement command
```

In this example, upon running this series of commands, the first command will be called, immediately start executing, and return.  The second command will then be added to the queue, and then cease blocking, as will the third and fourth. Then, while the first move command is still executing, the temperature will be printed out. After the first command ends, the next three will execute in sequence.

Output:
> t=0:  Move Command 1 started  
> t=0:  Move Command 2 Queued  
> t=0:  Move Command 3 Queued  
> t=0:  Move Command 4 Queued
> t=0:  26 # Temperature in degrees Celsius
>
> t=3:  Move Command 1 Finished  
> t=3:  Move Command 2 started
>
> t=6:  Move Command 2 Finished  
> t=6:  Move Command 3 started
>
> t=9:  Move Command 3 Finished  
> t=9:  Move Command 4 started
>
> t=12: Move Command 4 Finished  

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
> t=0:  Move Command 1 started  
> t=0:  Move Command 2 ignored  
> t=0:  Move Command 3 ignored  
> t=0:  Move Command 4 ignored  
> t=0:  26 # Temperature in degrees Celsius
>
> t=3:  Move Command 1 Finished  


## Override

In this asynchronous mode, a command returns directly after initiating.  If, upon entering a movement command, there is not currently a movement command executing, this movement command will be immediately executed.  If a movement command is currently executing, the currently executing movement command will be immediately terminated, and this command will be executed.  An example is below.

```py
# Assuming default execMode is override
move(angle=0, time=3)
move(angle=90, time=3)
move(angle=180, time=3)
move(angle=270, time=3)
print(getTemperature()) # getTemperature is not a movement command
```

In this example, upon running this series of commands, the first command will be called, immediately start executing, and return.  The second command will then be called, terminating the first and executing itself. The second and third commands will do likewise. Then, while the last movement command is still executing, the temperature will be printed out.  The only movement command to be completed will be the last one, while the first three would be only partially executed (move only until the next command was able to terminate it).

Output:
> t=0:  Move Command 1 started  
> t=0:  Move Command 1 Killed  
> t=0:  Move Command 2 started  
> t=0:  Move Command 2 Killed  
> t=0:  Move Command 3 started  
> t=0:  Move Command 3 Killed  
> t=0:  Move Command 4 started  
> t=12: 26 # Temperature in degrees Celsius
>
> t=3:  Move Command 4 Finished  

## Interactions between modes

Below are some Examples:

### Example 1: Queue + Synchronous

```py
# Add Items to the queue
move(angle=0, time=10, execMode="queue")
move(angle=180, time=10, execMode="queue")
move(angle=0, time=10, execMode="queue")
for i in range(3):
    print("Print statement " + str(i))
    sleep(1)
move(angle=180, time=10, execMode="synchronous")
print("Last Line")
```

Output:
> t=0:  Move Command 1 started  
> t=0:  Move Command 2 queued  
> t=0:  Move Command 3 queued
> t=0:  Print statement 1
> t=1:  Print statement 2
> t=2:  Print statement 3
> t=3:  Move command 4 called, waiting to execute
>
> t=10: Move Command 1 Finished  
> t=10: Move Command 2 started
>
> t=20: Move Command 2 Finished  
> t=20: Move Command 3 started
>
> t=30: Move Command 3 Finished  
> t=20: Move Command 4 started
>
> t=30: Move Command 4 Finished  
> t=30: Last Line

In this example, the first move command will executed, and the next 2 put in the queue.  The print loop will be started and will finish. When the 4th move command is called, it will wait until the CPU is free (until the entire queue has finished execution) to execute, blocking the entire time.

### Example 2: Queue + Override

```py
move(0, 10, execMode="queue")
move(180, 10, execMode="queue")
move(90, 10, execMode="override")
```

Output:
> t=0:  Move Command 1 Started  
> t=0:  Move Command 2 Queued  
> 
> t=0:  Move Command 3 Called  
> t=0:  Queue Cleared  
> t=0:  Move Command 1 Killed  
> t=0:  Move Command 3 Started
>  
> t=10:  Move Command 3 Finished  

In this example, the first command immediately executes and the second is added to the queue. The third will (1): Clear the Queue, (2): stop the currently executing command, and (3) execute.
