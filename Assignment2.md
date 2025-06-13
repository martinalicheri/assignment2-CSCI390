# Assignment 2

---
## A2-1 Corruption Risks during Context Switch

### Questions:
1. What is a context switch?
   - it is when the computer is running a program and then saves it to run another one.
2. What could go wrong if a context switch is not implemented correctly? Give a specific example.
   - Many things. For example, if they share the same stack, one process could overwrite another<br>
   and then when the computer returns to the first program, it is not as when it left it, and that can<br>
   cause many problems (like the classic one with the race condition and the bank accounts: this<br>
   could make someone withdraw money even if they don't have any left)
3. Why is stack corruption a serious issue? How can it manifest during a context switch?
   - it is really dangerous because two programs edit the same content. Perhaps one program has<br>
   nothing to do with the other, and totally messes up its content, so that when the program returns<br>
   to the first program that was run, the content was completely changed.
   - We can check if there is a risk by making it print a same message if they access a certain stack.
   - We could also debug the program by making sure that there are no variables leaking between<br>
   processes and that the register states and pointers are saved properly. We can also use `gdb`.

- Question: What’s wrong with this output? What do you think went wrong during the context switch?<br>
Explain clearly, referencing memory isolation and register/state separation.
  - The stacks should have been isolated and independent of each other, but instead they were<br>
  not, for both processes show that  they are accessing the same stack. When the context switch<br>
  happened, either the stack pointer was not changed, or the stack pointer of the second process<br>
  was mistakenly pointing to the same stack as Process A.


- What did you find most surprising or counterintuitive about how operating systems manage context<br>
switches? Did this change how you think about multitasking?
  - What surprised me, for some reason, is the fact that each process has its own stack. I would<br>
  have imagined that these things would be stored in the heap, so that they remain after the<br>
  functions end. However, the CPU uses stacks and pointers that hold addresses to return to it.<br>
  And it makes sense because there is one stack for each program, and you don't want all the<br>
  data of each program to be saved, or to make one have to worry about freeing it and all. I think<br>
  that would make memory leaks and all those sorts of problems much more likely.


---
## A2-2 Processes, Threads, and Join

### 1. Explain
*In your own words, what does the join() method do when working with threads or processes? <br>
List one advantage and one disadvantage of using threads compared to using processes.*

The `join()` method makes the parent thread wait until the child thread is done executing.<br>
One advantage: no race condition, no risks of program ending before other programs finish<br>
One disadvantage: if unnecessary, it just slows down the program

### 2. Code
*Write a small Python script that creates one thread to print a message after 3 seconds, while<br>
the main thread prints a countdown:*

```
# Expected behavior:
# Main thread counts down 3, 2, 1...
# Then the thread prints "Thread done!"

# Complete this code:
import threading
import time

def delayed_message():
    time.sleep(3)
    print("Thread done!")

# Your code below:
# 1. Create the thread
message_thread = threading.Thread(target=delayed_message)

# 2. Start the thread
message_thread.start()

# 3. Print a countdown in the main thread
i = 3
while i > 0:
   print(f"Countdown: {i}", end="\r")
   time.sleep(1)
   i -= 1

# 4. Join the thread
message_thread.join()
```


### 3. Reflect
*Write 3–5 sentences responding to the following:*

*How would the behavior change if you removed join()? In what kind of program might you use<br>
a thread to handle a long-running task? How are processes and threads different?*

In the python program I just wrote, I have tried many times and have seen nothing happen if I remove<br>
`join()`; however, in other programs it might happen that the main thread does not wait for other<br>
threads by default and so ends before the created threads finish.

If the tasks that need to be done need access to the same memory, then threads are the way to go.<br>
However, it is preferable that for big tasks one use processes, because these are safer since they<br>
don't affect each other (do not share memory).

Processes run independently, just like tabs on Google. Threads, however, is the way that the user<br>
can multitask within a process. This image helps: a process is a house, and threads are the people<br>
living in it. Each house has its address and its memory, but all the people in the house have access<br>
to that memory.


---
## A2-3: Goroutines and Concurrency

### 1. Explain
- *In your own words, what does a `sync.WaitGroup` do in a Go program? Why is it important when using<br>
goroutines?*
- *What would happen if you called `wg.Done()` more times than `wg.Add(n)`? What if you forgot<br>
to call it at all?*

The WaitGroup makes sure that all the go routines have finished before finishing the whole program. It<br>
keeps track of how many go routines the main program is waiting for to finish.

If `wg.Done()` is called more times than `wg.Add(n)`, then we get an error because the WaitGroup counter<br>
is negative. If I forget to call `wg.Done()`, the program will never end because the WaitGroup will never<br>
get to zero. The error that pops up says that all goroutines are asleep (meaning, they stopped and never<br>
finished their work)


### 2. Code
*Write a Go program that simulates a “startup boot sequence.” Your program should:*
- *Define three functions: loadConfig(), connectToDatabase(), and startServer(). Each should print<br>
three log-style lines with a 400ms pause between each line (use time.Sleep).*
- *Launch all three functions as goroutines using a single sync.WaitGroup, and ensure the main<br>
function waits for all of them to finish.*
- *After all steps have completed, print: "✅ System Ready".* 
- **Challenge: Add a slight twist—randomize the order in which the startup functions complete<br>
(use time.Sleep(time.Duration(rand.Intn(300)) * time.Millisecond) before starting<br>
each function’s loop).**

```go
package main

import(
   "fmt"
   "time"
   "sync"
   "math/rand"
)

func loadConfig(wg *sync.WaitGroup) {
   defer wg.Done()
   time.Sleep(time.Duration(rand.Intn(300)) * time.Millisecond)
   for i:=0; i<3; i++ {
	  fmt.Println("loading configuration")
      time.Sleep(400 * time.Millisecond)
   }
}

func connectToDatabases(wg *sync.WaitGroup) {
   defer wg.Done()
   time.Sleep(time.Duration(rand.Intn(300)) * time.Millisecond)
   for i:=0;i<3;i++ {
      fmt.Println("connecting to databases")
	  time.Sleep(400 * time.Millisecond)
   }
}

func startServer(wg *sync.WaitGroup) {
   defer wg.Done()
   time.Sleep(time.Duration(rand.Intn(300)) * time.Millisecond)
   for i:=0;i<3;i++ {
      fmt.Println("starting server")
	  time.Sleep(400 * time.Millisecond)
   }
}

func main() {
   var wg sync.WaitGroup
   wg.Add(3)

   go loadConfig(&wg)
   go connectToDatabases(&wg)
   go startServer(&wg)

   wg.Wait()
   fmt.Println("✅ System Ready")
```


### 3. Reflect
- *What would go wrong if you forgot to increment the WaitGroup counter before launching<br>
the goroutines?* 

If I forget to add the goroutines in the WaitGroup, the main program will finish before the other<br>
programs even get to start, and so they will not run.

- *How does adding randomized startup delay affect the output order of your program? Does it<br>
impact correctness?*

Since some goroutines might be waiting more than others, it might happen that even though one<br>
was called first, another might execute before it. Because of this, the order of the functions might<br>
be incorrect.

- *If you wanted one of the steps (e.g., `startServer()`) to wait until `loadConfig()` finishes, how<br>
would you restructure your program?*

I would take out the `defer wg.Done()` in the `startServer()` function, and then I would diminish the<br>
argument of the `wg.Add()` function to 2, and then I would comment out the "go" when I call the<br>
`startServer()` function in `main()`. In this way, `startServer()` will always show up last.


---
## A2-3 Monitoring Threads with pidstat

### 1. Explain
- *What is the difference between a thread and a process?<br>
In your answer, explain how threads share resources compared to processes.*

Process: instance of a program in execution (ex: running Chrome and Spotify - 2 processes)
- separate memory, slower, less possibility of corruption (one doesn't affect the other)
- use for safety and for heavier code
Thead: smallest unit of execution within a process
- shared memory, faster, more possibility of corruption (one down, affects others)
- use for performance and for lighter code

- *Why might a programmer choose to use multiple threads in a program?*

To multitask. Otherwise, the program will have to wait for one thing to finish executing<br>
before starting another.

### 2. Code
*You will complete a multithreaded Python program that creates several CPU-intensive threads.*<br>
*The function and structure are provided below. Your job is to write the logic that spawns 4 threads,*<br>
*each running `cpu_intensive_task()`. Make sure each thread is started and marked as a daemon.*

#### Note: You may need to do a little research on pidstat and on starting threads in python.

```
import threading
import time

def cpu_intensive_task():
    while True:
        pass  # Burn CPU

threads = []

for _ in range(4):
    t = threading.Threads(target=cpu_intensive_task)
    t.setDaemon(True)
    threads.append(t)
    t.start()

print("Threads started. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
```
*Once your program is running, use `ps aux | grep python` to get the PID.*<br>
*Then monitor the threads using:*

`pidstat -t -p <PID> 1`

*Submit your finished code!*


### 3. Reflect
- *How did each thread's CPU usage appear in the pidstat output?*

Each thread's usage was roughly 20%-25%. It makes sense that it is split evenly.<br>
However, sometimes one thread's usage was 9% while another's 38%.

- *If you added a time.sleep(1) inside one of the threads, how would that change its CPU usage?*

Yes. The CPU usage of that thread would diminish, as there would be a context switch. The thread<br>
being inactive for a bit, the system would jump to another one. Thus, the thread that sleeps would<br>
have a lower CPU usage than the others.

- *Why might thread-level monitoring be more helpful than process-level monitoring in*<br>
*diagnosing performance issues?*

Because threads are used for performance within a certain process. Threads are for managing<br>
lighter code and multitasking within the process. So if there is a problem with the performance<br>
within a process, a thread-level monitoring is more helpful.


---
## A2-4 Scheduling Simulator (FCFS vs. Round Robin)

### 1. Explain
- *Briefly describe the main difference between how First-Come, First-Served (FCFS)<br>
and Round Robin (RR) select the next process to run.*

FCFS is when the first process is run and the scheduler waits for that one to finish to execute the next.<br>
RR is when each process is run for a specific amount of time. If the process finished, it is popped<br>
from the queue; else, it is pushed to the back. Doing this, it'll act as a queue in circles until all<br>
processes finish.

- Why does Round Robin require a time quantum while FCFS does not?
Round Robin lets the processes run for a specific amount of time, allowing responsiveness and multitasking.<br>
FCFS simply waits for the process to finish to execute the next.

### 2. Code (Input Design)
Use the online simulator at [this link](https://scheduling-algorithm-simulator.vercel.app/).<br>
Create the following process set:
- P1 – Arrival: 0, Burst: 7
- P2 – Arrival: 2, Burst: 4
- P3 – Arrival: 4, Burst: 1

Run the simulation twice:
- Once using FCFS
- Once using Round Robin with a quantum of 2

For each run, record the following from the simulator:
- Gantt chart (you may copy the emoji-style output or take a screenshot)
- Turnaround time and ⏳ waiting time for each process
- Average turnaround and waiting times

[FCFS](../FCFS.png)
[Round Robin](../RR.png)

### 3. Reflect
- Which algorithm performed better in terms of average waiting time for this process set? Why?

The RR has the lesser Avg. Wait. Time. It makes sense, for the FCFS had to wait 7 units <br>
for the first process to finish, while the others would not because of the time quantum.<br>
Instead of some processes waiting a lot and some none, in RR they all wait a little bit.

- Did Round Robin’s time slicing benefit shorter processes like P3? How do you know?

Yes, because it was completed earlier in comparison to FCFS. It didn't have to wait for the<br>
longer process to finish running first.

- If P1’s burst time were increased to 12, how might that change the outcome under Round Robin?<br>
Try it and explain.

Prediction: it would just spend more time at the end to complete itself, but P2 and P3 would have<br>
already finished by then.<br>
Reality: just like predicted. Since each process only has time slots of 2 units, and they are run<br>
equally, then the longer processes will be the last to finish.


## A2-5 Simulating Round Robin Scheduling

### 1. Explain
- *How does Round Robin scheduling improve fairness compared to First-Come-First-Served?*

Because all processes get a chance to run. Whereas in FCFS, they have to wait till the first<br>
process that arrived finishes, which might be a really long process while the one that is<br>
waiting is very short.

- *What potential trade-offs are introduced when choosing a small vs. large time quantum?*

If small time quantum, then there are too many context-switches (slow!). If too large, then<br>
there is poor responsiveness, because the CPU takes too long on each task.

### 2. Code
*Write a short program (in Python or the language of your choice) that simulates Round Robin<br>
scheduling for the following workload:*

Processes = [ <br>
{"pid": "P1", "arrival_time": 0, "burst_time": 5}, <br>
{"pid": "P2", "arrival_time": 1, "burst_time": 3}, <br>
{"pid": "P3", "arrival_time": 2, "burst_time": 1} <br>
] <br>
time_quantum = 2 <br>

*Your program should output:*
- *Execution sequence with time slices, e.g., P1(2) → P2(2) → P1(2) → P3(1) → P1(1)*
- *Average waiting time and average turnaround time*

```python
class P:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.time_left = burst_time
        self.waiting_time = 0
        self.completion_time = 0
        self.turnaround_time = 0

    def __repr__(self):
        return self.name

p1 = P("p1", 0, 5)
p2 = P("p2", 1, 3)
p3 = P("p3", 2, 1)

def round_robin(p1,p2,p3, time_quantum):
    time = 0
    p_i = p1
    print("Execution Sequence: ", end="")
    while (p1.time_left >= 0) or (p2.time_left >= 0) or (p3.time_left >= 0):
        if p_i.time_left >= time_quantum:
            p_i.time_left -= time_quantum
            print(f"{p_i}({time_quantum}) -> ", end="")
            time += time_quantum
        elif (p_i.time_left < time_quantum) and (p_i.time_left > 0):
            print(f"{p_i}({p_i.time_left}) -> ", end="")
            time += p_i.time_left
            p_i.time_left = 0
        if p_i.time_left == 0:
            p_i.time_left = -1
            p_i.completion_time = time
            p_i.turnaround_time = p_i.completion_time - p_i.arrival_time
            p_i.waiting_time += p_i.turnaround_time - p_i.burst_time

        if p_i == p1: p_i = p2
        elif p_i == p2: p_i = p3
        elif p_i == p3: p_i = p1
        
    print("done!")

    print("-------")

    print("Average waiting time: %.2f" % ((p1.waiting_time + p2.waiting_time + p3.waiting_time) / 3))
    print("Average turnaround time: %.2f" % ((p1.turnaround_time + p2.turnaround_time + p3.turnaround_time) / 3))

round_robin(p1,p2,p3, 2)
```

### 3. Reflect
- *How did time slicing affect the response time of shorter processes?*

It minimizes it, because they get to start earlier, since they do not have to wait<br>
until the other processes (which might be long) finish running.

- *How would this execution pattern differ if the time quantum were increased to 4?*

```bash
Execution Sequence: p1(4) -> p2(3) -> p3(1) -> p1(1) -> done!
```

- *Which process waited the most, and why?*

If the quantum is 4, the process that most waited was p3. Since the quantum was too large,<br>
the longer processes that preceded it ran first, making it wait until it could run.


# What to Submit

**A link to a public GitHub repository containing your complete source code. Be sure the repo is viewable.**<br>
