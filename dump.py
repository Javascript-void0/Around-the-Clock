    # data = {}
    # data["members"] = []
    # data["nums"] = []
    # f = open(f'./DB/data.txt').read()
    # lines = f.splitlines()
    # lines = lines[2:]
    # for i in range(len(lines)):
    #     member = lines[i].split(': ')
    #     data["members"].append(member[0])
    #     data["nums"].append(int(member[1]))
    # print(data)
    
    # list = data["nums"]
    # final = []
    # for i in range(0, 10):
    #     max = 0
    #     for j in range(len(list)):
    #         if list[j] > max:
    #             max = list[j]
    #     list.remove(max)
    #     final.append(max)
    # print(final)

# SUB_COMMAND

# 1

# SUB_COMMAND_GROUP

# 2

# STRING

# 3

# INTEGER

# 4

# BOOLEAN

# 5

# USER

# 6

# CHANNEL

# 7

# ROLE

# 8

'''
        file_num = 0
        for file in os.listdir('./DB/txt'):
            file_num += 1
            if os.stat(f'./DB/txt/{file}').st_size <= 7800000:
                f = open(f'./DB/txt/{file}')
                f = f.read()
                lines = f.splitlines(True)
                lines.append(f'{member.id}: 1\n')
                with open(f'./DB/txt/{file}', 'w') as file:
                    file.writelines(lines)
                    file.close()
                    await log.send(f'```DATABASE: Registered {member}```')
                    return
        file_num += 1
        with open(f'./DB/txt/2.txt', 'w') as file:
            file.write(f'{member.id}: 1\n')
            file.close()
            await log.send(f'```DATABASE: Registered {member}```')
            return
'''