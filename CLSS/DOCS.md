# Documentation
Full docs for clss
## Variables
Variables are used to store data temporarily, to understand variables you have to understand the python code behind it. The variables are stored in a dictionary, which is a python variable but also kind of limits speed. Try to only store small bits of data under 50k characters or it might get problems. The lines are split by `;`, and any spaces that comes before non-space characters on each command is removed, so indents are possible. This also allows for creative formatting, like you can have new-lines anywhere. Just make sure each command is split by a semicolon.
#### Setting / declaring variables
Variables are automaticly declared, so to set a variable, you use `var` as the keyword.<br> Example usage: `var test=20;`<br>
#### Retrieving variables
Variables are checked for in the evaluate phase. If you for example type in `echo variable;` without declaring 'variable' it will not work, because it tries to evaluate it as a multi-input operator, like for example addition or multiplication. This makes it stuck on one line of code (in the interpreter) and it will output an error. If you type `echo "variable";` it will output variable, because it is evaluated as a string. If you declare the variable it will check for if that name is in the variables dictionary. Same applies for lists.
#### Lists (arrays)
Instead of using square brackets like any other programming language, clss uses a completely seperate dictionary to store lists. This is crucial to know before getting into lists, as you wont be able to set lists through the `var ..` command. Instead, declare lists with `declare example;`. Append with `append example="value";`, pop with `puncture example:1`. You can get the raw list the same way you get a variable.
