import os
import pygame
import random
from pygame import gfxdraw
from keras.models import load_model

def save_image(window):
    img = pygame.image.save(window, filepath + '\\number.jpeg')
    return img

def normalize(img):
    scaled_img = pygame.transform.scale(img, (28, 28))
    scaled_img = pygame.surfarray.array2d(scaled_img)
    scaled_img = scaled_img.reshape(1, 28, 28, 1)
    scaled_img = scaled_img.astype('float32')
    scaled_img /= 16777215
    return scaled_img

def predict_number(model, window):
    img = pygame.image.load(filepath + '\\number.jpeg')
    scaled_img = normalize(img)
    pred = model.predict(scaled_img)
    print(pred.argmax())
    window.fill(BLACK)

def main(window, model, brush):
    run = True
    window.fill(BLACK)
    button = pygame.Rect(0, 0, 100, 50)
    img = None

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    img = save_image(window)
                    predict_number(model, window)

        left_pressed, _, _ = pygame.mouse.get_pressed()
        if left_pressed:
            window.blit(brush, (x-10, y-10))
            pygame.display.update()

if __name__ == '__main__':
    ## Screen Size
    WIN_WIDTH = 200
    WIN_HEIGHT = 200
    RADIUS = 5
    BLACK = pygame.Color( 0 ,  0 ,  0 )
    WHITE = pygame.Color(255, 255, 255)
    GRAY = pygame.Color(30, 30, 30)
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    filepath = os.path.dirname(__file__)
    brush = pygame.image.load(filepath + '\\brush2.png')
    brush = pygame.transform.scale(brush, (20, 20))

    model = load_model(filepath + '\\cnn_mnist_model.h5')

    main(window, model, brush)
