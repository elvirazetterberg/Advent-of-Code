from cmath import inf
import re
from sys import path_hooks
import concurrent.futures as future
import numpy as np
import time

class AdventOfCode:
    def __init__(self, puzzle, extra_file=None):
        self.puzzle = puzzle
        self.extra_file = extra_file
        self.identity = self.identifier()
    
    def identifier(self):
        if self.puzzle == 'puzzle1.txt':
            advent1 = self.Puzzle1and2(self.puzzle)
            increases = advent1.puzzle1_part1()
            incr_in_threes = advent1.puzzle1_part2()
            return print('Increases: ', increases, '\nIncreases in threes: ', incr_in_threes)
        elif self.puzzle == 'puzzle2.txt':
            advent2 = self.Puzzle1and2(None, self.puzzle)
            (x,y) = advent2.position2()
            return print('(x,y): ', (x,y))
        elif self.puzzle == 'puzzle3.txt':
            advent3 = self.Puzzle3(self.puzzle)
            power_consumption = advent3.puzzle3()
            printer = advent3.puzzle3_part2()
            return print('P1 power cons: ', power_consumption, '\n', printer)
        elif self.puzzle == 'puzzle4.txt':
            advent4 = self.Puzzle4(self.puzzle, self.extra_file)
            score = advent4.puzzle4()
            return print('Score: ', score)
        elif self.puzzle == 'puzzle5.txt':
            advent5 = self.Puzzle5(self.puzzle)
            dangerous_coordinates = advent5.puzzle5()
            return print(dangerous_coordinates)
        elif self.puzzle == 'puzzle6.txt':
            advent6 = self.Puzzle6(self.puzzle)
            fish = advent6.puzzle()
            return print(fish)
        elif self.puzzle == 'test_7.txt' or self.puzzle == 'puzzle7.txt':
            advent7 = self.Puzzle7(self.puzzle)
            # x2 = advent7.optimal_alignment()
            fuel = advent7.puzzle()
            return print(fuel)
        elif self.puzzle == 'puzzle8.txt' or self.puzzle == 'test_8.txt':
            advent8 = self.Puzzle8(self.puzzle)
            unique = advent8.unique_number()
            return print(unique)

    
    class Puzzle1and2:
        def __init__(self, puzzle1=None, puzzle2 = None):
        
            self.floor_depths = self.reader(puzzle1)
            self.depth = 0
            self.horizontal = 0
            self.aim = 0
            self.pilot = self.reader(puzzle2)

        def reader(self, textfile):
            if textfile == None:
                return ['hej']
            else:
                puzzle = open(textfile, 'r')
                lista = puzzle.readlines()
                if textfile == 'puzzle1.txt':
                    nylista = [re.findall(r'[0-9]+', line) for line in lista]
                    nylista = [int(el[0]) for el in nylista]
                elif textfile == 'puzzle2.txt':
                    nylista = [el.split() for el in lista]
                return nylista
        
        def increase_counter(self, lst):

            def _increase_counter(previous, following):
                if len(following) == 0:
                    return 0
                elif len(following) <= 4:
                    if previous < following[0]:
                        return 1 + _increase_counter(following[0], following[1:])
                    else:
                        return _increase_counter(following[0], following[1:])
                else:
                    if previous < following[0]:
                        return 1 + _increase_counter(following[0], following[1:int(len(following)/2)+1]) + _increase_counter(following[int(len(following)/2)], following[int(len(following)/2)+1:])
                    else:
                        return _increase_counter(following[0], following[1:int(len(following)/2)+1]) + _increase_counter(following[int(len(following)/2)], following[int(len(following)/2)+1:])
        
            return _increase_counter(lst[0], lst[1:])

    
        def sliding_window(self):
            sliding_list = []
            i = 0
            for i in range(len(self.floor_depths)):
                el = self.floor_depths[i:i+3]
                if len(el) == 3:
                    sliding_list.append(sum(el))
            return sliding_list
        
        def position(self):
            for step in self.pilot:
                if step[0] == 'forward':
                    self.horizontal += int(step[1])
                elif step[0] == 'down':
                    self.depth += int(step[1])
                else:
                    self.depth -= int(step[1])
            return(self.horizontal, self.depth)
    
        def position2(self):
            for step in self.pilot:
                if step[0] == 'down':
                    self.aim += int(step[1])
                elif step[0] == 'up':
                    self.aim -= int(step[1])
                elif step[0] == 'forward':
                    self.horizontal += int(step[1])
                    self.depth += int(step[1])*self.aim
            return (self.horizontal, self.depth)
        
        def puzzle1_part1(self):
            return self.increase_counter(self.floor_depths)
    
        def puzzle1_part2(self):
            sliding_list = self.sliding_window()
            sliding_increase = self.increase_counter(sliding_list)
            return sliding_increase
    
    class Puzzle3:
        def __init__(self, puzzle3):
            self.binary = self.reader(puzzle3)
            self.gamma = 0
            self.epsilon = 0
        
        def reader(self, textfile):
            if textfile == None:
                return ['hej']
            else:
                puzzle = open(textfile, 'r')
                lista = puzzle.readlines()
                if textfile == 'puzzle3.txt':
                    nylista = [re.findall(r'[0-1]+', line) for line in lista]
                    nylista = [el[0] for el in nylista]
                return nylista

        def occurrence_ones(self, lista, pos):

            def _occurrence_ones(lista, pos):
                if len(lista) <= 1:
                    if len(lista) == 1:
                        return int(lista[0][pos])
                    else:
                        return 0       
                else:
                    binary = int(lista[0][pos])
                    first_half = lista[1:int(len(lista)/2)+1]
                    second_half = lista[int(len(lista)/2)+1:]

                    return binary + _occurrence_ones(first_half, pos) + _occurrence_ones(second_half, pos)

            return _occurrence_ones(lista, pos)

        def common_binary(self, lista):
            binary = ''
            for pos in range(len(lista[0])):
                occur = self.occurrence_ones(lista, pos)
                if occur >= len(lista)/2:
                    binary += '1'
                else:
                    binary += '0'
            return binary
    
        def uncommon_binary(self, lista):
            binary = ''
            for pos in range(len(lista[0])):
                occur = self.occurrence_ones(lista, pos)
                if occur >= len(lista)/2:
                    binary += '0'
                else:
                    binary += '1'
            return binary
    
        def binary_to_decimal(self, binary):
            decimal = 0
            for pos in range(len(binary)+1):
                if pos > 0 and binary[-pos] != '0':
                    decimal += 2**(pos-1)
            return decimal

        def bit_criteria(self, lista, common = True):

            def _bit_critera(lista):
                for pos in range(len(lista[0])):
                    if common == True:
                        reference = self.common_binary(lista)
                    else:
                        reference = self.uncommon_binary(lista)
                    
                    lista = _selector(lista, reference, pos)

                    if len(lista) == 1:
                        return lista[0]
        
            def _selector(lista, reference, pos):
                if len(lista) < 1:
                    return lista
                elif lista[0][pos] == reference[pos]:
                    first_half = lista[1:int(len(lista)/2)+1]
                    second_half = lista[int(len(lista)/2)+1:]
                    return [lista[0]] + _selector(first_half, reference, pos) + _selector(second_half, reference, pos)
                else:
                    first_half = lista[1:int(len(lista)/2)+1]
                    second_half = lista[int(len(lista)/2)+1:]
                    return _selector(first_half, reference, pos) + _selector(second_half, reference, pos)

            return _bit_critera(lista)
        
        def puzzle3(self):
            gamma = self.common_binary(self.binary)
            epsilon = ''
            for num in gamma:
                if num == '0':
                    epsilon += '1'
                else:
                    epsilon += '0'
            gamma_dec = self.binary_to_decimal(gamma)
            epsilon_dec = self.binary_to_decimal(epsilon)
            power_consumption = gamma_dec*epsilon_dec
            return power_consumption
    
        def puzzle3_part2(self):
            lista = self.binary
            oxygen_rating_bin = self.bit_criteria(lista)
            oxygen_rating_dec = self.binary_to_decimal(oxygen_rating_bin)
            CO2_rating_bin = self.bit_criteria(lista, False)
            CO2_rating_dec = self.binary_to_decimal(CO2_rating_bin)

            printer = f'Oxygen generator rating: {oxygen_rating_dec} \nCO2 scrubber rating: {CO2_rating_dec}'
            printer += f'\nLife support rating: {oxygen_rating_dec*CO2_rating_dec}'
            return printer
    
    class Puzzle4:
        def __init__(self, puzzle4, random_bingo):
            self.random_bingo = self.reader(random_bingo)
            self.bingoboards = self.reader(puzzle4)
            self.finished_boards = self.bingo_board(self.bingoboards)


        def reader(self, textfile):
            if textfile == None:
                return ['hej']
            else:
                puzzle = open(textfile, 'r')
                lista = puzzle.readlines()
                if textfile == 'random_bingo.txt':
                    nylista = re.split(',', lista[0])
                    nylista = [int(el) for el in nylista]
                elif textfile == 'puzzle4.txt':
                    mylista = [re.findall(r'[0-9]+', line) for line in lista if len(line) > 1]
                    nylista = [[int(mylista[n][m]) for m in range(len(mylista[0]))] for n in range(len(mylista))]
                elif textfile == 'test.txt':
                    mylista = [re.findall(r'[0-9]+', line) for line in lista if len(line) > 1]
                    nylista = [[int(mylista[n][m]) for m in range(len(mylista[0]))] for n in range(len(mylista))]
                elif textfile == 'random_test.txt':
                    nylista = re.split(',', lista[0])
                    nylista = [int(el) for el in nylista]
                return nylista
    
        def bingo_board(self, boardfile):
            boards = []
            amount_boards = int(len(boardfile)/5)
            lista = [x*5 for x in range(amount_boards)]
            for n in lista:
                boards.append(boardfile[n:n+5])
            boards = [np.array(board) for board in boards]
            return boards
    
        def bingo(self, board):
            rounds = 0
            fiveinarow = 0
            fiveinacolumn = 0
            for number in self.random_bingo:
                rounds += 1
                if number in board:
                    ind = np.where(board == number)
                    board[ind[0][0], ind[1][0]] = -1

                    for row in range(5):
                        fiveinarow = np.count_nonzero(board[row,:] == -1)
                        fiveinacolumn = np.count_nonzero(board[:,row] == -1)

                        if fiveinarow == 5 or fiveinacolumn == 5:
                            summa = 0
                            for row in range(5):
                                for el in range(5):
                                    if board[row,el] != -1:
                                        summa += board[row,el]
                            return (rounds, summa*number)
    
        def runner(self, n):
            b = self.finished_boards[n]
            rounds, score = self.bingo(b)
            return rounds, score
        
        def puzzle4(self):
            # nu kommer parallellprogrammeringen!
            with future.ProcessPoolExecutor() as ex:
                lst = list(range(len(self.finished_boards)))
                result = ex.map(self.runner, lst)
                lista = list(result)
                
                score  = [el[1] for el in lista]
                rounds = [el[0] for el in lista]
                winner = min(rounds)
                winner_score = score[rounds.index(winner)]

                loser = max(rounds)
                loser_score = score[rounds.index(loser)]

            return winner_score, loser_score

    class Puzzle5:
        def __init__(self, puzzle5):
            self.coordinate_list = self.reader(puzzle5)
            self.maximum_x = 0
            self.maximum_y = 0


        def reader(self, textfile):
            if textfile == None:
                return ['hej']
            else:
                puzzle = open(textfile, 'r')
                lista = puzzle.readlines()
                coordinates = [re.findall(r'[0-9]+', line) for line in lista]
                connected_coordinates = [[(int(el[0]),int(el[1])), (int(el[2]),int(el[3]))] for el in coordinates]
                return connected_coordinates
        
        def horizontal_or_vertical(self, coordinates):
            h_or_v = []
            for movement in coordinates:
                if movement[0][0] == movement[1][0] or movement[0][1] == movement[1][1]:
                    if movement[0][0] > self.maximum_x:
                        self.maximum_x = movement[0][0]
                    if movement[0][1] > self.maximum_y:
                        self.maximum_y = movement[0][1]
                    h_or_v.append(movement)
            return h_or_v
        
        def max_min(self, coordinates):
            for co in coordinates:
                if max(co[0][0], co[1][0]) > self.maximum_x:
                    self.maximum_x = max(co[0][0], co[1][0])
                if max(co[0][1], co[1][1]) > self.maximum_y:
                    self.maximum_y = max(co[0][1], co[1][1])
            return (self.maximum_x, self.maximum_y)
        
        def puzzle5(self):
            # h_or_v = self.horizontal_or_vertical(self.coordinate_list)
            mapp = self.mapping_vents(self.coordinate_list)
            print(mapp)
            danger_zones = np.count_nonzero(mapp >= 2) # rätt
            return danger_zones
        
        def mapping_vents(self, coordinates):
            (maxix, maxiy) = self.max_min(coordinates)
            mapp = np.zeros((maxix+1, maxiy+1), dtype = int)
            for coord in coordinates:    
                min_x, max_x = min(coord[0][0], coord[1][0]), max(coord[0][0], coord[1][0])                
                min_y, max_y = min(coord[0][1], coord[1][1]), max(coord[0][1], coord[1][1])

                if max_x == min_x:
                    mapp[min_y:max_y+1, min_x]=[el+1 for el in mapp[min_y:max_y+1, min_x]]

                elif max_y == min_y:
                    mapp[min_y, min_x:max_x+1]=[el+1 for el in mapp[min_y, min_x:max_x+1]]
                
                else: #45 degrees
                    x1, y1 = coord[0][0], coord[0][1]
                    diffx, diffy = coord[1][0] - x1, coord[1][1] -y1
                    stepsx, stepsy = int(diffx/abs(diffx)), int(diffy/abs(diffy))

                    for s in range(abs(diffx)+1):
                        mapp[y1, x1] += 1
                        x1 += stepsx
                        y1 += stepsy

            return mapp
    
    class Puzzle6:
        def __init__(self, puzzle6):
            self.cycles_lex = self.reader(puzzle6)
            self.cycle_length = 6
            self.born_length = 8
        
        def reader(self, textfile):
            if textfile == None:
                return ['hej']
            else:
                puzzle = open(textfile, 'r')
                lista = puzzle.readlines()
                cycles = [line.split(',') for line in lista]
                c = []
                for i in range(len(cycles)):
                    c += [int(el) for el in cycles[i]]
                c.sort()
                # Spara data som lexikon där varje timer är kopplad till ett antal fiskar.
                cycles_lex = {}
                for el in c:
                    if el not in cycles_lex:
                        cycles_lex[el] = 1
                    else:
                        cycles_lex[el] += 1
                return cycles_lex
        
        def new_day(self):
            new_lex = self.cycles_lex.copy()
            for key,val in self.cycles_lex.items():
                newkey = key - 1
                if newkey >= 0:
                    if newkey not in new_lex:
                        new_lex[newkey] = val
                    else:
                        new_lex[newkey] += val
                else:
                    if self.cycle_length not in new_lex:
                        new_lex[self.cycle_length] = val
                        new_lex[self.born_length] = val
                    else:
                        new_lex[self.cycle_length] += val
                        new_lex[self.born_length] += val
                new_lex[key] -= val
            return new_lex

        def puzzle(self):
            for days in range(256):
                self.cycles_lex.update(self.new_day())
            
            summa = 0
            for key, val in self.cycles_lex.items():
                summa += val
            return summa

    class Puzzle7:
        def __init__(self, puzzle7):
            self.positions = self.reader(puzzle7)
            self.optimum = self.optimal_alignment()
        
        def reader(self, textfile):
            if textfile == None:
                return ['hej']
            else:
                puzzle = open(textfile, 'r')
                lista = puzzle.readlines()
                cycles = [line.split(',') for line in lista]
                c = []
                for i in range(len(cycles)):
                    c += [int(el) for el in cycles[i]]
                c.sort()
                return c
        
        def optimal_alignment(self):
            
            def _optimal_alignment(ref1, fuel1, ref2, fuel2):
                # fuel1 = self.fuel2(ref1) # borde inte behöva kolla en två ggr
                # fuel2 = self.fuel2(ref2)
                if ref2 - ref1 == 1:
                    if fuel1 < fuel2:
                        return ref1, fuel1
                    else:
                        return ref2, fuel2
                else:                  
                    if fuel1 < fuel2:
                        ref2 -= int((ref2-ref1)/2)
                        fuel2 = self.fuel(ref2)
                    else:
                        ref1 += int((ref2-ref1)/2)
                        fuel1 = self.fuel(ref1)
                    return _optimal_alignment(ref1, fuel1, ref2, fuel2)
            
            ref1 = self.positions[0]
            ref2 = self.positions[-1]
            return _optimal_alignment(ref1, self.fuel2(ref1), ref2, self.fuel2(ref2))
        
        def fuel(self, opti):
            fuel = 0
            for i in range(len(self.positions)):
                if self.positions[i] >= opti:
                    fuel += self.positions[i] - opti
                else:
                    fuel += opti - self.positions[i]
            return fuel
        
        def fuel2(self, opti):
            fuel = 0
            for i in range(len(self.positions)):
                if self.positions[i] >= opti:
                    fuel += sum(range(self.positions[i]-opti+1)) # flyttar den från 5 till 2 = 1+2+3=6=sum(range(4))
                else:
                    fuel += sum(range(opti-self.positions[i]+1)) # från 1 till 3 = 1+2 = sum(range(3))
            return fuel
        
        def puzzle(self):
            pos, fuel = self.optimum
            return fuel

            # Dexters enklare lösning :(
            # optimal = float('inf')
            # for i in range(min(self.positions), max(self.positions)):
            #     fuel = 0
            #     for j in range(len(self.positions)):
            #         if i > self.positions[j]:
            #             fuel += i - self.positions[j]
            #             continue
            #         if self.positions[j] > i:
            #             fuel += self.positions[j] - i
            #             continue
            #         if i==self.positions[j]:
            #             continue
            #     if fuel < optimal:
            #         optimal = fuel
            # return optimal

    class Puzzle8:
        def __init__(self, puzzle8):
            self.signals = self.reader(puzzle8)
            self.segments = self.number_of_segments(self.signals)
            self.notebook = []
        
        def reader(self, textfile):
            if textfile == None:
                return ['hej']
            else:
                puzzle = open(textfile, 'r')
                lista = puzzle.readlines()
                lst = [re.findall(r'[|\w*]+', line) for line in lista]
                newlist = []
                for line in lst:
                    newlist.append([line[0:line.index('|')], line[line.index('|')+1:]])
                return newlist
        
        def number_of_segments(self, list):
            segments = {}
            for line in list:
                output = line[1]
                for seg in output:
                    length = len(seg)
                    if length not in segments:
                        segments[length] = 1
                    else:
                        segments[length] += 1
            return segments
        
        def unique_number(self):
            return self.segments[2] + self.segments[3] + self.segments[4] + self.segments[7]
        
        def unique_segments(self):
            for line in self.signal:
                output = line[1]
                unique = {}
                for seg in output:
                    length = len(seg)
                    if length in [2, 3, 4, 7]:
                        unique[length] = seg # eg. {2:ab, 3:cab}
                self.notebook += line + [unique]

        def signal_to_segment(self, input, unique):
            dic = {}
            for signal in input:
                length = len(signal)
                comparisons = [unique[2], unique[3], unique[4], unique[7]] # cf, acf, bcdf, abcdef # 1, 7, 4, 8
                # for el in signal:
                if length == 3:
                    dic['a'] = self.compare(signal, comparisons[0])
                elif length == 6:
                    letter = ['c', 'd', 'e']
                    comp = [comparisons[0], comparisons[2], comparisons[3]] # [1, 4, 8]
                    i = 0
                    while True:
                        dic[letter[i]] = self.compare(comp[i], signal)
                        i += 1
                elif length == 5:
                    b = self.compare(comparisons[3], signal + self.compare(comparisons[0], signal))
                    if b == True:
                        continue
                    else:
                        dic['b'] = b
            dic['f'] = signal

        def compare(self, signal, comparison):
            for el in signal:
                if el in comparison:
                    continue
                else:
                    return el
            return True



        
        def puzzle(self):
            for entry in self.notebook:
                translation = self.signal_to_segment(entry[0], entry[2]) # {a:x1, b:x2, c:x3...}

def main():

    ''' Day 1 '''
    # advent1 = AdventOfCode('puzzle1.txt')

    ''' Day 2 '''
    # advent2 = AdventOfCode('puzzle2.txt')

    ''' Day 3 '''
    # advent3 = AdventOfCode('puzzle3.txt')

    ''' Day 4 '''
    # advent4 = AdventOfCode('puzzle4.txt', 'random_bingo.txt')

    ''' Day 5 '''
    # advent5 = AdventOfCode('puzzle5.txt')
    
    ''' Day 6 '''
    # advent6 = AdventOfCode('puzzle6.txt')

    ''' Day 7 '''
    # advent7 = AdventOfCode('puzzle7.txt')
    
    ''' Day 8 '''
    advent8 = AdventOfCode('puzzle8.txt')
    # advent8 = AdventOfCode('test_8.txt')


if __name__ == '__main__':
    main()

