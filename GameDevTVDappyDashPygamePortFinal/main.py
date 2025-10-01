
# by Marlon Solleske, September 2025, inspired by GameDevTv's Raylib C++ course


import pygame
import random

class Nebula:
    def __init__(self,image_frame_list,position,speed):
        self.image_frame_list = image_frame_list
        self.frame_index = 0
        self.frame_speed = 24
        self.image = self.image_frame_list[self.frame_index]
        self.position = pygame.Vector2(*position)
        self.speed = speed
        self.active = True
        self.direction = pygame.Vector2(-1,0)


        self.collision_rect_width = 50
        self.collision_rect_height = 50
        self.collision_rect = pygame.Rect(self.position.x + self.image.get_width()/2,
                                          self.position.y + self.image.get_height()/2,
                                          self.collision_rect_width,
                                          self.collision_rect_height)

    def update(self,delta_time):

        self.frame_index += self.frame_speed * delta_time
        if(int(self.frame_index) > len(self.image_frame_list)-1):
            self.frame_index = 0

        self.image = self.image_frame_list[int(self.frame_index)]

        self.position.x += self.direction.x * self.speed * delta_time
        if self.position.x + self.image.get_width() < 0:
            self.active = False

        self.collision_rect.x = self.position.x + self.image.get_width()/2 - self.collision_rect_width/2
        self.collision_rect.y = self.position.y + self.image.get_height()/2 - self.collision_rect_height/2

    def draw(self,screen_surf):
        screen_surf.blit(self.image,(self.position.x,self.position.y))
        


    

class Background:
    def __init__(self,front,middle,back,front_speed,direction):
        self.direction = pygame.Vector2(*direction)
        window_width,window_height = pygame.display.get_window_size()
        front = pygame.transform.scale(front,(window_width,window_height))
        self.front_layer = front
        self.front_layer_2 = self.front_layer.copy()
        self.front_speed = front_speed

        middle = pygame.transform.scale(middle,(window_width,window_height))
        self.middle_layer = middle
        self.middle_layer_2 = self.middle_layer.copy()
        self.middle_speed = self.front_speed * 0.5

        back = pygame.transform.scale(back,(window_width,window_height))
        self.back_layer = back
        self.back_layer_2 = self.back_layer.copy()
        self.back_speed = self.front_speed * 0.25

        self.front_pos_1 = pygame.Vector2(0,0)
        self.front_pos_2 = pygame.Vector2(self.front_layer.get_width(),0)

        self.middle_pos_1 = pygame.Vector2(0,0)
        self.middle_pos_2 = pygame.Vector2(self.middle_layer.get_width(),0)

        self.back_pos_1 = pygame.Vector2(0,0)
        self.back_pos_2 = pygame.Vector2(self.back_layer.get_width(),0)


    def update(self,delta_time):
        self.front_pos_1.x += self.direction.x * self.front_speed * delta_time
        self.front_pos_2.x += self.direction.x * self.front_speed * delta_time
        if self.front_pos_1.x < -self.front_layer.get_width():
            self.front_pos_1.x = 0
            self.front_pos_2.x = self.front_layer.get_width()

        self.middle_pos_1.x += self.direction.x * self.middle_speed * delta_time
        self.middle_pos_2.x += self.direction.x * self.middle_speed * delta_time
        if self.middle_pos_1.x < - self.middle_layer.get_width():
            self.middle_pos_1.x = 0
            self.middle_pos_2.x = self.middle_layer.get_width()

        self.back_pos_1.x += self.direction.x * self.back_speed * delta_time
        self.back_pos_2.x += self.direction.x * self.back_speed * delta_time
        if self.back_pos_1.x < - self.back_layer.get_width():
            self.back_pos_1.x = 0
            self.back_pos_2.x = self.back_layer.get_width()


    def draw(self,screen_surf):
        screen_surf.blit(self.back_layer,(self.back_pos_1.x,self.back_pos_1.y))
        screen_surf.blit(self.back_layer_2,(self.back_pos_2.x,self.back_pos_2.y))

        screen_surf.blit(self.middle_layer,(self.middle_pos_1.x,self.middle_pos_2.y))
        screen_surf.blit(self.middle_layer_2,(self.middle_pos_2.x,self.middle_pos_2.y))

        screen_surf.blit(self.front_layer,(self.front_pos_1.x,self.front_pos_1.y))
        screen_surf.blit(self.front_layer_2,(self.front_pos_2.x,self.front_pos_2.y))


