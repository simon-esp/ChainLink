# Documentation
Full docs for chainlink scripting syntax
## Variables
Variables are used to store data temporarily, to understand variables you have to understand the python code behind it. The variables are stored in a dictionary, which is a python variable but also kind of limits speed. Try to only store small bits of data under 50k characters or it might get problems. The lines are split by `;`, and any spaces that comes before non-space characters on each command is removed, so indents are possible. This also allows for creative formatting, like you can have new-lines anywhere. Just make sure each command is split by a semicolon.
#### Setting / declaring variables
Variables are automaticly declared, so to set a variable, you use `var` as the keyword.<br> Example usage: `var test=20;`<br>
#### Retrieving variables
Variables are checked for in the evaluate phase. If you for example type in `echo variable;` without declaring 'variable' it will not work, because it tries to evaluate it as a multi-input operator, like for example addition or multiplication. This makes it stuck on one line of code (in the interpreter) and it will output an error. If you type `echo "variable";` it will output variable, because it is evaluated as a string. If you declare the variable it will check for if that name is in the variables dictionary. Same applies for lists.
#### Lists (arrays)
Instead of using square brackets like any other programming language, clss uses a completely seperate dictionary to store lists. This is crucial to know before getting into lists, as you wont be able to set lists through the `var ..` command. Instead, declare lists with `declare example;`. Append with `append example="value";`, pop with `puncture example:1`. You can get the raw list the same way you get a variable.
## Loops
Loops are surrounded in curly brackets, you can indent as you wish, the code inside the loop will be parsed before running. Make sure that you have a semicolon between each command and after the right curly bracket.
#### Repeat # times
To repeat a set amount of times, you can use the rep command. Usage is as follows: `rep 10:{echo "hello world";};`, you can have indents before each command inside, and you can nest like in any other program. The number to repeat by is evaluated, so you can type `var reps_done=3;var reps=10;rep reps - reps_done:{echo "+1 pushup";};`.
#### While loop
The while loop can be useful, you can repeat something until something is not true. For example you can type `while "True":{echo "hello world";};` to print a bunch of hello world's. These work like the rep command, so they can be nested and the condition is evaluated.
## Evaluation
Just about every input in clss is evaluated, the evaluation process is done to do calculations and conditions. Both the if and the var command uses the same evaluation. The evaluating script moves an imaginary pointer across the divided string (divided by spaces) and evaluates everything, so if variable chicken_nuggets = 20, then `echo chicken_nuggets - 10 ~i ate some~;` it would output 10. It doesnt have parenthathees and ignores the pemdas rule.
#### Conditions
`=`: Is equal to, remember the imaginary pointer, it is basicly an equivelent to `==` in python.<br>
`>`: Is greater than, it is basicly an equivelent to `>` in python.<br>
`<`: Is lesser than, it is basicly an equivelent to `<` in python.<br>
`!=`: Is NOT equal to, it is basicly an equivelent to `!=` in python.<br>
For example a "1" would also return true probably i havent tested yet
#### Operations
To understand operations you have to understand the code behind, it first parses the string (splitting into a list) then it evaluates each point inside the list, deleting the items it is done with. The current commands are:<br>
`+, -, *, /` are all pretty obvious<br>
`**` repeats the string on the left by the number on the right<br>
`++` joins left and right strings<br>
`# of #` is the letter of method, in python this would be `#[#]`<br>
`# of #` is the item in list method, in python this would also be `#[#]`<br>
Conditions can also be assigned to variables, lists and printed<br>
