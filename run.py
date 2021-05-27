#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import arcade
import math


SCREEN_WIDTH = 1800 #1000
SCREEN_HEIGHT = 1000 #650
SCREEN_TITLE = "Sarkadban"

GRID_PIXEL_SIZE = 128
#TILE_SCALING = 1
#CHARACTER_SCALING = 1

TILE_SCALING = 0.5
CHARACTER_SCALING = 0.5

WALKING_SPEED = 3
PUSHING_SPEED = 1.1
ROLLING_SPEED = 1



class GameView(arcade.View):



    

    def __init__(self):
    

        # Call the parent class and set up the window
        #super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        super().__init__()


        #self.datamusic = arcade.load_sound(MUSIC_INGAME)

        #self.datamusic.get_length()

        #self.player_music_ingame = None


        #self.set_exclusive_mouse(True) # capture mouse ; not in view ?

        #self.set_vsync(True)

        #self.camera = Camera2D(
        #    viewport=(0, 0, self.width, self.height),
        #    projection=(0, self.width, 0, self.height),
        #)


        

        self.mouse_pos = 0, 0

        

        

        
        #self.set_mouse_visible(True)
        self.window.set_mouse_visible(False)

       
        #self.frame_count = 0


        self.box_list = None
        self.target_list = None
        self.static_box_list = None

        #self.special_box_1 = None
        #self.special_target_1 = None

        #self.special_box_2 = None
        #self.special_target_2 = None

        self.wall_list = None

        self.startposition_list = None
        




        
        
        #self.dont_touch_list = None
        self.player_list = None
        

        
        self.player_sprite = None

        self.player_hit_box_list = None

        self.player_status = None
        

        # Our physics engine
        self.physics_engine_player2walls = None
        self.physics_engine_player2boxes = None


        self.engines_box2walls = []

        self.engines_box2boxes = []

        #.....................................................
        #self.water_list = None
        

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None
        #----------------------------------------
        

        

        # Keep track of the score
        self.score = 0
        self.lives = 0


        #self.ammo = 0
        #self.ammo_text = None # ????????????????????


        # Load sounds. Sounds from kenney.nl
        #self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        #self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")
        #self.death_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        # Level
        self.level = 1


    



    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        #arcade.schedule(self.krontab, ECLOSION_TIME_INTERVAL)

        self.box_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.static_box_list = arcade.SpriteList()

        #self.special_box_1 = None
        #self.special_target_1 = None

        #self.special_box_2 = None
        #self.special_target_2 = None

        self.wall_list = arcade.SpriteList()
        self.startposition_list = arcade.SpriteList()
        
        #self.dont_touch_list = None
        self.player_list = arcade.SpriteList()        
        self.player_sprite = arcade.SpriteList()

        self.player_hit_box_list = arcade.SpriteList()

        self.player_status = "waiting"

        startposition_layer_name = 'Startposition_layer'


        # Name of the layer in the file that has our platforms/walls
        walls_layer_name = 'Walls_layer'

        floor_layer_name = 'Floor_layer'
        boxes_layer_name = 'Boxes_layer'
        targets_layer_name = 'Targets_layer'
        static_boxes_layer_name = 'Static_boxes_layer'


        #waters_layer_name = "Waters"
        #macadams_layer_name = "ground_mac"
        #paves_layer_name = "ground_pav"
        #stairs_layer_name = "Stairs"


        # Map name
  
        #map_name = f"resources/tmx_maps/easymap1_level_{level}.tmx"
        map_name = f"resources/maps/level_{level}.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        

        # -- startposition ------------------------------------------------------------------------------------------------------------------------------------------------
        self.startposition_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=startposition_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        print("---> ", self.startposition_list[0])
        print(" X ", self.startposition_list[0].center_x)
        print(" Y ", self.startposition_list[0].center_y)

        start_XY = tuple((self.startposition_list[0].center_x,self.startposition_list[0].center_y))


        #image_source = "resources/images/animated_characters/policeboy_gun_128.png"

        #image_source = "resources/playerpic/user_up.gif"
        image_source = "resources/playerpic/user_up.png"

        static_box_image_source = "resources/items/box_static.png"

        
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        #self.player_sprite = SpriteWithHealth(image_source, CHARACTER_SCALING, max_health = PLAYER_MAX_HEALTH)


        self.player_sprite.center_x = start_XY[0]
        self.player_sprite.center_y = start_XY[1]
        self.player_list.append(self.player_sprite)


        # -- Walls
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=walls_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.floor_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=floor_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        
        self.box_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=boxes_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)


        
        self.target_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=targets_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        self.static_box_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=static_boxes_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)



        # Create the 'physics engine'
        self.physics_engine_player2walls = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        self.physics_engine_player2boxes = arcade.PhysicsEngineSimple(self.player_sprite, self.box_list)


        self.engines_box2walls = [arcade.PhysicsEngineSimple(box_sprite, self.wall_list) for box_sprite in self.box_list]
        self.engines_box2boxes = [arcade.PhysicsEngineSimple(box_sprite, self.box_list) for box_sprite in self.box_list]




    def on_show(self):

        #self.player_music_ingame = arcade.play_sound(self.datamusic)
        pass


    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color

        arcade.start_render()

        # Draw our sprites

        #self.startposition_list.draw()        ??
        
        self.wall_list.draw()
        self.floor_list.draw()
        self.box_list.draw()
        self.target_list.draw()
        self.static_box_list.draw()

        #self.water_list.draw()

        self.player_list.draw()


    def try_push(self):
        

        for box in self.player_hit_box_list:
            box.change_x = self.player_sprite.change_x *1.1
            box.change_y = self.player_sprite.change_y *1.1

            #box.change_x = WALKING_SPEED
            #box.change_y = WALKING_SPEED


    @property
    #def distance_player(self, target_sprite):
    def distance_player(self): #target will be player in this game , property instead of attribute for fresh values

        #dist = math.hypot(self.center_x - target_sprite.center_x, self.center_y - target_sprite.center_y)
        dist = math.hypot(self.player_sprite.center_x - target_sprite.center_x, self.player_sprite.center_y - target_sprite.center_y)

        return dist






    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        #self.player_hit_box_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                      self.box_list)


        if key == arcade.key.ESCAPE:
                raise Exception("\n\n      See You soon, fork it share it !")

        if key == arcade.key.SPACE:
            static_box_image_source = "resources/items/box_static.png"

            
            
            for box in self.box_list:

                hit_box2target_list = arcade.check_for_collision_with_list(box,
                                                              self.target_list)

                if hit_box2target_list != []:

                    #nearest_target = sorted(hit_box2target_list, key=lambda target: student.age)


                    new_static_box = arcade.Sprite(static_box_image_source, CHARACTER_SCALING)
                    new_static_box.center_x = hit_box2target_list[0].center_x
                    new_static_box.center_y = hit_box2target_list[0].center_y

                    box.remove_from_sprite_lists()
                    hit_box2target_list[0].remove_from_sprite_lists()

                    self.static_box_list.append(new_static_box)
                




        if self.player_hit_box_list != []:

        

            if key == arcade.key.UP:
                
                for box in self.player_hit_box_list:
                    if box.center_y < self.player_sprite.center_y + 128 and box.center_y < self.player_sprite.center_y + 150:
                        box.change_y = ROLLING_SPEED
                        #if self.distance_player(box) < 200:
                        #    box.change_y = ROLLING_SPEED

                self.player_sprite.change_y = PUSHING_SPEED

                
                

            elif key == arcade.key.DOWN:
                for box in self.player_hit_box_list:
                    #if box.center_y <= self.player_sprite.center_y + 128:
                    #if box.center_y <= self.player_sprite.center_y - 128 and box.center_y > self.player_sprite.center_y - 150:
                    if box.center_y + 127 < self.player_sprite.center_y: #and box.center_y < self.player_sprite.center_y + 150:
                        box.change_y = -ROLLING_SPEED

                self.player_sprite.change_y = -PUSHING_SPEED
                

            elif key == arcade.key.LEFT:
                for box in self.player_hit_box_list:
                    #if box.center_x + 127 < self.player_sprite.center_x:
                    if self.player_sprite.center_x < box.center_x + 128 and self.player_sprite.center_x < box.center_x + 150:
                        box.change_x = -ROLLING_SPEED

                self.player_sprite.change_x = -PUSHING_SPEED
                

            elif key == arcade.key.RIGHT:
                for box in self.player_hit_box_list:
                    if box.center_x < self.player_sprite.center_x + 128 and box.center_x < self.player_sprite.center_x + 150:
                        box.change_x = ROLLING_SPEED

                self.player_sprite.change_x = PUSHING_SPEED
                



            

        else:
            
            for box in self.box_list:
                box.change_x = 0
                box.change_y = 0 

            if key == arcade.key.UP:
                self.player_sprite.change_y = WALKING_SPEED
                #self.crosshair_sprite.change_y = WALKING_SPEED

            

            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -WALKING_SPEED
                #self.crosshair_sprite.change_y = -WALKING_SPEED
                

            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -WALKING_SPEED
                #self.crosshair_sprite.change_x = -WALKING_SPEED
                

            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = WALKING_SPEED
                #self.crosshair_sprite.change_x = WALKING_SPEED
                



            #elif key == arcade.key.ESCAPE:
            #    raise Exception("\n\n      See You soon, fork it share it !")




    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        self.player_status = "waiting"


        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


        #for box in self.player_hit_box_list:
        for box in self.box_list:
            #box.change_x = self.player_sprite.change_x
            #box.change_y = self.player_sprite.change_y

            box.change_x = 0
            box.change_y = 0

    def ProcessInput(self, direction):
        
        if direction == 0 and self.player[0] > 0:
            push1 = (self.player[0]-1, self.player[1])
            push2 = (self.player[0]-2, self.player[1])
        elif direction == 1 and self.player[0] < (self.map_size[0]-1):
            push1 = (self.player[0]+1, self.player[1])
            push2 = (self.player[0]+2, self.player[1])
        elif direction == 2 and self.player[1] > 0:
            push1 = (self.player[0], self.player[1]-1)
            push2 = (self.player[0], self.player[1]-2)
        elif direction == 3 and self.player[1] < (self.map_size[1]-1):
            push1 = (self.player[0], self.player[1]+1)
            push2 = (self.player[0], self.player[1]+2)
        else:
            return
        #-------------------------------------------------------------------------------------------------------------
        
        if self.Occ[push1[0]][push1[1]]:
            return
        elif self.furniture[push1[0]][push1[1]] >= 0:
            if push2[0] < 0 or push2[1] < 0 or push2[0] >= self.map_size[0] or push2[1] >= self.map_size[1]:
                return
            elif self.Occ[push2[0]][push2[1]] or self.furniture[push2[0]][push2[1]] >= 0:
                return
            else:
                self.player = (push1[0],push1[1])
                furntype = self.furniture[push1[0]][push1[1]]
                self.furniture[push1[0]][push1[1]] = -1
                if self.furniture_goals[push2[0]][push2[1]] == 1:
                    self.furniture[push2[0]][push2[1]] = furntype
                    self.furniture_goals[push2[0]][push2[1]] = 2
                    self.Occ[push2[0]][push2[1]] = True
                    self.goalsleft = self.goalsleft - 1
                else:
                    self.furniture[push2[0]][push2[1]] = furntype
        else:
            self.player = (push1[0],push1[1])


    def update(self, delta_time):
    
        """ Movement and game logic """
        #self.frame_count += 1
        self.player_list.update()

        self.box_list.update()
        self.target_list.update()


        self.physics_engine_player2walls.update()

        #self.physics_engine_player2boxes.update()


        

        for engine in self.engines_box2walls:
            engine.update()


        for engine in self.engines_box2boxes:
            engine.update()


        self.player_hit_box_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.box_list)



        



        # Generate a list of all sprites that collided with the player.
        #stairs_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                      self.stairs_list)



        for box in self.box_list:
            

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(box, self.target_list)
            print(f"$$   {hit_list}")







