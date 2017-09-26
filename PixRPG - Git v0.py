# PixRPG Demo SRC for GitHub #
# Re-Write 02 - Revision Time - 12th of November 2016, 04:39, 1.2 #
from __future__ import division


'''Actual Code Begins'''
# Import Modules #
import  pygame, random, ctypes, pickle, os, math, fractions, datetime
from    fractions       import *
from    pygame          import *
from    pygame.locals   import *
from    math            import *

from collections import OrderedDict

# Resolution Check - Get Max Res #
MAX_WIDTH   = ctypes.windll.user32.GetSystemMetrics(0) # Get System Res X #
MAX_HEIGHT  = ctypes.windll.user32.GetSystemMetrics(1) # Get System Res Y #

# Resolution Check - Get Aspect Ratio #
RES_GCD             = gcd(MAX_WIDTH , MAX_HEIGHT)
ASPECT_RATIO_W      = MAX_WIDTH      // RES_GCD
ASPECT_RATIO_H      = MAX_HEIGHT    //  RES_GCD

print (MAX_HEIGHT)
ASPECT_RATIO_VAL    = MAX_HEIGHT / MAX_WIDTH

print ("DEBUGSTRING - Resolution - " +str(MAX_WIDTH) +"x" +str(MAX_HEIGHT) +" | Res Val - " +str(ASPECT_RATIO_VAL))
print ("DEBUGSTRING - Technical Aspect Ratio - " +str(ASPECT_RATIO_W) +":" +str(ASPECT_RATIO_H))

# Resolution Check - Get height from a base of 320 Pix. #
TRUE_DEFAULT_WIDTH  = 320
TRUE_DEFAULT_HEIGHT = int(TRUE_DEFAULT_WIDTH * ASPECT_RATIO_VAL) # Don't ask, // wasn't enough.
print (ASPECT_RATIO_VAL)
print ("DEBUGSTRING - Final Res = " +str(TRUE_DEFAULT_WIDTH) +"x" +str(TRUE_DEFAULT_HEIGHT))

# Resolution Check - Set Resolutions #
# Set Current + Default Width to Aspect Ratio * 20
SCREEN_WIDTH        = TRUE_DEFAULT_WIDTH
SCREEN_HEIGHT       = TRUE_DEFAULT_HEIGHT
DEFAULT_WIDTH       = SCREEN_WIDTH
DEFAULT_HEIGHT      = SCREEN_HEIGHT
SAVED_WIDTH         = SCREEN_WIDTH
SAVED_HEIGHT        = SCREEN_HEIGHT

# Set up display and dupe surface #
FLAGS_RESIZABLE     = RESIZABLE
FLAGS_FULLSCREEN    = HWSURFACE |   DOUBLEBUF   | FULLSCREEN
TRUE_DISPLAY        = pygame.display.set_mode( (DEFAULT_WIDTH, DEFAULT_HEIGHT), FLAGS_RESIZABLE)
SCREEN_DISPLAY      = pygame.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT), HWSURFACE, 8)
TRUE_DISPLAY.set_alpha(None)

# Load PyGame & Sound System #
pygame.mixer.pre_init(44100, -16, 2, 1024)   # irrc, only default OGGs from Audacity work.
pygame.init()
pygame.font.init()
FONT_SIZE       = 15
FONT_TRUE_SIZE  = 12
FONT_MAX_W      = DEFAULT_WIDTH     //FONT_TRUE_SIZE     # Max font elements wide
FONT_MAX_H      = DEFAULT_HEIGHT    //FONT_TRUE_SIZE     # Max font elements high
GAME_FONT       = pygame.font.SysFont("pixrpg01", FONT_SIZE, False)
        
# Game Constants #
GAME_CLOCK                  = pygame.time.Clock()
GAME_FPS                    = 60
CONST_MILLISECONDS          = 1000//GAME_FPS     # Number of Milliseconds per Frame

# Global Timer #
Global_Timer                = 0
Global_Timer_Max            = 2 ** 32
Global_Timer_TimeScale      = 1
Global_Timer_Paused         = False

Demo_Timer                  = 0
Demo_Timer_Max              = GAME_FPS * 3

# Load Sprites & Textures #
CurrentBackground   = 'BACKGROUND.png'
CurrentChars        = 'CHARS.png'
CurrentColPal       = 'COLPAL.png'
CurrentEnemies      = 'ENEMIES.png'
CurrentForeground   = 'FOREGROUND.png'
CurrentSprites      = 'SPRITES.png'
CurrentTiles        = 'TILES.png'
CurrentTitle        = 'TITLE.png'

# Init - Set and resize textures #
BACKGROUND          = pygame.image.load(CurrentBackground)  .convert(8, HWSURFACE)
CHARS               = pygame.image.load(CurrentChars)       .convert(8, HWSURFACE)
COLPAL              = pygame.image.load(CurrentColPal)      .convert(8, HWSURFACE)
ENEMIES             = pygame.image.load(CurrentEnemies)     .convert(8, HWSURFACE)
FOREGROUND          = pygame.image.load(CurrentForeground)  .convert(8, HWSURFACE)
SPRITES             = pygame.image.load(CurrentSprites)     .convert(8, HWSURFACE)
TILES               = pygame.image.load(CurrentTiles)       .convert(8, HWSURFACE)
TITLE               = pygame.image.load(CurrentTitle)       .convert(8, HWSURFACE)

LOADED_TEXTURES     = [BACKGROUND, CHARS, COLPAL, ENEMIES, FOREGROUND, SPRITES, TILES, TITLE]

# Set Icon and Title Label at Top #
GAME_ICON       = pygame.image.load("ICON.png")         .convert_alpha()
GAME_TITLES = ["PixRPG","PixRPG - By JackM", "PixRPG - Bants"]
pygame.display.set_caption(GAME_TITLES[random.randint(0, (len(GAME_TITLES) - 1 ))])
pygame.display.set_icon(GAME_ICON)

# Game Base Values #
FullScreen          = False
CheckingVariables   = True

# No error checks here for string I'm lazy
Game_State          = int(input("What game state do you want (0 = Title, 1 = Game World, 2 = Background) - "))
if Game_State > 2:
    Game_State = 2
elif Game_State < 0:
    Game_State = 0
#Game_State          = 1    # 0 = Menus, 1 = World, 2 = Battles

# Character 1 Info
Char_Index_WorldDetails     = 0
Char_Index_TexDetails       = 1
Char_Index_Items            = 2
Char_Index_Stats            = 3
Char_Index_Quests           = 4
Char_Amount                 = 6     # Total # of Chars EVER
Char_Details_Default    = []

# Overworld - Moving Options, etc, these are NOT saved as you could load moving #
PlayerControlEnabled    = True
Moving                  = False
MovingLeft              = False
MovingRight             = False
MovingUp                = False
MovingDown              = False
Moving_Diagonal         = False
Moving_Diagonal_Time    = 0     # Current NumFrames before diagonal does nothing
Moving_Diagonal_MaxTime = 4     # NumFrames before stopping diagonally does nothing
Moving_Diagonal_WalkT   = 4     # NumFrames before stopping diagonally if walking
Moving_Diagonal_RunT    = 8     # NumFrames before stopping diagonally if running

Running                 = False
Running_Timer_Max       = 12    # NumFrames before running if holding space
Running_Timer           = 0
Diagonal_Direction      = 0

# Rendered Camera Section - Anything outside of this area will not be drawn, even if you're in the range.
Rendered_Section = [0, 0, 0, 0]     # A Rect-Like object that defines the quadrilateral area that is "loaded"           _X_L    = 0
Current_Tile_X_L = 0
Current_Tile_X_R = 0
Current_Tile_Y_T = 0
Current_Tile_Y_B = 0

# Overworld - Universal Character Stuff #
Player_Speed        = 1 # Character moves 1px per frame
Player_MaxSpeed     = 8 # If character is forced to move faster, their max speed is 8px
Player_RunSpeed     = 2 # Speed Char1 moves while running
Player_Direction    = 0 # Angle between 0 and 7

# Character - WalkCycle Stuff #
Player_WalkCycle     = 1 # Current Walk Cycle, STILL = 1, LL = 0, RL = 2
Player_WalkFrame     = 0 # Current Walk Frame, Modulos to Char1_Walk_I_End
Player_Walk_L_Start  = 1 # On this Walk Frame, Player's Left Leg is forward.
Player_Walk_L_End    = 11
Player_Walk_R_Start  = 21
Player_Walk_R_End    = 31
Player_Walk_I_End    = 41

# Colors, R/G/B Decimal Tuple, alpha isn't supported. #
COL_SKY             =   (155, 244, 255)         # Nice sky color. #
COL_COLORKEY        =   (255, 0, 255)           # Doesnt Matter, just here for clarity sake (Magenta is easily visible on Col 0)
COL_ELSE            =   (0, 0, 0)

# Color Index Values #
Color_Index         = list(COLPAL.get_palette())
for x in range (0, len(Color_Index)):
    Color_Index[x] = tuple(Color_Index[x])
    #print (int(Color_Index[x]))



# Color Index - RESERVED COLORS #
#Color_Index[1] = (0, 0, 0)          # Black Color
Color_Index[2] = (255, 255, 255)    # Debug Text or White
Color_Index[3] = (127, 100, 127)    # Debug BG or Grey

# No it's not, I forgot.
# Here's the Skinny, the MAP is actually a JPG which is converted to image data
# What we CAN do is take the value between 0-255, and then convert to a numberthat's looked up on a 16x16 (16*16 tiles) Grid
# Then, this is what happens, the game selects an area to render and the tile is done
TheWorld = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0,0,0,0],
    [1,1,1,1]

    ]


# Update Palette for Loaded Textures #
def UpdatePalette():
    for x in range (0, len(LOADED_TEXTURES)):
        LOADED_TEXTURES[x].set_palette(Color_Index)
        LOADED_TEXTURES[x].set_colorkey(Color_Index[0])

def SetPalette (Palette_BaseID, Palette_Colors):
    for x in range (0, len(Palette_Colors)):
        Color_Index[Palette_BaseID + x] = Palette_Colors[x]
    UpdatePalette()

# Sub - All Palette Scrollers #
GB_ColPal = [(57, 16, 60), (173, 41, 33), (222, 148, 74), (255, 239, 206)]
SetPalette(8, GB_ColPal)

# Here's the skin tones from light to dark + stranger/unique skins
Skindex_White   = [(255, 214, 193), (255, 201, 165), (211, 158, 126), (255, 240, 230)]  # WHITE:    Highlights, Normal, Shade, Albino
Skindex_Fair    = [(220, 170, 150), (229, 162, 120), (198, 129, 89), (127, 98, 90)]     # FAIR:     Highlights, Normal, Shade, Alt Black/DeSaturated
Skindex_Mid     = [(216, 151, 130), (198, 128, 103), (168, 100, 77), (255, 130, 107)]   # MID:      Highlights, Normal, Shade, Sunburn
Skindex_Brown   = [(127, 60, 38), (96, 48, 32), (63, 30, 19) , (150, 82, 73)]           # BROWN:    Highlights, Normal, Shade, Reddish Skin or darker suntan
Skindex_Black   = [(51, 32, 28), (38, 23, 19), (23, 15, 12), (25, 22, 30)]              # BLACK:    Highlights, Normal, Shade, Close to Blue/Exotic Black

