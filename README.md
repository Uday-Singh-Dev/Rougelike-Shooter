#Rogue-Like Shooter

A modular top-down rogue-like shooter built in Python using Pygame, structured across multiple files using object-oriented design principles to maintain scalability and clean separation of logic.

##Overview

This project was developed to explore real-time game systems such as AI behaviour, collision handling, rendering effects, and structured game state management. The codebase is organised into multiple files, separating entities, weapons, effects, and core game logic to ensure maintainability as the project expands.

The objective was not only to create a playable game, but to architect a system that allows new mechanics, weapons, and enemies to be added without rewriting core systems.

##Key Features

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

##Technologies Used

- Python  
- Pygame  

##What I Learned

- Structuring larger projects across multiple files  
- Managing real-time game loops efficiently  
- Designing modular systems that allow new features to be added easily  
- Implementing collision systems and state management without tightly coupling components  

##How to Run

1. Install Python 3.11 (supports pygame)  
2. Install Pygame:
   pip install pygame
3. Run the main file:
   run main1.py in IDLE python
