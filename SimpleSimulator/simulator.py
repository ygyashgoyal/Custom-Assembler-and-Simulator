def binary_deciaml(binary): #BINARY TO DECIMAL
    return int(binary,2)
def decimal_binary(decimal,num_bits):   #DECIMAL TO BINARY
    return format(decimal,f"0{num_bits}b")
def registers_binary(registers):    #REGISTERS TO BINARY
    return "".join(decimal_binary(reg,16) for reg in registers)
def flags_binary(overflow_flag):    #FLAGS TO BINARY
    return f"00000000{decimal_binary(overflow_flag,16)}"

machinecode = [
    "0001100000010100", #MOVE R2 TO R0
    "0001100100111000", #MOVE R3 TO R1
    "0001100110011010", #MOVE R4 TO R2
    "0001100000010100", #MOVE R2 TO R0
    "0011100000000000", #DIVIDE R0 BY R0
    "0111100000000000"  #HALT
]

registers = [0]*7
flags = 0
output = ""
for instruction in machinecode:
    opcode = instruction[:5]
    operands = [instruction[5:8],instruction[8:11]]
    if opcode == "00011":   #MOVE
        registers[binary_deciaml(operands[0])] = registers[binary_deciaml(operands[1])]
    elif opcode == "00111": #DIVIDE
        reg3,reg4 = map(binary_deciaml,operands)
        if registers[reg4] == 0:
            flags = 1
            registers[0] = registers[1] = 0
        else:
            flags = 0
            registers[0],registers[1] = divmod(registers[reg3],registers[reg4])
    elif opcode == "01101": #INVERT
        registers[binary_deciaml(operands[0])] = ~registers[binary_deciaml(operands[1])]
    elif opcode == "01110": #COMPARE
        reg1,reg2 = map(binary_deciaml, operands)
        flags = (registers[reg1] > registers[reg2]) - (registers[reg1] < registers[reg2])
    elif opcode == "00000": #ADDITION
        reg1,reg2,reg3 = map(binary_deciaml,operands)
        result = registers[reg2] + registers[reg3]
        flags = 1 if result > (2 ** 16 - 1) else 0
        registers[reg1] = result % (2 ** 16)
    elif opcode == "00001": #SUBTRACTION
        reg1,reg2,reg3 = map(binary_deciaml,operands)
        result = registers[reg2] - registers[reg3]
        flags = 1 if result < 0 else 0
        registers[reg1] = max(0, result)
    elif opcode == "00010": #MOVE IMMEDIATE
        reg1,imm = map(binary_deciaml,operands)
        registers[reg1] = imm
    elif opcode == "00110": #MULTIPLY
        reg1 = binary_deciaml(operands[0])
        reg2 = binary_deciaml(operands[1])
        reg3 = binary_deciaml(operands[2])
        result = registers[reg2] * registers[reg3]
        if result > (2 ** 16 - 1):
            flags = 1
            result = 0
        else:
            flags = 0
        registers[reg1] = result
    elif opcode == "00111": #DIVIDE
        reg3 = binary_deciaml(operands[0])
        reg4 = binary_deciaml(operands[1])
        if registers[reg4] == 0:
            flags = 1
            registers[R0] = 0
            registers[R1] = 0
        else:
            flags = 0
            registers[R0] = registers[reg3] // registers[reg4]
            registers[R1] = registers[reg3] % registers[reg4]
    elif opcode == "01000": #RIGHT SHIFT
        reg1 = binary_deciaml(operands[0])
        shiftamount = binary_deciaml(operands[1])
        registers[reg1] >>= shiftamount
    elif opcode == "01001": #LEFT SHIFT
        reg1 = binary_deciaml(operands[0])
        shiftamount = binary_deciaml(operands[1])
        registers[reg1] <<= shiftamount
    elif opcode == "01010": #XOR
        reg1 = binary_deciaml(operands[0])
        reg2 = binary_deciaml(operands[1])
        reg3 = binary_deciaml(operands[2])
        registers[reg1] = registers[reg2] ^ registers[reg3]
    elif opcode == "01011": #OR
        reg1 = binary_deciaml(operands[0])
        reg2 = binary_deciaml(operands[1])
        reg3 = binary_deciaml(operands[2])
        registers[reg1] = registers[reg2] | registers[reg3]
    elif opcode == "01100": #AND
        reg1 = binary_deciaml(operands[0])
        reg2 = binary_deciaml(operands[1])
        reg3 = binary_deciaml(operands[2])
        registers[reg1] = registers[reg2] & registers[reg3]

    pc_binary = decimal_binary(len(output) // 135,7)
    registers_binary = registers_binary(registers)
    flags_binary = flags_binary(flags)
    output += f"{pc_binary} {' '.join([registers_binary[i:i + 16] for i in range(0,112,16)])} {flags_binary}\n"

print(output)
