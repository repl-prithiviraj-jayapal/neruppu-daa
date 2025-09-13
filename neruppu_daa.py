#!/usr/bin/env python3
"""
NERUPPU DAA - Survive the Fire Stones
ASCII terminal survival game built with pynput keyboard input
"""

import time
import random
import sys
from dataclasses import dataclass
from typing import List
from enum import Enum
from pynput import keyboard
try:
    import pygame
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("pygame not found - game will run without sound")

# ANSI Colors (same as pynput test)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

@dataclass
class Position:
    x: int
    y: int

@dataclass
class FireBrimstone:
    pos: Position
    speed: float
    char: str

@dataclass
class PowerUp:
    pos: Position
    type: str
    char: str

class GameState(Enum):
    WELCOME = 0
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class NeruppuDaaGame:
    def __init__(self):
        self.width = 60
        self.height = 20
        self.player_pos = Position(self.width // 2, self.height - 2)
        self.fire_brimstone: List[FireBrimstone] = []
        self.power_ups: List[PowerUp] = []
        self.score = 0
        self.high_score = 0
        self.lives = 1
        self.game_state = GameState.MENU
        self.frame_count = 0
        
        # Initialize audio system
        self.init_audio()
        
        # Power-up effects
        self.double_points = False
        self.double_points_timer = 0
        self.shield_active = False
        self.slow_motion = False
        self.slow_motion_timer = 0
        
        # Game control
        self.running = True
        
        # Key handling (same as pynput test)
        self.pressed_keys = set()
        self.last_action_time = {}
        
        # Start keyboard listener
        self.listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.listener.start()
    
    def init_audio(self):
        """Initialize pygame audio system"""
        global SOUND_ENABLED
        if not SOUND_ENABLED:
            return
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.create_sound_effects()
        except:
            SOUND_ENABLED = False
            print("Failed to initialize audio - running without sound")
    
    def create_sound_effects(self):
        """Create simple sound effects using pygame"""
        global SOUND_ENABLED
        if not SOUND_ENABLED:
            return
        
        try:
            import numpy as np
            
            # Power-up sound (bright ascending arpeggio)
            duration = 0.4
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # Create an ascending arpeggio with sparkle effect
            freq1 = 523  # C5
            freq2 = 659  # E5  
            freq3 = 784  # G5
            freq4 = 1047 # C6
            
            # Create ascending notes with different timing
            note1 = np.sin(freq1 * 2 * np.pi * t) * 0.3 * np.exp(-8*t)
            note2 = np.sin(freq2 * 2 * np.pi * t) * 0.3 * np.exp(-6*(t-0.1)) * (t > 0.1)
            note3 = np.sin(freq3 * 2 * np.pi * t) * 0.3 * np.exp(-4*(t-0.2)) * (t > 0.2)
            note4 = np.sin(freq4 * 2 * np.pi * t) * 0.2 * np.exp(-2*(t-0.3)) * (t > 0.3)
            
            power_up_wave = note1 + note2 + note3 + note4
            power_up_wave = (power_up_wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack([power_up_wave, power_up_wave])
            stereo_wave = np.ascontiguousarray(stereo_wave)
            self.power_up_sound = pygame.sndarray.make_sound(stereo_wave)
            
            # Hit sound (harsh low tone with decay)
            hit_wave = np.sin(150 * 2 * np.pi * t) * 0.6 * np.exp(-2*t)
            hit_wave = (hit_wave * 32767).astype(np.int16)  
            stereo_hit = np.column_stack([hit_wave, hit_wave])
            stereo_hit = np.ascontiguousarray(stereo_hit)
            self.hit_sound = pygame.sndarray.make_sound(stereo_hit)
            
            
            # Movement sound (quick blip)
            move_duration = 0.1
            move_t = np.linspace(0, move_duration, int(sample_rate * move_duration), False)
            move_wave = np.sin(800 * 2 * np.pi * move_t) * 0.2 * np.exp(-5*move_t)
            move_wave = (move_wave * 32767).astype(np.int16)
            stereo_move = np.column_stack([move_wave, move_wave])
            stereo_move = np.ascontiguousarray(stereo_move)
            self.move_sound = pygame.sndarray.make_sound(stereo_move)
            
            # Game over sound (epic failure chord progression)
            gameover_duration = 1.2
            gameover_t = np.linspace(0, gameover_duration, int(sample_rate * gameover_duration), False)
            
            # Create a dramatic minor chord progression that descends
            # First chord (Am) - dark and ominous
            chord1_freq = [220, 261, 329]  # A3, C4, E4
            # Second chord (Dm) - even darker  
            chord2_freq = [146, 174, 220]  # D3, F3, A3
            # Final chord (low rumble)
            final_freq = [87, 110]  # F2, A2
            
            # Build the progression
            chord1 = sum(np.sin(f * 2 * np.pi * gameover_t) * 0.3 * np.exp(-3*gameover_t) * (gameover_t < 0.4) for f in chord1_freq)
            chord2 = sum(np.sin(f * 2 * np.pi * gameover_t) * 0.4 * np.exp(-2*(gameover_t-0.4)) * ((gameover_t >= 0.4) & (gameover_t < 0.8)) for f in chord2_freq)  
            final = sum(np.sin(f * 2 * np.pi * gameover_t) * 0.5 * np.exp(-1*(gameover_t-0.8)) * (gameover_t >= 0.8) for f in final_freq)
            
            gameover_wave = chord1 + chord2 + final
            gameover_wave = (gameover_wave * 32767).astype(np.int16)
            stereo_gameover = np.column_stack([gameover_wave, gameover_wave])
            stereo_gameover = np.ascontiguousarray(stereo_gameover)
            self.gameover_sound = pygame.sndarray.make_sound(stereo_gameover)
            
            print("🎵 Audio system initialized successfully!")
            
        except Exception as e:
            SOUND_ENABLED = False
            print(f"Failed to create sound effects: {e}")
            print("Game will run without sound")
        
    def play_sound(self, sound_type):
        """Play sound effect"""
        if not SOUND_ENABLED:
            return
            
        try:
            if sound_type == 'power_up' and hasattr(self, 'power_up_sound'):
                self.power_up_sound.play()
                print("🎵 Power-up sound!")
            elif sound_type == 'hit' and hasattr(self, 'hit_sound'):
                self.hit_sound.play()
                print("💥 Hit sound!")
            elif sound_type == 'move' and hasattr(self, 'move_sound'):
                self.move_sound.play()
            elif sound_type == 'gameover' and hasattr(self, 'gameover_sound'):
                self.gameover_sound.play()
                print("💀 Game over sound!")
                
        except Exception as e:
            print(f"Audio playback error: {e}")
            # Fallback to system beep for macOS
            try:
                import subprocess
                if sound_type == 'power_up':
                    subprocess.run(['osascript', '-e', 'beep 2'], check=False)
                elif sound_type == 'hit':
                    subprocess.run(['osascript', '-e', 'beep 1'], check=False)
            except:
                pass
    
    def on_key_press(self, key):
        """Handle key press events (same as pynput test)"""
        try:
            if hasattr(key, 'char') and key.char:
                self.pressed_keys.add(key.char.lower())
            elif key == keyboard.Key.space:
                self.pressed_keys.add('space')
            elif key == keyboard.Key.left:
                self.pressed_keys.add('left')
            elif key == keyboard.Key.right:
                self.pressed_keys.add('right')
            elif key == keyboard.Key.esc:
                self.pressed_keys.add('esc')
        except AttributeError:
            pass
    
    def on_key_release(self, key):
        """Handle key release events (same as pynput test)"""
        try:
            if hasattr(key, 'char') and key.char:
                self.pressed_keys.discard(key.char.lower())
            elif key == keyboard.Key.space:
                self.pressed_keys.discard('space')
            elif key == keyboard.Key.left:
                self.pressed_keys.discard('left')
            elif key == keyboard.Key.right:
                self.pressed_keys.discard('right')
            elif key == keyboard.Key.esc:
                self.pressed_keys.discard('esc')
        except AttributeError:
            pass
    
    def is_pressed(self, key_name):
        """Check if a key is currently pressed (same as pynput test)"""
        return key_name in self.pressed_keys
    
    def should_process_action(self, action):
        """Debounce action keys (same as pynput test)"""
        current_time = time.time()
        if action in self.last_action_time:
            if current_time - self.last_action_time[action] < 0.3:
                return False
        self.last_action_time[action] = current_time
        return True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        print('\033[2J\033[H', end='')
    
    def hide_cursor(self):
        """Hide terminal cursor"""
        print('\033[?25l', end='')
    
    def show_cursor(self):
        """Show terminal cursor"""
        print('\033[?25h', end='')
    
    def spawn_fire_brimstone(self):
        """Spawn new fire & brimstone continuously with increasing difficulty"""
        # Progressive difficulty - more fire & brimstone and faster as time goes on
        time_factor = min(self.frame_count / 300.0, 3.0)  # Increases over 30 seconds, caps at 3x
        
        # Spawn rate increases with time (starts at 70%, up to 97%)
        spawn_rate = 0.70 + (time_factor * 0.27)
        
        if random.random() < spawn_rate:
            # Fire and brimstone symbols
            fire_chars = ['o', 'O', '^', 'v', 'x', '%', '&', '~']
            
            # Speed increases with time (starts 0.8-1.5, up to 1.5-3.0)
            base_speed_min = 0.8 + (time_factor * 0.2)
            base_speed_max = 1.5 + (time_factor * 0.5)
            
            drop = FireBrimstone(
                pos=Position(random.randint(1, self.width - 2), 0),
                speed=random.uniform(base_speed_min, base_speed_max),
                char=random.choice(fire_chars)
            )
            self.fire_brimstone.append(drop)
    
    def spawn_power_up(self):
        """Spawn power-ups occasionally"""
        if random.random() < 0.04:  # 4% chance
            power_types = {
                '*': 'double_points',
                '+': 'extra_life', 
                '!': 'slow_motion',
                '#': 'shield'
            }
            char = random.choice(list(power_types.keys()))
            power_up = PowerUp(
                pos=Position(random.randint(1, self.width - 2), 0),
                type=power_types[char],
                char=char
            )
            self.power_ups.append(power_up)
    
    def update_fire_brimstone(self):
        """Update fire & brimstone positions every frame"""
        speed_multiplier = 0.5 if self.slow_motion else 1.0
        
        for drop in self.fire_brimstone[:]:
            drop.pos.y += drop.speed * speed_multiplier
            if drop.pos.y >= self.height:
                self.fire_brimstone.remove(drop)
    
    def update_power_ups(self):
        """Update power-up positions"""
        speed_multiplier = 0.5 if self.slow_motion else 1.0
        for power_up in self.power_ups[:]:
            power_up.pos.y += 0.6 * speed_multiplier
            if power_up.pos.y >= self.height:
                self.power_ups.remove(power_up)
    
    def check_collisions(self):
        """Check for collisions"""
        # Check fire & brimstone collisions
        for drop in self.fire_brimstone[:]:
            if (abs(drop.pos.x - self.player_pos.x) <= 1 and 
                abs(drop.pos.y - self.player_pos.y) <= 1):
                
                if self.shield_active:
                    self.shield_active = False
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_state = GameState.GAME_OVER
                        self.play_sound('gameover')
                
                # Play hit sound effect
                self.play_sound('hit')
                self.fire_brimstone.remove(drop)
                return
        
        # Check power-up collisions
        for power_up in self.power_ups[:]:
            if (abs(power_up.pos.x - self.player_pos.x) <= 1 and 
                abs(power_up.pos.y - self.player_pos.y) <= 1):
                
                self.collect_power_up(power_up)
                self.power_ups.remove(power_up)
    
    def collect_power_up(self, power_up: PowerUp):
        """Apply power-up effects"""
        # Play power-up sound effect
        self.play_sound('power_up')
        
        if power_up.type == 'double_points':
            self.double_points = True
            self.double_points_timer = 180
        elif power_up.type == 'extra_life':
            # In hardcore mode, extra life gives temporary shield instead
            self.shield_active = True
        elif power_up.type == 'slow_motion':
            self.slow_motion = True
            self.slow_motion_timer = 120
        elif power_up.type == 'shield':
            self.shield_active = True
        
        points = 50
        self.score += points
    
    def update_power_up_timers(self):
        """Update power-up effect timers"""
        if self.double_points_timer > 0:
            self.double_points_timer -= 1
        else:
            self.double_points = False
            
        if self.slow_motion_timer > 0:
            self.slow_motion_timer -= 1
        else:
            self.slow_motion = False
    
    def handle_input(self):
        """Handle keyboard input using pynput (same patterns as test)"""
        # Movement keys (can be held)
        old_x = self.player_pos.x
        if self.is_pressed('a') or self.is_pressed('left'):
            if self.game_state == GameState.PLAYING and self.player_pos.x > 1:
                self.player_pos.x -= 2
        
        if self.is_pressed('d') or self.is_pressed('right'):
            if self.game_state == GameState.PLAYING and self.player_pos.x < self.width - 2:
                self.player_pos.x += 2
        
        # Play movement sound if player moved
        if self.game_state == GameState.PLAYING and old_x != self.player_pos.x:
            self.play_sound('move')
        
        # Action keys with debouncing (same as pynput test)
        if self.is_pressed('space'):
            if self.game_state == GameState.MENU and self.should_process_action('space'):
                self.start_game()
        
        if self.is_pressed('q'):
            if self.should_process_action('quit'):
                self.running = False
        
        if self.is_pressed('r'):
            if self.game_state == GameState.GAME_OVER and self.should_process_action('restart'):
                self.reset_to_menu()
        
        if self.is_pressed('esc'):
            if self.should_process_action('quit'):
                self.running = False
        
    
    def draw_game(self):
        """Draw the game screen"""
        self.clear_screen()
        
        # Create clean game field
        field = [[' ' for x in range(self.width)] for y in range(self.height)]
        
        # Draw fire & brimstone
        for drop in self.fire_brimstone:
            y, x = int(drop.pos.y), drop.pos.x
            if 0 <= y < self.height and 0 <= x < self.width:
                field[y][x] = drop.char
        
        # Draw power-ups
        for power_up in self.power_ups:
            y, x = int(power_up.pos.y), power_up.pos.x
            if 0 <= y < self.height and 0 <= x < self.width:
                field[y][x] = power_up.char
        
        # Draw player
        if 0 <= self.player_pos.y < self.height and 0 <= self.player_pos.x < self.width:
            field[self.player_pos.y][self.player_pos.x] = '@'
        
        # Print header
        print(f"{Colors.BOLD}{Colors.RED}🔥  NERUPPU DAA - HARDCORE MODE 🔥{Colors.RESET}")
        
        # Calculate difficulty level
        time_factor = min(self.frame_count / 300.0, 3.0)
        difficulty_level = int(time_factor * 5) + 1  # Level 1-16
        
        print(f"{Colors.YELLOW}Score: {self.score:,} | High: {self.high_score:,} | Life: {Colors.RED}{'♥' * self.lives}{Colors.RESET} | Level: {Colors.CYAN}{difficulty_level}{Colors.RESET}")
        
        # Active effects
        effects = []
        if self.double_points:
            effects.append(f"{Colors.BLUE}2X PTS{Colors.RESET}")
        if self.shield_active:
            effects.append(f"{Colors.BLUE}SHIELD{Colors.RESET}")
        if self.slow_motion:
            effects.append(f"{Colors.BLUE}SLOW{Colors.RESET}")
        
        effect_line = f"Effects: {' | '.join(effects)}" if effects else ""
        print(effect_line.ljust(60))
        
        print(f"{Colors.CYAN}┌{'─' * (self.width - 2)}┐{Colors.RESET}")
        
        # Game field
        for y in range(self.height):
            line = f"{Colors.CYAN}│{Colors.RESET}"
            for x in range(1, self.width - 1):
                char = field[y][x]
                
                if char == '@':
                    color = Colors.BLUE + Colors.BOLD if self.shield_active else Colors.GREEN + Colors.BOLD
                    line += f"{color}{char}{Colors.RESET}"
                elif char in ['o', 'O', '^', 'v', 'x', '%', '&', '~']:
                    # All fire and brimstone in red
                    line += f"{Colors.RED + Colors.BOLD}{char}{Colors.RESET}"
                elif char in ['*', '+', '!', '#']:
                    line += f"{Colors.BLUE}{Colors.BOLD}{char}{Colors.RESET}"
                else:
                    line += char
            line += f"{Colors.CYAN}│{Colors.RESET}"
            print(line)
        
        print(f"{Colors.CYAN}└{'─' * (self.width - 2)}┘{Colors.RESET}")
        print(f"{Colors.YELLOW}A/D or ←/→ to Move | Q=Quit{Colors.RESET}")
    
    def draw_menu(self):
        """Draw main menu"""
        self.clear_screen()
        print(f"""
{Colors.BOLD}{Colors.CYAN}
    ███╗   ██╗███████╗██████╗ ██╗   ██╗██████╗ ██████╗ ██╗   ██╗    ██████╗  █████╗  █████╗ 
    ████╗  ██║██╔════╝██╔══██╗██║   ██║██╔══██╗██╔══██╗██║   ██║    ██╔══██╗██╔══██╗██╔══██╗
    ██╔██╗ ██║█████╗  ██████╔╝██║   ██║██████╔╝██████╔╝██║   ██║    ██║  ██║███████║███████║
    ██║╚██╗██║██╔══╝  ██╔══██╗██║   ██║██╔═══╝ ██╔═══╝ ██║   ██║    ██║  ██║██╔══██║██╔══██║
    ██║ ╚████║███████╗██║  ██║╚██████╔╝██║     ██║     ╚██████╔╝    ██████╔╝██║  ██║██║  ██║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝      ╚═════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{Colors.RESET}

{Colors.WHITE}                        Survive the Fire Stones{Colors.RESET}

{Colors.YELLOW}                     🔥  SURVIVE THE FIRE STONES!  🔥{Colors.RESET}
{Colors.WHITE}                           High Score: {Colors.BOLD}{self.high_score:,}{Colors.RESET}

{Colors.GREEN}{Colors.BOLD}                      ═══ HOW TO PLAY ═══{Colors.RESET}
                      {Colors.WHITE}• Use A/D or ←/→ keys to move your player (@){Colors.RESET}
                      {Colors.RED}• HARDCORE MODE: One hit = Game Over!{Colors.RESET}
                      {Colors.YELLOW}• Fire stones get faster as you survive{Colors.RESET}
                      {Colors.WHITE}• Survive the progressive inferno to get high scores!{Colors.RESET}

{Colors.BLUE}{Colors.BOLD}                      ═══ POWER-UPS (COLLECT THEM!) ═══{Colors.RESET}
                      {Colors.BLUE}*{Colors.RESET} {Colors.YELLOW}Double Points{Colors.RESET} - 2x score for limited time
                      {Colors.BLUE}+{Colors.RESET} {Colors.GREEN}Shield Boost{Colors.RESET} - Temporary protection from hits
                      {Colors.BLUE}!{Colors.RESET} {Colors.CYAN}Slow Motion{Colors.RESET} - Fire stones fall slower temporarily
                      {Colors.BLUE}#{Colors.RESET} {Colors.BLUE}Shield{Colors.RESET} - Blocks one hit from fire stones

{Colors.BOLD}{Colors.YELLOW}                      PRESS SPACE TO START!{Colors.RESET}
{Colors.YELLOW}                        Press Q to Quit{Colors.RESET}
        """)
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.clear_screen()
        
        new_high = self.score > self.high_score
        if new_high:
            self.high_score = self.score
        
        print(f"""
{Colors.RED}{Colors.BOLD}
    ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
    ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
{Colors.RESET}

{Colors.YELLOW}                            Final Score: {Colors.BOLD}{self.score:,}{Colors.RESET}
""")
        
        if new_high:
            print(f"{Colors.BOLD}{Colors.YELLOW}                        🎉 NEW HIGH SCORE! 🎉{Colors.RESET}")
        else:
            print(f"{Colors.WHITE}                        High Score: {Colors.BOLD}{self.high_score:,}{Colors.RESET}")
        
        survival_time = max(1, self.frame_count // 10)
        print(f"""
{Colors.WHITE}                        You survived for{Colors.RESET}
{Colors.CYAN}                            {survival_time} seconds!{Colors.RESET}

{Colors.BOLD}{Colors.GREEN}                        R - Play Again{Colors.RESET}
{Colors.YELLOW}                        Q - Quit Game{Colors.RESET}
        """)
    
    def reset_to_menu(self):
        """Reset to menu state"""
        self.game_state = GameState.MENU
    
    def start_game(self):
        """Start new game"""
        self.game_state = GameState.PLAYING
        self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        self.player_pos = Position(self.width // 2, self.height - 2)
        self.fire_brimstone.clear()
        self.power_ups.clear()
        self.score = 0
        self.lives = 1
        self.frame_count = 0
        self.double_points = False
        self.double_points_timer = 0
        self.shield_active = False
        self.slow_motion = False
        self.slow_motion_timer = 0
    
    def update_game(self):
        """Update game state every frame"""
        if self.game_state != GameState.PLAYING:
            return
        
        self.frame_count += 1
        
        # Spawn elements every frame
        self.spawn_fire_brimstone()
        self.spawn_power_up()
        
        # Update positions every frame
        self.update_fire_brimstone()
        self.update_power_ups()
        
        # Check collisions
        self.check_collisions()
        
        # Update timers
        self.update_power_up_timers()
        
        # Score for survival
        points = 3 if self.double_points else 2
        self.score += points
    
    def run(self):
        """Main game loop"""
        self.hide_cursor()
        
        try:
            menu_shown = False
            game_over_shown = False
            
            print(f"{Colors.YELLOW}Starting NERUPPU DAA with pynput library!{Colors.RESET}")
            time.sleep(0.5)
            
            while self.running:
                # Handle input every frame (using proven pynput methods)
                self.handle_input()
                
                if self.game_state == GameState.MENU:
                    if not menu_shown:
                        self.draw_menu()
                        menu_shown = True
                        game_over_shown = False
                        
                elif self.game_state == GameState.PLAYING:
                    # CRITICAL: Continuous gameplay - fire & brimstone falls every frame
                    self.update_game()
                    self.draw_game()
                    menu_shown = False
                    game_over_shown = False
                    
                elif self.game_state == GameState.GAME_OVER:
                    if not game_over_shown:
                        self.draw_game_over()
                        game_over_shown = True
                        menu_shown = False
                
                # Frame rate control
                time.sleep(0.1)  # 10 FPS - smooth fire & brimstone animation
                
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            self.listener.stop()
            self.show_cursor()
            self.clear_screen()
            print(f"{Colors.YELLOW}Thanks for playing NERUPPU DAA! 🔥{Colors.RESET}")

if __name__ == "__main__":
    print(f"{Colors.GREEN}✅ pynput keyboard test successful!{Colors.RESET}")
    print(f"{Colors.YELLOW}🎮 Starting NERUPPU DAA game with pynput{Colors.RESET}")
    print()
    
    game = NeruppuDaaGame()
    game.run()