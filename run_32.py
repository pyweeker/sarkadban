#! /usr/bin/env python3
# -*- coding: utf-8 -*-

print("https://github.com/pythonarcade/arcade/blob/development/arcade/examples/sprite_tiled_map.py")
print("https://github.com/pythonarcade/arcade/blob/development/arcade/examples/sprite_tiled_map_with_levels.py")



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
PUSHING_SPEED = 1
ROLLING_SPEED = 1.7

import json


TILE_SPRITE_SCALING = 0.5

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

        # Tilemap Object
        self.tile_map = None


        

        self.mouse_pos = 0, 0

        

        

        
        #self.set_mouse_visible(True)
        self.window.set_mouse_visible(False)

       
        #self.frame_count = 0


        
        
        

      

        

        
        self.topleft_corner = None
        self.startposition_list = None
        self.wall_list = None

        # floor

        self.target_list = None
        self.diamond_zone_list = None


        self.box_list = None
        self.diamond_list = None

        self.troll_list = None

        self.static_box_list = None
        self.static_diamond_list = None
        




        
        
        #self.dont_touch_list = None
        self.player_list = None
        

        
        self.player_sprite = None

        self.player_hit_box_list = None
        self.player_hit_diamond_list = None
        self.player_hit_troll_list = None
        

        self.player_status = None
        

        # Our physics engine
        self.physics_engine_player2walls = None
        self.physics_engine_player2boxes = None
        #physics_engine_player2diamonds = None
        # TROLL ???


        self.engines_box2walls = []
        self.engines_box2boxes = []

        self.engines_troll2walls = []
        self.engines_troll2trolls = []
        self.engines_troll2boxes = []

        self.engines_diamond2walls = []
        self.engines_diamond2boxes = []
        self.engines_diamond2trolls = []


     





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

        
        
        
        self.topleft_corner = arcade.SpriteList()
        self.startposition_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.target_list = arcade.SpriteList()
        self.diamond_zone_list = arcade.SpriteList()

        self.box_list = arcade.SpriteList()
        self.diamond_list = arcade.SpriteList()
        self.troll_list = arcade.SpriteList()

        self.static_box_list = arcade.SpriteList()
        self.static_diamond_list = arcade.SpriteList()
        
        #self.dont_touch_list = None
        self.player_list = arcade.SpriteList()        
        #self.player_sprite = arcade.SpriteList()
        self.player_sprite = arcade.Sprite()

        self.player_hit_box_list = arcade.SpriteList()
        self.player_hit_troll_list = arcade.SpriteList()
        self.player_hit_diamond_list = arcade.SpriteList()

        self.player_status = "waiting"

        startposition_layer_name = 'Startposition_layer'
        topleft_corner_layer_name = "Topleft_corner_layer"


        # Name of the layer in the file that has our platforms/walls
        walls_layer_name = 'Walls_layer'

        floor_layer_name = 'Floor_layer'
        boxes_layer_name = 'Boxes_layer'
        diamonds_layer_name = "Diamonds_layer"

        targets_layer_name = 'Targets_layer'
        diamond_zone_layer_name = 'Diamond_zone_layer'



        trolls_layer_name = 'Trolls_layer'
        
        static_boxes_layer_name = 'Static_boxes_layer'
        static_diamonds_layer_name = 'Static_diamonds_layer'


        #waters_layer_name = "Waters"
        #macadams_layer_name = "ground_mac"
        #paves_layer_name = "ground_pav"
        #stairs_layer_name = "Stairs"


        # Map name
  
        #map_name = f"resources/tmx_maps/easymap1_level_{level}.tmx"
        #map_name = f"resources/maps/level_{level}.tmx"

        # Read in the tiled map
        #tile_map = arcade.tilemap.read_tmx(map_name)

        self.load_level(self.level)


        #map_name = f"resources/maps/level_{level}.json"
        #tile_map = arcade.tilemap.load_tilemap(map_name)
        #tile_map.layer_options = {"Platforms": {"use_spatial_hash": True,"scaling": 2.5,},}




        # Calculate the right edge of the tile_map in pixels
        #self.end_of_map = tile_map.map_size.width * GRID_PIXEL_SIZE
        #self.end_of_map = tile_map.width * GRID_PIXEL_SIZE
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        

        #self.topleft_corner = arcade.tilemap.process_layer(map_object=tile_map,
        #                                              layer_name=topleft_corner_layer_name,
        #                                              scaling=TILE_SCALING,
        #                                              use_spatial_hash=True)




        #self.topleft_corner = tile_map.get_tilemap_layer(topleft_corner_layer_name)
        self.topleft_corner = self.tile_map.get_tilemap_layer(topleft_corner_layer_name)


        

        # -- startposition ------------------------------------------------------------------------------------------------------------------------------------------------
        #self.startposition_list = arcade.tilemap.process_layer(map_object=tile_map,
        #                                              layer_name=startposition_layer_name,
        #                                              scaling=TILE_SCALING,
        #                                              use_spatial_hash=True)


        #self.startposition_list = tile_map.get_tilemap_layer(startposition_layer_name)
        self.startposition_list = self.tile_map.get_tilemap_layer(startposition_layer_name)

        print(f"  ****  type(self.startposition_list) {type(self.startposition_list)} ")
        print(f"  ****  self.startposition_list {self.startposition_list} ")

        print("\n ****----------------------------------  !!! -------------------------------------******* \n")

        #print(type(self.startposition_list.data))

        for data in self.startposition_list.data:
            print(f"\n {data}")

        print("\n ****--------....---------------******* \n")



        print(f"self.tile_map  =>  {self.tile_map} ")
        print(f"dir(self.tile_map)  =>  {dir(self.tile_map)} ")

        print(f"self.tile_map.object_lists  =>  {self.tile_map.object_lists} ")

        print(f"self.tile_map.tiled_map  =>  {self.tile_map.tiled_map} ")


        


        

        #print(self.tile_map.data)


        #print(self.startposition_list.data)

        print(">>>   for layers in self.tile_map.tiled_map.layers   >>>>> \n\n\n ")

        for layer in self.tile_map.tiled_map.layers:
            print(layer)

        

        #print("---> ", self.startposition_list[0]) # TypeError: 'TileLayer' object is not subscriptable

        #print(" X ", self.startposition_list[0].center_x)
        #print(" Y ", self.startposition_list[0].center_y)

        #start_XY = tuple((self.startposition_list[0].center_x,self.startposition_list[0].center_y))

        #start_XY = tuple((666,666))


        #image_source = "resources/images/animated_characters/policeboy_gun_128.png"

        #image_source = "resources/playerpic/user_up.gif"
        image_source = "resources/playerpic/user_up.png"

        static_box_image_source = "resources/items/box_static.png"

        
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        #self.player_sprite = SpriteWithHealth(image_source, CHARACTER_SCALING, max_health = PLAYER_MAX_HEALTH)




        #self.player_sprite.center_x = start_XY[0]
        #self.player_sprite.center_y = start_XY[1]
        #
        self.player_list = self.tile_map.get_tilemap_layer(startposition_layer_name)

        for line in self.player_list.data:
            for row in line:
                print(row)
                #print(type(row))
                if row == 2:
                    #row = str(row)

                    #index_row = row.index('2')
                    index_line = self.player_list.data.index(line)

                    #index_row = row.index(index_line)

                    index_row = self.player_list.data[index_line].index(row)

                    #print(f"    index_line {index_line}")
                    print(f" index_row {index_row}    index_line {index_line}")

                    self.player_sprite.center_x = index_row * GRID_PIXEL_SIZE * TILE_SCALING
                    self.player_sprite.center_y = index_line * GRID_PIXEL_SIZE * TILE_SCALING


                    self.player_list = arcade.SpriteList()
                    self.player_list.append(self.player_sprite)



                    print(f"index_line  {index_line}       index_row {index_row} ")
                    print(f"self.player_sprite.center_x  {self.player_sprite.center_x}       self.player_sprite.center_y {self.player_sprite.center_y} ")


                    





        #self.player_list.append(self.player_sprite)

        self.wall_list = self.tile_map.get_tilemap_layer(walls_layer_name)

        self.wall_list = self.tile_map.get_tilemap_layer(walls_layer_name)
        self.floor_list = self.tile_map.get_tilemap_layer(floor_layer_name)
        self.target_list = self.tile_map.get_tilemap_layer(targets_layer_name)
        self.diamond_zone_list = self.tile_map.get_tilemap_layer(diamond_zone_layer_name)
        self.box_list = self.tile_map.get_tilemap_layer(boxes_layer_name)
        self.diamond_list = self.tile_map.get_tilemap_layer(diamonds_layer_name)
        self.troll_list = self.tile_map.get_tilemap_layer(trolls_layer_name)


        # -- Walls

        #f"./resources/maps/level_{level}.json", scaling=TILE_SPRITE_SCALING,layer_options=layer_options
        
        
        level = self.level
        troll_layer = 8
        #map_name = f":resources:maps/level_{level}.json"
        map_name = f"./resources/maps/level_{level}.json"
        with open(map_name, 'r') as f:
            precursor_content = json.load(f)

        data_gruyere = precursor_content['layers'][troll_layer]["data"]
        data_granit = list() #integers corresponding to textures

        for data in data_gruyere:
            if data != 0:
                data_granit.append(data)

        print("!!!!!!!!!!!")


        print(f"self.troll_list   {self.troll_list}")
        print(f"\n tatoo guid desactivated ...")

        #for troll_sprite in self.troll_list:
        #    troll_sprite.guid = data_granit[self.troll_list.index(troll_sprite)]



        #self.static_box_list = arcade.tilemap.process_layer(map_object=tile_map,
        #                                              layer_name=static_boxes_layer_name,
        #                                              scaling=TILE_SCALING,
        #                                              use_spatial_hash=True)

        #self.static_diamond_list = arcade.tilemap.process_layer(map_object=tile_map,
        #                                              layer_name=static_diamonds_layer_name,
        #                                              scaling=TILE_SCALING,
        #                                              use_spatial_hash=True)


        self.static_box_list = self.tile_map.get_tilemap_layer(static_boxes_layer_name)
        self.static_diamond_list = self.tile_map.get_tilemap_layer(static_diamonds_layer_name)



        # Create the 'physics engine'
        #self.physics_engine_player2walls = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        #self.tile_map.sprite_lists[]
        self.physics_engine_player2walls = arcade.PhysicsEngineSimple(self.player_sprite, self.tile_map.sprite_lists[walls_layer_name])

        

        #self.physics_engine_player2boxes = arcade.PhysicsEngineSimple(self.player_sprite, self.box_list)

        


        #self.engines_box2walls = [arcade.PhysicsEngineSimple(box_sprite, self.wall_list) for box_sprite in self.box_list]
        #self.engines_box2walls = [arcade.PhysicsEngineSimple(box_sprite, self.tile_map.sprite_lists[walls_layer_name]) for box_sprite in self.box_list]
        self.engines_box2walls = [arcade.PhysicsEngineSimple(box_sprite, self.tile_map.sprite_lists[walls_layer_name]) for box_sprite in self.tile_map.sprite_lists[boxes_layer_name]]




        #self.engines_box2boxes = [arcade.PhysicsEngineSimple(box_sprite, self.box_list) for box_sprite in self.box_list]
        self.engines_box2boxes = [arcade.PhysicsEngineSimple(box_sprite, self.tile_map.sprite_lists[boxes_layer_name]) for box_sprite in self.tile_map.sprite_lists[boxes_layer_name]]


        #self.engines_box2trolls = [arcade.PhysicsEngineSimple(box_sprite, self.troll_list) for box_sprite in self.box_list]


        #self.engines_troll2walls = [arcade.PhysicsEngineSimple(troll_sprite, self.wall_list) for troll_sprite in self.troll_list]
        self.engines_troll2walls = [arcade.PhysicsEngineSimple(troll_sprite, self.tile_map.sprite_lists[walls_layer_name]) for troll_sprite in self.tile_map.sprite_lists[trolls_layer_name]]

        #self.engines_troll2trolls = [arcade.PhysicsEngineSimple(troll_sprite, self.troll_list) for troll_sprite in self.troll_list]
        self.engines_troll2trolls = [arcade.PhysicsEngineSimple(troll_sprite, self.tile_map.sprite_lists[trolls_layer_name]) for troll_sprite in self.tile_map.sprite_lists[trolls_layer_name]]

        #self.engines_troll2boxes = [arcade.PhysicsEngineSimple(troll_sprite, self.box_list) for troll_sprite in self.troll_list]
        self.engines_troll2boxes = [arcade.PhysicsEngineSimple(troll_sprite, self.tile_map.sprite_lists[boxes_layer_name]) for troll_sprite in self.tile_map.sprite_lists[trolls_layer_name]]


        #self.engines_diamond2walls = [arcade.PhysicsEngineSimple(diamond_sprite, self.wall_list) for diamond_sprite in self.diamond_list]
        #self.engines_diamond2boxes = [arcade.PhysicsEngineSimple(diamond_sprite, self.troll_list) for diamond_sprite in self.diamond_list]
        #self.engines_diamond2trolls = [arcade.PhysicsEngineSimple(diamond_sprite, self.box_list) for diamond_sprite in self.diamond_list]



    def load_level(self, level):
        
        #layer_options = {"Platforms": {"use_spatial_hash": True}}
        layer_options = {"Walls_layer": {"use_spatial_hash": True}}

        # Read in the tiled map
        #self.tile_map = arcade.load_tilemap(
        #    f":resources:tiled_maps/level_{level}.json", scaling=TILE_SPRITE_SCALING
        #)

        self.tile_map = arcade.load_tilemap(
            #f"resources/maps/level_{level}.json", scaling=TILE_SPRITE_SCALING
            #f"resources/maps/level_{level}.json", scaling=TILE_SPRITE_SCALING,layer_options=layer_options
            f"./resources/maps/level_{level}.json", scaling=TILE_SPRITE_SCALING,layer_options=layer_options
        )


        #level_1.json

        # --- Walls ---

        # Calculate the right edge of the tile_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)




    def on_show(self):

        #self.player_music_ingame = arcade.play_sound(self.datamusic)
        pass


    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color

        arcade.start_render()

        # Draw our sprites

        #self.startposition_list.draw()        ??

        #self.topleft_corner.draw()

        
        #self.wall_list.draw()

        #self.target_list.draw()
        #self.diamond_zone_list.draw()
        

        #self.floor_list.draw()

        #self.box_list.draw()
        #self.diamond_list.draw()
        #self.troll_list.draw()

        
        #self.static_box_list.draw()
        #self.static_diamond_list.draw()

        #self.water_list.draw()

        

        for sp_lst in self.tile_map.sprite_lists:
            #sp_lst.update()
            #print("drawing -> ",sp_lst)
            self.tile_map.sprite_lists[sp_lst].draw()
            #print("ok")

        self.player_list.draw()



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

            static_diamond_image_source = "resources/items/diamond_static.png"



            #self.tile_map.sprite_lists[boxes_layer_name]




            #for box in self.box_list: # TypeError: 'TileLayer' object is not iterable          
            for box in self.tile_map.sprite_lists["Boxes_layer"]:

                #hit_box2target_list = arcade.check_for_collision_with_list(box, self.target_list)
                hit_box2target_list = arcade.check_for_collision_with_list(box, self.tile_map.sprite_lists["Targets_layer"])

                if hit_box2target_list != []:

                    #nearest_target = sorted(hit_box2target_list, key=lambda target: student.age)


                    new_static_box = arcade.Sprite(static_box_image_source, CHARACTER_SCALING)
                    new_static_box.center_x = hit_box2target_list[0].center_x
                    new_static_box.center_y = hit_box2target_list[0].center_y

                    box.remove_from_sprite_lists()
                    hit_box2target_list[0].remove_from_sprite_lists()

                    #self.static_box_list.append(new_static_box)
                    self.tile_map.sprite_lists["Static_boxes_layer"].append(new_static_box)


            #for diamond in self.diamond_list:
            for diamond in self.tile_map.sprite_lists["Diamonds_layer"]:

                #hit_diamond2diamond_zone_list = arcade.check_for_collision_with_list(diamond,self.diamond_zone_list)
                hit_diamond2diamond_zone_list = arcade.check_for_collision_with_list(diamond,self.tile_map.sprite_lists["Diamond_zone_layer"])

                if hit_diamond2diamond_zone_list != []:



                    new_static_diamond = arcade.Sprite(static_diamond_image_source, CHARACTER_SCALING)
                    new_static_diamond.center_x = hit_diamond2diamond_zone_list[0].center_x
                    new_static_diamond.center_y = hit_diamond2diamond_zone_list[0].center_y

                    diamond.remove_from_sprite_lists()
                    hit_diamond2diamond_zone_list[0].remove_from_sprite_lists()

                    #self.static_diamond_list.append(new_static_diamond)
                    self.tile_map.sprite_lists["Static_diamonds_layer"].append(new_static_diamond)

        

        if key == arcade.key.NUM_0: # SAVE IT

            level = self.level

            map_name = f":resources:maps/level_{level}.json"

            with open(map_name, 'r') as f:
                

                precursor_content = json.load(f)


            modiflist = precursor_content['layers'][1]["data"]

            print(f"____ old modiflist is {modiflist}  and his len is {len(modiflist)}")
            value = 1

            topleftX = self.topleft_corner[0].center_x
            topleftY = self.topleft_corner[0].center_y

            grid_width = precursor_content['layers'][1]["width"]
            grid_height = precursor_content['layers'][1]["height"]

            renderorder = precursor_content['renderorder']
            orientation = precursor_content['orientation']

            #-----------------------------------------------------------------------

            playerX=self.player_sprite.center_x
            playerY=self.player_sprite.center_y

            column = (playerX - topleftX) / (GRID_PIXEL_SIZE * TILE_SCALING)
            row = (topleftY - playerY) / (GRID_PIXEL_SIZE * TILE_SCALING)

            round_column = round(column)
            round_row = round(row)

            new_index = round_column + (round_row * grid_width)
            new_index = int(new_index)



            modiflist = [0 for i in range(grid_width * grid_height)] 


            modiflist[new_index] = value

            print(f"  \n\n\n====================================================================================================================== ")
            print(f"  renderorder {renderorder}      orientation {orientation}      topleftX corner {topleftX}             topleftY corner {topleftY}                  ")
            print(f"  playerX {playerX}      playerY {playerY}               ")
            print(f"  column {column}      round_column {round_column}          row {row}             round_row {round_row}        ")
            print(f"  new_index {new_index} ")
            print(f"  modiflist {modiflist} ")
            print(f"  \n\n\n====================================================================================================================== ")


            precursor_content['layers'][1]["data"] = modiflist

            #-------------------------------------------------------------------

            modifbox = [0 for i in range(grid_width * grid_height)]
            value_box = 7
            box_layer_index = 6

            for box in self.box_list:
                box_X = box.center_x 
                box_Y = box.center_y

                column = (box_X - topleftX) / (GRID_PIXEL_SIZE * TILE_SCALING)
                row = (topleftY - box_Y) / (GRID_PIXEL_SIZE * TILE_SCALING)

                round_column = round(column)
                round_row = round(row)

                new_index = round_column + (round_row * grid_width)
                new_index = int(new_index)

                
                
                modifbox[new_index] = value_box


            precursor_content['layers'][box_layer_index]["data"] = modifbox

            #-------------------------------------------------------------------

            modifboxstatic = [0 for i in range(grid_width * grid_height)]
            value_box = 12
            box_layer_index = 9

            for box in self.static_box_list:
                box_X = box.center_x 
                box_Y = box.center_y

                column = (box_X - topleftX) / (GRID_PIXEL_SIZE * TILE_SCALING)
                row = (topleftY - box_Y) / (GRID_PIXEL_SIZE * TILE_SCALING)

                round_column = round(column)
                round_row = round(row)

                new_index = round_column + (round_row * grid_width)
                new_index = int(new_index)

                
                
                modifboxstatic[new_index] = value_box


            precursor_content['layers'][box_layer_index]["data"] = modifboxstatic

            #---------------------------------------------------------------------

            modif_trolls = [0 for i in range(grid_width * grid_height)]
            troll_layer_index = 8

            for troll in self.troll_list:
                troll_X = troll.center_x 
                troll_Y = troll.center_y

                column = (troll_X - topleftX) / (GRID_PIXEL_SIZE * TILE_SCALING)
                row = (topleftY - troll_Y) / (GRID_PIXEL_SIZE * TILE_SCALING)

                round_column = round(column)
                round_row = round(row)

                new_index = round_column + (round_row * grid_width)
                new_index = int(new_index)

                modif_trolls[new_index] = troll.guid


            precursor_content['layers'][troll_layer_index]["data"] = modif_trolls





            

            with open(map_name, 'w') as modified_file:
                
                modified_file.write(json.dumps(precursor_content))




        if key == arcade.key.ENTER: # LOADING

            level = self.level

            map_name = f"resources/maps/level_{level}.json"


            with open(map_name, 'r') as f:
                

                json_content = json.load(f)

                print("\n ===========================================>>>>>>>>>>>>>>>>>>>>>>>><")

                print(json_content)

                for layer in json_content['layers']:
                    print("\n\n\n")
                    print(layer["name"])
                    print(layer["data"])


                print("\n =====================>>>>>>>>>>>>>>>>><")

                print(json_content['layers'][5]["data"])


        #if self.player_hit_box_list != [] or self.player_hit_troll_list != []:
        if self.player_hit_box_list != [] or self.player_hit_troll_list != [] or self.player_hit_diamond_list != []:

        

            if key == arcade.key.UP:
                
                for box in self.player_hit_box_list:
                    if box.center_y < self.player_sprite.center_y + 128 and box.center_y < self.player_sprite.center_y + 150:
                        box.change_y = ROLLING_SPEED

                for troll in self.player_hit_troll_list:
                    if troll.center_y < self.player_sprite.center_y + 128 and troll.center_y < self.player_sprite.center_y + 150:
                        troll.change_y = ROLLING_SPEED

                for diamond in self.player_hit_diamond_list:
                    if diamond.center_y < self.player_sprite.center_y + 128 and diamond.center_y < self.player_sprite.center_y + 150:
                        diamond.change_y = ROLLING_SPEED
                        

                self.player_sprite.change_y = PUSHING_SPEED

                
                

            elif key == arcade.key.DOWN:
                for box in self.player_hit_box_list:                    
                    if box.center_y < self.player_sprite.center_y + 128: #and box.center_y < self.player_sprite.center_y + 150:
                        box.change_y = -ROLLING_SPEED

                for troll in self.player_hit_troll_list:                    
                    if troll.center_y < self.player_sprite.center_y + 128: #and box.center_y < self.player_sprite.center_y + 150:
                        troll.change_y = -ROLLING_SPEED

                for diamond in self.player_hit_diamond_list:                    
                    if diamond.center_y < self.player_sprite.center_y + 128: #and box.center_y < self.player_sprite.center_y + 150:
                        diamond.change_y = -ROLLING_SPEED

                self.player_sprite.change_y = -PUSHING_SPEED
                

            elif key == arcade.key.LEFT:
                for box in self.player_hit_box_list:                    
                    if self.player_sprite.center_x < box.center_x + 128 and self.player_sprite.center_x < box.center_x + 150:
                        box.change_x = -ROLLING_SPEED

                for troll in self.player_hit_troll_list:                    
                    if self.player_sprite.center_x < troll.center_x + 128 and self.player_sprite.center_x < troll.center_x + 150:
                        troll.change_x = -ROLLING_SPEED

                for diamond in self.player_hit_diamond_list:                    
                    if self.player_sprite.center_x < diamond.center_x + 128 and self.player_sprite.center_x < diamond.center_x + 150:
                        diamond.change_x = -ROLLING_SPEED

                self.player_sprite.change_x = -PUSHING_SPEED
                

            elif key == arcade.key.RIGHT:
                for box in self.player_hit_box_list:
                    if box.center_x < self.player_sprite.center_x + 128 and box.center_x < self.player_sprite.center_x + 150:
                        box.change_x = ROLLING_SPEED

                for troll in self.player_hit_troll_list:
                    if troll.center_x < self.player_sprite.center_x + 128 and troll.center_x < self.player_sprite.center_x + 150:
                        troll.change_x = ROLLING_SPEED

                for diamond in self.player_hit_diamond_list:
                    if diamond.center_x < self.player_sprite.center_x + 128 and diamond.center_x < self.player_sprite.center_x + 150:
                        diamond.change_x = ROLLING_SPEED

                self.player_sprite.change_x = PUSHING_SPEED
                



            

        else:
            # => key release
            #for box in self.box_list:
            #    box.change_x = 0
            #    box.change_y = 0 

            #for troll in self.troll_list:
            #    troll.change_x = 0
            #    troll.change_y = 0

            #for diamond in self.diamond_list:
            #    diamond.change_x = 0
            #    diamond.change_y = 0

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
        #self.tile_map.sprite_lists[boxes_layer_name]

        #for box in self.box_list:
        for box in self.tile_map.sprite_lists["Boxes_layer"]:            

            box.change_x = 0
            box.change_y = 0

        for troll in self.tile_map.sprite_lists["Trolls_layer"]:
        #for troll in self.troll_list:            

            troll.change_x = 0
            troll.change_y = 0


        for diamond in self.tile_map.sprite_lists["Diamonds_layer"]:
        #for diamond in self.diamond_list:            

            diamond.change_x = 0
            diamond.change_y = 0



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
        print(dir(self.player_list))

        #self.box_list.update()  # AttributeError: 'TileLayer' object has no attribute 'update'

        #self.tile_map.sprite_lists[boxes_layer_name].update()  # NameError: name 'boxes_layer_name' is not defined
        #self.tile_map.sprite_lists["Boxes_layer"].update() # OK

        for sp_lst in self.tile_map.sprite_lists:
            #sp_lst.update()
            print("updating -> ",sp_lst)
            self.tile_map.sprite_lists[sp_lst].update()
            print("ok")




        #self.diamond_list.update()

        #self.troll_list.update()

        #self.target_list.update()
        #self.diamond_zone_list.update()


        self.physics_engine_player2walls.update()

        #self.physics_engine_player2boxes.update()

        #self.physics_engine_player2diamonds.update()

        #-----------------------------------------------------------


        

        for engine in self.engines_box2walls:
            engine.update()


        for engine in self.engines_box2boxes:
            engine.update()

        #-----------------------------------------------------------



        for engine in self.engines_troll2walls:
            engine.update()

        for engine in self.engines_troll2trolls:
            engine.update()

        for engine in self.engines_troll2boxes:
            engine.update()

        #-----------------------------------------------------------
        for engine in self.engines_diamond2walls:
            engine.update()

        

        for engine in self.engines_diamond2boxes:
            engine.update()

        for engine in self.engines_diamond2trolls:
            engine.update()

        #------------------------------------------------------------------------


        #self.player_hit_box_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                      self.box_list)


        #self.player_hit_troll_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                      self.troll_list)


        #self.player_hit_diamond_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                      self.diamond_list)



        self.player_hit_box_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.tile_map.sprite_lists["Boxes_layer"])


        self.player_hit_troll_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.tile_map.sprite_lists["Trolls_layer"])


        self.player_hit_diamond_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.tile_map.sprite_lists["Diamonds_layer"])


        #--------------------------------------------------------------------------

        if self.player_sprite.right >= self.end_of_map:
            if self.level < self.max_level:
                self.level += 1
                self.load_level(self.level)
                self.player_sprite.center_x = 128
                self.player_sprite.center_y = 64
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
            else:
                self.game_over = True




        



        # Generate a list of all sprites that collided with the player.
        #stairs_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                      self.stairs_list)



        #for box in self.box_list:
            

            # Check this bullet to see if it hit a coin
        #    hit_list = arcade.check_for_collision_with_list(box, self.target_list)
        #    print(f"$$   {hit_list}")







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
    