SetPalette(160, Skindex_White)
SetPalette(164, Skindex_Fair)
SetPalette(168, Skindex_Mid)
SetPalette(172, Skindex_Brown)
SetPalette(176, Skindex_Black)

# Color Index, Force Bittification of Palette (Modulos by this amount) #
def ForceBits(NumBits):
    for x in range (0, Color_Index_Length):
        Color_Index[x] = (Color_Index[x][0] - Color_Index[x][0] % NumBits, Color_Index[x][1] - Color_Index[x][1] % NumBits, Color_Index[x][2] - Color_Index[x][2] % NumBits)

# World Camera #
Camera_Offset_X = 0
Camera_Offset_Y = 0
Camera_Offset_Enabled   = False

# Player Stuff #
Player_InControl = True     # Player can control their character at all

Player_Render_Width    = 15
Player_Render_Height   = 25
Player_Render_XPos  =   12  
Player_Render_YPos  =   5

Player_Blit_XPos    = DEFAULT_WIDTH//2      - (Player_Render_Width//2)
Player_Blit_YPos    = DEFAULT_HEIGHT//2     - (Player_Render_Height//2)

Player_Hitbox_XPos      = Player_Blit_XPos
Player_Hitbox_YPos      = int(Player_Blit_YPos + (Player_Render_Height * 0.75) )
Player_Hitbox_Width     = 15
Player_Hitbox_Height    = (Player_Blit_YPos + Player_Render_Height) - Player_Hitbox_YPos


Player_XPos = 0 # Player's XPos on World
Player_YPos = 0 # Player's YPos on World
Player_XChange = 0
Player_YChange = 0



# GAMELIMITS - DISABLE/CHANGE THESE BY INCREASING THE RANGE #
# Do not change these default numbers unless you know what you're doing #
# Because, these are used to prevent color corruption #
# If you REALLY want to disable them, change the range values from 0 - 256; this will allow you to overwrite other colors in the game without limits #
# For example, COLPAG_BGS is used to ensure the scroll effect does not leak out during testing/debugging and overwrite other colors I may not check #
# Therefore, the limit is in place as FIRST NUMBER INCLUSIVE, LAST EXCLUSIVE #
# The RANGE is converted to a list automatically, so COLPAL_DEBUG[0] = 0, [1] = 1, so on...
# Final Number is [len(LISTNAME)-1]

# These are NOT enforced; and some colors can be reused such as Enemies/BGs being un-needed on World

COLPAL_DEBUG                = range(0, 8)       # RESERVED/DEBUG
COLPAL_HUD                  = range(8, 16)      # HUD       Colors
COLPAL_ICONS                = range(16, 32)     # HUD       Icons
COLPAL_TILES_BGS            = range(32, 160)    # World     Tiles
COLPAL_SPRITES_ENEMIES      = range(160, 224)   # Battle    BG
COLPAL_OTHER                = range(248, 256)   # Battle    Enemies/FX

# RPG Limits #
Level_Max       = 99    # Level limit in game
Items_Max       = 99    # Max number of items per slot
Stats_Max       = 255   # Highest value a skill can be
HP_Max          = 999   # Highest amount of HP you can have
PP_Max          = 999   # Highest amount of Mana you can have
Damage_Max      = 9999  # Highest possible hit you can make

# Debug Stuff #
Debug_DrawText      = False                 # Enable/Disable Debug Text
Debug_DrawPalette   = False                 # Enable/Disable Palette Info.
Debug_BGInfo        = False                 # Enable/Disable Background Info.
Debug_DrawScanLines = False                 # Enable/Disable Scanlines
Debug_HL_Palette    = False                 # Does nothing, TODO WIP it's supposed to color every pixel with said color on the screen.
Debug_Draw_ROT      = False                 # Draw rule of thirds, for cinematic purposes
Debug_Cheats        = False                 # General Cheats I guess
Debug_Height        = FONT_TRUE_SIZE + 1    # Size of Debug Text Boxes

# LONG List of comments for use in the cheats menu #
Cheats_BG               = 0                             # What Background to view
Cheats_Parameters       = 0                             # What BG Parameter to load
Cheats_Interval_Int     = 1                             # On scoll, how much an int incs/decs by
Cheats_Interval_Float   = 0.05                          # On scroll, how much does a float inc/dec by

# UserTest Enable/Disable #
UserTest_EnableDebug    = True      # Enable/Disable Debug Commands, can be a bit buggy, especially with ScreenClippers

