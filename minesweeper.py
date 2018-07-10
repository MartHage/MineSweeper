from selenium import webdriver
from selenium.webdriver import ActionChains
import time

w = 30
h = 16
# w = 3
# h = 3


def valid_square(y, x):
    if x < 0 or x >= w:
        return False
    if y < 0 or y >= h:
        return False
    return True
  

def find_best_square(formatted_grid):
    prob_grid = [[1.0 for x in range(w)] for y in range(h)]
    secure_squares = []
    all_squares = []
    #print(prob_grid)
    for i in range(w):
        for j in range(h):
            content = formatted_grid[j][i]
            if content > 0:
                count = 0
                squares = []
                count_flagged = 0
                for x in range(3):
                    for y in range(3):
                        if valid_square(j + x - 1, i + y - 1):
                            if formatted_grid[j + x - 1][i + y - 1] == -1:
                                count += 1
                                squares.append([j+x-1, i+y-1])
                                all_squares.append([j+x-1, i+y-1])
                            elif formatted_grid[j + x - 1][i + y - 1] == -2:
                                count_flagged += 1
                #print(squares)

                if content != count_flagged:
                    for square in squares:
                        prob_grid[square[0]][square[1]] *= (1-(content-count_flagged)/count)
                elif len(squares) > 0:
                    secure_squares.append([squares[0][1], squares[0][0], -1])
                    
    # x, y, score
    best = [-1, -1, 1.0]
    for i in range(w):
        for j in range(h):
            prob_grid[j][i] = 1 - prob_grid[j][i]
            score = prob_grid[j][i]
            if 0 < score < best[2] and len(secure_squares) == 0:
                count = 0
                for x in range(3):
                    for y in range(3):
                        if valid_square(j + x - 1, i + y - 1):
                            if formatted_grid[j + x - 1][i + y - 1] >= 0:
                                count += 1
                if count >= 2:
                    best[0] = i
                    best[1] = j
                    best[2] = score
            elif score == 1.0:
                secure_squares.append([i, j, score])

    # for row in formatted_grid:
    #     print('[%s]' % (' '.join('%03s' % i for i in row)))
    #for row in prob_grid:
    #    print('[%s]' % (' '.join('%03s' % i for i in row)))

    if len(secure_squares) > 0:
        return secure_squares
    else:
        if best[1] == -1:
            return [[int(w/2), int(h/2), 0]]
        else:
            return [best]


def load_browser():
    print('Starting Firefox')
    driver_init = webdriver.Chrome()
    driver_init.get("http://minesweeperonline.com/#")
    print('Firefox Loaded')

    for i in range(2):
        time.sleep(1)
        print(2-i)
    print(0)

    return driver_init


def update_grid(i, j, is_flag):
    if is_flag:
        formattedGrid[j][i] = -2
    if formattedGrid[j][i] == -1:
        class_name = driver.find_element_by_id(str(j+1)+'_'+str(i+1)).get_attribute('class')
        if class_name[:11] == 'square open':
            formattedGrid[j][i] = int(class_name[-1])
            if formattedGrid[j][i] == 0:
                for x in range(3):
                    for y in range(3):
                        if valid_square(j + y - 1, i + x - 1):
                            update_grid(i + x - 1, j + y - 1, is_flag)



driver = load_browser()

grid = [[driver.find_element_by_id(str(y+1)+'_'+str(x+1)) for x in range(w)] for y in range(h)]

while True:
    formattedGrid = [[-1 for x in range(w)] for y in range(h)]
    not_failed = True
    while not_failed:
        best_squares = find_best_square(formattedGrid)
        for best_square in best_squares:
            isFlag = False
            if best_square[2] == 1.0:
                isFlag = True
                actionChains = ActionChains(driver)
                actionChains.context_click(grid[best_square[1]][best_square[0]]).perform()
            else:
                grid[best_square[1]][best_square[0]].click()
                # print(best_square)
                if driver.find_element_by_id('face').get_attribute('class') == 'facedead':
                    not_failed = False
                    driver.find_element_by_id('face').click()

            update_grid(best_square[0], best_square[1], isFlag)
