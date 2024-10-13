import pygame
import sys
import random
import math
import os

class TerrainGenerator:
    def __init__(self) :
        self.__map_height = 512
        self.__map_width = 20
        self.map = [[0 for i in range(self.__map_width)] for i in range(self.__map_height)]

        self.__terrain_height = int(self.__map_height / 2 + 20)
        self.seed = 0
        self.terrain_type = self.__getrandom(2)
        self.terrain_type_list = []

        self.sea_level = int(self.__map_height / 2 - 15)
        self.sand_level = int(self.__map_height / 2 - 12)

    # 获取随机值的私有方法
    def __getrandom(self ,max_value):
        return int(math.ceil((math.ceil(random.random() * 10)) / (10 / max_value)))

    def __generateland(self, new_map, change_height, change_frequency, generate_soil, new_terrain_height):
        for i in range(self.__map_width):
            terrain_change = self.__getrandom(change_frequency)
            if terrain_change == 1:
                new_terrain_height += self.__getrandom(change_height)
            elif terrain_change == 2:
                new_terrain_height -= self.__getrandom(change_height)

            for j in range(new_terrain_height):
                new_map[self.__map_height - 1 - j][i] = 1

            if generate_soil:
                soil_height = self.__getrandom(3)
                for j in range(soil_height):
                    new_map[self.__map_height - new_terrain_height - j - 1][i] = 2

                new_map[self.__map_height - new_terrain_height - soil_height - 1][i] = 3

        return new_map, new_terrain_height

    def __generatehardstone(self,new_map):
        for i in range(self.__map_width):
            for j in range(5):
                if self.__getrandom(j + 1) == 1:
                    new_map[self.__map_height - j - 1][i] = 4

        return new_map

    # 地形生成的私有方法
    def __terraingenerator(self, new_terrain_height, terrain_type):
        self.new_terrain_height = new_terrain_height
        new_map = [[0 for i in range(self.__map_width)] for i in range(self.__map_height)]

        if new_terrain_height < self.sea_level:
            terrain_type = 3

        if self.sea_level <= new_terrain_height < self.sand_level:
            terrain_type = 4

        elif self.__getrandom(6) == 1:
            terrain_type = self.__getrandom(2)

        # 平原
        if terrain_type == 1:
            new_map, new_terrain_height = self.__generateland(new_map, 1, 10, True, new_terrain_height)

        # 山脉
        if terrain_type == 2:
            new_map, new_terrain_height = self.__generateland(new_map, 3, 3, False, new_terrain_height)

        # 海
        if terrain_type == 3:
            change_height = 1
            change_frequency = 5

            for i in range(self.__map_width):
                terrain_change = self.__getrandom(change_frequency)
                if terrain_change == 1:
                    new_terrain_height += self.__getrandom(change_height)
                elif terrain_change == 2:
                    new_terrain_height -= self.__getrandom(change_height)

                for j in range(new_terrain_height):
                    new_map[self.__map_height - 1 - j][i] = 1

                for j in range(3):
                    new_map[self.__map_height - new_terrain_height - j - 1][i] = 5

                for j in range(self.__map_height - new_terrain_height - self.__map_height + self.sea_level - 3):
                    new_map[self.__map_height - new_terrain_height - j - 4][i] = 6

        # 海滩
        if terrain_type == 4:
            change_height = 1
            change_frequency = 6

            for i in range(self.__map_width):
                terrain_change = self.__getrandom(change_frequency)
                if terrain_change == 1:
                    new_terrain_height += self.__getrandom(change_height)
                elif terrain_change == 2:
                    new_terrain_height -= self.__getrandom(change_height)

                for j in range(new_terrain_height):
                    new_map[self.__map_height - 1 - j][i] = 1

                for j in range(3):
                    new_map[self.__map_height - new_terrain_height - j - 1][i] = 5

        new_map = self.__generatehardstone(new_map)

        return new_terrain_height, new_map, terrain_type

    # 第一次地形生成的方法
    def firstterraingenerator(self):
        self.__terrain_height, self.map, self.terrain_type = self.__terraingenerator(self.__terrain_height, self.terrain_type)
        self.terrain_type_list.append(self.terrain_type)

    # 完整地形生成的方法
    def wholeterraingenerator(self, number):
        for i in range(number):
            self.__terrain_height, temp_map, self.terrain_type = self.__terraingenerator(self.__terrain_height , self.terrain_type)
            self.terrain_type_list.append(self.terrain_type)

            for j in range(self.__map_height):
                self.map[j] = self.map[j] + temp_map[j]

    # 设置随机种子的方法
    def setseed(self, seed):
        self.seed = seed
        random.seed(self.seed)

