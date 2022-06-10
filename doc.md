
# Table of Contents
1. [General info](#General-info)
2. [Technologies](#Technologies)
3. [Motivation](#Motivation)
4. [Initial goals](#Initial-goals)
5. [Achieved goals](#Achieved-goals)

# General info
The aim of our project was to create language that generates UML diagrams. Our language allows to create:
-  class diagrams
-  use case diagrams
-  sequence diagrams. 

Our language allows to save generated diagrams *png* file.  

# Technologies
In our project we used:
- Python
- ANTLR4
- PlantUML

# Motivation
We wanted to created simple, intuitive language to create UML diagrams. It's useful particullary for students, who have many projects requiring the use of UML diagrams. Also it may be usable for us in the future. 

# Initial goals
Funcionalities we planned to include in our language:

* **Diagrams:**

    **1.Class diagrams** with keywords (*class*, *interface*, *abstract*). Diagram contains objects with specific types (*public*, *private*, *protected*)

    **2. Use case diagrams** and actors

    **3. Sequence diagrams**  with activation and deactivation on lifelines and delayed messages. 
* **Objects:**
    
    * Themes 
    * Notes
    * Packages
    * Lists
* **For loops**
* **Functions**
* **Diagram execution** with option of saving whole diagram or only neccessary information to specific png file. 
* **Conections** between class diagrams

# Achieved goals
In class and use case **diagrams** we realised all planned features, in sequence diagrams we didn't manage to handle activation and deactivation of lifelines.

We created **notes** that can be attached to all of the objects.

Also we implemented **packages**, which can contain all types of diagrams, even if some are connected.

In our language users can write their own **functions** with various amount of arguments. All functions have a return statement. Objets are returned in a list, which can be empty. 

Also user can use recurrention with specific depth - default depth is 1. 

Blocks can have a spepcific type of **connections**. Connection types can be write in two ways:
* **By using words:**
 inherit, implement, associate, depend, aggregate, compose;
* **or by using arrows**: [x<, <, <<, \, //, \\, o<, \\o ], [., -, _], [>x, >, >>, \, //, \\, >o, o\\]

Objects declared in global scope can be used in other scopes. 

Diagram can be **executed** using *exec* keyword in diagram body. User can add filename to which diagram will be saved. In global scope, after exec keyword, user has to write specific diagram name. 
    
