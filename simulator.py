import pygame
import requests
import queue
from io import BytesIO
from PIL import Image

def run_matrix_simulator(song_queue):
    pygame.init()
    SCALE = 8
    # Fenêtre carrée 64x64 sans espace pour la barre
    screen = pygame.display.set_mode((64 * SCALE, 64 * SCALE))
    clock = pygame.time.Clock()
    
    current_surface = None
    
    running = True
    while running:
        try:
            # On récupère les messages sans attendre
            msg = song_queue.get_nowait()
            if isinstance(msg, tuple):
                if msg[0] == "DOWNLOAD":
                    track = msg[1]
                    url = track.get_cover_image()
                    if url:
                        try:
                            response = requests.get(url, timeout=10)
                            if "image" in response.headers.get("Content-Type", ""):
                                img = Image.open(BytesIO(response.content)).convert("RGB").resize((64, 64))
                                img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
                                current_surface = pygame.transform.scale(img_surface, (64 * SCALE, 64 * SCALE))
                        except Exception as e:
                            print(f"DEBUG: Erreur image : {e}")
                elif msg[0] == "CLEAR":
                    current_surface = None
        except queue.Empty:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Nettoyage et affichage simple
        screen.fill((0, 0, 0))
        if current_surface:
            screen.blit(current_surface, (0, 0))
        
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()