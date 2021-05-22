import sys
from time import sleep
import pygame

from bullets import Bullet
from alien import Alien



def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):
    "Respond to keypresses and mouse events"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets, sb)

        elif event.type == pygame.KEYUP:
           check_keyup_events(event, ship)

def start_game(ai_settings, screen, stats, aliens, bullets, ship, sb):
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game statistics
    stats.reset_stats()
    stats.game_active = True

    # Empty the list of the aliens and bullets
    aliens.empty()
    bullets.empty()

    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    #Reset game settings
    ai_settings.initialize_dynamic_settings()

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb):
    "Start a new game when the player clicks play"
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, aliens, bullets, ship, sb)



def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets, sb):
    "Respond to keypresses"
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
       fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, aliens, bullets, ship, sb)



def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    "Update position of bullets and get rid of old bullets"
    #update bullet positions
    bullets.update()

    #Get rid of the bullets which have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    "Fire a bullet if limit not reached yet"
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    "Create a full fleet of aliens."
    #Create an alien and find the number of aliens in a row.
    #Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_row = get_number_of_rows(ai_settings, ship.rect.height, alien.rect.height)
    number_of_aliens_x = get_number_of_aliens_x(ai_settings, alien.rect.width)

    #Create the first row of aliens
    for row_number in range(number_row):

        for alien_number in range(number_of_aliens_x):
            # Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_of_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_of_rows(ai_settings, ship_height, alien_height):
    "Determine the number of rows of aliens that fit on the screen."
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_of_rows = int(available_space_y / (2 * alien_height))
    return number_of_rows

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    "Check if the fleet is at an edge and then update the positions of all aliens in the fleet."
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #Look for alien-ship collision.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    #Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_fleet_edges(ai_settings, aliens):
    "Respond appropriately if any aliens have reached an edge."
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    "Drop the entire fleet and change the fleet's direction."
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
    "Respond to bullet-alien collisions"
    #Remove any bullets and aliens that have collected.
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #Destroy existing bullets and create new fleet.
        bullets.empty()
        aliens.empty()
        ai_settings.increase_speed()

        #Increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    "Respond to ship being hit bt alien"
    if stats.ships_left > 1:
        #Decrement ships_left
        stats.ships_left -= 1

        sb.prep_ships()

        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    "Check if any aliens have reached the bottom of the screen."
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat this the same as if the ship got hit
            ship_hit(ai_settings, stats, screen, ship,aliens, bullets, sb)
            break

def check_high_score(stats, sb):
    "Check to see if there's a new high score"
    if stats.score > stats.high_score:
        with open('best_score', 'w') as fo:
            fo.write(str(stats.score))
        stats.high_score = stats.score
        sb.prep_high_score()





def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
    "Update images on the screen and flip to the new screen."
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    ship.blitme()
    aliens.draw(screen)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()


    # Make the most recently drawn screen visible.
    pygame.display.flip()

    # Redraw all bullets behind snip and  aliens


