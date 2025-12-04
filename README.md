# ============================================================================

# PYGAME BOMBERMAN - GAME ARCHITECTURE DOCUMENTATION

# ============================================================================

#

# PROJECT: Bomberman Game Clone

# LANGUAGE: Python 3 with Pygame

# PURPOSE: Recreation of classic Bomberman arcade game

#

# ============================================================================

# TABLE OF CONTENTS

# ============================================================================

# 1. Project Structure

# 2. File Documentation

# 3. Game Architecture

# 4. Game Loop Flow

# 5. Camera System Explained

# 6. Collision Detection

# 7. Controls & Features

# 8. How to Run

#

# ============================================================================

# 1. PROJECT STRUCTURE

# ============================================================================

#

# Pygame_Bomberman/

# ├── main.py # Entry point - Bomberman game controller

# ├── game.py # Core game logic - Game class

# ├── character.py # Player character - Character class

# ├── blocks.py # Block types - Blocks, Hard_block, Soft_Block classes

# ├── assets.py # Asset management - Assets class

# ├── gamesetting.py # Global configuration - Constants, settings

# ├── requirement.txt # Python dependencies

# ├── images/ # Game sprite sheets and assets

# │ ├── owncreation.png # Player character sprite sheet

# │ ├── sprite_sheet (1).png # Block sprite sheet

# │ └── [other sprites]

# ├── .venv/ # Python virtual environment

# └── **pycache**/ # Compiled Python files

#

# ============================================================================

# 2. FILE DOCUMENTATION

# ============================================================================

#

# ## main.py - ENTRY POINT & WINDOW MANAGER

# ============================================================================

# CLASS: Bomberman

#

# RESPONSIBILITIES:

# - Initialize the game window and Pygame

# - Manage the main game loop (input → update → draw)

# - Handle window events (resize, fullscreen toggle, quit)

# - Coordinate between display, game logic, and assets

#

# KEY FEATURES:

# - Resizable window (can drag edges to resize)

# - Fullscreen toggle with F11 (hides taskbar, hides cursor)

# - Event centralization (all events processed here, forwarded down)

# - Frame rate control (60 FPS target)

#

# KEY METHODS:

# - **init**(): Initialize window, assets, game instance

# - input(): Poll events, handle resize/fullscreen, forward events

# - update(): Tick frame timer, delegate game updates

# - draw(): Clear screen, draw game world, update display

# - rungame(): Main game loop (runs until quit)

#

# STATE VARIABLES:

# - self.screen: pygame.Surface - the display window

# - self.windowed_size: (int, int) - stored window size for fullscreen toggle

# - self.fullscreen: bool - current fullscreen state

# - self.running: bool - controls the game loop

#

#

# ## game.py - CORE GAME LOGIC

# ============================================================================

# CLASS: Game

#

# RESPONSIBILITIES:

# - Manage all game entities (player, blocks)

# - Generate and manage the game level/world

# - Implement camera system with smooth following and deadzone

# - Coordinate sprite rendering with camera offsets

# - Handle level generation and block placement

#

# KEY FEATURES:

# - Camera with deadzone (player can move without camera moving)

# - Smooth camera interpolation (lerp) for polished feel

# - Adaptive camera size (works on any display resolution)

# - Level generation with hard and soft blocks

#

# KEY METHODS:

# - **init**(): Create player, level, and camera system

# - input(events): Forward events to player

# - update(): Update all sprites, interpolate camera

# - update_camera(centerx, centery): Calculate camera position based on player

# - draw(window): Render all game visuals with camera offsets

# - generate_level_matrix(rows, cols): Create the game level

# - insert_hard_block_into_matrix(matrix): Place indestructible blocks

# - insert_soft_block_into_matrix(matrix): Randomly place destroyable blocks

#

# STATE VARIABLES:

# - self.PLAYER: Character - the player sprite

# - self.groups: dict - sprite groups (hard_block, soft_block, player)

# - self.level_matrix: list - 2D grid of blocks (grid coordinates)

# - self.x_camera_offset, self.y_camera_offset: float - current camera position

# - self.cam_target_x, self.cam_target_y: float - where camera is moving toward

# - self.camera_lerp: float - camera follow smoothness (0.14 default)

# - self.deadzone_ratio: float - deadzone size (0.6 = 60% of screen)

#

# CAMERA SYSTEM EXPLAINED:

# - Deadzone: Central area of screen where player can move without camera moving