class Player:
    def __init__(self,anim_frame_list,position):
        self.anim_frame_list = anim_frame_list
        self.position = pygame.Vector2(*position)
        self.y_velocity = 0
        self.jump_velocity = 750
        self.frame_index = 0
        self.frame_speed = 12
        self.image = self.anim_frame_list[self.frame_index]
        self.on_ground = False
        self.key_pressed = False
        self.collision_rect_width = 50
        self.collision_rect_height = 50
        self.collision_rect = pygame.Rect(self.position.x + self.image.get_width()/2 - self.collision_rect_width/2
                                          ,self.position.y + self.image.get_height()/2 - self.collision_rect_height/2
                                          ,self.collision_rect_width,self.collision_rect_height)

        self.jumping = False
       


    def jump(self):
        if self.on_ground and not self.jumping:
            self.y_velocity = -self.jump_velocity
            self.jumping = True

    def cancel_jump(self):
        if self.jumping:
            if self.y_velocity < 0:
                self.y_velocity /= 4

    def update(self,delta_time,gravity_const):
        
        keys_pressed = pygame.key.get_pressed()
        

        self.frame_index += self.frame_speed * delta_time
        if(int(self.frame_index) > len(self.anim_frame_list)-1):
            self.frame_index = 0

        self.image = self.anim_frame_list[int(self.frame_index)]

        self.y_velocity += gravity_const * delta_time
        self.position.y += self.y_velocity * delta_time

        if self.position.y + self.image.get_height() > pygame.display.get_surface().get_height():
            self.y_velocity = 0
            self.position.y = pygame.display.get_surface().get_height() - self.image.get_height()
            self.jumping = False
            self.on_ground = True
            


        self.collision_rect.x = self.position.x + self.image.get_width()/2 - self.collision_rect_width/2
        self.collision_rect.y = self.position.y + self.image.get_height()/2 - self.collision_rect_height/2
            
            

    def draw(self,screen_surf):
        screen_surf.blit(self.image,(self.position.x,self.position.y))
        

