with open('unformatted_output.txt') as file:
    line_num = 0
    next_ip = 2
    next_name = 3
    next_status = 9
    last_key = ""
    clients = []
    for line in file.readlines():
        line_num += 1

        if line_num == next_ip:
            last_key = line
            next_ip += 10

        if line_num == next_name:
            last_key = last_key + line
            next_name += 10

        if (line_num == next_status): 
            if line == 'on\n':
                clients.append(last_key)
            next_status += 10

    print(clients)