# - Deadzone width/height = screen_width/height \* deadzone_ratio

# - Only when player leaves deadzone does camera start following

# - Interpolation: Camera smoothly moves toward target position using lerp

# - camera.current += (target - current) \* lerp_value

# - Lower lerp = smoother, slower follow

# - Clamping: Camera never goes past map boundaries

#

#

# ## character.py - PLAYER CHARACTER

# ============================================================================

# CLASS: Character (extends pygame.sprite.Sprite)

#

# RESPONSIBILITIES:

# - Handle player input and movement

# - Perform collision detection with blocks

# - Manage animation frame switching

# - Trigger camera updates based on position

#

# KEY FEATURES:

# - 4-directional movement (WASD / Arrow keys)

# - Smooth animation based on movement direction

# - Pixel-perfect collision detection with blocks

# - 2-phase collision (slide along walls)

# - Automatic camera following

#

# KEY METHODS:

# - **init**(): Initialize player sprite, position, animation

# - input(events): Process movement input

# - update(): Called each frame (currently empty)

# - draw(window, x_offset=0, y_offset=0): Render character with camera offset

# - animate(action): Switch animation frames based on elapsed time

# - check_collision(): Test if character is touching solid blocks

# - move(action): Move player in direction, check collisions, animate

#

# STATE VARIABLES:

# - self.x, self.y: float - pixel position in world

# - self.row_num, self.col_num: int - grid position

# - self.alive: bool - whether character is alive

# - self.speed: int - pixels per frame (3 default)

# - self.action: str - current movement direction

# - self.image_dict: dict - all animation frames indexed by action

# - self.index: int - current animation frame index

# - self.anim_time: int - milliseconds between animation frames

# - self.offset: int - hitbox offset for centering

#

# MOVEMENT PHYSICS:

# - Two-phase collision detection allows sliding along walls

# - Phase 1: Move X axis, check collision, undo if hit

# - Phase 2: Move Y axis, check collision, undo if hit

# - Result: Player can squeeze through diagonal gaps

#

#

# ## blocks.py - BLOCK/TILE CLASSES

# ============================================================================

# CLASS: Blocks (Base class, extends pygame.sprite.Sprite)

#

# RESPONSIBILITIES:

# - Define base functionality for all block types

# - Handle sprite rendering with camera offset

# - Manage collision properties (passable/solid)

#

# CLASS: Hard_block (extends Blocks)

# - Indestructible barriers forming the maze

# - passable = False (solid, cannot pass through)

# - Placed in border and checkerboard interior pattern

#

# CLASS: Soft_Block (extends Blocks)

# - Destructible blocks that can be blown up

# - passable = False (solid, cannot pass through)

# - Randomly placed throughout map

# - Avoided in player starting area

#

# KEY METHODS (all block types):

# - **init**(): Create block at grid position

# - update(): Called each frame (currently empty for blocks)

# - draw(window, x_offset=0, y_offset=0): Render block with camera offset

#

# STATE VARIABLES:

# - self.x, self.y: float - pixel position in world

# - self.row, self.col: int - grid position

# - self.passable: bool - whether player can walk through

# - self.image: pygame.Surface - current sprite image

#

#

# ## assets.py - ASSET MANAGEMENT

# ============================================================================

# CLASS: Assets

#

# RESPONSIBILITIES:

# - Load sprite sheets from image files

# - Extract individual sprites from sprite sheets

# - Provide organized access to all game graphics

#

# KEY METHODS:

# - load_sprite_sheet(path, filename): Load and cache sprite sheet image

# - load_sprite_range(coords, sheet, ...): Extract sprites and organize by action

#

# ASSET ORGANIZATION:

# - Player character: owncreation.png (325x257) → animation sequences

# - Blocks: sprite_sheet (1).png → hard blocks, soft blocks, background

# - Background: Procedurally created red squares (64x64 pixels each)

#

#

# ## gamesetting.py - GLOBAL CONFIGURATION

# ============================================================================

# PURPOSE:

# - Central location for all game constants

# - Easy tuning of game parameters

#

# KEY CONSTANTS:

# - SCREENWIDTH, SCREENHEIGHT: Initial window size (1280x720)

# - FPS: Frame rate (60)

# - ROWS, COLS: Game level grid size (20x40)

# - SIZE: Tile size in pixels (64)

# - Y_OFFSET: Vertical offset for visual alignment (92 pixels)

# - Player animation frame coordinates (PLAYER dict)