class Game:
    BLACK = (0,0,0)
    PURPLE = (200,0,220)

    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    WHITE = (255,255,255)

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.font_40 = pygame.font.Font(None,40) #standard pygame font
        self.font_60 = pygame.font.Font(None,60)

        self.screen_width = 800
        self.screen_height = 380
        self.app_title = "Game Dev TV Dappy Dash"
        self.fps_cap = 60
        self.fps_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption(self.app_title)


        self.scarfy_speed = 300
        self.gravity_const = 1000 #p/s/s
        self.game_state = 0
        self.nebulae_dodged = 0
        self.game_level = 1
        self.dist_to_goal = random.randint(self.scarfy_speed * 10,self.scarfy_speed * 60)

        self.foreground_image = pygame.image.load("./textures/foreground.png").convert_alpha()
        self.midground_image = pygame.image.load("./textures/back-buildings.png").convert_alpha()
        self.background_image = pygame.image.load("./textures/far-buildings.png").convert_alpha()
        
        self.background_layers = Background(self.foreground_image,self.midground_image,self.background_image,self.scarfy_speed,(-1,1))
        
        # extract the frames from sprite sheet
        self.scarfy_image_strip = pygame.image.load("./textures/scarfy.png").convert_alpha()
        self.scarfy_anim_frames = []
        scarfy_frame_num = 6
        scarfy_frame_width = self.scarfy_image_strip.get_width()/scarfy_frame_num
        scarfy_frame_height = self.scarfy_image_strip.get_height()
        for frame_num in range(scarfy_frame_num):
            self.scarfy_anim_frames.append(self.scarfy_image_strip.subsurface(pygame.Rect(frame_num*scarfy_frame_width,0,scarfy_frame_width,scarfy_frame_height)))

        self.player_scarfy = Player(self.scarfy_anim_frames,(self.screen_width*0.01,self.screen_height/2))



        # extract frames from nebula sprite sheet
        self.nebula_sprite_sheet = pygame.image.load("./textures/12_nebula_spritesheet.png").convert_alpha()
        self.nebula_orig_frames = []
        neb_cols = 8
        neb_rows = 8
        neb_frame_width = self.nebula_sprite_sheet.get_width()/neb_cols
        neb_frame_height = self.nebula_sprite_sheet.get_height()/neb_rows
        for frame_row in range(neb_rows):
            for frame_col in range(neb_cols):
                self.nebula_orig_frames.append(self.nebula_sprite_sheet.subsurface(pygame.Rect(frame_col*neb_frame_width,frame_row*neb_frame_height,neb_frame_width,neb_frame_height)))

                if frame_row == 7 and frame_col == 4:
                    break
            if frame_row == 7 and frame_col == 4:
                break


        self.red_tint_neb_frames = self.create_tinted_frames(self.nebula_orig_frames,self.RED)
        self.green_tint_neb_frames = self.create_tinted_frames(self.nebula_orig_frames,self.GREEN)
        self.blue_tint_neb_frames = self.create_tinted_frames(self.nebula_orig_frames,self.BLUE)

        self.neb_color_dict = {
            1 : self.nebula_orig_frames,
            2 : self.red_tint_neb_frames,
            3 : self.green_tint_neb_frames,
            4 : self.blue_tint_neb_frames
        }
        


        self.nebula_list = []
        self.spawn_nebulas(2)

    def check_player_nebula_collision(self):
        for neb in self.nebula_list:
            if neb.collision_rect.colliderect(self.player_scarfy.collision_rect):
                self.game_state = 1

    def display_score(self):
        score_str = f"Nebulae dodged: {self.nebulae_dodged}"
        score_str_surf = self.font_40.render(score_str,False,self.WHITE)
        self.screen.blit(score_str_surf,(10,10))

    def display_goal_dist(self):
        goal_dist_str = f"Goal distance: {round(self.dist_to_goal)}"
        goal_dist_surf = self.font_40.render(goal_dist_str,False,self.WHITE)
        self.screen.blit(goal_dist_surf,(self.screen_width - 300,10))


    def display_current_level(self):
        level_str = f"Level: {self.game_level}"
        level_surf = self.font_40.render(level_str,False,self.WHITE)
        self.screen.blit(level_surf,(self.screen_width/2 - level_surf.get_width()/2,10))

    def spawn_nebulas(self,max_neb_num):
        frame_height = self.nebula_sprite_sheet.get_height() / 8
        if len(self.nebula_list) == 0:
            for neb_num in range(max_neb_num):
                rand_col_num = random.randint(1,4)
                rand_x = random.randint(pygame.display.get_window_size()[0],pygame.display.get_window_size()[0] * 2)
                rand_y = random.randint(0,pygame.display.get_window_size()[1] - int(frame_height))
                rand_speed = random.randint(150,500)
                self.nebula_list.append(Nebula(self.neb_color_dict[rand_col_num],(rand_x,rand_y),rand_speed))


    def update_all_nebulas(self,delta_time):
        for neb in self.nebula_list:
            neb.update(delta_time)

    def draw_all_nebulas(self,screen_surf):
        for neb in self.nebula_list:
            if neb.position.x < pygame.display.get_window_size()[0]:
                neb.draw(screen_surf)

    
    def remove_inactive_nebulas(self):
        for neb in self.nebula_list:
            if not neb.active:
                self.nebulae_dodged += 1
                self.nebula_list.remove(neb)
                
        

    def create_tinted_frames(self,frame_list,tint_color):
        tinted_frames = []
        for orig_frame in frame_list:
            # print(orig_frame)
            bottom = orig_frame.copy().convert_alpha()
            top = orig_frame.copy()
            for pixel_y in range(top.get_height()):
                for pixel_x in range(top.get_width()):
                    pixel_color = top.get_at((pixel_x,pixel_y))
                    tinted_color = (
                        pixel_color[0] * tint_color[0] // 255,
                        pixel_color[1] * tint_color[1] // 255,
                        pixel_color[2] * tint_color[2] // 255
                    )
                    top.set_at((pixel_x,pixel_y),tinted_color)
            
            top.set_colorkey((0,0,0))
            top.set_alpha(128)
            bottom.blit(top,(0,0))
            tinted_frames.append(bottom)
        return tinted_frames

    def update(self,delta_time):
        self.background_layers.update(delta_time)
        self.player_scarfy.update(delta_time,self.gravity_const)


        self.update_all_nebulas(delta_time)

        self.remove_inactive_nebulas()
        self.spawn_nebulas(2)


        self.check_player_nebula_collision()


        self.dist_to_goal -= self.scarfy_speed * delta_time

        if self.dist_to_goal <= 0:
            self.game_state = 2


    def draw(self):
        self.background_layers.draw(self.screen)

        if self.dist_to_goal < self.screen_width:
            pygame.draw.line(self.screen,self.GREEN,(self.dist_to_goal,0),(self.dist_to_goal,self.screen_height),width=3)

        self.display_score()
        self.display_current_level()
        self.display_goal_dist()

        self.player_scarfy.draw(self.screen)

        self.draw_all_nebulas(self.screen)


    def reset(self):
        self.nebulae_dodged = 0
        self.nebula_list.clear()
        self.game_state = 0
        self.game_level = 1

    def proceed_to_next(self):
        self.nebula_list.clear()
        self.game_state = 0
        self.game_level += 1
        self.dist_to_goal = random.randint(self.scarfy_speed * 10,self.scarfy_speed * 60)


    def game_over_screen(self,running):
        self.screen.fill(self.RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()

        
        game_level_str = f"Level Done: {self.game_level}"
        game_level_surf = self.font_60.render(game_level_str,True,self.WHITE)
        self.screen.blit(game_level_surf,(self.screen_width/2 - game_level_surf.get_width()/2,self.screen_height/2 - game_level_surf.get_height()/2 - 100))

        nebulae_dodged_str = f"Nebulae Dodged: {self.nebulae_dodged}"
        nebulae_dodged_surf = self.font_60.render(nebulae_dodged_str,True,self.WHITE)
        self.screen.blit(nebulae_dodged_surf,(self.screen_width/2 - nebulae_dodged_surf.get_width()/2,self.screen_height/2 - nebulae_dodged_surf.get_height()/2 - 50))


        game_over_str = "Game Over"
        game_over_str_surf = self.font_60.render(game_over_str,True,self.WHITE)
        self.screen.blit(game_over_str_surf,(self.screen_width/2 - game_over_str_surf.get_width()/2,self.screen_height/2 - game_over_str_surf.get_height()/2))

        prompt_str = "Hit SPACE to restart!"
        prompt_str_surf = self.font_60.render(prompt_str,True,self.WHITE)
        self.screen.blit(prompt_str_surf,(self.screen_width/2 - prompt_str_surf.get_width()/2,self.screen_height/2 - prompt_str_surf.get_height()/2 + 50))

        return running
    

    def goal_reached_screen(self,running):
        self.screen.fill(self.GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.proceed_to_next()

        next_level_str = f"Great! You made it to level {self.game_level + 1}!"
        next_level_surf = self.font_60.render(next_level_str,True,self.WHITE)
        self.screen.blit(next_level_surf,(self.screen_width/2 - next_level_surf.get_width()/2,self.screen_height/2 - next_level_surf.get_height()/2))

        prompt_str = "Hit the SPACE key to continue!"
        prompt_surf = self.font_60.render(prompt_str,True,self.WHITE)
        self.screen.blit(prompt_surf,(self.screen_width/2 - prompt_surf.get_width()/2,self.screen_height/2 - prompt_surf.get_height()/2 + 50))

        return running

    def run(self):

        running = True
        while running:
            
            if self.game_state == 0:
                delta_time = self.fps_clock.tick(self.fps_cap)/1000
                self.screen.fill(self.PURPLE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player_scarfy.jump()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            self.player_scarfy.cancel_jump()

                pygame.display.set_caption(self.app_title + f" {round(self.fps_clock.get_fps(),2)}")
                
                self.update(delta_time)
                self.draw()
            elif self.game_state == 1:
                self.fps_clock.tick(self.fps_cap)
                running = self.game_over_screen(running)

            elif self.game_state == 2:
                self.fps_clock.tick(self.fps_cap)
                running = self.goal_reached_screen(running)

            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()