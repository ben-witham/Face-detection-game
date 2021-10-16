import random
import arcade
import cv2
import mediapipe as mp

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50
PLAYER_SPEED = 10
MOVEMENT_BUFFER_X = 25
MOVEMENT_BUFFER_Y = 10

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Set up face detection library and the webcam
mp_face_detection = mp.solutions.face_detection
video = cv2.VideoCapture(0)

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    last_face_pos = None
    current_face_pos = None

    def get_last_face_pos(self):
        """ A getter for the last_face_pos var"""
        return self.last_face_pos

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "The Amazing Game")

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.timer = 0 

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0

        #Timer
        self.timer = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite("character.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("coin_01.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)
        
        # Sets up the initial face positions
        ret, image = video.read()
        self.last_face_pos = self.find_face(image, self.get_last_face_pos())

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"

        # Calculate and output seconds
        minutes = int(self.timer) // 60
        seconds = float(self.timer) % 60
        rounded_seconds = round(seconds, 1)
        timer_out = f"Time: {minutes} minutes {rounded_seconds} seconds"

        # Prints the text on the window
        arcade.draw_text(timer_out,10, 40, arcade.color.WHITE, 14)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)

        self.coin_list.update()

        ret, image = video.read()
        self.current_screen = image
        self.current_face_pos = self.find_face(self.current_screen, self.get_last_face_pos())

        self.player_movement()


        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
        
    def on_update(self, delta_time: float):
        """ Updates the timer"""
        self.timer += delta_time

    def player_movement(self):
        """Moves the player based on the players face"""

        #Gets direction of movement from the player's face
        dx = self.get_dx()
        dy = self.get_dy()

        #Moves the player
        self.player_sprite.center_x += dx
        self.player_sprite.center_y += dy

        # Bounds control for X axis
        if self.player_sprite.center_x > SCREEN_WIDTH:
            self.player_sprite.center_x = SCREEN_WIDTH
        elif self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0
        
        #Bounds Control for Y axis
        if self.player_sprite.center_y > SCREEN_HEIGHT:
            self.player_sprite.center_y = SCREEN_HEIGHT
        elif self.player_sprite.center_y < 0:
            self.player_sprite.center_y = 0



    def get_dx(self):
        """The player's head movement is measured against the game start position and then the dx is calculated on whether enough movement is made"""
        last_center = (self.last_face_pos.relative_bounding_box.xmin + (self.last_face_pos.relative_bounding_box.width/2)) * SCREEN_WIDTH
        current_center = (self.current_face_pos.relative_bounding_box.xmin + (self.current_face_pos.relative_bounding_box.width/2)) * SCREEN_WIDTH

        #Buffers are made so the movement is not too jerky
        high_buffer = last_center + MOVEMENT_BUFFER_X
        low_buffer = last_center - MOVEMENT_BUFFER_X

        #Finds direction needed for the x axis
        if current_center > high_buffer:
            return PLAYER_SPEED
        elif current_center < low_buffer:
            return -PLAYER_SPEED
        else:
            return 0

    def get_dy(self):
        """PLayers head movement is measured an dy is calculated from it"""
        last_center = (1-self.last_face_pos.relative_bounding_box.ymin + (self.last_face_pos.relative_bounding_box.width/2)) * SCREEN_HEIGHT
        current_center = (1-self.current_face_pos.relative_bounding_box.ymin + (self.current_face_pos.relative_bounding_box.width/2)) * SCREEN_HEIGHT

        #Buffer to decrease jerky movement, buffers are different because it is harder to move your head in the y axis
        high_buffer = last_center + MOVEMENT_BUFFER_Y
        low_buffer = last_center - MOVEMENT_BUFFER_Y

        #Returns correct direction for y axis
        if current_center > high_buffer:
            return PLAYER_SPEED
        elif current_center < low_buffer:
            return -PLAYER_SPEED
        else:
            return 0

    def find_face(self, frame, last_face_pos):
        """Finds face in the provided frame"""

        # Using mediapipe
        with mp_face_detection.FaceDetection(model_selection = 0, 
            min_detection_confidence = 0.5) as face_detection:

            #Preprocessing
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)

            #Face detection
            results = face_detection.process(frame)
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # if face is detected, return that face, otherwise use starting face area
            if results.detections:
                for detection in results.detections:
                    return detection.location_data
            else:
                return last_face_pos


def main():
    """ Main method """

    window = MyGame()
    window.setup()
    arcade.run()



if __name__ == "__main__":
    main()