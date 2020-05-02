from kivy.graphics import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.text import LabelBase
from time import sleep

#length and width of the playground
pglength = 1920
pgwidth = 1080
coor =(pglength,pgwidth)


# Redraw Function(For binding self.pos and self.Rect.pos)
def redraw(self, args):
        self.Rect.size = self.size
        self.Rect.pos = self.pos
#------------------------main widget classes----------------------------------#        
# Player Class               
class Player(Widget): 
    def __init__(self,playerpos):
        Widget.__init__(self,
        size=(60,60),
        center_x = playerpos[0],
        center_y = playerpos[1])   
        
        #args
        self.alive = True
        self.vel = 15    #For jumping
        self.count = 0
        #Add bullet to player class
        self.bullet_num = 2
        self.bullet_rec = 0
        self.bullet = Bullet((self.center_x,self.center_y))
        self.add_widget(self.bullet)
        self.hold_bullet_status = True
        
        #Fall(Here Fall is just an animation and I do not set the vel)
        
        
        
        #draw player
        with self.canvas:
            # Color(1,0,0)
            self.Rect=Rectangle(source ='creeper.jpg',
                      size=self.size,pos=self.pos)
        self.bind(pos = redraw,size = redraw)

 
            
    # skills
    def hold_bullet(self):
        self.bullet.center_x = self.center_x
        self.bullet.center_y = self.center_y

        
    def shoot(self,veldir,enemy):
        if abs(self.bullet.center_x- 0.5*pglength) <= 0.5*pglength:
            self.bullet.center_x += self.bullet.vel*veldir
        else:
            self.hold_bullet_status = True
            self.bullet_num -= 1
        #Killed others successfully    This is a action of enemy
        if abs(self.bullet.center_y-enemy.center_y      #ensure safety of enemy if he/she dead in advance
               ) <= 60 and abs(self.bullet.center_x-enemy.center_x) <= 60 and self.alive:
            self.hold_bullet_status = True
            enemy.die=Die((enemy.center_x,enemy.center_y))
            enemy.add_widget(enemy.die)
            enemy.count = 100
            enemy.alive = False

    
    def jump_skill(self):
        if self.count <= 20:
            self.pos = (self.pos[0],self.pos[1]+self.vel)
            self.count += 1
            return True
        elif self.count <= 41:
            self.pos = (self.pos[0],self.pos[1]-self.vel)
            self.count += 1
            return True
        #End
        elif self.count == 42:
            self.count = 0
            return False
        #Die case
        elif self.count == 100:
            if self.pos[1] >= -60:
                self.pos = (self.pos[0],self.pos[1]-self.vel)
                return True
            return False
        
    def fall(self):
        self.alive = False
        self.die = Die((self.center_x,self.center_y))
        self.add_widget(self.die)
        anim = Animation(y=-self.size[1])
        anim.start(self)
        

        
#Bullet        
class Bullet(Widget):
    def __init__(self,bulletpos):
        Widget.__init__(self,
        size=(40,40),
        center_x = bulletpos[0],
        center_y = bulletpos[1])   
        
        #args
        self.vel = 20
        #draw
        with self.canvas:
            # Color(1,0,0)
            self.Rect=Rectangle(source ='bullet.png',
                      size=self.size,pos=self.pos)
        self.bind(pos = redraw,size = redraw)


   
        
#Board   
class Board(Widget):
    def __init__(self,number):
        self.width = 170
        self.gap = 70
        self.vel = 1
        #self.veldir: SEE Widget Box(The moving direction of board)
        #self.timer:  SEE Widget Box(Determine when the board moving direction will change)
        Widget.__init__(self,
                        size = (self.width,20),
                        pos = ((-self.width/2+(self.width+self.gap)*number),
                                0.5*pgwidth-50))
        with self.canvas:
            self.Rect=Rectangle(source='board.png',size=self.size,pos=self.pos)
        self.bind(pos = redraw,size = redraw)
        
    def moving(self,timer):
        if timer > 0:
            if self.center_x == -0.5*self.width:
                self.pos = (pglength+self.gap,
                            self.pos[1])
            self.pos =(self.pos[0] - self.vel,self.pos[1])
        
        if timer < 0:
            if self.center_x == pglength + 0.5*self.width:
                self.pos = (-self.gap-self.width,
                            self.pos[1])
            self.pos =(self.pos[0] + self.vel,self.pos[1])            
#------------------------Effect aimed Widget Classes--------------------------#            
# Die label Class
class Die(Widget):
    def __init__(self,diepos):
        Widget.__init__(self,
        size=(200,60),center_x = diepos[0],center_y= pgwidth/2) 
        with self.canvas.after:
            # Color(1,0,0)
            Rectangle(source ='wasted.png',
                      size=self.size,pos = self.pos)
