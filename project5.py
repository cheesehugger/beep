from columns import GameField, GameOverError, Jewel
import pygame


"""
Game music from https://freemusicarchive.org/genre/Chiptune
Title: Lose your head
Artist: Eggy Toast
"""


COLORS = {
    "S": (110, 5, 170),  # Purple
    "T": (210, 0, 0),  # Red
    "V": (230, 0, 210),  # Pink
    "W": (220, 110, 0),  # Orange
    "X": (225, 215, 0),  # Yellow
    "Y": (50, 20, 215),  # Blue
    "Z": (45, 175, 15)  # Green
}

DARKER_COLORS = {
    "S": (55, 0, 90),  # Purple
    "T": (110, 0, 0),  # Red
    "V": (130, 0, 120),  # Pink
    "W": (150, 70, 0),  # Orange
    "X": (130, 125, 0),  # Yellow
    "Y": (30, 10, 110),  # Blue
    "Z": (25, 110, 10)  # Green
}


class ColumnsGame:
    def __init__(self):
        self._field = GameField()
        self._clock = pygame.time.Clock()
        self._field.set_rows(13)
        self._field.set_columns(6)
        self._field.create_empty_game_field()
        self._running = True
        self._music_playing = True


    def run(self) -> None:
        """Run the game"""
        pygame.init()

        self._change_display_size((600, 700))
        
        try:
            self._play_music()

            ticks = 0
            while self._running:
                self._redraw()
                self._clock.tick(30)
                self._events()

                ticks += 1
                if ticks == 30:  # Only apply gravity once per second
                    self._do_game_tick()
                    ticks = 0

        except GameOverError:
            self._redraw()
            while self._running:
                self._events()

        finally:
            pygame.mixer.music.stop()
            pygame.quit()


    def _events(self) -> None:
        """Get user's input and take action accordingly"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self._running = False

            elif event.type == pygame.VIDEORESIZE:
                self._change_display_size(event.size)

            elif event.type == pygame.KEYDOWN:
                if event.__dict__["unicode"] == " ":
                    self._field.rotate_faller()

                elif event.__dict__["key"] == 1073741904:
                    self._field.move_faller_left()

                elif event.__dict__["key"] == 1073741903:
                    self._field.move_faller_right()

                elif event.__dict__["unicode"] == "m":
                    if self._music_playing:
                        pygame.mixer.music.pause()
                        self._music_playing = False
                    else:
                        pygame.mixer.music.unpause()
                        self._music_playing = True


    def _do_game_tick(self) -> None:
        """Do the actions of a single game tick if applicable"""
        self._field.apply_single_gravity_tick()
        self._field.create_faller()


    def _redraw(self) -> None:
        """Redraw the PyGame window"""
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(45, 45, 45))
        self._draw_field()

        pygame.display.flip()


    def _draw_field(self) -> None:
        """
        Draw the game field in the PyGame window
        """

        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()

        for row, sublist in enumerate(self._field.field()[2:]):
            for column, element in enumerate(sublist):

                left = column * (width / 12) + (width / 4)
                top = row * (height / 14) + (height / 14)

                if element != 0:  # Cell with jewel in it
                    
                    pygame.draw.rect(  # Grey square behind jewel
                        surface, pygame.Color(175, 175, 175),
                        pygame.Rect(left, top, width / 12, height / 14))
        
                    rect = pygame.Rect(  # Jewel square
                        left + (width * (2.5 / 600)), 
                        top + (height * (3 / 700)), 
                        width * .075, 
                        height * .6)

                    color = self._get_jewel_color(element)

                    pygame.draw.rect(surface, color, rect)


                else:  # Cell without jewel in it
                    
                    pygame.draw.rect(  # Grey squares
                        surface, pygame.Color(175, 175, 175),
                        pygame.Rect(left, top, surface.get_width() / 12, surface.get_height() / 14))

                    pygame.draw.rect(  # Smaller black square
                        surface, pygame.Color(0, 0, 0),
                        pygame.Rect(
                            left + (width * (2.5 / 600)), 
                            top + (height * (3 / 700)), 
                            width * .075, 
                            height * .6))


    def _get_jewel_color(self, jewel: Jewel) -> pygame.Color:
        """Given a jewel's letter, return its corresponding PyGame color"""
        if jewel.landed():
            for key in DARKER_COLORS.keys():
                if key == jewel.jewel():
                    return pygame.Color(DARKER_COLORS[key])
        else:
            for key in COLORS.keys():
                if key == jewel.jewel():
                    return pygame.Color(COLORS[key])


    def _change_display_size(self, size: tuple) -> None:
        """Change the display size when window is resized"""
        pygame.display.set_mode(size, pygame.RESIZABLE)
        self._redraw()


    def _play_music(self) -> None:
        """Play the game music with PyGame"""
        try:  # Try to play game music
            pygame.mixer.music.load("src\\game_music.mp3")
            pygame.mixer.music.play(loops=-1)
        except pygame.error:  # Oh well
            pass

        try:
            pygame.mixer.music.load("game_music.mp3")
            pygame.mixer.music.play(loops=-1)
        except pygame.error:
            pass


if __name__ == "__main__":
    ColumnsGame().run()
