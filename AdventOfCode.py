import re
from sys import path_hooks
import concurrent.futures as future

class AdventOfCode:
    def __init__(self, puzzle1=None, puzzle2=None, puzzle3 = None, random_bingo = None, puzzle4 = None):
        self.floor_depths = self.reader(puzzle1)

        self.depth = 0
        self.horizontal = 0
        self.aim = 0
        self.pilot = self.reader(puzzle2)

        self.binary = self.reader(puzzle3)
        self.gamma = 0
        self.epsilon = 0

        self.random_bingo = self.reader(random_bingo)
        self.bingoboards = self.reader(puzzle4)
        self.finished_boards = self.bingo_board(self.bingoboards)

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
            elif textfile == 'puzzle3.txt':
                nylista = [re.findall(r'[0-1]+', line) for line in lista]
                nylista = [el[0] for el in nylista]
            elif textfile == 'random_bingo.txt':
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

        def bit_critera(lista):
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

        return bit_critera(lista)
    
    def bingo_board(self, boardfile):
        boards = []
        amount_boards = int(len(boardfile)/5)
        lista = [x*5 for x in range(amount_boards)]
        for n in lista:
            boards.append(boardfile[n:n+5])
        return boards
    
    def bingo(self, board):
        
        fiveinarow = 0
        for number in self.random_bingo:
            for row in range(5):
                if number in board[row]:
                    ind = board[row].index(number)
                    board[row][ind] = 'X'
                    fiveinarow = board[row].count('X')
            if fiveinarow == 5: #bingo!
                summa = 0
                for row in range(5):
                    for el in range(5):
                        if board[row][el] != 'X':
                            summa += board[row][el]
                return summa*number
    
    def runner(self, n):
        b = self.finished_boards[n]
        score = self.bingo(b)
        return score

    def puzzle1_part1(self):
        return self.increase_counter(self.floor_depths)
    
    def puzzle1_part2(self):
        sliding_list = self.sliding_window()
        sliding_increase = self.increase_counter(sliding_list)
        return sliding_increase
    
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
        return print(printer)

    def puzzle4(self):
        # nu kommer parallellprogrammeringen!
        with future.ProcessPoolExecutor() as ex:
            lst = list(range(len(self.finished_boards)))
            results = ex.map(self.runner, lst)

            res = list(results)
        
        return print(max(res))

        


def main():

    ''' Day 1 '''
    advent1 = AdventOfCode('puzzle1.txt')
    # increases = advent1.puzzle1_part1()
    # increases_in_threes = advent1.puzzle1_part2()

    ''' Day 2 '''
    advent2 = AdventOfCode(None, 'puzzle2.txt')
    # (x,y) = advent2.position2()

    ''' Day 3 '''
    advent3 = AdventOfCode(None, None, 'puzzle3.txt')
    # advent3.puzzle3_part2()

    ''' Day 4 '''
    # advent4 = AdventOfCode(None, None, None, 'random_bingo.txt', 'puzzle4.txt')
    advent4 = AdventOfCode(None, None, None, 'random_test.txt', 'test.txt')
    advent4.puzzle4()


if __name__ == '__main__':
    main()