#Count down
class Countdown(Widget):
    def __init__(self):
        Widget.__init__(self,
                        size = (200,100),
                        center_x = 0.5*pglength,
                        center_y = 0.5*pgwidth+50)
        with self.canvas:
            self.Rect = Rectangle(source = 'billboard.png',
                      size = self.size,
                      pos = self.pos)
        self.number = Label(text = '',
                              markup = True,
                              font_size = 90,
                              font_name = '8_bit',
                              center_x = self.center_x,
                              center_y = self.center_y+10)
        self.add_widget(self.number)
        self.bind(pos = redraw,size = redraw)
    def count_down(self,count):
        if int(count/120) != 0:
            self.number.text = '[color=f4e75a]{}[/color]'.format(int(count/120))
        else:
            self.number.text = '[color=f4e75a]{}[/color]'.format('Start!')
            self.number.font_size = 50
    
        
#-------------------------Main game operation part---------------------------#
class Widget_box_class(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Widget.__init__(self,
        size=coor) 
        with self.canvas.before:
            Rectangle(source ='bg.png',
                      size=self.size,pos = self.pos)
        self.keycode = ''
        self.gameover = False
        self.winner = ''
        self.effect_time = 1*120
        self.W_hold = False
        self.up_hold = False
        self.start_detect = False
        self.board_timer = -6*120 #in Sec
        self.board_standard = 6*120 #in Sec
        self.boards_center_list =[]
        self.keycode = ''
        self.keydir = {97:'A',115:'S',100:'D',119:'W',276:'left',275:'right',274:'down',273:'up'}
    #Loading all of the widgets
        #Loading Players
        self.player1 = Player(playerpos=(pglength/4,pgwidth/2))
        self.player2 = Player(playerpos=(3*pglength/4,pgwidth/2))
        self.add_widget(self.player1)
        self.add_widget(self.player2)
        #Loading count down effects
        self.prepare_time = 4*120
        self.countdown = Countdown()
        self.add_widget(self.countdown)
        #Loading Labels
            #Bullet number label
        self.bullet_label1 = Label(text = ' ',
                              markup = True,
                              font_size = 50,
                              font_name = '8_bit',
                              center_x = self.player1.center_x,
                              center_y = 1/4*pgwidth)
        
        self.bullet_label2 = Label(text = ' ',
                              markup = True,
                              font_size = 50,
                              font_name = '8_bit',
                              center_x = self.player2.center_x,
                              center_y = 1/4*pgwidth)        
        self.add_widget(self.bullet_label1)
        self.add_widget(self.bullet_label2)

        
        #Loading boards:
        for i in range(9):
            exec('self.board{} = Board(i)'.format(i))
            exec('self.add_widget(self.board{})'.format(i))

        #Bind keyboard action
        self.keyboard=Window.bind(on_key_down=self.key_action)
    # UPDATE!  
    def update(self,dt):  #Write return True if u want to skip the next code
    #Effects   (They have a return)
        #At start point
            #Froze the screen, count down to let players prepare
        if self.prepare_time > 0:
            self.countdown.count_down(self.prepare_time)
            self.prepare_time -= 1
            return True
        elif self.prepare_time == 0:
            self.countdown.animation = Animation(y=-self.size[1])
            self.countdown.animation.start(self.countdown)
            self.countdown.number.text =''
            self.prepare_time -= 1
            self.start_detect = True
            return True
        #At end point
            #Find the winner, end the game, however let the die animation finished
        if not (self.player1.alive and self.player2.alive) and self.gameover == False:
            if self.player1.alive == False and self.player2.alive == False:
                self.winner = 'NA!'
            elif self.player1.alive:
                self.winner = 'Player1!'
            elif self.player2.alive:
                self.winner = 'Player2!'
            self.gameover = True
            #Give 1s for the effect to complete and then froze the screen    
        if self.gameover == True:
            if self.effect_time >= 0:
                self.effect_time -= 1
            else:         #Borrow from the count down label to display the winner haha
                self.countdown.number.text = '[color=0000CD]Winner: [/color][color=DC143C]{}[/color]'.format(self.winner)
                self.countdown.number.pos[1] = 0.5*pgwidth -250
                return True
            
            
        
        
    #Routine
        
        #Hold Bullet and Bomb,calcuclate recovery time
        self.player1.bullet_rec += 1
        self.player2.bullet_rec += 1
        self.bullet_label1.text = '[color=a3de83]Bullet: [/color][color=fa4659]{}[/color]'.format(self.player1.bullet_num)
        self.bullet_label2.text = '[color=a3de83]Bullet: [/color][color=fa4659]{}[/color]'.format(self.player2.bullet_num)        
        self.add_bullet_time = 4  #Seconds need to add bullet
        if self.player1.bullet_rec == self.add_bullet_time*120:
            self.player1.bullet_num += 1
            self.player1.bullet_rec = 0
            print(self.player1.bullet_num)
            
        if self.player2.bullet_rec == self.add_bullet_time*120:  #Seconds need to add bullet
            self.player2.bullet_num += 1
            self.player2.bullet_rec = 0           
            print(self.player2.bullet_num)
        #Board Move + provide a center list:
        self.board_timer += 1
        if self.board_timer == self.board_standard:
            self.board_timer = -self.board_standard
        self.boards_center_list = []
        for i in range(9):
            exec('self.board{}.moving(self.board_timer)'.format(i))
            exec('self.boards_center_list.append(self.board{}.center_x)'.format(i))
        #Fall   
        self.fall1 = True  #This can also serve as a switch in testing
        self.fall2 = True
                                              #Ensure the safe of player if his/her enemy is killed
        if self.player1.pos[1] == pgwidth/2 - self.player1.size[1]/2 and self.effect_time == 1*120:
            for i in self.boards_center_list:
                if abs(i-self.player1.center_x) <= ( self.player1.size[1] + self.board1.size[0])/2:
                    self.fall1 = False
            if self.fall1 == True:   #Ensure the safe of player if his/her enemy is killed       
                self.player1.fall()
                
                                              #Ensure the safe of player if his/her enemy is killed
        if self.player2.pos[1] == pgwidth/2 - self.player2.size[1]/2 and self.effect_time == 1*120:
            for i in self.boards_center_list:
                if abs(i-self.player2.center_x) <= ( self.player2.size[1] + self.board1.size[0])/2:
                    self.fall2 = False
            if self.fall2 == True:   
                self.player2.fall()

           
        
    #Response  (response to the keyboard event)
        #Jump
        if self.keycode == 'W' or self.W_hold == True:
            if self.keycode == 'W':
                self.W_hold = True
                self.keycode = ''
            if self.W_hold == True:
                self.W_hold = self.player1.jump_skill()
                
        if self.keycode == 'up' or self.up_hold == True:
            if self.keycode == 'up':
                self.up_hold = True
                self.keycode = ''
            if self.up_hold == True:
                self.up_hold = self.player2.jump_skill()
        #Shoot
        if self.keycode == 'D' and self.player1.bullet_num > 0:
            self.player1.hold_bullet_status = False
        if self.player1.hold_bullet_status == False:
            self.player1.shoot(1,self.player2)                  
        else:                                          
            self.player1.hold_bullet()
        if self.keycode == 'left' and self.player2.bullet_num > 0:    
            self.player2.hold_bullet_status = False            
        if self.player2.hold_bullet_status == False:
            self.player2.shoot(-1,self.player1)
        else:
            self.player2.hold_bullet()
        # keycode
        self.keycode =''
                                            
    def key_action(self,*args):
        if self.player1.alive and self.player2.alive and self.start_detect == True:  #if two ppl are alive
            if args[1] in self.keydir.keys():
                self.keycode = self.keydir[args[1]]
        return True
    
# ------------Function to Build and Run the App, Do not modify it!------------#
class OfficalApp(App):
    def build(self):
        self.title='Love then kill by James_Nolan'
        Window.fullscreen = 1
        Window.size = (pglength/2,pgwidth/2)
        #Loading widget box
        self.widget_box = Widget_box_class()
        #refresh the position of everything(controled by update)
        Clock.schedule_interval(self.widget_box.update, 1.0 / 120)           
        return self.widget_box
if __name__=='__main__':
    #Load a cool font!
    from kivy.core.text import LabelBase
    LabelBase.register(name='8_bit',
            fn_regular = '8_bit.ttf',
            fn_bold = '8_bit.ttf')
    #RUN!
    OfficalApp().run()



#SITATION
''' 
Background
https://wallhere.com/zh/wallpaper/728497
'Wasted' logo
https://toppng.com/ideal-gta-5-background-gta-v-wasted-logo-roblox-san-andreas-wasted-PNG-free-PNG-Images_251267
Bullet
https://www.mcmod.cn/item/97491.html
Billboard: From Minecraft game
Font
https://www.mcbbs.net/thread-53754-1-1.html
Board(Modified from Stick)
https://minecraft-zh.gamepedia.com/index.php?title=木棍&variant=zh-sg
Creeper
https://wallpapersafari.com/minecraft-wallpapers-creeper-head/
'''
     
