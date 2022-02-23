One. Overall description 

DEMO:(Youtube: https://youtu.be/a9598FzhCR4)

This is a 2-player game. 
2 players can use keyboard to control 2 cute creepers. They can control creepers to jump, shoot to other player and plant bomb. They are all on floating boards that keeps moving, in a time period all the boards will move to one direction and the direction will change in next period.  there is no friction between players and board so one will fall and die if it slides out from the board. Being shot by opponent will also cause death. Once one player died, the game will end and announce the winner. There will be no winner if 2 players died at exactly the same time.

Two. How to play the game

Jump( key ‘W’ for player 1 and ‘UP’ for player 2)
Player need to jump at a proper time in order to avoid the bullet shot form his/her opponent.
Player also need to jump in order to be always on the board.
Jumping takes some time and therefore player need to seize the time in order to land exactly on another board.
There is no limitation of jumping, as long as the player is on the board, he/she can jump.

Shoot( key ‘D’ for player 1 and key ‘Left’ for player 2)
Player can shoot to opponent, as long as the bullet hit the opponent successfully, the player win. However, there is a limitation of bullet number. Player can only shoot when his/her bullet number is greater than 0. At the start of the game, 2 players have a certain number of bullet. After a certain amount of time, their bullet number will both increase by 1. Although the aim is to let the opponent die, one cannot bully other by realising bullet nearly at the same time and at different height which will cause the other player have nowhere to escape and 100% die, he/ she maybe cry after being treated like that. That is not what I want to happen. Hence, One can only shoot 2nd time when the bullet of the 1st shooting have flied out of the screen. 

They need some strategies if they want to be a good player: 
When to shoot? Is it good to shoot when jumping or shoot when player is on the board?
How to wisely use my limited bullets?
When to jump to make sure I will land on another board safely?
When to jump in order to elude the bullet?
Is there a ‘Perfect match’(Time to shoot and the position of the boards) that can let opponent have NO WAY to escape?(Opponent can never elude the bullet and land on board at the same time)

Three. Code Structure: 
(Indentation indicate the belonging relationship, The word in brackets indicate the class name)

OfficalApp(App)
	self.widget_box (Widget_box_class)
		self.player1(Player)
			self.bullet(Bullet)
			self.die(Die)      
			#Die case 1:Added by the opponent player only if the opponent player has killed this player by bullet
			#Die case 2: Added by itself when it falls
		self.player2(Player)
			self.bullet(Bullet)
			self.die(Die)      
			#Die case 1:Added by the opponent player only if the opponent player has killed this player by bullet
			#Die case 2: Added by itself when it falls
		self.countdown(Countdown)
		self.bullet_label1(Label)  #Show bullet number of player1
		self.bullet_label2(Label)  #show bullet number of player2
		self.board0(Board)
		self.board1(Board)
		self.board2(Board)
		self.board3(Board)
		self.board4(Board)
		self.board5(Board)
		self.board6(Board)
		self.board7(Board)
		self.board8(Board)

Four: Detailed description of components of the code
(See comments of the code to find more detailed description)

0.redraw   (This is a function)
Set the position and size of the rectangle of a widget to the position and size of the widget it self so that when widget is moving, the rectangle will move at the same time. It is a global function so that every widget can call it to realise this function when needed.	

Classes:
1.Player(Widget)
Draw a player
Bind drawing’s position and player’s position
Initialise variables 
Add a ‘Bullet’ instance to it
Define all players’ skill: hold_bullet, shoot, jump_skill, fall

2.Bullet(Widget)
Draw a bullet
Bind drawing’s position and bullet’s position
Initialise the velocity variable

3.Board(Widget)
Draw a board
Bind drawing’s position and board’s position
Define the boarding moving rule

4.Die(Widget)
Draw ‘Wasted’ logo when player died.

5.Countdown
Draw a billboard
Bind drawing’s position and Countdown widget’s position
Draw a label to count down(3—-2—-1—-Start!)

6.Widget_box_class(Widget)
Draw the background
Initialise variables
Add its child instances
Bind keyboard_action function to on_key_down event
Function ‘update’: The code that need to be refreshed all the time.They have different categories:
	Effects: They will have a return, which will prevent the code after the return to execute, hence the function here is froze the board and player, do a count down when the app is just started and also froze the board and player, give a announcement of final winner when one player die and game is over.
	Routine: They will do the routine job which means that the ‘keyboard independent job’. they do not need to listen to the key code. Their jobs contain animations and also changes of variables. More detailed description is i the comments of the update part in the code.
	Response: Here contains actions after a certain key is being pressed. They are ‘jump’ and ‘shoot’. every time when this part end, I set the key code to be ‘’ so that those code can only be activated once, right after a key is being pressed. in the next refreshing, if on key is pressed, this part will now be triggered and if animations and calculations about jumping and shooting are not done, they will be done by the ‘Routine’ part.
Function ‘key_action’: translate the received key code number to their name, save it to a variable and the variable will then be called by other part of the class to execute response.

7.OfficialApp(App)
Set the title of App
Set the Window size
Loading the widget_box that contains all of the widgets
Run ‘update’ function in the widget_box every 1/120 s to give a 120Hz refresh rate of animation.

