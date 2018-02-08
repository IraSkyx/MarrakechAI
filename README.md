# PrinceAI
AI for the Marrakech game

## Prince1 :
- AI minimax (2 players) which plays perfectly.
- Works well in 3x3 board size by passing first turn.

## Prince2 :
- AI MiniMax which estimates the plays by stopping the search.
- Works well in 3x3 board size, estimates well in 5x5.

## Prince3 :
- Classic Alpha Beta AI.
- Works well in 3x3 board size by passing first turn, 10 min of execution instead. No estimations so 5x5 board size is quite long.

## Prince4 :
- Alpha Beta AI with a few optimizations on move order (with shuffle)
- Opening table
- Stop optimizations once it reaches nearly the end of the play tree.  

## Prince5 :
- MaxN AI for 3 or more players. Works well in 3x3 board size. No estimations so 5x5 is quite long. 
- Strategy method defines if the AI should rather keep the current value or replace it with the return value of the last _maxN() call.

## Prince6 :
- MaxN AI for 3 or more players which estimates the play tree.
- Strategy method defines if the AI should rather keep the current value or replace it with the return value of the last _maxN() call.
- Works well in 3x3 board size, estimates well in 5x5.

## Prince7 :
- Paranoid variant of Prince6
- Strategy method defines if the AI should rather keep the current value or replace it with the return value of the last _maxN() call.
- Works well in 3x3 board size, estimates well in 5x5.

## Prince8 :
- Offensive variant of Prince6
- Strategy method defines if the AI should rather keep the current value or replace it with the return value of the last _maxN() call.
- Works well in 3x3 board size, estimates well in 5x5.

## Prince9 :
- Complex variant (which plays Offensive against the player in the lead when it loses, Paranoid when it wins or Classic otherwise) of Prince6.
- Strategy method defines if the AI should rather keep the current value or replace it with the return value of the last _maxN() call. It chooses the strategy called depending on its current position in the game.
- Works well in 3x3 board size, estimates well in 5x5.
