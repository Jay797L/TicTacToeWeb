# Project 03 — Python_Bootcamp

**Summary:**  
In this project, you will learn how to create a web application in Python using Flask.

💡 [Click here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) to share your feedback on this project. It’s anonymous and helps our team improve the learning experience. We recommend completing the survey right after finishing the project.

## Contents

  - [Chapter I](#chapter-i)
  - [Chapter II](#chapter-ii)
    - [General Information](#general-information)
    - [Topics to Study](#topics-to-study)
  - [Chapter III](#chapter-iii)
    - [Task 0. Project Setup](#task-0-project-setup)
    - [Task 1. Creating the Project Structure](#task-1-creating-the-project-structure)
    - [Task 2. Implementing the Domain Layer](#task-2-implementing-the-domain-layer)
    - [Task 3. Implementing the Datasource Layer](#task-3-implementing-the-datasource-layer)
    - [Task 4. Implementing the Web Layer](#task-4-implementing-the-web-layer)
    - [Task 5. Implementing the DI Layer](#task-5-implementing-the-di-layer)


## Chapter I

**Instructions**

1. Throughout the course, you will often feel uncertain and short of information — this is normal. Remember, the repository and Google are always with you. So are your peers and Rocket.Chat. Communicate. Search. Use common sense. Don’t be afraid to make mistakes.
2. Be careful with your sources. Verify. Think. Analyze. Compare.
3. Read tasks carefully. Read them several times.
4. It’s better to read examples carefully too. They may contain something not explicitly stated in the task.
5. You might encounter contradictions, when something new in the task or example contradicts what you already know. If that happens, try to figure it out. If you can’t, write down your question as an open issue and resolve it during your work. Don’t leave open questions unresolved.
6. If a task seems unclear or impossible — it just seems that way. Try to break it down. Likely, individual parts will become clear.
7. You will meet different tasks on your way. Bonus tasks are for the most meticulous and curious. These tasks are more difficult and optional, but completing them gives extra experience and knowledge.
8. Don’t try to cheat the system or others. You will only cheat yourself.
9. Have a question? Ask the peer on your right. If that doesn’t help, ask the one on your left.
10. When you get help — always understand fully why, how, and what for. Otherwise, help will be meaningless.
11. Always push only to the develop branch! The master branch will be ignored. Work inside the src directory.
12. Your directory must not contain any files other than those specified in the tasks.

## Chapter II

### General Information

**A web application** is a client-server application where the client interacts with the web server through a browser. The logic of a web application is distributed between the server and the client, data storage is primarily on the server, and information exchange occurs over the network.

**Flask** is one of the most popular frameworks for creating web applications in Python. Its advantages include:

- **Ease of use:** Flask has a simple and intuitive syntax, making it ideal for beginner developers or those who prefer clear and straightforward code.
- **Good documentation:** Flask offers well-structured and clear documentation that simplifies getting started and troubleshooting.
- **Flexibility:** Flask provides a flexible and modular approach to web development, allowing you to choose only the components and features needed for your project.
- **Support for RESTful API:** Flask includes convenient tools for developing RESTful APIs, such as routing, data serialization, and request/response handling.
- **Good integration with other tools:** Flask easily integrates with popular Python libraries and tools like SQLAlchemy for database work and Jinja2 for templating.

These advantages make Flask an attractive choice for developers aiming to build fast, scalable, and maintainable web applications in Python.

### Topics to Study

- Web application
- Flask for the backend
- API
- Minimax algorithm
- MVC

## Chapter III

## Project: Tic-Tac-Toe
The project is created once and used for all subsequent tasks.

### Task 0. Project Setup

To develop in Python, you will need to install the appropriate interpreter. It can be downloaded from the official website. After installation, you can use the command line and/or various integrated development environments (IDEs) to work on projects.  
A project in this context is a set of .py files containing Python code, which can be run individually via the command python filename.py (or python3) or imported into a common file often named main.py.  
In PyCharm, creating a project is straightforward: you just select the Python interpreter to use, specify the save path and project name. You can also create a virtual environment, which is convenient for large projects with many dependencies (libraries, frameworks).

### Task 1. Creating the Project Structure

- Each layer should be a separate module.
- The project structure must include the following layers: **web**, **domain**, **datasource**, and **di**.
- The **web** layer must contain at least the packages: model, module, route, and mapper for client interaction.
- The **domain** layer must include at least the packages: model and service for implementing the business logic.
- The **datasource** layer must include at least the packages: model, repository, and mapper for data handling (e.g., database operations).
- The **di** layer contains configurations for dependency injection.

### Task 2. Implementing the Domain Layer

- Define the game board model as an integer matrix.
- Define the current game model, which has a UUID and the game board.
- Define a service interface with the following methods:
  - a method to get the next move of the current game using the Minimax algorithm;
  - a method to validate the current game board (checking that previous moves have not been altered);
  - a method to check if the game has ended.
- Models, interfaces, and implementations should be placed in separate files.

### Task 3. Implementing the Datasource Layer

- Implement a storage class for storing current games.
- Use thread-safe collections for storage.
- Define models for the game board and current game.
- Implement mappers between domain and datasource models (domain<->datasource).
- Implement a repository to work with the storage class with the following methods:
  - a method to save the current game;
  - a method to retrieve the current game.
- Create a class implementing the service interface that accepts the repository as a parameter for working with the storage class.
- Models, interfaces, and implementations should be placed in separate files.

### Task 4. Implementing the Web Layer

- Define models for the game board and the current game.
- Implement mappers between domain and web models (domain<->web).
- Implement a Flask controller with a POST method /game/{current_game_UUID} that accepts the current game with a user-updated game board and returns the current game with the computer-updated game board in response.
- If an invalid current game with an updated board is sent, return an error with a description.
- Support multiple games running simultaneously.
- Models, interfaces, and implementations should be in separate files.

### Task 5. Implementing the DI Layer

- Implement a Container class that defines the dependency graph.
- It must include at least:
  - a singleton storage class;
  - a repository for working with the storage class;
  - a service for working with the repository.