# Tile Stuff #
Tile_Length             = 16                                        # Dimensions in pixel of a tile (16x16 was common in old games)
Max_Tiles_X             = (TILES.get_width()    // Tile_Length)     # This is actually how many tiles fit on the TEXTURE SOURCE WIDTH
Max_Tiles_Y             = (TILES.get_height()   // Tile_Length)     # This is actually how many tiles fit on the TEXTURE SOURCE HEIGHT

Console_Enabled         = False     # Is console...on?
Console_Input           = ""        # Leave blank but does nothing
Console_Parameter       = []        # Value parsed per command
Console_Parsing         = False     # Is console parsing value?
Console_Text2           = GAME_FONT.render("Type your command here!", 0, Color_Index[2])
Console_Text2_String    = []

# Despite what it says, it can only render one background at a time due to a Logic Error :)
All_BGS              = [ OrderedDict  ( [ ('DoOnceFailSafe', True), ('DoOnceLoading', True), ('DoOncePalette', True), ('IsRendered',True),  ('Source',      BACKGROUND),    ('Texture',    None), ('IsTiled',True),    ('IsResizedPostTiling',False), ('TileType',0), ('IsResized',False), ('ForceWidth',64), ('ForceHeight',64), ('TexWidth',55),  ('TexHeight',55), ('TexXPos',395), ('TexYPos',130), ('TexFlippedX',False), ('TexFlippedY',False), ('TexRot', 0), ('SineAmp',8), ('SineFreq',16), ('SineSpeed',1), ('SineXChange', 0), ('SineYChange',0), ('SineSize',1), ('SineIgnoreLines',2),   ('SineTime',Global_Timer), ('SineXMult', 1), ('SineYMult', 1), ('SineVert',False), ('SineLoops',True), ('SineXOffset',0), ('SineYOffset',0),   ('WaveType',sin), ('SinePaused', False), ('PaletteIsScroll', True),    ('ScrollBaseID', 64), ('ScrollTime', 3), ('ScrollColors', [(16, 0, 250),  ] ), ('ScrollAmount', 0), ('ScrollPingPong', True), ('ScrollBackwards', False), ('NonScrollColors', [(0,0,0), (255,255,255) ]), ('NonScrollIDs', [0,10] ) ] ),]

# README - Refer to BG Examples.txt
Rendered_BG_IDs         = [0] # LIST, All of the Backgrounds in Order of Rendering Time (Background Backgrounds come first)

SaveNumber = 0
# Load all Chars with Default Data, before loading from save #
for x in range (0, Char_Amount):
    Char_Details_Default.append([ ["Save #" +str(SaveNumber),"Game Start!" ,"Time: " +str(Global_Timer//GAME_FPS * 60 * 60) +":" +str(Global_Timer//GAME_FPS * 60) +":" +str(Global_Timer//GAME_FPS) ],    [0, 0], [15, 25, 0, 0 ], [0, 0, 0], [0]     ])
    
SaveIcon_Dir = 'saves\savicons'

# Saves Code #
if not os.path.exists(SaveIcon_Dir):
    os.makedirs(SaveIcon_Dir)
    
def NewGame(SaveNumber):
    SaveData = open("pixrpg_save"+str(SaveNumber) +".txt","w")
    SaveData.write(str(Char_Details_Default))
    SaveData.close()
    
NewGame(0)
SaveIcons_List = []

for root, dirs, files in os.walk(SaveIcon_Dir):
    for file in files:
        if file.endswith(".png"):
            LoadedFile = os.path.join(root, file)
            SaveIcons_List.append(pygame.image.load(LoadedFile)         .convert(8, HWSURFACE))

# Title, 3D Logo TODO
# Create logo text that appears from the bottom and bends into place
PixRPG_Title    = []
for x in range (0, len("PIXRPG")):
    PixRPG_Title.append([SPRITES.subsurface(4, 5 * x, 8, 5), DEFAULT_WIDTH - (8 * 5), DEFAULT_HEIGHT + DEFAULT_HEIGHT * (x * 0.25) ])
    PixRPG_Title[x][0] = pygame.transform.scale(PixRPG_Title[x][0], (PixRPG_Title[x][0].get_width() * 5, PixRPG_Title[x][0].get_height() * 5))
    PixRPG_Title[x][0].set_colorkey(Color_Index[0])

# Logo Parameters #
PixRPG_Title_Complete           = False                                             # Is the title sequence complete via the last letter getting into place
PixRPG_Title_Complete_MakeSurf  = True                                              # Create Surface on Done
PixRPG_Title_Selection          = 1                                                 # Current Menu Choice
PixRPG_Title_Pointer            = SPRITES.subsurface(12, 0, 8, 5)                   # Pointer Texture
PixRPG_Title_ReadyTime          = 280                                               # Frames until game is "ready - DEFAULT = 280"
PixRPG_Title_State              = 0                                                 # What menu we're on, 0 is default main menu
PixRPG_Title_Selection_Memory   = PixRPG_Title_Selection                            # When selection is made, this is the choice you go back to
PixRPG_Title_BG                 = pygame.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT))   # Background is a striped texture
BlackScreen                     = pygame.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT))   # BlackScreen used for Circle
BlackScreen.set_colorkey        (Color_Index[1])                                    # BlackScreens color key is the circles color DO NOT CHANGE

# PixRPG Demo Settings #
PixRPG_Demo                 = False                         # Is Demo running?
PixRPG_Demo_CircleWidth     = int(DEFAULT_HEIGHT * 1.33)    # Circle starts to creep in edges of screen @ 367.15 px
PixRPG_Demo_MaxWidth        = PixRPG_Demo_CircleWidth       # Also this is the maximum circle width


# Demo Formatting
# Demo is a 3D/4D Array with scenes listed by line
# XPos/YPos = Initial X/Y to put player + is updated by World_XPos/World_YPos
# Character Sprites to load (Which chars are loaded + who to load)
# LIST - Actions/Events at what Times
# StartFadeOut - Frame # on which the circle takes over the screen
# LoadNext - Frame # on which circle expands and next scene plays - Next scene is already "loaded" anyway
'''
PixRPG_Demo_List            = [
    [   [XPOS, YPOS], [CharSpriteDetails], [WorldDetails], [Action, Time], [StartFadeOut, LoadNext]      ], # Scene 1
    [   [XPOS, YPOS], [CharSpriteDetails], [WorldDetails], [Action, Time], [StartFadeOut, LoadNext]      ], # Scene 2
    [   [XPOS, YPOS], [CharSpriteDetails], [WorldDetails], [Action, Time], [StartFadeOut, LoadNext]      ], # Scene 3
    [   [XPOS, YPOS], [CharSpriteDetails], [WorldDetails], [Action, Time], [StartFadeOut, LoadNext]      ], # Scene 4

        ] # First, stage 1, list LENGTH of demo before circle fades, THEN list location of map to render, THEN list movements, THEN list actions on what frames
'''

for x in range (12, 64):
    SetPalette(x, [(57 + (x - 8), 16 + (x - 8), 60 + (x - 8))])

# Set Sky Color
Color_Index[248] = COL_SKY

for x in range (DEFAULT_HEIGHT):
    pygame.draw.line(PixRPG_Title_BG, Color_Index[(14 + x)//8], (0, x), (DEFAULT_WIDTH, x), 1)

# Cursor Code #
Cursor_Vertical         = False
Cursor_Horizontal       = False
Cursor_Select           = False
Cursor_Back             = False
AboutToQuit    = False

# Screenshot Code - Create Dir if no screenshots dir #
ScreenShotting      = False
if not os.path.exists('screenshots/'):
    os.makedirs('screenshots/')


# SFX Code #
SFX_Cursor_V    = pygame.mixer.Sound('SFX/cursor_v.ogg')    # Verti Cursor
SFX_Cursor_H    = pygame.mixer.Sound('SFX/cursor_h.ogg')    # Horiz Cursor
SFX_Cursor_S    = pygame.mixer.Sound('SFX/cursor_s.ogg')    # Slect Cursor
SFX_Cursor_B    = pygame.mixer.Sound('SFX/cursor_b.ogg')    # BacKB Cursor
SFX_Error       = pygame.mixer.Sound('SFX/error.ogg')       # Error Sound

# MUS Code #
MUS_TITLE       = pygame.mixer.music.load('SFX/TITLETEST.ogg')

# Final Checkup #
UpdatePalette()

'''ACTUAL GAME LOOP STARTS'''
while True:
    Player_XPos_Diff = Player_XPos
    Player_YPos_Diff = Player_YPos
    
    Mouse_XPos, Mouse_YPos  = pygame.mouse.get_pos()
    Mouse_Center_X, Mouse_Center_Y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
    Game_Scale_X    = round( (SCREEN_WIDTH  / DEFAULT_WIDTH),2)
    Game_Scale_Y    = round( (SCREEN_HEIGHT / DEFAULT_HEIGHT), 2)
    RelX, RelY      = Mouse_XPos // Game_Scale_X , Mouse_YPos // Game_Scale_Y
    
    if RelX > DEFAULT_WIDTH:
        RelX = DEFAULT_WIDTH
    elif RelX < 0:
        RelX = 0

    if RelY > DEFAULT_HEIGHT:
        RelY = DEFAULT_HEIGHT
    elif RelY < 0:
        RelY = 0
        
    PressedKeys     = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if Demo_Timer < Demo_Timer_Max:
                PixRPG_Demo_CircleWidth     = int(DEFAULT_HEIGHT * 1.33)
                Demo_Timer      = 0         # Just undo that time if we press a key

            if event.key        == K_PRINT:
                ScreenShotting = True

            if event.key        == K_LEFT:
                if Debug_Cheats:
                    Cheats_Parameters -= 1

            if event.key        == K_RIGHT:
                if Debug_Cheats:
                    Cheats_Parameters += 1

            # GUI Browsing     
            if Game_State == 0:
                # If we're not transitioning to a demo, do actions
                if Demo_Timer < Demo_Timer_Max:
                    if event.key        == K_DOWN:
                        PixRPG_Title_Selection += 1
                        Cursor_Vertical = True
                    elif event.key      == K_UP:
                        PixRPG_Title_Selection -= 1
                        Cursor_Vertical = True

                    if event.key        == K_RETURN:
                        Cursor_Select   = True
                    if event.key        == K_ESCAPE:
                        Cursor_Back     = True

            if event.key        == K_SPACE:
                
                if Debug_Cheats:
                    if type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is int:
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] = -All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]]


            if event.key        == K_UP:
                if Debug_Cheats:
                    Cheats_BG -= 1
                    
            if event.key        == K_DOWN:
                if Debug_Cheats:
                    Cheats_BG += 1

            

            if Console_Enabled:
                
                if pygame.key.name(event.key) == "space" or (len (pygame.key.name(event.key)) == 1 and not PressedKeys[K_LALT] and not pygame.key.name(event.key) == "`"):
                    
                    if pygame.key.name(event.key) == "space":
                        Console_Input += " "
                    else:
                        Console_Input += pygame.key.name(event.key)
                    
                # If user is done, parse it
                if pygame.key.name(event.key) == "return" and not PressedKeys[K_LALT]:
                    Console_Parsing = True
                if pygame.key.name(event.key) == "backspace" and not PressedKeys[K_LALT]:
                    Console_Input = Console_Input[:-1]
                
            if PressedKeys[K_LALT]:
                if event.key        == K_RETURN:
                    FullScreen = not FullScreen
                    if FullScreen:
                        SCREEN_WIDTH        = MAX_WIDTH
                        SCREEN_HEIGHT       = MAX_HEIGHT
                        TRUE_DISPLAY        = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS_FULLSCREEN)
                        Game_Scale_X    = round( (SCREEN_WIDTH / DEFAULT_WIDTH),2)
                        Game_Scale_Y    = round( (SCREEN_HEIGHT/ DEFAULT_HEIGHT), 2)
                        CheckingVariables   = True
                        GAME_CLOCK.tick()
                        
                    else:
                        SCREEN_WIDTH    = DEFAULT_WIDTH
                        SCREEN_HEIGHT   = DEFAULT_HEIGHT
                        CheckingVariables   = True
                        TRUE_DISPLAY    = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FLAGS_RESIZABLE)
                        GAME_CLOCK.tick()

                if event.key        == K_F4:
                    pygame.quit()

                # DEBUG TOGGLES DO NOT EDIT #
                if UserTest_EnableDebug:
                    if event.key        == K_i:
                        Debug_DrawText = not Debug_DrawText

                    if event.key        == K_c:
                        Debug_DrawPalette = not Debug_DrawPalette

                    if event.key        == K_b:
                        Debug_BGInfo = not Debug_BGInfo
                        
                    if event.key        == K_s:
                        Debug_DrawScanLines = not Debug_DrawScanLines

                    if event.key        == K_SPACE:
                        Debug_HL_Palette = not Debug_HL_Palette

                    if event.key        == K_r:
                        Debug_Draw_ROT = not Debug_Draw_ROT

                    if event.key        == K_q:
                        Debug_Cheats = not Debug_Cheats

                    if event.key        == K_BACKQUOTE:
                        Console_Enabled     = not Console_Enabled
                        if not Console_Enabled:
                            Console_Input = ""
                            Console_Text2_String = []
                            Console_Text2       = GAME_FONT.render("Type your command here!", 0, Color_Index[2])
        
        if event.type == VIDEORESIZE:
            if not FullScreen:
                SCREEN_WIDTH    = event.w
                SCREEN_HEIGHT   = event.h
                
                if SCREEN_WIDTH > MAX_WIDTH:
                    SCREEN_WIDTH = MAX_WIDTH
                
                if SCREEN_HEIGHT > MAX_HEIGHT:
                    SCREEN_HEIGHT = MAX_HEIGHT
                    
                SAVED_WIDTH     = SCREEN_WIDTH
                SAVED_HEIGHT    = SCREEN_HEIGHT

                CheckingVariables = True
                TRUE_DISPLAY      = pygame.display.set_mode((SAVED_WIDTH, SCREEN_HEIGHT), FLAGS_RESIZABLE)

        if event.type == MOUSEBUTTONUP:
            if Debug_Cheats:
                if event.button == 4:
                    if type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is int:
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] -= Cheats_Interval_Int
                    elif type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is bool:
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] = not All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]]
                    elif type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is float:
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] -= Cheats_Interval_Float
                        
                elif event.button == 5:
                    if type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is int:
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] += Cheats_Interval_Int
                    elif type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is bool: # Horray redundent code
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] = not All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]]
                    elif type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is float:
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] += Cheats_Interval_Float
                    # Choose the one you don't want below ! #

    '''DO ONCES - BACKGROUND'''
    # FailSafe - Cheats Params #
    if Cheats_Parameters < 0:
        Cheats_Parameters = len(All_BGS[Cheats_Parameters] ) - 1
        
    if Cheats_Parameters >= len(list(All_BGS[0].items())):
        Cheats_Parameters = 0
        
    if Cheats_BG < 0:
        Cheats_BG = 0
        
    if Cheats_BG >= len(All_BGS):
        Cheats_BG -= 1
        
    # Update and Render Backgrounds #
    # Check every BG for parameters, then perform a DoOnce, THEN BLIT THE FINAL MATERIAL
    # DoOnce - Subsurface Each BG #

    # KLUDGE - PixRPGs Title is Kludged Together Rather Poorly with LITERALS #
    # Load Game + Title Screen
    if Game_State == 0:
        SCREEN_DISPLAY.blit(PixRPG_Title_BG, (0, 0))
            
        # FAILSAFE - Change stuff if not ready
        if Global_Timer < PixRPG_Title_ReadyTime:
            PixRPG_Title_Selection  = 1
            if Cursor_Vertical:
                Cursor_Vertical     = False
            if Cursor_Horizontal:
                Cursor_Horizontal   = False
            if Cursor_Select:
                Cursor_Select       = False
            if Cursor_Back:
                Cursor_Back         = False
                
        if not PixRPG_Title_Complete:
                
            if int(PixRPG_Title[0][1]) == 22:
                PixRPG_Title_Complete = True
            for x in range (0, len(PixRPG_Title)):
                PixRPG_Title[x][2] -= 2.8

                # BAD KLUDGES HERE, PLEASE REVISE THESE #
                if PixRPG_Title[x][2]       < 24:
                    PixRPG_Title[x][2]      = 24
                    if PixRPG_Title[x][1]   > (22 + (PixRPG_Title[x][0].get_width() * x * 1.2)):
                        PixRPG_Title[x][1]  -= 1.5
                    if PixRPG_Title[x][1]   < 22:
                        PixRPG_Title[x][1]  = 22
                    
                SCREEN_DISPLAY.blit(PixRPG_Title[x][0], (PixRPG_Title[x][1], PixRPG_Title[x][2]))
                for x in range (32 + PixRPG_Title[x][0].get_height(), DEFAULT_HEIGHT):
                    SineX = 32 * sin((x + int(0.5 * 5 + 0.5) + 0.5) / 32) * 1
                    SCREEN_DISPLAY.blit(SCREEN_DISPLAY, (SineX - 50, x), (0, x, DEFAULT_WIDTH, 1))
                
                    
                    
            
        if PixRPG_Title_Complete:
            if PixRPG_Title_Complete_MakeSurf:
                PixRPG_Title_XPos = PixRPG_Title[0][1]
                PixRPG_Title_YPos = PixRPG_Title[0][2]

                # Title Strings in a nice litle 3D list instead #

                # Format:
                # [
                # [GAME FONT, YPOS ],
                # [EXAMPLE 2]
                # ]           END OF ENTRY 0.
                PixRPG_Title_Strings = [
                    # Screen 1 (Main Title)
                    [
                    [GAME_FONT.render("By JackM  2017 = V1.3", 0, Color_Index[2]), 60   ],
                    [GAME_FONT.render("New Game",   0, Color_Index[2]), 90                      ],
                    [GAME_FONT.render("Continue",   0, Color_Index[2]), 105                     ],
                    [GAME_FONT.render("Options",    0, Color_Index[2]), 120                     ],
                    [GAME_FONT.render("Quit",       0, Color_Index[2]), 135                     ],
                    ],

                    # Screen 2 (New File)
                    [
                    [GAME_FONT.render("NEW GAME",       0, Color_Index[2]),      10],
                    [GAME_FONT.render("Select a file to start your adventure!",       0, Color_Index[2]),      32]
                    
                    ],
                    
                    # Screen 3 (Select File)
                    [
                    [GAME_FONT.render("CONTINUE GAME",       0, Color_Index[2]),   10],
                    [GAME_FONT.render("Select a file to start playing!",       0, Color_Index[2]),      32]
                    ],

                    # Screen 4 (Options)
                    [
                    [GAME_FONT.render("OPTIONS",       0, Color_Index[2]),   10],
                    [GAME_FONT.render("SET FULLSCREEN = ",       0, Color_Index[2]),   32],
                    
                    ],

                    # Screen 5 (Quit Screen)

                    [
                    [GAME_FONT.render("REALLY QUIT?",       0, Color_Index[2]),      10],
                    [GAME_FONT.render("YES",       0, Color_Index[2]),      90],
                    [GAME_FONT.render("NO",       0, Color_Index[2]),       105]
                    ],

                ]       # Overall End of Strings!

                # For each string, generate the widths in another table as we cannot 
                '''
                for x in range (len(PixRPG_Title_Strings)):
                    PixRPG_Title_XPoses.append([])
                    for y in range (len(PixRPG_Title_Strings[x])):
                        PixRPG_Title_XPoses[y].append(DEFAULT_WIDTH//2 - (PixRPG_Title_Strings[x][y][0].get_width()// 2))     # Get XPos of Text to Centralize it
                '''

                # Title Strings #
                
                PixRPG_Title = SCREEN_DISPLAY.subsurface(PixRPG_Title_XPos, PixRPG_Title_YPos, PixRPG_Title[5][1] +PixRPG_Title[5][0].get_width() - PixRPG_Title[0][1] , PixRPG_Title[0][0].get_height())
                PixRPG_Title.set_colorkey(Color_Index[0])
                PixRPG_Title_Complete_MakeSurf = False
                
            else:
                if Global_Timer <= PixRPG_Title_ReadyTime:
                    SCREEN_DISPLAY.blit(PixRPG_Title, (PixRPG_Title_XPos, PixRPG_Title_YPos) )
                    
                    
                # Do Onces on the timer
                if Global_Timer == PixRPG_Title_ReadyTime:
                    PixRPG_Title_ReadyTime = 0
                    Global_Timer = 0
                   #pygame.mixer.music.play(-1, 0)
                    
                if Cursor_Back:
                    PixRPG_Title_Selection = PixRPG_Title_Selection_Memory
                    if PixRPG_Title_State != 0:
                        PixRPG_Title_State = 0
                    else:
                        PixRPG_Title_Selection_Memory = PixRPG_Title_Selection
                        PixRPG_Title_Selection  = 2  # Default to NO through ESC Means of Quit
                        PixRPG_Title_State      = 4
                
                if Global_Timer >= PixRPG_Title_ReadyTime:
                    
                    if PixRPG_Title_State == 0:
                        if PixRPG_Title_Selection < 1:
                            PixRPG_Title_Selection = 4
                        elif PixRPG_Title_Selection > 4:
                            PixRPG_Title_Selection = 1
                        PixRPG_Title_Selection_Memory = PixRPG_Title_Selection      # If in menu 0, memorize what selection we're on for when you press esc
                        #SCREEN_DISPLAY.blit(PixRPG_Title, (PixRPG_Title_XPos, PixRPG_Title_YPos))
                        TMP_COPYDISPLAY = SCREEN_DISPLAY
                            
                        for x in range (PixRPG_Title.get_width()):
                            SineX = 3 * sin((x + int(Global_Timer + 0.5) + 0.5) / 16) * 1
                            SCREEN_DISPLAY.blit(PixRPG_Title, (PixRPG_Title_XPos + x, PixRPG_Title_YPos + SineX), (x, 0, 1, PixRPG_Title.get_width()))
                        
                        
                        if Cursor_Select and not Console_Enabled:
                            PixRPG_Title_State = PixRPG_Title_Selection
                            if PixRPG_Title_State == 4:
                                PixRPG_Title_Selection = 2  # Default to NO through Enter Means of Quit
                            else:
                                PixRPG_Title_Selection = 1

                    elif PixRPG_Title_State == 1:
                        if PixRPG_Title_Selection < 1:
                            PixRPG_Title_Selection = 1
                        elif PixRPG_Title_Selection > 1:
                            PixRPG_Title_Selection = 1

                    elif PixRPG_Title_State == 2:
                        if PixRPG_Title_Selection < 1:
                            PixRPG_Title_Selection = 1
                        elif PixRPG_Title_Selection > 1:
                            PixRPG_Title_Selection = 1

                        for icons in range (len(SaveIcons_List)):
                            SCREEN_DISPLAY.blit(SaveIcons_List[icons], (20, 20 + (10 * x)))

                    elif PixRPG_Title_State == 3:
                        if PixRPG_Title_Selection < 1:
                            PixRPG_Title_Selection = 1
                        elif PixRPG_Title_Selection > 1:
                            PixRPG_Title_Selection = 1

                    elif PixRPG_Title_State == 4:
                        
                        if PixRPG_Title_Selection < 1:
                            PixRPG_Title_Selection = 2
                        elif PixRPG_Title_Selection > 2:
                            PixRPG_Title_Selection = 1

                        if Cursor_Select:
                            if PixRPG_Title_Selection == 1:
                                AboutToQuit = True
                                Quit_Timer = 0
                                Quit_Timer_Interval = 0.6
                                Final_Time = (Global_Timer % Global_Timer_Max) + ( (DEFAULT_HEIGHT * 1.4) /Quit_Timer_Interval)  # And yes you cannot overflow this, run into 10 seconds.
                                FutureClockPrev = (Global_Timer % Global_Timer_Max) + (( (DEFAULT_HEIGHT * 1.4) /Quit_Timer_Interval) //10)
                            elif PixRPG_Title_Selection == 2:
                                PixRPG_Title_State  = 0
                                PixRPG_Title_Selection = PixRPG_Title_Selection_Memory

                    SCREEN_DISPLAY.blit(GAME_FONT.render("DEBUG - CHOICE = " +str(PixRPG_Title_Selection), 0, Color_Index[2]), (0, 100))
                    SCREEN_DISPLAY.blit(GAME_FONT.render("DEBUG - MEMORY = " +str(PixRPG_Title_Selection_Memory), 0, Color_Index[2]), (0, 110))
                    SCREEN_DISPLAY.blit(GAME_FONT.render("DEBUG - STATE = " +str(PixRPG_Title_State), 0, Color_Index[2]), (0, 120))

                    for x in range (0, len(PixRPG_Title_Strings[PixRPG_Title_State])):
                        SCREEN_DISPLAY.blit(PixRPG_Title_Strings[PixRPG_Title_State][x][0], (DEFAULT_WIDTH//2 - (PixRPG_Title_Strings[PixRPG_Title_State][x][0].get_width()//2), PixRPG_Title_Strings[PixRPG_Title_State][x][1]))

                    SCREEN_DISPLAY.blit(PixRPG_Title_Pointer, (DEFAULT_WIDTH//2 - (PixRPG_Title_Strings[PixRPG_Title_State][PixRPG_Title_Selection][0].get_width()//2) - (PixRPG_Title_Pointer.get_width() * 2),  PixRPG_Title_Strings[PixRPG_Title_State][PixRPG_Title_Selection][1] + (PixRPG_Title_Pointer.get_width() // 2)))
                    
                    Demo_Timer += 1
                    if Demo_Timer >= Demo_Timer_Max:
                        if PixRPG_Demo_CircleWidth == PixRPG_Demo_MaxWidth:
                            pygame.mixer.music.fadeout(CONST_MILLISECONDS * 120)
                        BlackScreen.fill (Color_Index[0])
                        PixRPG_Demo_TextureMask = pygame.draw.circle(BlackScreen, Color_Index[1], (DEFAULT_WIDTH//2, DEFAULT_HEIGHT//2), PixRPG_Demo_CircleWidth, 0)
                        
                        PixRPG_Demo_CircleWidth -= 2    # Must be int!
                        SCREEN_DISPLAY.blit(BlackScreen, (0, 0))
                        
                        # Negatives are impossible as the check overwrites it beforehand
                        if PixRPG_Demo_CircleWidth <= 0:
                            Global_Timer            = 0     # Set global timer to 0 for demo purposes
                            Demo_Timer              = 0     # And the demo timer to ensure it doesnt bug over when the demo is done
                            PixRPG_Demo_CircleWidth = 0     # And the circles width should then fix itself to 0 in case it's negative
                            SCREEN_DISPLAY.fill     (Color_Index[0])    # Fill screen with nothing
                            Game_State              = 1     # And force game into demo mode by loading Mode 1
                            PixRPG_Demo             = True  # Enable Demo
                            Player_InControl        = False # Disable Player Movements until end of demo

                    
            
    elif Game_State == 1:           # World Screen #
        SCREEN_DISPLAY.fill(Color_Index[248])     # Fill with Color 32 (Sky)
        
        
        # Are we in the demo?
        if PixRPG_Demo:
            
            if PixRPG_Demo_CircleWidth <= PixRPG_Demo_MaxWidth and PixRPG_Demo_CircleWidth >= 0:

                # Create Screen FX, fill entire surface black, then draw a secondary circle on top
                BlackScreen.fill (Color_Index[0])
                PixRPG_Demo_TextureMask = pygame.draw.circle(BlackScreen, Color_Index[1], (DEFAULT_WIDTH//2, DEFAULT_HEIGHT//2), PixRPG_Demo_CircleWidth, 0)
                PixRPG_Demo_CircleWidth += 2    # Must be int!
                
                # Render Black Screen with Circle on top, which has the circle masked out of it, allowing us to see through
                SCREEN_DISPLAY.blit(BlackScreen, (0, 0))    

        else:
            
            # If the player is in control, let them move, movement can still occur elsewhere and in demos #
            if Player_InControl and not Console_Enabled:
                
                Moving_Diagonal = False
                Moving = False
                if PressedKeys[K_w]:
                    
                    MovingUp = True
                else:
                    MovingUp = False
                    
                if PressedKeys[K_a]:
                    MovingLeft = True
                else:
                    MovingLeft = False
                    
                    
                if PressedKeys[K_s]:
                    MovingDown = True
                else:
                    MovingDown = False
                    
                if PressedKeys[K_d]:
                    MovingRight = True
                else:
                    MovingRight = False


                if MovingLeft and MovingRight:
                    MovingLeft = False
                    MovingRight = False

                if MovingUp and MovingDown:
                    MovingUp = False
                    MovingDown = False 

                if PressedKeys[K_SPACE]:
                    if Running:
                        Running = False
                        Running_Timer = 0
                    else:
                        Running_Timer += 1
                        if Running_Timer >= Running_Timer_Max:
                            Running_Timer = Running_Timer_Max
                else:
                    if Running_Timer == Running_Timer_Max:
                        Running = True
                        Diagonal_Direction = Player_Direction
                    else:
                        Running_Timer = 0


                if Running:
                    Moving_Diagonal_MaxTime = Moving_Diagonal_RunT
                else:
                    Moving_Diagonal_MaxTime = Moving_Diagonal_WalkT
                    
                if MovingUp or MovingDown or MovingLeft or MovingRight:
                    Moving = True
                
            if Running:
                
                if MovingUp:
                    Player_Direction = 4
                    
                if MovingDown:
                    Player_Direction = 0
                    
                if MovingLeft:
                    Player_Direction = 6
                    
                if MovingRight:
                    Player_Direction = 2
                    
                if MovingUp and MovingLeft:
                    Player_Direction = 5
                    Moving_Diagonal = True
                    
                if MovingUp and MovingRight:
                    Player_Direction = 3
                    Moving_Diagonal = True
                    
                if MovingDown and MovingLeft:
                    Player_Direction = 7
                    Moving_Diagonal = True
                    
                if MovingDown and MovingRight:
                    Player_Direction = 1
                    Moving_Diagonal = True
                    
                if Player_Direction == 0 or Player_Direction == 1 or Player_Direction == 7:     # DOWN
                    Player_YChange = Player_RunSpeed
                if Player_Direction == 3 or Player_Direction == 4 or Player_Direction == 5:   # UP
                    Player_YChange = -Player_RunSpeed
                    
                if Player_Direction == 1 or Player_Direction == 2 or Player_Direction == 3:      # RIGHT
                    Player_XChange = Player_RunSpeed
                if Player_Direction == 5 or Player_Direction == 6 or Player_Direction == 7:      # LEFT
                    Player_XChange = -Player_RunSpeed
                    
            elif Moving:
                Running_Timer = 0
                    
                if MovingUp:
                    Player_Direction = 4
                    Player_YChange = -Player_Speed
                    
                if MovingDown:
                    Player_Direction = 0
                    Player_YChange = Player_Speed
                    
                if MovingLeft:
                    Player_Direction = 6
                    Player_XChange = -Player_Speed
                    
                if MovingRight:
                    Player_XChange = Player_Speed
                    Player_Direction = 2
                    
                if MovingUp and MovingLeft:
                    Player_Direction = 5
                    Moving_Diagonal = True
                    
                elif MovingUp and MovingRight:
                    Player_Direction = 3
                    Moving_Diagonal = True
                    
                elif MovingDown and MovingLeft:
                    Player_Direction = 7
                    Moving_Diagonal = True
                    
                elif MovingDown and MovingRight:
                    Player_Direction = 1
                    Moving_Diagonal = True


                Player_WalkFrame += 1
                Player_WalkFrame %= Player_Walk_I_End

                if Player_WalkFrame     in range(Player_Walk_L_Start, Player_Walk_L_End):
                    Player_WalkCycle = 0
                elif Player_WalkFrame   in range(Player_Walk_L_End, Player_Walk_R_Start) or Player_WalkFrame   in range(Player_Walk_R_End, Player_Walk_I_End):
                    Player_WalkCycle = 1
                elif Player_WalkFrame   in range(Player_Walk_R_Start, Player_Walk_R_End):
                    Player_WalkCycle = 2

                else:
                    Player_WalkCycle = 0

            else:
                Player_WalkFrame = 0
                Player_WalkCycle = 1
                Player_XChange = 0
                Player_YChange = 0

            if Moving_Diagonal:
                Diagonal_Direction = Player_Direction
                Moving_Diagonal_Time    = 0
            else:
                Moving_Diagonal         = False
                Moving_Diagonal_Time    += 1
                if Moving_Diagonal_Time >= Moving_Diagonal_MaxTime:
                    Moving_Diagonal_Time = Moving_Diagonal_MaxTime
                
            if Moving_Diagonal_Time < Moving_Diagonal_MaxTime:
                Player_Direction = Diagonal_Direction
                    
            Player_XPos += Player_XChange
            Player_YPos += Player_YChange

            # Proc - Prevent movement sticking #
            if not (MovingLeft or MovingRight):
                Player_XChange = 0
            if not (MovingUp or MovingDown):
                Player_YChange = 0
            
            # Apply Cancel Outs
            # Disable going below Tile 0
            if Player_XPos < 0:
                Running = False
                Running_Timer = 0
                Player_XPos = 0
                if not (MovingUp or MovingDown):
                    Moving = False
                    
            # Disable going off Row 1    
            if Player_YPos < 0:
                Player_YPos = 0
                if not (MovingLeft or MovingRight):
                    Moving = False
                    Running = False
                    Running_Timer = 0
                    
        
        # Draw Tiles! #
        # Find Tile Range to be rendered

        Current_Tile_XPos   = Player_XPos % Tile_Length
        Current_Tile_YPos   = Player_YPos % Tile_Length
        #if Cols_Max > len(TheWorld[Rows_Max] - 1):
         #   Cols_Max = len(TheWorld[Rows_Max] - 1)
        
        for rows in range (0   ,  1):
           for cols in range (0   , 1):
               SCREEN_DISPLAY.blit(TILES.subsurface ( (Tile_Length * TheWorld[rows][cols]) % Max_Tiles_X  , Tile_Length * TheWorld[rows][cols] // Max_Tiles_Y, Tile_Length, Tile_Length), (-Player_XPos + Player_Hitbox_XPos + (Tile_Length * rows) , -Player_YPos + Player_Hitbox_YPos + (Tile_Length * cols) ) )
              # Max_Tiles_X

        pygame.draw.rect(SCREEN_DISPLAY, Color_Index[0], (Player_Hitbox_XPos, Player_Hitbox_YPos, Player_Hitbox_Width, Player_Hitbox_Height), 1)
        SCREEN_DISPLAY.blit(SPRITES.subsurface( (Player_Render_XPos + (Player_Render_Width * Player_Direction), Player_Render_YPos + (Player_Render_Height * Player_WalkCycle), Player_Render_Width, Player_Render_Height) ), (Player_Blit_XPos, Player_Blit_YPos))
        #SCREEN_DISPLAY.blit(TEST, (0, 0) )

    elif Game_State == 2:
        SCREEN_DISPLAY.fill(Color_Index[0])     # Fill with Color 32 (Sky)
        
        for BG in range (0, len(Rendered_BG_IDs)):
            if All_BGS[BG]['IsRendered']:
                
                # Backgrounds - Failsafe Values (Can be under-run in BG Debug, etc) and in INIT
                if All_BGS[BG]['DoOnceFailSafe']:
                    if  All_BGS[BG]['SineSize'] < 1:
                        All_BGS[BG]['SineSize'] = 1
                        
                    if  All_BGS[BG]['SineIgnoreLines'] < 1:
                        All_BGS[BG]['SineIgnoreLines'] = 1

                    if  All_BGS[BG]['TileType'] > 3:
                        All_BGS[BG]['TileType'] = 3
                        
                    if  All_BGS[BG]['TileType'] < 0:
                        All_BGS[BG]['TileType'] = 0

                    if  All_BGS[BG]['ForceWidth'] <= 0:
                        All_BGS[BG]['ForceWidth'] = 1

                    if  All_BGS[BG]['ForceHeight'] <= 0:
                        All_BGS[BG]['ForceHeight'] = 1

                    if  All_BGS[BG]['TexWidth'] <= 0:
                        All_BGS[BG]['TexWidth'] = 1

                    if  All_BGS[BG]['TexHeight'] <= 0:
                        All_BGS[BG]['TexHeight'] = 1

                    if  All_BGS[BG]['ScrollTime'] <= 0:
                        All_BGS[BG]['ScrollTime'] = 1
                    
                    if  All_BGS[BG]['TexXPos'] < 0:
                        All_BGS[BG]['TexXPos'] = All_BGS[BG]['Source'].get_width() - All_BGS[BG]['TexWidth']
                        
                    elif All_BGS[BG]['TexXPos'] > All_BGS[BG]['Source'].get_width() - All_BGS[BG]['TexWidth']:
                        All_BGS[BG]['TexXPos'] = 0

                    if  All_BGS[BG]['TexYPos'] < 0:
                        All_BGS[BG]['TexYPos'] = All_BGS[BG]['Source'].get_height() - All_BGS[BG]['TexHeight']
                        
                    elif All_BGS[BG]['TexYPos'] > All_BGS[BG]['Source'].get_height() - All_BGS[BG]['TexHeight']:
                        All_BGS[BG]['TexYPos'] = 0

                    if  All_BGS[BG]['SineFreq']  == 0:
                        All_BGS[BG]['SineFreq']   = 1
                        
                    if All_BGS[BG]['ScrollBaseID'] not in   COLPAL_TILES_BGS:
                        if      All_BGS[BG]['ScrollBaseID']      < COLPAL_TILES_BGS[0]:
                                All_BGS[BG]['ScrollBaseID']     = COLPAL_TILES_BGS[0]
                        elif    All_BGS[BG]['ScrollBaseID']    > COLPAL_TILES_BGS[len(COLPAL_TILES_BGS) -1]:
                                All_BGS[BG]['ScrollBaseID']     = COLPAL_TILES_BGS[len(COLPAL_TILES_BGS) -1]

                    if type(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]) is float:
                        All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]] = round(All_BGS[Cheats_BG][list(All_BGS[Cheats_BG].keys())[Cheats_Parameters]], 2)

                    if len(All_BGS[BG]['NonScrollColors']) == 0:
                        All_BGS[BG]['NonScrollIDs'] = []
                        All_BGS[BG]['NonScrollColors'] = [(0,0,0)]
                        
                    elif len(All_BGS[BG]['NonScrollColors']) < len(All_BGS[BG]['NonScrollIDs']):
                        TEMP_MissingElements = len(All_BGS[BG]['NonScrollIDs']) - len(All_BGS[BG]['NonScrollColors'])
                        for x in range (0, TEMP_MissingElements):
                            All_BGS[BG]['NonScrollColors'].append(All_BGS[BG]['NonScrollColors'][len(All_BGS[BG]['NonScrollColors']) -1])
                        del TEMP_MissingElements
                    
                    All_BGS[BG]['DoOnceFailSafe'] = False

                if All_BGS[BG]['DoOnceLoading']:
                    
                    for x in range(0, len(All_BGS[BG]['NonScrollIDs'])):
                        Color_Index[All_BGS[BG]['NonScrollIDs'][x]] = All_BGS[BG]['NonScrollColors'][x]
                        
                    All_BGS[BG]['Source'].set_palette(Color_Index)
                    All_BGS[BG]['Texture']   = All_BGS[BG]['Source'].subsurface(All_BGS[BG]['TexXPos'], All_BGS[BG]['TexYPos'], All_BGS[BG]['TexWidth'], All_BGS[BG]['TexHeight'])
                    
                    if All_BGS[BG]['TexFlippedX'] or All_BGS[BG]['TexFlippedY']:
                        All_BGS[BG]['Texture']       = pygame.transform.flip(All_BGS[BG]['Texture'], All_BGS[BG]['TexFlippedX'], All_BGS[BG]['TexFlippedY'])
                    if All_BGS[BG]['IsResized']:
                        All_BGS[BG]['Texture']       = pygame.transform.scale(All_BGS[BG]['Texture'], (All_BGS[BG]['ForceWidth'], All_BGS[BG]['ForceHeight']))

                    if All_BGS[BG]['IsTiled']:
                        TEMP_Surface = pygame.Surface((All_BGS[BG]['Texture'].get_width() * (DEFAULT_WIDTH//All_BGS[BG]['Texture'].get_width() + 1), All_BGS[BG]['Texture'].get_height() * (DEFAULT_HEIGHT//All_BGS[BG]['Texture'].get_height() + 1)), HWSURFACE, 8)
                        TEMP_Surface.set_palette(Color_Index)
                        
                        # Normal Mode, tile as normal until you fill screen
                        for x in range (0, DEFAULT_WIDTH//All_BGS[BG]['Texture'].get_width() + 1):
                            for y in range (0, DEFAULT_HEIGHT//All_BGS[BG]['Texture'].get_height() + 1):
                                TEMP_Surface.blit(All_BGS[BG]['Texture'], (All_BGS[BG]['Texture'].get_width() * x, All_BGS[BG]['Texture'].get_height() * y))

                        # HMirror - Render one Half as normal, then render on another half HORIZONTALLY   
                        if All_BGS[BG]['TileType'] == 1:
                            TEMP_Surface1   = TEMP_Surface.copy()
                            TEMP_Surface1   = TEMP_Surface1.subsurface((0, 0, TEMP_Surface.get_width(), TEMP_Surface.get_height()))
                            TEMP_Surface2   = pygame.transform.flip(TEMP_Surface1, True, False)
                            TEMP_Surface.blit(TEMP_Surface2, (DEFAULT_WIDTH//2, 0))
                            
                        # VMirror - Render one Half as normal, then render on another half VERTICALLY   
                        elif All_BGS[BG]['TileType'] == 2:
                            TEMP_Surface1   = TEMP_Surface.copy()
                            TEMP_Surface1   = TEMP_Surface1.subsurface((0, 0, DEFAULT_WIDTH, DEFAULT_HEIGHT//2))
                            TEMP_Surface2   = pygame.transform.flip(TEMP_Surface1, False, True)
                            TEMP_Surface.blit(TEMP_Surface2, (0, DEFAULT_HEIGHT//2))
                            
                        # VHMirror - Render one Half as normal, then render on another half OMNI
                        elif All_BGS[BG]['TileType'] == 3:
                            TEMP_Surface1   = TEMP_Surface.copy()
                            TEMP_Surface1   = TEMP_Surface1.subsurface((0, 0, DEFAULT_WIDTH//2, DEFAULT_HEIGHT//2))
                            TEMP_Surface2   = pygame.transform.flip(TEMP_Surface1, True, False)
                            TEMP_Surface.blit(TEMP_Surface2, (DEFAULT_WIDTH//2, 0))
                            TEMP_Surface1   = TEMP_Surface.copy()
                            TEMP_Surface1   = TEMP_Surface1.subsurface((0, 0, DEFAULT_WIDTH, DEFAULT_HEIGHT//2))
                            TEMP_Surface2   = pygame.transform.flip(TEMP_Surface1, False, True)
                            TEMP_Surface.blit(TEMP_Surface2, (0, DEFAULT_HEIGHT//2))
                        
                        elif All_BGS[BG]['TileType'] == 2:
                            # 2 Mirror Mode Verti (FORCE RESIZES TO HALF SCREEN BTW) #
                            for x in range (0, ( DEFAULT_WIDTH//All_BGS[BG]['Texture'].get_width() + 2) //2):
                                for y in range (0, (DEFAULT_HEIGHT//All_BGS[BG]['Texture'].get_height() + 2)//2):
                                    TEMP_Surface.blit(All_BGS[BG]['Texture'], (All_BGS[BG]['Texture'].get_width() * x, All_BGS[BG]['Texture'].get_height() * y))

                        elif All_BGS[BG]['TileType'] == 3:
                            # 4 Way Mirror Mode (FORCE RESIZES TO HALF SCREEN BTW) #
                            for x in range (0, ( DEFAULT_WIDTH//All_BGS[BG]['Texture'].get_width() + 2) //2):
                                for y in range (0, (DEFAULT_HEIGHT//All_BGS[BG]['Texture'].get_height() + 2)//2):
                                    TEMP_Surface.blit(All_BGS[BG]['Texture'], (All_BGS[BG]['Texture'].get_width() * x, All_BGS[BG]['Texture'].get_height() * y))
                        
                        All_BGS[BG]['Texture'] = TEMP_Surface
                        del TEMP_Surface
                        
                    # DONOTCHANGE, SKY COLOR IS IGNORED ??
                    # SKY IS COLORKEY, I AM AWARE THIS SOUNDS REDUNDENT AS WE COULD JUST RENDER 0 BUT ITS BECAUSE "SKY" WON'T UPDATE PROPERLY BUT WE CAN REMOVE THIS
                    All_BGS[BG]['Texture'].set_colorkey(Color_Index[0])
                    if All_BGS[BG]['TexRot'] != 0:
                        All_BGS[BG]['Texture'] = pygame.transform.rotate(All_BGS[BG]['Texture'], All_BGS[BG]['TexRot'])
                    All_BGS[BG]['DoOnceLoading'] = False
                    


                # IF The Palette Scrolls, Update the Colors #
                if All_BGS[BG]['DoOncePalette']:
                    for x in range (0, len(All_BGS[BG]['ScrollColors'])):
                        Color_Index[ All_BGS[BG]['ScrollBaseID'] + x] = All_BGS[BG]['ScrollColors'][(x - All_BGS[BG]['ScrollAmount']) % len(All_BGS[BG]['ScrollColors'])]
                    All_BGS[BG]['Texture'].set_palette(Color_Index)
                    All_BGS[BG]['DoOncePalette'] = False

                # If Pally is Scroll #
                if All_BGS[BG]['PaletteIsScroll']:
                    if Global_Timer % All_BGS[BG]['ScrollTime'] == 0:
                        
                        # A Ping-Pong Palette means the Palette increases, then decreases when it hits the end, back and forth.
                        if All_BGS[BG]['ScrollBackwards']:
                            All_BGS[BG]['ScrollAmount'] -= 1
                        else:
                            All_BGS[BG]['ScrollAmount'] += 1
                            
                        # Limit the thingmagick so it won't load an invalid color #
                        if All_BGS[BG]['ScrollAmount'] >= len(All_BGS[BG]['ScrollColors']) -1:
                            All_BGS[BG]['ScrollAmount'] = len(All_BGS[BG]['ScrollColors'])-1
                            
                            if All_BGS[BG]['ScrollPingPong']:
                                All_BGS[BG]['ScrollBackwards'] = True
                            else:
                                All_BGS[BG]['ScrollAmount'] = 0

                        if All_BGS[BG]['ScrollAmount'] <  0:
                            All_BGS[BG]['ScrollAmount'] = 0

                        if All_BGS[BG]['ScrollPingPong']:
                            if All_BGS[BG]['ScrollAmount'] <= 0:
                                All_BGS[BG]['ScrollBackwards'] = False
                        
                        # Finally, Perform Update Palette #
                        All_BGS[BG]['DoOncePalette']    = True

                
                
                All_BGS[BG]['SineXOffset'] += All_BGS[BG]['SineXChange']
                All_BGS[BG]['SineYOffset'] += All_BGS[BG]['SineYChange']
                
                if All_BGS[BG]['SineLoops']:
                    if All_BGS[BG]['SineXOffset'] > All_BGS[BG]['Texture'].get_width():
                        All_BGS[BG]['SineXOffset'] = 0
                    elif All_BGS[BG]['SineXOffset'] < 0:
                        All_BGS[BG]['SineXOffset'] = All_BGS[BG]['Texture'].get_width()

                    if All_BGS[BG]['SineYOffset'] > All_BGS[BG]['Texture'].get_height():
                        All_BGS[BG]['SineYOffset'] = 0
                    elif All_BGS[BG]['SineYOffset'] < 0:
                        All_BGS[BG]['SineYOffset'] = All_BGS[BG]['Texture'].get_height()

                    if All_BGS[BG]['SineIgnoreLines'] == 0:
                        All_BGS[BG]['SineIgnoreLines'] = 1
                 
                if not All_BGS[BG]['SinePaused']:
                    All_BGS[BG]['SineTime'] = Global_Timer
                    
                if not All_BGS[BG]['SineVert']:
                    FinalX      = All_BGS[BG]['SineXOffset']
                    Distance_Y  = All_BGS[BG]['SineYOffset']
                    
                    for y in range (0, All_BGS[BG]['Texture'].get_height() , All_BGS[BG]['SineSize']):
                        
                            if y % All_BGS[BG]['SineIgnoreLines'] == 0:
                                
                                if All_BGS[BG]['SineXMult'] != 0:
                                    Distance_X = (x + int(All_BGS[BG]['SineAmp'] * All_BGS[BG]['WaveType']((y + int(All_BGS[BG]['SineTime'] * All_BGS[BG]['SineSpeed'] + 0.5) + 0.5) / All_BGS[BG]['SineFreq']) + 0.5) * All_BGS[BG]['SineXMult'] ) + All_BGS[BG]['SineXOffset']

                                    FinalX = Distance_X #int(Distance_X/2 + 0.5 + All_BGS[BG]['SineXOffset'])
                                    if All_BGS[BG]['SineLoops']:
                                        FinalX %= All_BGS[BG]['Texture'].get_width()
                                Distance_Y = (y + int(All_BGS[BG]['SineAmp'] * All_BGS[BG]['WaveType']((y + int(All_BGS[BG]['SineTime'] * All_BGS[BG]['SineSpeed'] + 0.5) + 0.5) / All_BGS[BG]['SineFreq']) + 0.5) * All_BGS[BG]['SineYMult'] ) + All_BGS[BG]['SineYOffset']
                                if All_BGS[BG]['SineLoops']:
                                    if Distance_Y < 0:
                                            Distance_Y      +=  All_BGS[BG]['Texture']               .get_height()
                                            Distance_Y      =   Distance_Y % All_BGS[BG]['Texture']  .get_height()
                                            
                                    elif    Distance_Y      >=   All_BGS[BG]['Texture']              .get_height():
                                            Distance_Y      -=  All_BGS[BG]['Texture']               .get_height()
                                            Distance_Y      =   Distance_Y % All_BGS[BG]['Texture']  .get_height()
                                else:
                                    
                                    if      Distance_Y      <   0:
                                            Distance_Y      =   All_BGS[BG]['Texture']               .get_height()
                                            
                                    elif    Distance_Y      >=  All_BGS[BG]['Texture']               .get_height() :
                                            Distance_Y      =   All_BGS[BG]['Texture']               .get_height()
                                            
                                if All_BGS[BG]['SineLoops']:
                                    FinalX = FinalX % All_BGS[BG]['Texture'].get_width()
                                    if FinalX < 0:
                                        SCREEN_DISPLAY.blit ( All_BGS[BG]['Texture'], ( 0, y ) , (FinalX + All_BGS[BG]['Texture'].get_width(), Distance_Y, All_BGS[BG]['Texture'].get_width(), All_BGS[BG]['SineSize'] ) )
                                    elif FinalX > 0:
                                        SCREEN_DISPLAY.blit ( All_BGS[BG]['Texture'], ( 0, y ) , (FinalX - All_BGS[BG]['Texture'].get_width(), Distance_Y, All_BGS[BG]['Texture'].get_width(), All_BGS[BG]['SineSize'] ) )
                                SCREEN_DISPLAY.blit (All_BGS[BG]['Texture'], ( 0, y ) , (FinalX, Distance_Y, All_BGS[BG]['Texture'].get_width(), All_BGS[BG]['SineSize']) )
                            
                elif All_BGS[BG]['SineVert'] == 1:
                    FinalY      = All_BGS[BG]['SineYOffset']
                    Distance_X  = All_BGS[BG]['SineXOffset']
                    
                    for x in range (0, All_BGS[BG]['Texture'].get_width(), All_BGS[BG]['SineSize']):
                        if x % All_BGS[BG]['SineIgnoreLines'] == 0:
                        
                            if All_BGS[BG]['SineYMult'] != 0:
                                Distance_Y = All_BGS[BG]['SineAmp'] * All_BGS[BG]['WaveType']((x + int(All_BGS[BG]['SineTime'] * All_BGS[BG]['SineSpeed'] + 0.5) + 0.5) / All_BGS[BG]['SineFreq']) * All_BGS[BG]['SineYMult']
                                FinalY = int(Distance_Y/2 + 0.5 + All_BGS[BG]['SineYOffset'])
                                if All_BGS[BG]['SineLoops']:
                                    FinalY %= All_BGS[BG]['Texture'].get_height()
                        
                            
                            Distance_X = (x + int(All_BGS[BG]['SineAmp'] * All_BGS[BG]['WaveType']((x + int(All_BGS[BG]['SineTime'] * All_BGS[BG]['SineSpeed'] + 0.5) + 0.5) / All_BGS[BG]['SineFreq']) + 0.5) * All_BGS[BG]['SineXMult'] ) + All_BGS[BG]['SineXOffset']
                            if All_BGS[BG]['SineLoops']:
                                if Distance_X < 0:
                                        Distance_X      +=  All_BGS[BG]['Texture'].get_width()
                                        Distance_X      =   Distance_X % All_BGS[BG]['Texture'].get_width()
                                        
                                elif    Distance_X      >=  All_BGS[BG]['Texture'].get_width():
                                        Distance_X      -=  All_BGS[BG]['Texture'].get_width()
                                        Distance_X      =   Distance_X % All_BGS[BG]['Texture'].get_width()
                            else:
                                
                                if      Distance_X      <   0:
                                        Distance_X      =   All_BGS[BG]['Texture'].get_width()
                                        
                                elif    Distance_X      >=  All_BGS[BG]['Texture'].get_width():
                                        Distance_X      =   All_BGS[BG]['Texture'].get_width()
                                        
                            if All_BGS[BG]['SineLoops']:
                                FinalY = FinalY % All_BGS[BG]['Texture'].get_height()
                                if FinalY < 0:
                                    SCREEN_DISPLAY.blit (All_BGS[BG]['Texture'], ( x, 0 ) , (Distance_X, FinalY + All_BGS[BG]['Texture'].get_height(), All_BGS[BG]['SineSize'], All_BGS[BG]['Texture'].get_height() ) )
                                elif FinalY > 0:
                                    SCREEN_DISPLAY.blit (All_BGS[BG]['Texture'], ( x, 0 ) , (Distance_X, FinalY - All_BGS[BG]['Texture'].get_height(), All_BGS[BG]['SineSize'], All_BGS[BG]['Texture'].get_height() ) )
                            SCREEN_DISPLAY.blit (All_BGS[BG]['Texture'], ( x, 0 ) , (Distance_X, FinalY, All_BGS[BG]['SineSize'], All_BGS[BG]['Texture'].get_height()) )
                            

                
                            
                # MISC - IF CHEATING, ALWAYS ENABLE DoOnces
                if Debug_Cheats or Debug_DrawPalette:
                    All_BGS[BG]['DoOncePalette']    = True
                    All_BGS[BG]['DoOnceLoading']    = True
                    All_BGS[BG]['DoOnceFailSafe']   = True

    if not Global_Timer_Paused:
        Global_Timer += Global_Timer_TimeScale
    Line1 = GAME_FONT.render("COLPAL (ALT + C)", 0, Color_Index[2], Color_Index[3])


    # DEBUG - GAME CONSOLE #
    if Console_Enabled:
        TEMP_SURFACE = pygame.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        TEMP_SURFACE.fill(Color_Index[0])
        TEMP_SURFACE.set_alpha(192)
        SCREEN_DISPLAY.blit(TEMP_SURFACE, (0,0))
        
        Console_Text = GAME_FONT.render(Console_Input, 0, Color_Index[2])
        Console_Watermark = GAME_FONT.render("Console Enabled [ALT + `], TYPE CVARLIST for cmds", 0, Color_Index[2])

        if len(Console_Input) > 0:
            Console_Text2_String = []
            
        
        
        TEMP_SURFACE = pygame.Surface((8,8))
        TEMP_SURFACE.fill(Color_Index[2])
        if len(Console_Text2_String) == 0:
            if Global_Timer % GAME_FPS > GAME_FPS//2:
                SCREEN_DISPLAY.blit(TEMP_SURFACE, (Console_Text.get_width(),0))

        
        SCREEN_DISPLAY.blit(Console_Text, (0,0))
        SCREEN_DISPLAY.blit(Console_Watermark, (DEFAULT_WIDTH - Console_Watermark.get_width(), DEFAULT_HEIGHT - Console_Watermark.get_height()))
        
        for x in range (0, len(Console_Text2_String)):
            Console_Text2 = GAME_FONT.render(Console_Text2_String[x], 0, Color_Index[2])
            SCREEN_DISPLAY.blit(Console_Text2, (0,   Console_Text.get_height() * x ))
        
        if Console_Parsing:
            Console_Input = Console_Input.upper()
            Console_Allowed_Inputs = ["CVARLIST","ABOUT","BGS","SETPOS","FREEZE","COLPAL","GETTIME","TIMESCALE","SETFPS", "QQQ"]

            # Here's how CVAR VALUE works #
            # One the first space, break the string into two: The CVAR and Value
            if " " in Console_Input:
                Console_Input = ' '.join(Console_Input.split())
                Console_NumSpaces = Console_Input.count(" ")
                for x in range (1, Console_NumSpaces + 1):
                    Console_Parameter.append(Console_Input.split(" ")[x])
                Console_Input       = Console_Input.split(" ")[0]
            
            if Console_Input in Console_Allowed_Inputs:
                
                if Console_Input == Console_Allowed_Inputs[0]:          # CVARLIST  - 0
                    Console_Text2_String = [str(Console_Allowed_Inputs)]
                    
                if Console_Input == Console_Allowed_Inputs[1]:          # ABOUT     - 1
                    Console_Text2_String = ["PixRPG by JackM  (V1.3 - 12/01/2017)" ,"(V1.3 - 12/01/2017) V1.3.141", "Rev Date 12/01/2017. Additionally, this is a test of the linebreak system"]
                    
                elif Console_Input == Console_Allowed_Inputs[2]:        # BGS       - 2
                    Console_Text2_String = ["Current Rendered BG IDS" +str(Rendered_BG_IDs)]

                elif Console_Input == Console_Allowed_Inputs[3]:        # SETPOS      - 3

                    if len(Console_Parameter) == 0:
                        Console_Text2_String = ["Set your X and Y Position to anything; beware of bugs and sequence breaks!"]
                    
                    for params in range (0, len(Console_Parameter)):
                        
                        if Console_Parameter[params].isdigit():
                            if params == 0:
                                Player_XPos = int(Console_Parameter[0])
                            else:
                                Player_YPos = int(Console_Parameter[1])
                                
                            Console_Text2_String = ["Poof! Set Players Location to " +str(Player_XPos) +"," +str(Player_YPos) +"!"]
                        else:
                            Console_Text2_String = ["Invalid Pos (2 Args, X/YPos)!"]
                            break
                        
                elif Console_Input == Console_Allowed_Inputs[4]:        # FREEZE    - 4
                    Global_Timer_Paused = not Global_Timer_Paused
                    if Global_Timer_Paused:
                        Console_Text2_String = ["Froze the Global Timer!"]
                    else:
                        Console_Text2_String = ["Unfroze the Global Timer!"]
                    

                elif Console_Input == Console_Allowed_Inputs[5]:        # COLPAL    - 5
                    Debug_DrawPalette = not Debug_DrawPalette

                elif Console_Input == Console_Allowed_Inputs[6]:        # GETTIME    - 6
                    Console_Text2_String = ["GT = " +str(Global_Timer), "Timer Interval = " +str(Global_Timer_TimeScale) ]

                elif Console_Input == Console_Allowed_Inputs[7]:        # TIMESCALE    - 7
                    try:
                        if len(Console_Parameter) == 1:
                            Global_Timer_TimeScale = float(Console_Parameter[0])
                            if Global_Timer_TimeScale < 0:
                                Global_Timer_TimeScale = 0
                            Console_Text2_String = ["Set TimeScale to " +str(Global_Timer_TimeScale) +"!"]
                        else:
                            Console_Text2_String = ["Invalid (1 ARG FLOAT)-Current TimeScale = " +str(Global_Timer_TimeScale)]
                        
                    except:
                        Console_Text2_String = ["Invalid TimeScale!"]
                        
                elif Console_Input == Console_Allowed_Inputs[8]:        # SETFPS    - 8
                    for params in range (0, len(Console_Parameter)):
                        if Console_Parameter[params].isdigit():
                            GAME_FPS = int(Console_Parameter[0])
                            Console_Text2_String = ["Set FPS to " +str(GAME_FPS) +"! (DEFAULT = 60)"]
                        else:
                            Console_Text2_String = ["Invalid FPS (<0 or not INT)"]

                elif Console_Input == Console_Allowed_Inputs[9]:        # QQQ    - 9
                    pygame.quit()
            else:
                Console_Text2_String = ["Invalid CVAR!"]
                SFX_Error.play()

                

            # TRUNCATE Console Output if length is longer than width of screen
            CONSOLE_WHILELOOP = 0
            while CONSOLE_WHILELOOP != len(Console_Text2_String):
                if len(Console_Text2_String[CONSOLE_WHILELOOP]) > FONT_MAX_W:
                    Console_Text2_String_Copy = Console_Text2_String[CONSOLE_WHILELOOP][FONT_MAX_W:]
                    Console_Text2_String.insert(CONSOLE_WHILELOOP + 1, Console_Text2_String_Copy)       # If text of one line is too long, break to next line
                    Console_Text2_String[CONSOLE_WHILELOOP] = Console_Text2_String[CONSOLE_WHILELOOP][:FONT_MAX_W]
                CONSOLE_WHILELOOP += 1

            Console_Input = ""
            Console_Parsing = False
            Console_Parameter = []
        

    if Debug_BGInfo:
        SCREEN_DISPLAY.fill(Color_Index[248])
        BGLine = GAME_FONT.render("View BG Info (ALT+B)", 0, Color_Index[2], Color_Index[3])
        SCREEN_DISPLAY.blit(BGLine, (0,0))
        StoredHeight = BGLine.get_height() * 2
        
        for BG in range (0, len(All_BGS)):
            if All_BGS[BG]['IsRendered']:
                TEMP_Surface = All_BGS[BG]['Source'].subsurface(All_BGS[BG]['TexXPos'], All_BGS[BG]['TexYPos'], All_BGS[BG]['TexWidth'], All_BGS[BG]['TexHeight'])
                if TEMP_Surface.get_width() >= 32:
                    TEMP_Surface = pygame.transform.scale(TEMP_Surface, (32, TEMP_Surface.get_height()))
                if TEMP_Surface.get_height() >= 32:
                    TEMP_Surface = pygame.transform.scale(TEMP_Surface, (TEMP_Surface.get_width(), 32))
                    
                BG_Info = GAME_FONT.render("ID " +str(BG) +str(" = W") +str(All_BGS[BG]['TexWidth']) +str(" = H") +str(All_BGS[BG]['TexHeight']) +str(" = X") +str(All_BGS[BG]['TexXPos']) +str(" = Y") +str(All_BGS[BG]['TexYPos']), 0, Color_Index[2], Color_Index[3])
                BG_Info2 = GAME_FONT.render("A" +str(All_BGS[BG]['SineAmp']) +str(" = F") +str(All_BGS[BG]['SineFreq']) +str(" = S") +str(All_BGS[BG]['SineSpeed']) +str(" = T") +str(All_BGS[BG]['SineTime']), 0, Color_Index[2], Color_Index[3])
                SCREEN_DISPLAY.blit(BG_Info, (TEMP_Surface.get_width(),   StoredHeight))
                SCREEN_DISPLAY.blit(BG_Info2, (TEMP_Surface.get_width(),  StoredHeight + BG_Info.get_height()))
                TEMP_Surface.set_palette(Color_Index)
                SCREEN_DISPLAY.blit(TEMP_Surface, (0,StoredHeight))
                StoredHeight += All_BGS[BG]['TexHeight']
    
    if Debug_DrawPalette:
        Debug_PaletteTex    = pygame.Surface( (4,64), HWSURFACE, 8)
        Debug_PaletteTex.set_palette(Color_Index)
        
        for x in range (0, len(Color_Index)):
            Debug_PaletteTex.set_at((x % Debug_PaletteTex.get_width(), x // Debug_PaletteTex.get_width()), Color_Index[x])
            
        Debug_PaletteTex    =   pygame.transform.scale(Debug_PaletteTex, (8, 128))
        Palette_BlitX       =   DEFAULT_WIDTH - Debug_PaletteTex.get_width()//2 - Line1.get_width()  // 2
        ChosenColor         =   ((int(RelX) - Palette_BlitX) // 2) + ((int(RelY) - Debug_Height * 2) //2 ) * 16
        SCREEN_DISPLAY.blit (Debug_PaletteTex, (DEFAULT_WIDTH - Debug_PaletteTex.get_width(), Line1.get_height()))
        ColorAtMouse = SCREEN_DISPLAY.get_at((int(RelX), int(RelY)))
        
        try:
            Line2 = GAME_FONT.render("PALETTE ID=" +str(Color_Index.index(ColorAtMouse)).zfill(3), 0, Color_Index[2], Color_Index[3])
        except:
            Line2 = GAME_FONT.render("FAILSAFE - COLOR NOT IN PALETTE", 0, Color_Index[2], Color_Index[3])

        Line3 = GAME_FONT.render("R=" +str(ColorAtMouse.r).zfill(3) +" G=" +str(ColorAtMouse.g).zfill(3) +" B=" +str(ColorAtMouse.b).zfill(3), 0, Color_Index[2], Color_Index[3])
        Line4 = GAME_FONT.render("X:" +str(int(RelX)) +"| Y:" +str(int(RelY)), 0, Color_Index[2], Color_Index[3])
        
        # Draw Color Palette #
        SCREEN_DISPLAY.blit(Line1, (DEFAULT_WIDTH - Line1.get_width(), 0))
        SCREEN_DISPLAY.blit(Line2, (DEFAULT_WIDTH - Line2.get_width(), DEFAULT_HEIGHT - Debug_Height))
        SCREEN_DISPLAY.blit(Line3, (DEFAULT_WIDTH - Line3.get_width(), DEFAULT_HEIGHT - Debug_Height * 2 ))
        SCREEN_DISPLAY.blit(Line4, (DEFAULT_WIDTH - Line4.get_width(), DEFAULT_HEIGHT - Debug_Height * 3 ))   
        pygame.draw.rect(SCREEN_DISPLAY, Color_Index[1], (263, 116, 25, 25))
        pygame.draw.rect(SCREEN_DISPLAY, ColorAtMouse, (264, 117, 23, 23))

    if Debug_Draw_ROT:
        pygame.draw.line(SCREEN_DISPLAY, Color_Index[1], (DEFAULT_WIDTH//3, 0), (DEFAULT_WIDTH//3, DEFAULT_HEIGHT))
        pygame.draw.line(SCREEN_DISPLAY, Color_Index[1], (DEFAULT_WIDTH//1.5, 0), (DEFAULT_WIDTH//1.5, DEFAULT_HEIGHT))
        pygame.draw.line(SCREEN_DISPLAY, Color_Index[1], (0, DEFAULT_HEIGHT//3), (DEFAULT_WIDTH, DEFAULT_HEIGHT//3))
        pygame.draw.line(SCREEN_DISPLAY, Color_Index[1], (0, DEFAULT_HEIGHT//1.5), (DEFAULT_WIDTH, DEFAULT_HEIGHT//1.5))
        
    if Debug_Cheats:
        SCREEN_DISPLAY.blit(GAME_FONT.render("EDIT MODE (ALT + Q)", 0, Color_Index[2], Color_Index[3]) ,(0, DEFAULT_HEIGHT - (Debug_Height * 1) ))
        SCREEN_DISPLAY.blit(GAME_FONT.render("SELECTED BG - " +str(Cheats_BG), 0, Color_Index[2], Color_Index[3]) ,(0, DEFAULT_HEIGHT - (Debug_Height * 4)))
        SCREEN_DISPLAY.blit(GAME_FONT.render("PARAM #" +str(Cheats_Parameters) +" - " +str(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][0]) +" " +str(list(All_BGS[Cheats_BG].items())[Cheats_Parameters][1]), 0, Color_Index[2], Color_Index[3]) ,(0, DEFAULT_HEIGHT - (Debug_Height * 3)))
        SCREEN_DISPLAY.blit(GAME_FONT.render("Change per scroll - INT - " +str(Cheats_Interval_Int) +" - FLOAT - " +str(Cheats_Interval_Float), 0, Color_Index[2], Color_Index[3]) ,(0, DEFAULT_HEIGHT - (Debug_Height * 2)))
        
    if Debug_DrawText:
        SCREEN_DISPLAY.blit(GAME_FONT.render("Debug Info Enabled (ALT + I)", 0, Color_Index[2], Color_Index[3]), (0, 0))
        SCREEN_DISPLAY.blit(GAME_FONT.render("== GAME SETTINGS ==", 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 1))
        SCREEN_DISPLAY.blit(GAME_FONT.render("FPS: " +str(int ( GAME_CLOCK.get_fps()) ), 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 2))
        SCREEN_DISPLAY.blit(GAME_FONT.render("Global Timer = " +str(Global_Timer) +"/" +str(Global_Timer_Max) + " | Demo Timer = " +str(Demo_Timer) +"/" +str(Demo_Timer_Max), 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 3))

        if Game_State == 1:
            SCREEN_DISPLAY.blit(GAME_FONT.render("Player Pos: " +str(Player_XPos) +"," +str(Player_YPos) , 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 4))
            SCREEN_DISPLAY.blit(GAME_FONT.render("Movement U: " +str(MovingUp) +" D " +str(MovingDown) +" L " +str(MovingLeft) +" R " +str(MovingRight) , 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 5))
            SCREEN_DISPLAY.blit(GAME_FONT.render("Direction: " +str(Player_Direction) +" | ANG: " +str(Player_Direction * (360//8) ), 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 6))
            SCREEN_DISPLAY.blit(GAME_FONT.render("Walking? : " +str(Moving) +" | Going Diag? " +str(Moving_Diagonal), 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 7))
            SCREEN_DISPLAY.blit(GAME_FONT.render("Current Tile - X: " +str(Current_Tile_XPos) +" Y: " +str(Current_Tile_YPos) +" | SUM: " +str(Current_Tile_XPos + Current_Tile_YPos) , 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 8))
            SCREEN_DISPLAY.blit(GAME_FONT.render("Walk Frame: " +str(Player_WalkFrame) +" Cycle: " +str(Player_WalkCycle) , 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 9))
            SCREEN_DISPLAY.blit(GAME_FONT.render("RunTime: " +str(Running_Timer) +"/" +str(Running_Timer_Max) +" | Running? - " +str(Running) , 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 10))
            SCREEN_DISPLAY.blit(GAME_FONT.render("DiagTime: " +str(Moving_Diagonal_Time) +"/" +str(Moving_Diagonal_MaxTime) +" | Diag Angle - " +str(Diagonal_Direction) , 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 11))
            SCREEN_DISPLAY.blit(GAME_FONT.render("DISTTRAVELLED X:" +str(Player_XPos - Player_XPos_Diff) +" Y:" +str(Player_YPos - Player_YPos_Diff) , 0, Color_Index[2], Color_Index[3]), (0, Debug_Height * 12))
            
    # PLAY SOUNDS AND RENDER #
    if not AboutToQuit:
        if Cursor_Vertical:
            SFX_Cursor_V.play()
            Cursor_Vertical     = False
        if Cursor_Horizontal:
            SFX_Cursor_H.play()
            Cursor_Horizontal   = False

    
    if AboutToQuit:
        PixRPG_Title_Selection  = 0
        PixRPG_Title_State      = 0
        SCREEN_DISPLAY.fill(sorted(Color_Index[Global_Timer // 4 % 256 ]))
        SCREEN_DISPLAY.blit(GAME_FONT.render("PIXRPG, BY JackM", 0, Color_Index[2]), (50, DEFAULT_HEIGHT - Quit_Timer))
        SCREEN_DISPLAY.blit(GAME_FONT.render("GFX BY JackM", 0, Color_Index[2]), (50, DEFAULT_HEIGHT * 1.1 - Quit_Timer))
        SCREEN_DISPLAY.blit(GAME_FONT.render("SAMPLES/MISC CREDITS IN CREDITS FOLDER", 0, Color_Index[2]), (50, DEFAULT_HEIGHT * 1.2 - Quit_Timer))
        SCREEN_DISPLAY.blit(GAME_FONT.render("THANK YOU FOR PLAYING, or just quitting :>", 0, Color_Index[2]), (50, DEFAULT_HEIGHT * 1.3 - Quit_Timer))
        Quit_Timer += Quit_Timer_Interval
        if Global_Timer > FutureClockPrev:
            if Cursor_Select or Cursor_Back:
                Global_Timer = Final_Time
        if  Global_Timer == Final_Time:
            print ("DEBUGSTRING - KILLED GAME!")
            quit()
            pygame.quit()
            
    if Cursor_Select:
        if not Console_Enabled:
            SFX_Cursor_S.play()
        Cursor_Select       = False
        
    if Cursor_Back:
        SFX_Cursor_B.play()
        Cursor_Back = False
        
    SCREEN_DISPLAY      = pygame.transform.scale(SCREEN_DISPLAY, (SCREEN_WIDTH, SCREEN_HEIGHT))
    TRUE_DISPLAY.blit(SCREEN_DISPLAY, (0,0))
    
    if ScreenShotting:
        Now = datetime.datetime.now()
        ScreenShotDir = 'screenshots/' +str(Now) +'.png'
        ScreenShotDir = ScreenShotDir.replace(" ", "_")
        ScreenShotDir = ScreenShotDir.replace(":", ".")
        pygame.image.save(TRUE_DISPLAY, ScreenShotDir)
        ScreenShotting = False
    
    SCREEN_DISPLAY      = pygame.transform.scale(SCREEN_DISPLAY, (DEFAULT_WIDTH, DEFAULT_HEIGHT))
    pygame.display.flip()
    GAME_CLOCK.tick(GAME_FPS)
    SCREEN_DISPLAY.set_palette(Color_Index)