# - Block sprite coordinates (HARD_BLOCK, SOFT_BLOCK dicts)

# - Colors for UI and debugging (BLACK, RED, GREEN, etc.)

#

# TUNING PARAMETERS:

# Change these values in gamesetting.py to adjust gameplay:

# - SIZE: Change tile size (affects everything)

# - ROWS/COLS: Change map size

# - Player speed: Set in Character.**init**() (default 3)

# - Camera lerp: Set in Game.**init**() (default 0.14)

# - Deadzone ratio: Set in Game.**init**() (default 0.6)

#

# ============================================================================

# 3. GAME ARCHITECTURE OVERVIEW

# ============================================================================

#

# ENTITY HIERARCHY:

#

# Bomberman (Main Controller)

# ├── GAME (Game Logic)

# │ ├── PLAYER (Character)

# │ │ └── Animation State

# │ ├── groups["player"]

# │ │ └── Sprites: Player

# │ ├── groups["hard_block"]

# │ │ └── Sprites: Hard_block instances

# │ ├── groups["soft_block"]

# │ │ └── Sprites: Soft_Block instances

# │ └── Camera System

# │ ├── Current Offsets (x_camera_offset, y_camera_offset)

# │ ├── Target Offsets (cam_target_x, cam_target_y)

# │ ├── Deadzone (centered rectangle)

# │ └── Interpolation (lerp)

# └── ASSETS (Asset Manager)

# ├── Player sprites

# ├── Block sprites

# └── Background sprites

#

# DATA FLOW:

#

# 1. INPUT STAGE:

# main.input() → polls pygame events

# ↓

# Handles resize/fullscreen/quit events

# ↓

# Forwards events to game.input(events)

# ↓

# game.input() forwards to character.input(events)

# ↓

# character processes movement keys

#

# 2. UPDATE STAGE:

# main.update() → ticks frame timer, calls game.update()

# ↓

# game.update() → updates all sprites

# ↓

# character.move() handles movement, collision, animation

# ↓

# character calls game.update_camera() to calculate new camera position

# ↓

# game.update() interpolates camera toward target

#

# 3. RENDER STAGE:

# main.draw() → fills screen with black, calls game.draw()

# ↓

# game.draw() → fills background, draws tiles with camera offset

# ↓

# Loops through all sprite groups, calling draw(window, cam_x, cam_y)

# ↓

# Each sprite draws itself shifted by camera offset

# ↓

# pygame.display.update() swaps buffers to display frame

#

# ============================================================================

# 4. GAME LOOP FLOW (main.rungame())

# ============================================================================

#

# while running:

# 1. input() # Process user input and window events

# 2. update() # Advance game state and timing

# 3. draw() # Render all visuals to screen

# ↓

# Frame completes, loop repeats 60 times per second

#

# Each iteration:

# - Handles movement input

# - Updates character position and animation

# - Updates camera position (smoothly following character)

# - Detects collisions

# - Renders entire game world with camera offset

# - Swaps display buffer to show the frame

#

# ============================================================================

# 5. CAMERA SYSTEM DETAILED EXPLANATION

# ============================================================================

#

# PURPOSE: Follow the player while maintaining visible game world

#

# THREE KEY CONCEPTS:

#

# A. DEADZONE (No Camera Movement Zone)

# ┌────────────────────────────┐

# │ Camera View │

# │ ┌──────────────────────┐ │

# │ │ │ │

# │ │ Deadzone Area │ │

# │ │ (60% of screen) │ │

# │ │ │ │

# │ │ Player can move │ │

# │ │ here without │ │

# │ │ camera moving │ │

# │ │ │ │

# │ └──────────────────────┘ │

# │ │

# │ Camera moves when player │

# │ leaves this central zone │

# └────────────────────────────┘

#

# Implementation:

# deadzone_ratio = 0.6 # 60% of screen

# dz_width = screen_width \* 0.6

# dz_height = screen_height \* 0.6

# dz_left = (screen_width - dz_width) / 2

#

# B. INTERPOLATION (Smooth Camera Follow)

# Instead of snapping camera to player instantly:

#

# current_offset += (target_offset - current_offset) \* lerp

#

# Example with lerp = 0.14:

# Frame 1: offset = 0, target = 100

# new offset = 0 + (100-0)\*0.14 = 14

# Frame 2: offset = 14, target = 100

# new offset = 14 + (100-14)\*0.14 = 26

