import pygame
from pygame.locals import *
from random import shuffle


class Question:
    def __init__(self, question, options, correct_answer, explanation):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation


questions_data = [
    ("Что выведет код: print(2 + 2 * 2)?",
     ["6", "8", "SyntaxError"],
     0,
     "Правильный ответ: 6. Сначала выполняется умножение (2*2=4), затем сложение (2+4=6)."),

    ("Какой тип данных изменяем (mutable) в Python?",
     ["Список (list)", "Кортеж (tuple)", "Строка (str)"],
     0,
     "Правильный ответ: Список (list). Списки можно изменять после создания, в отличие от кортежей и строк."),

    ("Что делает метод .strip() для строк?",
     ["Удаляет пробелы с обоих концов", "Разделяет строку на части", "Переводит в верхний регистр"],
     0,
     "Правильный ответ: Удаляет пробелы с обоих концов. Метод strip() удаляет пробелы и другие символы с начала и конца строки."),

    ("Как получить последний элемент списка lst?",
     ["lst[len(lst)]", "lst[-1]", "lst.last()"],
     1,
     "Правильный ответ: lst[-1]. В Python отрицательные индексы позволяют обращаться к элементам с конца списка."),

    ("Что такое 'list comprehension'?",
     ["Список с комментариями", "Способ создания списков", "Метод сортировки списка"],
     1,
     "Правильный ответ: Способ создания списков. List comprehension - это лаконичный способ создания списков в Python.")
]


questions = []
for qd in questions_data:
    questions.append(Question(qd[0], qd[1], qd[2], qd[3]))
shuffle(questions)


WIDTH, HEIGHT = 900, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_SIZE = 32
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 50
MARGIN = 20


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тест по программированию на Python")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', FONT_SIZE)
title_font = pygame.font.SysFont('Arial', 48)

def draw_text(surface, font_obj, color, text, x, y, centered=True):
    label = font_obj.render(text, True, color)
    if centered:
        rect = label.get_rect(center=(x, y))
    else:
        rect = label.get_rect(topleft=(x, y))
    surface.blit(label, rect)
    return rect


def draw_button(surface, x, y, width, height, text, color=BLACK, bg_color=WHITE):
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    pygame.draw.rect(surface, color, (x, y, width, height), 2)
    draw_text(surface, font, color, text, x + width // 2, y + height // 2)


def show_question(question, question_num, total_questions):
    global current_question_idx, score, show_explanation

    show_explanation = False
    selected_answer = None
    answer_checked = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONUP and not answer_checked:
                pos = pygame.mouse.get_pos()
                for i, option in enumerate(question.options):
                    x = WIDTH // 2 - BUTTON_WIDTH // 2
                    y = HEIGHT // 2 + i * (BUTTON_HEIGHT + MARGIN)
                    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if button_rect.collidepoint(pos):
                        selected_answer = i
                        answer_checked = True
            elif event.type == pygame.MOUSEBUTTONUP and answer_checked:
                pos = pygame.mouse.get_pos()
                if next_button_rect.collidepoint(pos):
                    if selected_answer == question.correct_answer:
                        score += 1
                    return 'next'
                elif explanation_button_rect.collidepoint(pos):
                    show_explanation = not show_explanation

        screen.fill(WHITE)

        progress_text = f"Вопрос {question_num + 1} из {total_questions}"
        draw_text(screen, font, BLACK, progress_text, WIDTH - 150, 30)


        draw_text(screen, title_font, BLUE, "Тест по Python", WIDTH // 2, 50)
        draw_text(screen, font, BLACK, question.question, WIDTH // 2, 150)


        for i, option in enumerate(question.options):
            x = WIDTH // 2 - BUTTON_WIDTH // 2
            y = HEIGHT // 2 + i * (BUTTON_HEIGHT + MARGIN)


            if answer_checked and selected_answer == i:
                if i == question.correct_answer:
                    btn_color = GREEN
                elif selected_answer == i and selected_answer != question.correct_answer:
                    btn_color = RED
                else:
                    btn_color = BLACK
            else:
                btn_color = BLACK

            draw_button(screen, x, y, BUTTON_WIDTH, BUTTON_HEIGHT, option, btn_color)

        if answer_checked:
            next_button_rect = draw_button(screen, WIDTH - BUTTON_WIDTH - 20, HEIGHT - 70,
                                           BUTTON_WIDTH, BUTTON_HEIGHT, "Следующий", BLUE)

            explanation_button_rect = draw_button(screen, 20, HEIGHT - 70,
                                                  BUTTON_WIDTH, BUTTON_HEIGHT,
                                                  "Объяснение" if not show_explanation else "Скрыть",
                                                  BLUE)

            if show_explanation:

                pygame.draw.rect(screen, WHITE, (50, HEIGHT - 150, WIDTH - 100, 100))
                pygame.draw.rect(screen, BLUE, (50, HEIGHT - 150, WIDTH - 100, 100), 2)


                words = question.explanation.split()
                lines = []
                current_line = ""

                for word in words:
                    test_line = current_line + word + " "
                    if font.size(test_line)[0] < WIDTH - 120:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word + " "

                if current_line:
                    lines.append(current_line)

                for i, line in enumerate(lines):
                    draw_text(screen, font, BLACK, line, 70, HEIGHT - 130 + i * 30, False)

        pygame.display.update()
        clock.tick(60)



def show_result(score, total_questions):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(pos):
                    return 'restart'

        screen.fill(WHITE)


        draw_text(screen, title_font, BLUE, "Результаты теста", WIDTH // 2, 100)


        result_text = f"Вы ответили правильно на {score} из {total_questions} вопросов"
        draw_text(screen, font, BLACK, result_text, WIDTH // 2, 200)


        percentage = score / total_questions * 100
        if percentage >= 80:
            grade = "Отлично!"
            color = GREEN
        elif percentage >= 60:
            grade = "Хорошо!"
            color = (0, 200, 0)
        elif percentage >= 40:
            grade = "Удовлетворительно"
            color = (200, 200, 0)
        else:
            grade = "Попробуйте еще раз!"
            color = RED

        draw_text(screen, title_font, color, grade, WIDTH // 2, 300)


        restart_button_rect = draw_button(screen, WIDTH // 2 - BUTTON_WIDTH // 2, 400,
                                          BUTTON_WIDTH, BUTTON_HEIGHT, "Пройти еще раз", BLUE)

        pygame.display.update()
        clock.tick(60)



def main():
    global current_question_idx, score, questions

    while True:

        current_question_idx = 0
        score = 0
        shuffle(questions)


        state = 'question'  # начальное состояние игры
        running = True

        while running:
            if state == 'question':
                result = show_question(questions[current_question_idx],
                                       current_question_idx, len(questions))
                if result == 'quit':
                    running = False
                elif result == 'next':
                    current_question_idx += 1
                    if current_question_idx >= len(questions):
                        state = 'result'

            elif state == 'result':
                result = show_result(score, len(questions))
                if result == 'restart':
                    state = 'question'
                    break
                else:
                    running = False

        if not running:
            break

    pygame.quit()


if __name__ == "__main__":
    main()