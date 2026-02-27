# Rogue-Like Shooter
![Gameplay](0227.gif)

A modular top-down rogue-like shooter built in Python using Pygame, structured across multiple files using object-oriented design principles to maintain scalability and clean separation of logic.

## Overview

This project was developed to explore real-time game systems such as AI behaviour, collision handling, rendering effects, and structured game state management. The codebase is organised into multiple files, separating entities, weapons, effects, and core game logic to ensure maintainability as the project expands.

The objective was not only to create a playable game, but to architect a system that allows new mechanics, weapons, and enemies to be added without rewriting core systems.

## Key Features

- Enemy AI with movement logic and animations  
- Multiple weapon types with switching mechanics  
- Bullet physics and collision detection  
- Round-based progression system  
- Between-round upgrade shop  
- Dynamic lighting and overlay effects  
- Screen shake and fade transitions  
- Particle systems and explosion effects  
- Health, ammo, and dash mechanics  

##Architecture Highlights

- Multi-file structure separating game state, entities, and rendering logic  
- Object-oriented design for enemies, weapons, and projectiles  
- Centralised game loop managing updates and rendering  
- Collision and physics systems separated from UI logic  

## Technologies Used

- Python  
- Pygame  

## What I Learned

- Structuring larger projects across multiple files  
- Managing real-time game loops efficiently  
- Designing modular systems that allow new features to be added easily  
- Implementing collision systems and state management without tightly coupling components

## How to play and controls
WASD-movement
LShift-Dash
Click/HoldClick-shoot
R-Reload
1,2-weapon switching

you will fight rounds of enemies and gain score. However you will be given a shop
between rounds to change guns or upgrade them. Convert score into money and purchase
these updates. (If your character has score of them the score increases
more when they kill an enemy however also halfs when the player is hit)

## How to Run

1. Install Python 3.11 (supports pygame)  
2. Install Pygame:
   pip install pygame
3. Run the main file:
   run python main1.py