# ... continues until offset ≈ 100

#

# Lower lerp value = smoother but slower follow

# Higher lerp value = snappier, more responsive follow

#

# C. CLAMPING (Keep Camera In Bounds)

# Camera should never show empty space beyond map edges:

#

# max_x = total_map_width - screen_width

# max_y = total_map_height - screen_height

#

# clamp(offset):

# if offset < 0: return 0

# if offset > max: return max

# return offset

#

# COMPLETE CAMERA CALCULATION:

#

# Each frame when player moves:

# 1. Calculate where player is on screen (player_screen_pos)

# 2. Check if player is outside deadzone

# 3. If outside: calculate where camera should be to keep player at edge

# 4. Clamp target to valid range (don't go past map boundaries)

# 5. Interpolate current offset toward target

# 6. Use offset when drawing to shift world position

#

# ============================================================================

# 6. COLLISION DETECTION SYSTEM

# ============================================================================

#

# TWO-PHASE COLLISION FOR SMOOTH WALL SLIDING:

#

# Problem: Character collides head-on with diagonal wall corner

# Without two-phase: Stuck, can't move at all

#

# Solution: Separate X and Y movement:

#

# Phase 1 - Horizontal Movement:

# ├─ Try to move player X coordinate

# ├─ Check for collision

# └─ If collision: undo X movement only

#

# Phase 2 - Vertical Movement:

# ├─ Try to move player Y coordinate

# ├─ Check for collision

# └─ If collision: undo Y movement only

#

# Result: Player slides along the wall diagonally!

#

# COLLISION DETECTION IMPLEMENTATION:

#

# 1. Character has hitbox (smaller than visual sprite)

# rect.inflate(-20, -20) shrinks hitbox by 20 pixels

#

# 2. Each frame when moving:

# hard_hits = pygame.sprite.spritecollide(player, hard_blocks, False)

# soft_hits = pygame.sprite.spritecollide(player, soft_blocks, False)

#

# 3. Check each colliding block's 'passable' attribute

# if not block.passable: # Solid block

# undo_movement()

#

# 4. Collision handled separately for X and Y

# This allows sliding along walls instead of stopping dead

#

# ============================================================================

# 7. CONTROLS & FEATURES

# ============================================================================

#

# MOVEMENT:

# - WASD or Arrow Keys: Move in four directions

# - Movement is smooth and continuous

# - Cannot move through solid blocks

#

# WINDOW MANAGEMENT:

# - Click and drag window edges to resize (in windowed mode)

# - F11: Toggle between fullscreen (hides taskbar) and windowed

# - ESC: Quit the game

# - Close window: Quit the game

#

# GAME FEATURES IMPLEMENTED:

# ✓ Resizable window with adaptive camera

# ✓ Fullscreen toggle with F11

# ✓ Smooth camera following with deadzone

# ✓ 4-directional movement with collision detection

# ✓ Wall-sliding for smooth gameplay

# ✓ Sprite animation based on direction

# ✓ Level generation with hard and soft blocks

# ✓ Adaptive UI (works on any resolution)

#

# FEATURES NOT YET IMPLEMENTED:

# □ Bombs and explosions

# □ Power-ups

# □ Enemy AI

# □ Sound effects and music

# □ Game states (menu, pause, game over)

#

# ============================================================================

# 8. HOW TO RUN

# ============================================================================

#

# PREREQUISITES:

# - Python 3.7+

# - Pygame library

#

# INSTALLATION:

# 1. Install Python from python.org

# 2. Install Pygame: pip install pygame

# 3. Navigate to project folder: cd Pygame_Bomberman

#

# RUNNING THE GAME:

# python main.py

# or

# python -u main.py (unbuffered output for debugging)

#

# TROUBLESHOOTING:

# - "ModuleNotFoundError: No module named 'pygame'"

# → Run: pip install pygame

#

# - "FileNotFoundError: images/owncreation.png"

# → Ensure images folder exists with sprite sheets

#

# - "Pygame QUIT event not working"

# → Try running from terminal instead of IDE

#

# - "Fullscreen not hiding taskbar"

# → This is normal on some systems; F11 still works to toggle

#

# ============================================================================

# END OF DOCUMENTATION

# ============================================================================

#

# For questions or modifications, refer to the inline comments in each file.

# Each method has detailed docstrings explaining its purpose and parameters.

#

# Last Updated: December 4, 2025

# Game Version: 0.2 (Camera system implemented)