def terrainpygameprinter(map, number, x):
    pygame.init()
    screen = pygame.display.set_mode((20 * number * x, 512 * x))
    pygame.display.set_caption("Terrain Generator")

    colour_map = {
        0 : (50,233,233), # 空气
        1 : (192,192,192), # 石头
        2 : (48,5,52), # 泥土
        3 : (0,255,0), # 草
        4 : (0,0,0), # 坚硬石
        5 : (240,240,128), # 沙子
        6 : (0,128,255) # 水
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for i in range(len(map)):
            for j in range(len(map[i])):
                pygame.draw.rect(screen, colour_map[map[i][j]], (j * x, i * x, x, x))

        for i in range(len(terrain.terrain_type_list)):
            if terrain.terrain_type_list[i] == 1:
                pygame.draw.rect(screen,(0,255,0),((0 + i * 20,0),(20,20)))
            elif terrain.terrain_type_list[i] == 2:
                pygame.draw.rect(screen, (192,192,192), ((0 + i * 20,0),(20,20)))
            elif terrain.terrain_type_list[i] == 3:
                pygame.draw.rect(screen, (0,128,255), ((0 + i * 20,0),(20,20)))
            elif terrain.terrain_type_list[i] == 4:
                pygame.draw.rect(screen, (240,240,128), ((0 + i * 20,0),(20,20)))

        for i in range(number - 1):
            pygame.draw.rect(screen, (255, 255, 255), ((0 + (i + 1) * 20, 0), (1, 512)))

        pygame.display.update()

# 测试类
class TerminalMapPrinter:
    def __init__(self):
        self.__PRINT_WIDTH = 20
        self.__PRINT_HEIGHT = 20

        self.__color_map = {
            0 : "\033[48;5;12m", # 空气
            1 : "\033[48;2;192;192;192m", # 石头
            2 : "\033[48;5;52m", # 泥土
            3 : "\033[48;5;118m", # 草
            4 : "\033[48;2;128;128;16m", # 树木
            5 : "\033[48;2;64;192;32m" # 树叶
        }

    # 打印整个地图的方法
    def printwholemap(self):
        for i in range(256):
            for j in range(20):
                print(self.__color_map[terrain.map[i][j]] + "  \033[0m", end="")
            print()

class InputBox:
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32) , size = 50) -> None:
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('black')  # 未被选中的颜色
        self.color_active = pygame.Color('white')  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = "" # 输入的内容
        self.done = False
        self.font = pygame.font.Font(None, size)

    def dealevent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.boxBody.collidepoint(event.pos):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:  # 键盘输入响应
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        txtsurface = self.font.render(self.text, True, self.color)  # 文字转换为图片
        width = max(200, txtsurface.get_width()+10)  # 当文字过长时，延长文本框
        self.boxBody.w = width
        screen.blit(txtsurface, (self.boxBody.x+5, self.boxBody.y+5))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)

    def gettext(self):
        return self.text

terrain = TerrainGenerator()
printer = TerminalMapPrinter()
# printer.printWholeMap()

stone_block = pygame.image.load(r"./Images/Stone.png")
stone_block = pygame.transform.scale(stone_block, (80, 80))
soil_block = pygame.image.load(r"./Images/Soil.png")
soil_block = pygame.transform.scale(soil_block, (80, 80))
grass_block = pygame.image.load(r"./Images/GrassBlock.png")
grass_block = pygame.transform.scale(grass_block, (80, 80))

