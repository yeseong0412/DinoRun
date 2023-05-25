import pygame
import sys
import random

pygame.init()
pygame.display.set_caption('DinoRun~!')
MAX_WIDTH = 800
MAX_HEIGHT = 400
SCORE_INCREMENT = 10
TREE_INTERVAL_MIN = 150  # 나무가 나타나는 최소 주기 (픽셀 단위)
TREE_INTERVAL_MAX = 300  # 나무가 나타나는 최대 주기 (픽셀 단위)

# 화면 상태
MENU_STATE = 0
GAME_STATE = 1
ENDING_STATE = 2

# 메뉴화면
def show_menu(screen):
    screen.fill((255, 255, 255))

    font = pygame.font.Font(None, 48)
    title_text = font.render("DinoRun", True, (0, 0, 0))
    start_text = font.render("Press R to Start", True, (0, 0, 0))
    exit_text = font.render("Press Q to Exit", True, (0, 0, 0))
    hidden_ending_text = font.render("Press H for Hidden Ending", True, (0, 0, 0))  # 히든 엔딩 텍스트 추가

    title_rect = title_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2 - 50))
    start_rect = start_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2))
    exit_rect = exit_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2 + 50))
    hidden_ending_rect = hidden_ending_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2 + 100))  # 히든 엔딩 텍스트 위치 설정

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(exit_text, exit_rect)
    screen.blit(hidden_ending_text, hidden_ending_rect)  # 히든 엔딩 텍스트 화면에 표시

    pygame.display.update()



#게임오버 화면
def show_game_over(screen, score):
    screen.fill((255, 255, 255))
    #화면 흰색 채우기

    font = pygame.font.Font(None, 36)
    text = font.render("Game Over Dino Die...", True, (255, 0, 0)) #Game over출력
    text_rect = text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect) #스코어 출력

    imgGameOver = pygame.image.load('images/dinoDie.png') #사망한 다이노 보여주기
    game_over_rect = imgGameOver.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2))
    screen.blit(imgGameOver, game_over_rect)

    pygame.display.update()
    pygame.time.wait(2000) #게임오버 이후 멈출 시간 설정 (단위는 1000/1s)
    #화면 힌색채우기
    screen.fill((255, 255, 255))

#엔딩화면
def show_ending(screen):
    screen.fill((255, 255, 255)) #기존 뛰던 다이노 그림 삭제
    pygame.display.update()

    imgEnding1 = pygame.image.load('images/ending1.png')
    imgEnding2 = pygame.image.load('images/ending2.jpg')
    imgEnding3 = pygame.image.load('images/ending3.jpg')

    screen.blit(imgEnding1, (screen.get_width() // 2 - imgEnding1.get_width() // 2, screen.get_height() // 2 - imgEnding1.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(1500)

    screen.blit(imgEnding2, (screen.get_width() // 2 - imgEnding2.get_width() // 2, screen.get_height() // 2 - imgEnding2.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(1500)

    screen.blit(imgEnding3, (screen.get_width() // 2 - imgEnding3.get_width() // 2, screen.get_height() // 2 - imgEnding3.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(1500)
# 히든 엔딩 화면
def show_hidden_ending(screen):
    screen.fill((0, 0, 0))  # 배경을 검은색으로 설정
    pygame.display.update()

    # imgHiddenEnding = pygame.image.load('images/hidden_ending.png')  # 히든 엔딩 이미지 로드
    # ending_rect = imgHiddenEnding.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2))
    # screen.blit(imgHiddenEnding, ending_rect)

    pygame.display.update()
    pygame.time.wait(3000)  # 히든 엔딩 화면을 보여준 후 일정 시간 대기

#트리랑 박았는지 확인
def check_collision(din_rect, tree_rect):
    if din_rect.colliderect(tree_rect):
        return True
    return False

#메인 구문
def main():
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    fps = pygame.time.Clock()

    state = MENU_STATE  # 초기 상태는 메뉴 상태로 설정

    #입력 감지 (키보드)
    while True:
        if state == MENU_STATE:
            show_menu(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 'R' 키를 누르면 게임 시작
                        state = GAME_STATE
                    elif event.key == pygame.K_q:  # 'Q' 키를 누르면 게임 종료
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_h:  # 'H' 키를 누르면 히든 엔딩 화면으로 이동
                        show_hidden_ending(screen)
                        state = MENU_STATE

        elif state == GAME_STATE:
            # 기초적인 화면 구성
            imgDin1 = pygame.image.load('images/dino1.png')
            imgDin2 = pygame.image.load('images/dino2.png')
            din_height = imgDin1.get_size()[1]
            din_bottom = MAX_HEIGHT - din_height
            din_x = 50
            din_y = din_bottom
            jump_top = 200
            leg_swap = True
            is_bottom = True
            is_go_up = False

            imgTree = pygame.image.load('images/tree.png').convert_alpha()  # 이미지 로드 (나무)
            tree_height = imgTree.get_size()[1]
            tree_x = MAX_WIDTH
            tree_y = MAX_HEIGHT - tree_height

            score = 0  # 스코어 설정 (초기값 0)
            game_over = False

            font = pygame.font.Font(None, 36)

            tree_interval = random.randint(TREE_INTERVAL_MIN, TREE_INTERVAL_MAX)  # 첫 번째 나무가 나타나는 주기
            tree_counter = tree_interval

            while not game_over:
                screen.fill((255, 255, 255))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:  # 스페이스바를 누를 때에만 점프가 가능하도록 함
                            if is_bottom:
                                is_go_up = True
                                is_bottom = False
                        elif event.key == pygame.K_ESCAPE:  # 'ESC' 키를 누르면 메뉴 화면으로 돌아감
                            state = MENU_STATE
                            game_over = True

                if is_go_up:
                    din_y -= 10.0

                elif not is_go_up and not is_bottom:
                    din_y += 10.0

                if is_go_up and din_y <= jump_top:
                    is_go_up = False

                if not is_bottom and din_y >= din_bottom:
                    is_bottom = True
                    din_y = din_bottom

                tree_x -= 12.0
                if tree_x <= 0:
                    tree_x = MAX_WIDTH
                    score += SCORE_INCREMENT

                    # 나무가 나타나는 주기 재설정
                    tree_interval = random.randint(TREE_INTERVAL_MIN, TREE_INTERVAL_MAX)
                    tree_counter = tree_interval

                din_rect = pygame.Rect(din_x, din_y, imgDin1.get_width(), imgDin1.get_height())
                tree_rect = pygame.Rect(tree_x, tree_y, imgTree.get_width(), imgTree.get_height())

                if check_collision(din_rect, tree_rect) or score >= 100:
                    game_over = True

                screen.blit(imgTree, (tree_x, tree_y))

                if leg_swap:
                    screen.blit(imgDin1, (din_x, din_y))
                    leg_swap = False

                else:
                    screen.blit(imgDin2, (din_x, din_y))
                    leg_swap = True

                score_text = font.render(f"Score: {score}", True, (0, 0, 0))
                screen.blit(score_text, (10, 10))

                pygame.display.update()
                fps.tick(30)  # 속도임 높이면 난이도 업 낮추면 난이도 다운

            if score >= 100:  # 스코어가 100이라면 엔딩으로
                show_ending(screen)

            else:  # 아니라면 게임오버로
                show_game_over(screen, score)

        elif state == ENDING_STATE:
            # 엔딩 상태에 필요한 작업 수행
            pass

if __name__ == '__main__':
    main()
