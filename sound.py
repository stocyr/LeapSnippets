import pygame, time

pygame.mixer.pre_init(44100,-16,2, 128)
pygame.mixer.init()
pygame.init()

#pygame.mixer.music.load('click_down2.ogg')
#pygame.mixer.music.play(1, 1)

sound = pygame.mixer.Sound('click_down2.ogg')
sound.play()

time.sleep(1)