class Game:
    def __init__(self):
        self.__PRINT_WIDTH = 15
        self.__PRINT_HEIGHT = 10
        self.__BLOCK_SIZE = 80

        self.__SCREEN_WIDTH = self.__PRINT_WIDTH * self.__BLOCK_SIZE
        self.__SCREEN_HEIGHT = self.__PRINT_HEIGHT * self.__BLOCK_SIZE

        self.x = 5
        self.y = len(terrain.map) - 1

        self.offset_x = 0
        self.offset_y = 0

        pygame.init()

        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.screen = pygame.display.set_mode((self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))
        pygame.display.set_caption("FreeWorld Pygame")

        self.icon_surface = pygame.image.load(r"./Images/GameLogo.png")
        pygame.display.set_icon(self.icon_surface)

        self.screen_picture_map = {
            1: stone_block,  # 石头
            2: soil_block,  # 泥土
            3: grass_block  # 草
        }

        self.key_list = []

    def set_location(self):
        while terrain.map[self.y][self.x] != 0:
            self.y -= 1

    def run(self):
        self.set_location()
        # 主游戏循环
        while True:
            self.screen.fill((50,233,233))
            if self.x > len(terrain.map[0]) - 10:
                terrain.wholeterraingenerator(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            key_list = pygame.key.get_pressed()
            if key_list[pygame.K_a]:
                self.offset_x -= 0.1
            if key_list[pygame.K_d]:
                self.offset_x += 0.1
            if key_list[pygame.K_w]:
                self.offset_y -= 0.1
            if key_list[pygame.K_s]:
                self.offset_y += 0.1

            if int(self.offset_x) == 1 or int(self.offset_x) == -1:
                self.x += int(self.offset_x)
                self.offset_x = 0

            if int(self.offset_y) == 1 or int(self.offset_y) == -1:
                self.y += int(self.offset_y)
                self.offset_y = 0

            start_x = self.x - int(self.__PRINT_WIDTH / 2) - 2
            start_y = self.y - int(self.__PRINT_HEIGHT / 2) - 2

            for i in range(self.__PRINT_HEIGHT + 4):
                for j in range(self.__PRINT_WIDTH + 4):
                    # pygame.draw.rect(screen, screen_color_map[terrain.map[START_Y + i][START_X + j]], (j * BLOCK_SIZE - offset_x * BLOCK_SIZE, i * BLOCK_SIZE - offset_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    if terrain.map[start_y + i][start_x + j] in self.screen_picture_map:
                        self.screen.blit(self.screen_picture_map[terrain.map[start_y + i][start_x + j]], (j * self.__BLOCK_SIZE - self.offset_x * self.__BLOCK_SIZE, i * self.__BLOCK_SIZE - self.offset_y * self.__BLOCK_SIZE))

            pygame.time.Clock().tick(60)
            pygame.display.update()

class CreateSurface:
    def __init__(self):
        self.__SCREEN_WIDTH = 1200
        self.__SCREEN_HEIGHT = 800

        pygame.init()

        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.screen = pygame.display.set_mode((self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))
        pygame.display.set_caption("FreeWorld Pygame")

        self.icon_surface = pygame.image.load(r"./Images/GameLogo.png")
        pygame.display.set_icon(self.icon_surface)

        self.seed = 0

        self.title_font = pygame.font.SysFont("SimHei",110)
        self.title_text = self.title_font.render("FreeWorld 游戏设置", True, (255, 255, 255))
        self.seed_font = pygame.font.SysFont("SimHei", 60)
        self.seed_text = self.seed_font.render("种子：", True, (255, 255, 255))
        self.begin_font = pygame.font.SysFont("SimHei", 50)
        self.begin_text = self.begin_font.render("完成设置", True, (0,0,0))

        self.button_down = pygame.image.load(r"./Images/ButtonOff.png")
        self.button_down = pygame.transform.scale(self.button_down, (360, 72))
        self.button_down = pygame.transform.flip(self.button_down, True, False)
        self.button_up = pygame.image.load(r"./Images/ButtonOn.png")
        self.button_up = pygame.transform.scale(self.button_up, (360, 72))
        self.button_up = pygame.transform.flip(self.button_up, True, False)

        self.begin_rect = pygame.Rect(100, 660, 320 * 1.2, 60 * 1.2)
        self.seed_input_box = InputBox(pygame.Rect(280, 274, 300, 50) ,50)

        # 感谢黄羿杰提供的“毛玻璃特效”，但是因为速度问题，没有实装
        # self.rect_surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
        # self.rect_surface_rect = self.rect_surface.get_rect(center=self.screen.get_rect().center)
        # self.screen.blit(self.rect_surface, self.rect_surface_rect)
        #
        # self.blur_surface = pygame.transform.gaussian_blur(self.screen, 15).convert_alpha()
        # self.mask_surface = pygame.Surface(self.blur_surface.get_size(), pygame.SRCALPHA)
        #
        # pygame.draw.rect(self.rect_surface, (255, 255, 255, int(255 * 0.05)), self.rect_surface.get_rect(),
        #                  border_radius=6)
        # pygame.draw.rect(self.mask_surface, (255) * 3, self.rect_surface_rect, border_radius=6)
        # self.blur_surface.blit(self.mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        # self.screen.blit(self.blur_surface, (0, 0))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.begin_rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_begin()

                self.seed_input_box.dealevent(event)

            self.screen.fill((255,255,255))

            for i in range(self.__SCREEN_HEIGHT // 80):
                for j in range(self.__SCREEN_WIDTH // 80):
                    if i == 0:
                        self.screen.blit(grass_block, (j * 80, i * 80))
                    elif 2 >= i > 0:
                        self.screen.blit(soil_block, (j * 80, i * 80))
                    elif i > 2:
                        self.screen.blit(stone_block, (j * 80, i * 80))

            self.screen.blit(self.title_text, (100, 100))
            self.screen.blit(self.seed_text, (100, 270))

            if self.begin_rect.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.button_down, (100, 660))
            else:
                self.screen.blit(self.button_up, (100, 660))

            self.screen.blit(self.begin_text, (168, 672))
            self.seed_input_box.draw(self.screen)

            pygame.time.Clock().tick(60)
            pygame.display.update()

    def game_begin(self):
        if self.seed_input_box.gettext() != "":
            self.seed = int(self.seed_input_box.gettext())

        terrain.setseed(self.seed)
        terrain.firstterraingenerator()
        terrain.wholeterraingenerator(5)

        game = Game()
        game.run()

class BeginGame:
    def __init__(self):
        pygame.init()

        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("FreeWorld Pygame")

        self.icon_surface = pygame.image.load(r"./Images/GameLogo.png")
        self.background_surface = pygame.transform.scale(self.icon_surface, (635,600))
        pygame.display.set_icon(self.icon_surface)

        self.title_font = pygame.font.SysFont("SimHei",145)
        self.title_text = self.title_font.render("FreeWorld", True, (0, 0, 0))

        self.button_font = pygame.font.SysFont("SimHei", 45)
        self.button_text = self.button_font.render("即刻开始", True, (0, 0, 0))

        self.button_down = pygame.image.load(r"./Images/ButtonOff.png")
        self.button_down = pygame.transform.scale(self.button_down, (320 * 1.2, 60 * 1.2))
        self.button_down = pygame.transform.flip(self.button_down, True, False)
        self.button_up = pygame.image.load(r"./Images/ButtonOn.png")
        self.button_up = pygame.transform.scale(self.button_up, (320 * 1.2, 60 * 1.2))
        self.button_up = pygame.transform.flip(self.button_up, True, False)

        self.begin_rect = pygame.Rect(208, 350, 320 * 1.2, 60 * 1.2)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.begin_rect.collidepoint(pygame.mouse.get_pos()):
                        create_surface = CreateSurface()
                        create_surface.run()

                        pygame.quit()

            self.screen.fill((255,255,255))

            self.screen.blit(self.background_surface, (82,0))
            self.screen.blit(self.title_text, (70,120))

            if self.begin_rect.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.button_down, (208, 350))
            else:
                self.screen.blit(self.button_up, (208, 350))

            self.screen.blit(self.button_text, (300, 365))

            pygame.display.update()

if __name__ == '__main__':
    begin_game = BeginGame()
    begin_game.run()
