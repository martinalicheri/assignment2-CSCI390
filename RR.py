class P:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.time_left = burst_time
        self.waiting_time = 0
        self.completion_time = 0
        self.turnaround_time = 0

    def __str__(self):
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

    print("P1 Waiting Time: %d" % p1.waiting_time)
    print("P2 Waiting Time: %d" % p2.waiting_time)
    print("P3 Waiting Time: %d" % p3.waiting_time)

    print("-------")

    print("P1 Turnaround Time: %d" % p1.turnaround_time)
    print("P2 Turnaround Time: %d" % p2.turnaround_time)
    print("P3 Turnaround Time: %d" % p3.turnaround_time)

    print("-------")

    print("Average waiting time: %.2f" % ((p1.waiting_time + p2.waiting_time + p3.waiting_time) / 3))
    print("Average turnaround time: %.2f" % ((p1.turnaround_time + p2.turnaround_time + p3.turnaround_time) / 3))

round_robin(p1,p2,p3, 4)