class InstructionView(arcade.View):

    def __init__(self):
        
        super().__init__()
        
        #self.music_intro = arcade.load_sound(MUSIC_INTRO)

        #self.looping_music = True



        #print("type(self.music_intro)   : ", type(self.music_intro))


        #self.player_music_intro = None


        # ////
        #self.stars = make_star_field(150)
        #self.skyline1 = make_skyline(SCREEN_WIDTH * 5, 250, (80, 80, 80))
        #self.skyline2 = make_skyline(SCREEN_WIDTH * 5, 150, (50, 50, 50))

        pass




    
    
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        
        

        #self.player_music_intro.EOS_LOOP = 'loop'
        #self.player_music_intro = arcade.play_sound(self.music_intro)
        

        #print("type(self.player_music_intro)   : ", type(self.player_music_intro))


    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


        #start_time = int(round(time.time() * 1000))
        arcade.start_render()

        #self.stars.draw()
        #self.skyline1.draw()
        #self.skyline2.draw()
        #end_time = int(round(time.time() * 1000))
        #total_time = end_time - start_time

        arcade.draw_text(f"Intro page", -150 + SCREEN_WIDTH//2, 200 + SCREEN_HEIGHT//2, arcade.color.RED, font_size = 40)

        #if self.music_intro.is_complete(self.player_music_intro) is True:
        #    self.player_music_intro = arcade.play_sound(self.music_intro)


        arcade.draw_text(f"Click Left laser , click Right Grenade, arrows to move", 100, 10, arcade.color.YELLOW, font_size = 10)




    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup(level=1)
        arcade.set_background_color(arcade.csscolor.BLACK)


        #try:
        #    self.music_intro.stop(self.player_music_intro)
        #except ValueError:
        #    print("music already finished")  # ValueError: list.remove(x): x not in list   media.Source._players.remove(player)

        self.window.show_view(game_view)


    def on_update(self, delta_time):
        """ Movement and game logic """
        #self.skyline1.center_x -= 0.5
        #self.skyline2.center_x -= 1

        pass








def main():

#window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)

    

    #start_view = GameView()
    #window.show_view(start_view)
    
    #start_view.setup()
    #start_view.setup(level=1)

    start_view = InstructionView()
    window.show_view(start_view)

    
    arcade.run()


if __name__ == "__main__":
    main()
    


