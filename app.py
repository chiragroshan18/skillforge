import os
import uuid
from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

SKILLS = [
    {
        "id": "html-css",
        "name": "HTML & CSS",
        "category": "Web Technology",
        "description": "Semantic markup, modern layout techniques, Flexbox, CSS Grid, and responsive design fundamentals.",
        "difficulty": "Easy",
        "question_count": 10,
        "icon": "layout"
    },
    {
        "id": "javascript",
        "name": "JavaScript",
        "category": "Programming",
        "description": "ES6+ syntax, asynchronous JS, DOM manipulation, promises, event loop, and scope chain.",
        "difficulty": "Medium",
        "question_count": 10,
        "icon": "code"
    },
    {
        "id": "python",
        "name": "Python",
        "category": "Programming",
        "description": "Data types, OOP principles, list comprehensions, decorators, generators, and standard library modules.",
        "difficulty": "Medium",
        "question_count": 10,
        "icon": "terminal"
    },
    {
        "id": "sql",
        "name": "SQL",
        "category": "Database",
        "description": "Relational query design, JOIN operations, aggregation, indexing, subqueries, and normalization.",
        "difficulty": "Medium",
        "question_count": 10,
        "icon": "database"
    },
    {
        "id": "data-structures",
        "name": "Data Structures",
        "category": "Computer Science",
        "description": "Arrays, Linked Lists, Stacks, Queues, Binary Trees, Graphs, Hash Tables, and algorithm complexity.",
        "difficulty": "Hard",
        "question_count": 10,
        "icon": "cpu"
    },
    {
        "id": "web-tech",
        "name": "Web Technology",
        "category": "Web Technology",
        "description": "HTTP protocol, REST architecture, client-server communication, JSON parsing, and web security basics.",
        "difficulty": "Medium",
        "question_count": 10,
        "icon": "globe"
    },
    {
        "id": "computer-networks",
        "name": "Computer Networks",
        "category": "Networking",
        "description": "OSI model, TCP/IP stack, IP routing, DNS resolution, sockets, and network transport protocols.",
        "difficulty": "Hard",
        "question_count": 10,
        "icon": "wifi"
    },
    {
        "id": "cloud-fundamentals",
        "name": "Cloud Fundamentals",
        "category": "Cloud",
        "description": "IaaS, PaaS, SaaS delivery models, virtualization, containerization, cloud storage, and serverless concepts.",
        "difficulty": "Easy",
        "question_count": 10,
        "icon": "cloud"
    }
]

QUESTIONS = [
    {
        "id": "q_html_1",
        "skill_id": "html-css",
        "question": "Which HTML5 element is used to encapsulate standalone, self-contained content such as a blog post?",
        "options": [
            {"id": "A", "text": "<section>"},
            {"id": "B", "text": "<article>"},
            {"id": "C", "text": "<div>"},
            {"id": "D", "text": "<aside>"}
        ],
        "correct_answer": "B",
        "explanation": "<article> represents a self-contained composition that is intended to be independently reusable or distributable.",
        "difficulty": "Easy"
    },
    {
        "id": "q_html_2",
        "skill_id": "html-css",
        "question": "Which CSS property specifies how elements wrap inside a Flexbox container?",
        "options": [
            {"id": "A", "text": "flex-wrap"},
            {"id": "B", "text": "flex-flow-wrap"},
            {"id": "C", "text": "wrap-content"},
            {"id": "D", "text": "box-wrap"}
        ],
        "correct_answer": "A",
        "explanation": "flex-wrap determines whether flex items are forced onto a single line or can wrap onto multiple lines.",
        "difficulty": "Easy"
    },
    {
        "id": "q_html_3",
        "skill_id": "html-css",
        "question": "What is the CSS specificity score of a single ID selector?",
        "options": [
            {"id": "A", "text": "0, 0, 0, 1"},
            {"id": "B", "text": "0, 0, 1, 0"},
            {"id": "C", "text": "0, 1, 0, 0"},
            {"id": "D", "text": "1, 0, 0, 0"}
        ],
        "correct_answer": "C",
        "explanation": "Specificity is represented as (inline, ID, class/attribute/pseudo-class, element). An ID selector contributes 0,1,0,0.",
        "difficulty": "Medium"
    },
    {
        "id": "q_html_4",
        "skill_id": "html-css",
        "question": "Which CSS unit is relative to the root element font size (<html>)?",
        "options": [
            {"id": "A", "text": "em"},
            {"id": "B", "text": "rem"},
            {"id": "C", "text": "vh"},
            {"id": "D", "text": "%"}
        ],
        "correct_answer": "B",
        "explanation": "'rem' stands for Root EM and is relative to the font-size of the root HTML element.",
        "difficulty": "Easy"
    },
    {
        "id": "q_html_5",
        "skill_id": "html-css",
        "question": "Which CSS Grid property defines explicitly named grid tracks using template strings?",
        "options": [
            {"id": "A", "text": "grid-template-areas"},
            {"id": "B", "text": "grid-auto-flow"},
            {"id": "C", "text": "grid-template-columns"},
            {"id": "D", "text": "grid-area-map"}
        ],
        "correct_answer": "A",
        "explanation": "grid-template-areas specifies named grid areas for layout positioning.",
        "difficulty": "Medium"
    },
    {
        "id": "q_html_6",
        "skill_id": "html-css",
        "question": "In the CSS Box Model, which property sits between padding and margin?",
        "options": [
            {"id": "A", "text": "content"},
            {"id": "B", "text": "border"},
            {"id": "C", "text": "outline"},
            {"id": "D", "text": "box-sizing"}
        ],
        "correct_answer": "B",
        "explanation": "The CSS box model consists of Content -> Padding -> Border -> Margin.",
        "difficulty": "Easy"
    },
    {
        "id": "q_html_7",
        "skill_id": "html-css",
        "question": "What is the default value of the CSS 'position' property?",
        "options": [
            {"id": "A", "text": "relative"},
            {"id": "B", "text": "absolute"},
            {"id": "C", "text": "static"},
            {"id": "D", "text": "fixed"}
        ],
        "correct_answer": "C",
        "explanation": "HTML elements are positioned 'static' by default, following normal page flow.",
        "difficulty": "Easy"
    },
    {
        "id": "q_html_8",
        "skill_id": "html-css",
        "question": "Which HTML attribute provides alternative text for accessibility and broken image loading?",
        "options": [
            {"id": "A", "text": "title"},
            {"id": "B", "text": "alt"},
            {"id": "C", "text": "aria-label"},
            {"id": "D", "text": "caption"}
        ],
        "correct_answer": "B",
        "explanation": "The 'alt' attribute on <img> tags provides alternative text description for screen readers and missing media.",
        "difficulty": "Easy"
    },
    {
        "id": "q_html_9",
        "skill_id": "html-css",
        "question": "What does 'box-sizing: border-box' do?",
        "options": [
            {"id": "A", "text": "Adds additional margin inside the container border"},
            {"id": "B", "text": "Includes padding and border within the element's total specified width and height"},
            {"id": "C", "text": "Removes borders when element overflows"},
            {"id": "D", "text": "Forces all child elements to inherit border width"}
        ],
        "correct_answer": "B",
        "explanation": "border-box ensures width/height calculation includes content, padding, and border.",
        "difficulty": "Medium"
    },
    {
        "id": "q_html_10",
        "skill_id": "html-css",
        "question": "Which media query feature checks screen orientation?",
        "options": [
            {"id": "A", "text": "(orientation: portrait)"},
            {"id": "B", "text": "(device-aspect: vertical)"},
            {"id": "C", "text": "(screen-view: height-max)"},
            {"id": "D", "text": "(view-mode: mobile)"}
        ],
        "correct_answer": "A",
        "explanation": "The orientation media feature accepts 'portrait' or 'landscape' values.",
        "difficulty": "Hard"
    },

    {
        "id": "q_js_1",
        "skill_id": "javascript",
        "question": "Which built-in JavaScript method converts a JSON string into a JavaScript object?",
        "options": [
            {"id": "A", "text": "JSON.stringify()"},
            {"id": "B", "text": "JSON.parse()"},
            {"id": "C", "text": "JSON.toObject()"},
            {"id": "D", "text": "JSON.decode()"}
        ],
        "correct_answer": "B",
        "explanation": "JSON.parse() parses a JSON string, constructing the JavaScript value or object described by the string.",
        "difficulty": "Easy"
    },
    {
        "id": "q_js_2",
        "skill_id": "javascript",
        "question": "What will 'typeof null' return in JavaScript?",
        "options": [
            {"id": "A", "text": "'null'"},
            {"id": "B", "text": "'undefined'"},
            {"id": "C", "text": "'object'"},
            {"id": "D", "text": "'boolean'"}
        ],
        "correct_answer": "C",
        "explanation": "In JavaScript, typeof null returns 'object'. This is a historical bug in JS preserved for backward compatibility.",
        "difficulty": "Medium"
    },
    {
        "id": "q_js_3",
        "skill_id": "javascript",
        "question": "Which array method creates a new array with all elements that pass the test implemented by a provided function?",
        "options": [
            {"id": "A", "text": "map()"},
            {"id": "B", "text": "filter()"},
            {"id": "C", "text": "reduce()"},
            {"id": "D", "text": "forEach()"}
        ],
        "correct_answer": "B",
        "explanation": "filter() creates a shallow copy of a portion of a given array, filtered down to just the elements that pass the test function.",
        "difficulty": "Easy"
    },
    {
        "id": "q_js_4",
        "skill_id": "javascript",
        "question": "What is the output of '0 == false' and '0 === false' in JavaScript?",
        "options": [
            {"id": "A", "text": "true and true"},
            {"id": "B", "text": "false and false"},
            {"id": "C", "text": "true and false"},
            {"id": "D", "text": "false and true"}
        ],
        "correct_answer": "C",
        "explanation": "== performs loose equality coercion (0 equals false), while === performs strict equality checking without type coercion.",
        "difficulty": "Easy"
    },
    {
        "id": "q_js_5",
        "skill_id": "javascript",
        "question": "Which keyword declares a block-scoped variable that cannot be re-assigned?",
        "options": [
            {"id": "A", "text": "var"},
            {"id": "B", "text": "let"},
            {"id": "C", "text": "const"},
            {"id": "D", "text": "static"}
        ],
        "correct_answer": "C",
        "explanation": "const creates block-scoped read-only references to values.",
        "difficulty": "Easy"
    },
    {
        "id": "q_js_6",
        "skill_id": "javascript",
        "question": "What mechanism allows JavaScript functions to retain access to variables from their enclosing lexical scope even after that scope has executed?",
        "options": [
            {"id": "A", "text": "Callback queue"},
            {"id": "B", "text": "Closure"},
            {"id": "C", "text": "Prototype chain"},
            {"id": "D", "text": "Hoisting"}
        ],
        "correct_answer": "B",
        "explanation": "A closure is the combination of a function bundled together with references to its surrounding state (lexical environment).",
        "difficulty": "Hard"
    },
    {
        "id": "q_js_7",
        "skill_id": "javascript",
        "question": "Which ES6 feature extracts properties from objects or items from arrays into distinct variables?",
        "options": [
            {"id": "A", "text": "Destructuring assignment"},
            {"id": "B", "text": "Spread syntax"},
            {"id": "C", "text": "Rest parameters"},
            {"id": "D", "text": "Template literals"}
        ],
        "correct_answer": "A",
        "explanation": "Destructuring assignment allows unpacking values from arrays or properties from objects into distinct variables.",
        "difficulty": "Medium"
    },
    {
        "id": "q_js_8",
        "skill_id": "javascript",
        "question": "Which promise method resolves when all input promises have resolved, or rejects if any promise rejects?",
        "options": [
            {"id": "A", "text": "Promise.race()"},
            {"id": "B", "text": "Promise.all()"},
            {"id": "C", "text": "Promise.any()"},
            {"id": "D", "text": "Promise.allSettled()"}
        ],
        "correct_answer": "B",
        "explanation": "Promise.all() fulfills when all promises fulfill and rejects immediately if any promise rejects.",
        "difficulty": "Medium"
    },
    {
        "id": "q_js_9",
        "skill_id": "javascript",
        "question": "What is the result of 'Promise.resolve(5).then(x => x + 2)'?",
        "options": [
            {"id": "A", "text": "Returns a resolved Promise with value 7"},
            {"id": "B", "text": "Returns the primitive number 7"},
            {"id": "C", "text": "Throws a TypeError"},
            {"id": "D", "text": "Returns undefined"}
        ],
        "correct_answer": "A",
        "explanation": ".then() handlers always return a new Promise wrapping the returned value.",
        "difficulty": "Hard"
    },
    {
        "id": "q_js_10",
        "skill_id": "javascript",
        "question": "What handles microtasks like Promise callbacks in the JavaScript runtime environment?",
        "options": [
            {"id": "A", "text": "Macro Task Queue"},
            {"id": "B", "text": "Microtask Queue"},
            {"id": "C", "text": "Call Stack Sync Engine"},
            {"id": "D", "text": "Render Pipeline"}
        ],
        "correct_answer": "B",
        "explanation": "Promise callbacks are placed into the Microtask Queue, which executes before the next Event Loop tick / macrotask.",
        "difficulty": "Hard"
    },

    {
        "id": "q_py_1",
        "skill_id": "python",
        "question": "Which built-in Python data structure is mutable, ordered, and allows duplicate elements?",
        "options": [
            {"id": "A", "text": "Tuple"},
            {"id": "B", "text": "Set"},
            {"id": "C", "text": "List"},
            {"id": "D", "text": "Dictionary"}
        ],
        "correct_answer": "C",
        "explanation": "Lists are mutable, ordered sequences in Python that accept duplicates.",
        "difficulty": "Easy"
    },
    {
        "id": "q_py_2",
        "skill_id": "python",
        "question": "What expression creates a list of even numbers from 0 to 8 using list comprehension?",
        "options": [
            {"id": "A", "text": "[x for x in range(10) if x % 2 == 0]"},
            {"id": "B", "text": "(x for x in range(10) if x % 2 == 0)"},
            {"id": "C", "text": "[x if x % 2 == 0 for x in range(10)]"},
            {"id": "D", "text": "{x for x in range(10) if x % 2 == 0}"}
        ],
        "correct_answer": "A",
        "explanation": "[expression for item in iterable if condition] is the list comprehension syntax in Python.",
        "difficulty": "Easy"
    },
    {
        "id": "q_py_3",
        "skill_id": "python",
        "question": "What is the purpose of the '__init__' method in a Python class?",
        "options": [
            {"id": "A", "text": "To destroy object instances from memory"},
            {"id": "B", "text": "To serve as the constructor initializer when creating a class instance"},
            {"id": "C", "text": "To import base modules automatically"},
            {"id": "D", "text": "To static-type class attributes"}
        ],
        "correct_answer": "B",
        "explanation": "__init__ acts as the constructor method that initializes instance attributes when an object is instantiated.",
        "difficulty": "Easy"
    },
    {
        "id": "q_py_4",
        "skill_id": "python",
        "question": "What does the '*args' parameter allow a Python function to accept?",
        "options": [
            {"id": "A", "text": "Arbitrary keyword arguments as a dict"},
            {"id": "B", "text": "Variable number of positional arguments as a tuple"},
            {"id": "C", "text": "Required static type parameters"},
            {"id": "D", "text": "Pointers to global variables"}
        ],
        "correct_answer": "B",
        "explanation": "*args receives arbitrary positional arguments packed into a tuple.",
        "difficulty": "Medium"
    },
    {
        "id": "q_py_5",
        "skill_id": "python",
        "question": "What function decorator in Python transforms a method into a read-only property?",
        "options": [
            {"id": "A", "text": "@classmethod"},
            {"id": "B", "text": "@staticmethod"},
            {"id": "C", "text": "@property"},
            {"id": "D", "text": "@abstractmethod"}
        ],
        "correct_answer": "C",
        "explanation": "@property turns a method into a getter attribute on class instances.",
        "difficulty": "Medium"
    },
    {
        "id": "q_py_6",
        "skill_id": "python",
        "question": "What is the key difference between a Python Generator function and a regular function?",
        "options": [
            {"id": "A", "text": "Generators use 'yield' to lazily produce values one at a time"},
            {"id": "B", "text": "Generators run on a separate CPU core"},
            {"id": "C", "text": "Generators cannot accept parameters"},
            {"id": "D", "text": "Generators return lists instead of single objects"}
        ],
        "correct_answer": "A",
        "explanation": "Generators yield values lazily using the yield statement, preserving their execution context state.",
        "difficulty": "Medium"
    },
    {
        "id": "q_py_7",
        "skill_id": "python",
        "question": "What dictionary method retrieves a key's value without raising a KeyError if the key is missing?",
        "options": [
            {"id": "A", "text": "dict.find(key)"},
            {"id": "B", "text": "dict.get(key, default)"},
            {"id": "C", "text": "dict.fetch(key)"},
            {"id": "D", "text": "dict.lookup(key)"}
        ],
        "correct_answer": "B",
        "explanation": "dict.get(key, default) returns the value or default (None if unspecified) if key does not exist.",
        "difficulty": "Easy"
    },
    {
        "id": "q_py_8",
        "skill_id": "python",
        "question": "What module in Python standard library provides deep object cloning?",
        "options": [
            {"id": "A", "text": "clone"},
            {"id": "B", "text": "copy"},
            {"id": "C", "text": "duplication"},
            {"id": "D", "text": "object_ref"}
        ],
        "correct_answer": "B",
        "explanation": "The 'copy' module provides copy.deepcopy() for recursive deep object cloning.",
        "difficulty": "Medium"
    },
    {
        "id": "q_py_9",
        "skill_id": "python",
        "question": "What is GIL in CPython?",
        "options": [
            {"id": "A", "text": "Global Interface Library for C bindings"},
            {"id": "B", "text": "Global Interpreter Lock preventing multiple threads from executing CPython bytecode simultaneously"},
            {"id": "C", "text": "General Input Layer for async I/O"},
            {"id": "D", "text": "Garbage Inspection Loop for reference counting"}
        ],
        "correct_answer": "B",
        "explanation": "The GIL is a mutex that prevents multiple native threads from executing CPython bytecodes at once.",
        "difficulty": "Hard"
    },
    {
        "id": "q_py_10",
        "skill_id": "python",
        "question": "Which context manager syntax guarantees resources like files are properly closed after execution?",
        "options": [
            {"id": "A", "text": "using open('file.txt') as f:"},
            {"id": "B", "text": "with open('file.txt') as f:"},
            {"id": "C", "text": "try open('file.txt') as f:"},
            {"id": "D", "text": "auto f = open('file.txt')"}
        ],
        "correct_answer": "B",
        "explanation": "The 'with' statement invokes context managers (__enter__ and __exit__ methods) to safely manage resources.",
        "difficulty": "Medium"
    },

    {
        "id": "q_sql_1",
        "skill_id": "sql",
        "question": "Which SQL clause is used to filter records resulting from an aggregate function like GROUP BY?",
        "options": [
            {"id": "A", "text": "WHERE"},
            {"id": "B", "text": "HAVING"},
            {"id": "C", "text": "FILTER"},
            {"id": "D", "text": "ORDER BY"}
        ],
        "correct_answer": "B",
        "explanation": "HAVING filters aggregated groups after GROUP BY, whereas WHERE filters individual rows before aggregation.",
        "difficulty": "Easy"
    },
    {
        "id": "q_sql_2",
        "skill_id": "sql",
        "question": "Which JOIN returns all records from the left table and matched records from the right table?",
        "options": [
            {"id": "A", "text": "INNER JOIN"},
            {"id": "B", "text": "RIGHT JOIN"},
            {"id": "C", "text": "LEFT JOIN"},
            {"id": "D", "text": "FULL OUTER JOIN"}
        ],
        "correct_answer": "C",
        "explanation": "LEFT JOIN (or LEFT OUTER JOIN) preserves all rows from the left table regardless of matches in the right table.",
        "difficulty": "Easy"
    },
    {
        "id": "q_sql_3",
        "skill_id": "sql",
        "question": "Which command removes all rows from a table without logging individual row deletions, making it faster than DELETE?",
        "options": [
            {"id": "A", "text": "DROP TABLE"},
            {"id": "B", "text": "TRUNCATE TABLE"},
            {"id": "C", "text": "REMOVE ALL"},
            {"id": "D", "text": "CLEAR TABLE"}
        ],
        "correct_answer": "B",
        "explanation": "TRUNCATE TABLE quickly removes all rows from a table by deallocating table pages.",
        "difficulty": "Medium"
    },
    {
        "id": "q_sql_4",
        "skill_id": "sql",
        "question": "What type of key uniquely identifies each record in a database table?",
        "options": [
            {"id": "A", "text": "Foreign Key"},
            {"id": "B", "text": "Candidate Key"},
            {"id": "C", "text": "Primary Key"},
            {"id": "D", "text": "Super Key"}
        ],
        "correct_answer": "C",
        "explanation": "A Primary Key uniquely identifies each row in a database table and cannot contain NULL values.",
        "difficulty": "Easy"
    },
    {
        "id": "q_sql_5",
        "skill_id": "sql",
        "question": "What is the outcome of a Cartesian Product in SQL when performing a CROSS JOIN between Table A (5 rows) and Table B (4 rows)?",
        "options": [
            {"id": "A", "text": "9 rows"},
            {"id": "B", "text": "20 rows"},
            {"id": "C", "text": "5 rows"},
            {"id": "D", "text": "0 rows"}
        ],
        "correct_answer": "B",
        "explanation": "CROSS JOIN multiplies the rows of both tables (5 x 4 = 20 total output combinations).",
        "difficulty": "Medium"
    },
    {
        "id": "q_sql_6",
        "skill_id": "sql",
        "question": "Which SQL aggregate function counts the total number of non-null values in a column?",
        "options": [
            {"id": "A", "text": "SUM()"},
            {"id": "B", "text": "COUNT()"},
            {"id": "C", "text": "TOTAL()"},
            {"id": "D", "text": "TALLY()"}
        ],
        "correct_answer": "B",
        "explanation": "COUNT(column_name) returns the number of non-NULL values in the specified column.",
        "difficulty": "Easy"
    },
    {
        "id": "q_sql_7",
        "skill_id": "sql",
        "question": "What relational algebra condition states that every foreign key value must match a primary key value in the referenced table?",
        "options": [
            {"id": "A", "text": "Domain Integrity"},
            {"id": "B", "text": "Referential Integrity"},
            {"id": "C", "text": "Entity Integrity"},
            {"id": "D", "text": "Atomicity Constraint"}
        ],
        "correct_answer": "B",
        "explanation": "Referential Integrity ensures relationships between tables remain consistent across foreign key constraints.",
        "difficulty": "Medium"
    },
    {
        "id": "q_sql_8",
        "skill_id": "sql",
        "question": "Which database normalization form eliminates partial dependency on a composite primary key?",
        "options": [
            {"id": "A", "text": "1NF"},
            {"id": "B", "text": "2NF"},
            {"id": "C", "text": "3NF"},
            {"id": "D", "text": "BCNF"}
        ],
        "correct_answer": "B",
        "explanation": "Second Normal Form (2NF) requires 1NF compliance and that all non-key attributes are fully dependent on the primary key.",
        "difficulty": "Hard"
    },
    {
        "id": "q_sql_9",
        "skill_id": "sql",
        "question": "What does ACID property 'I' stand for in database transaction design?",
        "options": [
            {"id": "A", "text": "Indexability"},
            {"id": "B", "text": "Isolation"},
            {"id": "C", "text": "Immutability"},
            {"id": "D", "text": "Inheritance"}
        ],
        "correct_answer": "B",
        "explanation": "Isolation ensures concurrent transactions execute independently without interfering with each other.",
        "difficulty": "Medium"
    },
    {
        "id": "q_sql_10",
        "skill_id": "sql",
        "question": "Which SQL keyword prevents duplicate records from being returned in query result sets?",
        "options": [
            {"id": "A", "text": "UNIQUE"},
            {"id": "B", "text": "DISTINCT"},
            {"id": "C", "text": "SINGLE"},
            {"id": "D", "text": "NO_DUPLICATES"}
        ],
        "correct_answer": "B",
        "explanation": "SELECT DISTINCT removes duplicate rows from the query output.",
        "difficulty": "Easy"
    },

    {
        "id": "q_ds_1",
        "skill_id": "data-structures",
        "question": "What is the average-case search time complexity of a Hash Table with good hash distribution?",
        "options": [
            {"id": "A", "text": "O(1)"},
            {"id": "B", "text": "O(log n)"},
            {"id": "C", "text": "O(n)"},
            {"id": "D", "text": "O(n^2)"}
        ],
        "correct_answer": "A",
        "explanation": "Hash tables provide constant O(1) average time complexity for lookup operations.",
        "difficulty": "Medium"
    },
    {
        "id": "q_ds_2",
        "skill_id": "data-structures",
        "question": "Which data structure follows the LIFO (Last In, First Out) principle?",
        "options": [
            {"id": "A", "text": "Queue"},
            {"id": "B", "text": "Stack"},
            {"id": "C", "text": "Binary Heap"},
            {"id": "D", "text": "Linked List"}
        ],
        "correct_answer": "B",
        "explanation": "Stacks operate on LIFO principle (push, pop).",
        "difficulty": "Easy"
    },
    {
        "id": "q_ds_3",
        "skill_id": "data-structures",
        "question": "In a balanced Binary Search Tree (BST) with n elements, what is the worst-case search complexity?",
        "options": [
            {"id": "A", "text": "O(1)"},
            {"id": "B", "text": "O(log n)"},
            {"id": "C", "text": "O(n)"},
            {"id": "D", "text": "O(n log n)"}
        ],
        "correct_answer": "B",
        "explanation": "A balanced BST maintains height O(log n), making search, insertion, and deletion O(log n).",
        "difficulty": "Medium"
    },
    {
        "id": "q_ds_4",
        "skill_id": "data-structures",
        "question": "Which tree traversal visits node sequence: Left Subtree -> Root -> Right Subtree?",
        "options": [
            {"id": "A", "text": "Pre-order"},
            {"id": "B", "text": "In-order"},
            {"id": "C", "text": "Post-order"},
            {"id": "D", "text": "Level-order"}
        ],
        "correct_answer": "B",
        "explanation": "In-order traversal visits left child, root node, then right child (producing sorted order in a BST).",
        "difficulty": "Medium"
    },
    {
        "id": "q_ds_5",
        "skill_id": "data-structures",
        "question": "What graph algorithm finds the shortest path between nodes in a weighted graph with non-negative edge weights?",
        "options": [
            {"id": "A", "text": "Dijkstra's Algorithm"},
            {"id": "B", "text": "Depth-First Search (DFS)"},
            {"id": "C", "text": "Kruskal's Algorithm"},
            {"id": "D", "text": "Floyd-Warshall"}
        ],
        "correct_answer": "A",
        "explanation": "Dijkstra's algorithm computes single-source shortest paths on non-negative weighted graphs.",
        "difficulty": "Hard"
    },
    {
        "id": "q_ds_6",
        "skill_id": "data-structures",
        "question": "Which queue variant allows insertion and deletion from both front and rear ends?",
        "options": [
            {"id": "A", "text": "Priority Queue"},
            {"id": "B", "text": "Circular Queue"},
            {"id": "C", "text": "Deque (Double-Ended Queue)"},
            {"id": "D", "text": "Monotonic Queue"}
        ],
        "correct_answer": "C",
        "explanation": "A Deque allows items to be added or removed from either the front or the back.",
        "difficulty": "Medium"
    },
    {
        "id": "q_ds_7",
        "skill_id": "data-structures",
        "question": "What is the space complexity of an adjacency matrix representation of a graph with V vertices?",
        "options": [
            {"id": "A", "text": "O(V)"},
            {"id": "B", "text": "O(V + E)"},
            {"id": "C", "text": "O(V^2)"},
            {"id": "D", "text": "O(E^2)"}
        ],
        "correct_answer": "C",
        "explanation": "An adjacency matrix is a V x V 2D array, consuming O(V^2) memory space regardless of edge count E.",
        "difficulty": "Hard"
    },
    {
        "id": "q_ds_8",
        "skill_id": "data-structures",
        "question": "Which sorting algorithm operates with O(n log n) worst-case time complexity and is a stable sort?",
        "options": [
            {"id": "A", "text": "Quick Sort"},
            {"id": "B", "text": "Merge Sort"},
            {"id": "C", "text": "Heap Sort"},
            {"id": "D", "text": "Selection Sort"}
        ],
        "correct_answer": "B",
        "explanation": "Merge sort guarantees O(n log n) performance in all cases and preserves relative order of equal elements (stable).",
        "difficulty": "Hard"
    },
    {
        "id": "q_ds_9",
        "skill_id": "data-structures",
        "question": "What node reference does the tail node of a singly linked list point to?",
        "options": [
            {"id": "A", "text": "Head node"},
            {"id": "B", "text": "Null / None"},
            {"id": "C", "text": "Self reference"},
            {"id": "D", "text": "Previous node"}
        ],
        "correct_answer": "B",
        "explanation": "In a linear singly linked list, the tail node's next pointer points to Null (or None).",
        "difficulty": "Easy"
    },
    {
        "id": "q_ds_10",
        "skill_id": "data-structures",
        "question": "What collision resolution technique links all items hashing to the same bucket in a linked list?",
        "options": [
            {"id": "A", "text": "Linear Probing"},
            {"id": "B", "text": "Separate Chaining"},
            {"id": "C", "text": "Quadratic Probing"},
            {"id": "D", "text": "Double Hashing"}
        ],
        "correct_answer": "B",
        "explanation": "Separate chaining maintains a linked list of records for each hash table bucket.",
        "difficulty": "Medium"
    },

    {
        "id": "q_web_1",
        "skill_id": "web-tech",
        "question": "Which HTTP request method is idempotent and intended to completely replace an existing resource?",
        "options": [
            {"id": "A", "text": "POST"},
            {"id": "B", "text": "PUT"},
            {"id": "C", "text": "PATCH"},
            {"id": "D", "text": "OPTIONS"}
        ],
        "correct_answer": "B",
        "explanation": "PUT is idempotent and replaces the target resource with the request payload.",
        "difficulty": "Medium"
    },
    {
        "id": "q_web_2",
        "skill_id": "web-tech",
        "question": "What HTTP status code represents '201 Created'?",
        "options": [
            {"id": "A", "text": "Resource deleted successfully"},
            {"id": "B", "text": "Request succeeded and a new resource was created"},
            {"id": "C", "text": "Request redirected to new location"},
            {"id": "D", "text": "Accepted for background processing"}
        ],
        "correct_answer": "B",
        "explanation": "HTTP 201 Created indicates successful resource creation.",
        "difficulty": "Easy"
    },
    {
        "id": "q_web_3",
        "skill_id": "web-tech",
        "question": "What browser mechanism restricts web pages from making AJAX requests to a different domain than the origin domain?",
        "options": [
            {"id": "A", "text": "Same-Origin Policy (SOP)"},
            {"id": "B", "text": "Content Security Policy (CSP)"},
            {"id": "C", "text": "Cross-Site Scripting (XSS)"},
            {"id": "D", "text": "Strict Transport Security (HSTS)"}
        ],
        "correct_answer": "A",
        "explanation": "The Same-Origin Policy is a fundamental security model restricting cross-domain script access.",
        "difficulty": "Medium"
    },
    {
        "id": "q_web_4",
        "skill_id": "web-tech",
        "question": "Which HTTP header enables cross-origin resource access for specified origins?",
        "options": [
            {"id": "A", "text": "Access-Control-Allow-Origin"},
            {"id": "B", "text": "X-Frame-Options"},
            {"id": "C", "text": "Authorization-Bearer"},
            {"id": "D", "text": "Set-Cookie"}
        ],
        "correct_answer": "A",
        "explanation": "Access-Control-Allow-Origin is a CORS header indicating whether response sharing is permitted with the requesting origin.",
        "difficulty": "Easy"
    },
    {
        "id": "q_web_5",
        "skill_id": "web-tech",
        "question": "What type of web storage stores data with no expiration time across browser sessions?",
        "options": [
            {"id": "A", "text": "sessionStorage"},
            {"id": "B", "text": "localStorage"},
            {"id": "C", "text": "Cookie"},
            {"id": "D", "text": "Cache Storage"}
        ],
        "correct_answer": "B",
        "explanation": "localStorage data persists indefinitely until explicitly cleared, surviving browser restarts.",
        "difficulty": "Easy"
    },
    {
        "id": "q_web_6",
        "skill_id": "web-tech",
        "question": "What security vulnerability occurs when malicious scripts are injected into trusted web applications and executed by victims?",
        "options": [
            {"id": "A", "text": "SQL Injection (SQLi)"},
            {"id": "B", "text": "Cross-Site Scripting (XSS)"},
            {"id": "C", "text": "Cross-Site Request Forgery (CSRF)"},
            {"id": "D", "text": "Server-Side Template Injection (SSTI)"}
        ],
        "correct_answer": "B",
        "explanation": "XSS occurs when untrusted user input is rendered in client browsers without proper sanitization.",
        "difficulty": "Medium"
    },
    {
        "id": "q_web_7",
        "skill_id": "web-tech",
        "question": "What cookie attribute prevents client-side scripts (like JavaScript document.cookie) from accessing the cookie?",
        "options": [
            {"id": "A", "text": "Secure"},
            {"id": "B", "text": "SameSite"},
            {"id": "C", "text": "HttpOnly"},
            {"id": "D", "text": "Domain"}
        ],
        "correct_answer": "C",
        "explanation": "HttpOnly prevents client-side scripts from reading cookie data, mitigating XSS token theft.",
        "difficulty": "Medium"
    },
    {
        "id": "q_web_8",
        "skill_id": "web-tech",
        "question": "What protocol upgrade does WebSocket use during its initial handshake?",
        "options": [
            {"id": "A", "text": "HTTP 101 Switching Protocols"},
            {"id": "B", "text": "HTTP 200 OK"},
            {"id": "C", "text": "HTTP 301 Moved Permanently"},
            {"id": "D", "text": "HTTP 426 Upgrade Required"}
        ],
        "correct_answer": "A",
        "explanation": "WebSocket connection establishes via HTTP GET request with 'Upgrade: websocket' header, receiving 101 Switching Protocols.",
        "difficulty": "Hard"
    },
    {
        "id": "q_web_9",
        "skill_id": "web-tech",
        "question": "Which HTTP status code indicates '403 Forbidden'?",
        "options": [
            {"id": "A", "text": "Authentication credentials are missing"},
            {"id": "B", "text": "Server understands request but refuses to authorize access"},
            {"id": "C", "text": "Requested resource could not be found"},
            {"id": "D", "text": "Server encountered an unhandled exception"}
        ],
        "correct_answer": "B",
        "explanation": "403 Forbidden means the server authenticated the user but refuses authorization rights to the resource.",
        "difficulty": "Easy"
    },
    {
        "id": "q_web_10",
        "skill_id": "web-tech",
        "question": "What standard architectural constraint of REST states that no client context is stored on the server between requests?",
        "options": [
            {"id": "A", "text": "Cacheable"},
            {"id": "B", "text": "Stateless"},
            {"id": "C", "text": "Layered System"},
            {"id": "D", "text": "Uniform Interface"}
        ],
        "correct_answer": "B",
        "explanation": "Stateless constraint requires every client request to contain all information needed to process it.",
        "difficulty": "Medium"
    },

    {
        "id": "q_cn_1",
        "skill_id": "computer-networks",
        "question": "Which layer of the OSI model handles end-to-end communication, flow control, and error recovery using TCP/UDP?",
        "options": [
            {"id": "A", "text": "Network Layer (Layer 3)"},
            {"id": "B", "text": "Transport Layer (Layer 4)"},
            {"id": "C", "text": "Data Link Layer (Layer 2)"},
            {"id": "D", "text": "Session Layer (Layer 5)"}
        ],
        "correct_answer": "B",
        "explanation": "Transport Layer (Layer 4) provides transparent transfer of data between end users.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cn_2",
        "skill_id": "computer-networks",
        "question": "What protocol translates human-readable domain names (e.g. google.com) into numerical IP addresses?",
        "options": [
            {"id": "A", "text": "DHCP"},
            {"id": "B", "text": "ARP"},
            {"id": "C", "text": "DNS"},
            {"id": "D", "text": "ICMP"}
        ],
        "correct_answer": "C",
        "explanation": "Domain Name System (DNS) resolves domain names to IP addresses.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cn_3",
        "skill_id": "computer-networks",
        "question": "What sequence of packets completes the standard TCP three-way handshake?",
        "options": [
            {"id": "A", "text": "SYN -> SYN-ACK -> ACK"},
            {"id": "B", "text": "ACK -> SYN -> FIN"},
            {"id": "C", "text": "REQ -> RES -> CONFIRM"},
            {"id": "D", "text": "PING -> PONG -> ACK"}
        ],
        "correct_answer": "A",
        "explanation": "TCP connection establishment sends SYN from client, SYN-ACK response from server, then ACK from client.",
        "difficulty": "Medium"
    },
    {
        "id": "q_cn_4",
        "skill_id": "computer-networks",
        "question": "What is the standard netmask for a IPv4 Class C CIDR /24 subnet?",
        "options": [
            {"id": "A", "text": "255.0.0.0"},
            {"id": "B", "text": "255.255.0.0"},
            {"id": "C", "text": "255.255.255.0"},
            {"id": "D", "text": "255.255.255.255"}
        ],
        "correct_answer": "C",
        "explanation": "/24 CIDR prefix represents 24 network bits = 255.255.255.0.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cn_5",
        "skill_id": "computer-networks",
        "question": "Which protocol resolves IP addresses to physical MAC addresses on a local area network?",
        "options": [
            {"id": "A", "text": "ARP (Address Resolution Protocol)"},
            {"id": "B", "text": "RARP"},
            {"id": "C", "text": "NAT"},
            {"id": "D", "text": "BGP"}
        ],
        "correct_answer": "A",
        "explanation": "ARP maps dynamic Layer 3 IPv4 addresses to physical Layer 2 MAC addresses.",
        "difficulty": "Medium"
    },
    {
        "id": "q_cn_6",
        "skill_id": "computer-networks",
        "question": "What port number is standard for HTTPS encrypted web traffic?",
        "options": [
            {"id": "A", "text": "80"},
            {"id": "B", "text": "22"},
            {"id": "C", "text": "443"},
            {"id": "D", "text": "8080"}
        ],
        "correct_answer": "C",
        "explanation": "Port 443 is the standard default port for HTTP over TLS/SSL (HTTPS).",
        "difficulty": "Easy"
    },
    {
        "id": "q_cn_7",
        "skill_id": "computer-networks",
        "question": "What transport layer protocol is connectionless, lightweight, and low-latency without delivery guarantees?",
        "options": [
            {"id": "A", "text": "TCP"},
            {"id": "B", "text": "UDP"},
            {"id": "C", "text": "SCTP"},
            {"id": "D", "text": "FTP"}
        ],
        "correct_answer": "B",
        "explanation": "User Datagram Protocol (UDP) is connectionless and prioritized for speed over reliability.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cn_8",
        "skill_id": "computer-networks",
        "question": "What algorithm prevents switching loops in Ethernet network topologies?",
        "options": [
            {"id": "A", "text": "Spanning Tree Protocol (STP)"},
            {"id": "B", "text": "Open Shortest Path First (OSPF)"},
            {"id": "C", "text": "Border Gateway Protocol (BGP)"},
            {"id": "D", "text": "Distance Vector Routing"}
        ],
        "correct_answer": "A",
        "explanation": "STP builds a loop-free logical topology for Ethernet networks.",
        "difficulty": "Hard"
    },
    {
        "id": "q_cn_9",
        "skill_id": "computer-networks",
        "question": "What ICMP command utility measures packet round-trip time and route hops to a destination host?",
        "options": [
            {"id": "A", "text": "traceroute / tracert"},
            {"id": "B", "text": "netstat"},
            {"id": "C", "text": "nslookup"},
            {"id": "D", "text": "ipconfig"}
        ],
        "correct_answer": "A",
        "explanation": "traceroute tracks the IP hop path and latency packets take across routers.",
        "difficulty": "Medium"
    },
    {
        "id": "q_cn_10",
        "skill_id": "computer-networks",
        "question": "What is the maximum payload length (MTU) for standard Ethernet frames?",
        "options": [
            {"id": "A", "text": "512 bytes"},
            {"id": "B", "text": "1500 bytes"},
            {"id": "C", "text": "4096 bytes"},
            {"id": "D", "text": "65535 bytes"}
        ],
        "correct_answer": "B",
        "explanation": "Standard Ethernet Maximum Transmission Unit (MTU) size is 1500 bytes.",
        "difficulty": "Hard"
    },

    {
        "id": "q_cloud_1",
        "skill_id": "cloud-fundamentals",
        "question": "Which cloud service model provides virtual machines, virtual storage, and raw networking components?",
        "options": [
            {"id": "A", "text": "IaaS (Infrastructure as a Service)"},
            {"id": "B", "text": "PaaS (Platform as a Service)"},
            {"id": "C", "text": "SaaS (Software as a Service)"},
            {"id": "D", "text": "FaaS (Function as a Service)"}
        ],
        "correct_answer": "A",
        "explanation": "IaaS delivers fundamental compute, network, and storage infrastructure on demand.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cloud_2",
        "skill_id": "cloud-fundamentals",
        "question": "What cloud architecture paradigm automatically scales individual function executions in response to events without provisioning servers?",
        "options": [
            {"id": "A", "text": "Monolithic Hosting"},
            {"id": "B", "text": "Serverless / FaaS"},
            {"id": "C", "text": "Bare Metal Provisioning"},
            {"id": "D", "text": "Static Cluster Deployment"}
        ],
        "correct_answer": "B",
        "explanation": "Serverless (FaaS) allows running code without configuring or managing underlying server instances.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cloud_3",
        "skill_id": "cloud-fundamentals",
        "question": "Which term describes automatically increasing or decreasing cloud resources matching real-time user traffic demand?",
        "options": [
            {"id": "A", "text": "Auto Scaling / Elasticity"},
            {"id": "B", "text": "Fault Tolerance"},
            {"id": "C", "text": "High Availability"},
            {"id": "D", "text": "Disaster Recovery"}
        ],
        "correct_answer": "A",
        "explanation": "Elasticity refers to the ability to scale compute resources dynamically up or down.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cloud_4",
        "skill_id": "cloud-fundamentals",
        "question": "What open-source container engine packages applications and their dependencies into standardized lightweight isolated containers?",
        "options": [
            {"id": "A", "text": "Kubernetes"},
            {"id": "B", "text": "Docker"},
            {"id": "C", "text": "Hyper-V"},
            {"id": "D", "text": "Terraform"}
        ],
        "correct_answer": "B",
        "explanation": "Docker standardizes software execution in containerized environments.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cloud_5",
        "skill_id": "cloud-fundamentals",
        "question": "What is the primary role of Kubernetes in cloud engineering?",
        "options": [
            {"id": "A", "text": "Relational Database Engine"},
            {"id": "B", "text": "Container Orchestration"},
            {"id": "C", "text": "DNS Name Registrar"},
            {"id": "D", "text": "CSS Style Compiler"}
        ],
        "correct_answer": "B",
        "explanation": "Kubernetes automates deployment, scaling, and management of containerized applications.",
        "difficulty": "Medium"
    },
    {
        "id": "q_cloud_6",
        "skill_id": "cloud-fundamentals",
        "question": "In the Cloud Shared Responsibility Model, who is responsible for managing physical server hardware security?",
        "options": [
            {"id": "A", "text": "Customer / End-User"},
            {"id": "B", "text": "Cloud Service Provider (CSP)"},
            {"id": "C", "text": "Third-Party Auditor"},
            {"id": "D", "text": "Local ISP"}
        ],
        "correct_answer": "B",
        "explanation": "The Cloud Provider manages security OF the cloud (physical infrastructure, hardware, host OS).",
        "difficulty": "Easy"
    },
    {
        "id": "q_cloud_7",
        "skill_id": "cloud-fundamentals",
        "question": "Which technology enables multiple isolated Virtual Machines (VMs) to run on a single physical host hardware machine?",
        "options": [
            {"id": "A", "text": "Hypervisor"},
            {"id": "B", "text": "Load Balancer"},
            {"id": "C", "text": "API Gateway"},
            {"id": "D", "text": "Content Delivery Network (CDN)"}
        ],
        "correct_answer": "A",
        "explanation": "A Hypervisor creates and runs virtual machines by abstracting physical host hardware.",
        "difficulty": "Medium"
    },
    {
        "id": "q_cloud_8",
        "skill_id": "cloud-fundamentals",
        "question": "What type of storage is unstructured blob/object storage accessed via HTTP APIs (e.g. AWS S3, Azure Blob)?",
        "options": [
            {"id": "A", "text": "Block Storage"},
            {"id": "B", "text": "Object Storage"},
            {"id": "C", "text": "File Storage (NFS)"},
            {"id": "D", "text": "RAM Cache"}
        ],
        "correct_answer": "B",
        "explanation": "Object storage manages data as objects with metadata and unique identifiers accessed via web APIs.",
        "difficulty": "Medium"
    },
    {
        "id": "q_cloud_9",
        "skill_id": "cloud-fundamentals",
        "question": "What cloud deployment model combines private on-premise infrastructure with public cloud services?",
        "options": [
            {"id": "A", "text": "Public Cloud"},
            {"id": "B", "text": "Private Cloud"},
            {"id": "C", "text": "Hybrid Cloud"},
            {"id": "D", "text": "Community Cloud"}
        ],
        "correct_answer": "C",
        "explanation": "Hybrid cloud integrates private infrastructure with public cloud environments.",
        "difficulty": "Easy"
    },
    {
        "id": "q_cloud_10",
        "skill_id": "cloud-fundamentals",
        "question": "What does RPO (Recovery Point Objective) define in disaster recovery planning?",
        "options": [
            {"id": "A", "text": "Maximum acceptable duration of data loss measured in time"},
            {"id": "B", "text": "Maximum allowed time to restore services after outage"},
            {"id": "C", "text": "The total financial budget for cloud backups"},
            {"id": "D", "text": "The total bandwidth limit of cloud network tunnels"}
        ],
        "correct_answer": "A",
        "explanation": "RPO measures the maximum acceptable age of files/data loss during a disaster.",
        "difficulty": "Hard"
    }
]

SKILLS_BY_ID = {s["id"]: s for s in SKILLS}
QUESTIONS_BY_ID = {q["id"]: q for q in QUESTIONS}

assessments_by_id = {}
attempts_by_id = {}
attempts_list = []

def seed_initial_attempts():
    sample_attempts_data = [
        ("html-css", 9, 1, 0, "2026-09-24 10:15:00"),
        ("javascript", 8, 2, 0, "2026-09-24 14:30:00"),
        ("python", 7, 2, 1, "2026-09-25 09:20:00"),
        ("sql", 8, 1, 1, "2026-09-25 16:45:00"),
        ("data-structures", 6, 3, 1, "2026-09-26 08:10:00")
    ]
    for skill_id, correct, incorrect, unanswered, ts in sample_attempts_data:
        skill = SKILLS_BY_ID.get(skill_id)
        if not skill:
            continue
        tot = correct + incorrect + unanswered
        pct = round((correct / tot) * 100, 1)
        att_id = f"att_seed_{uuid.uuid4().hex[:8]}"
        
        skill_qs = [q for q in QUESTIONS if q["skill_id"] == skill_id]
        reviews = []
        for idx, q in enumerate(skill_qs[:tot]):
            if idx < correct:
                st = "correct"
                u_ans = q["correct_answer"]
            elif idx < correct + incorrect:
                st = "incorrect"
                wrong_opts = [o["id"] for o in q["options"] if o["id"] != q["correct_answer"]]
                u_ans = wrong_opts[0] if wrong_opts else "A"
            else:
                st = "unanswered"
                u_ans = None
            reviews.append({
                "question_id": q["id"],
                "question": q["question"],
                "options": q["options"],
                "user_answer": u_ans,
                "correct_answer": q["correct_answer"],
                "explanation": q["explanation"],
                "status": st
            })

        attempt_obj = {
            "attempt_id": att_id,
            "assessment_id": f"asm_seed_{uuid.uuid4().hex[:6]}",
            "student_name": "Test Student",
            "skill_id": skill_id,
            "skill_name": skill["name"],
            "timestamp": ts,
            "total": tot,
            "correct": correct,
            "incorrect": incorrect,
            "unanswered": unanswered,
            "score_percentage": pct,
            "reviews": reviews
        }
        attempts_by_id[att_id] = attempt_obj
        attempts_list.append(attempt_obj)

seed_initial_attempts()

def find_skill(skill_id):
    return SKILLS_BY_ID.get(skill_id)

def find_question(question_id):
    return QUESTIONS_BY_ID.get(question_id)

def find_attempt(attempt_id):
    return attempts_by_id.get(attempt_id)

def get_questions_for_skill(skill_id):
    return [q for q in QUESTIONS if q["skill_id"] == skill_id]

def generate_attempt_id():
    return f"att_{uuid.uuid4().hex[:10]}"

def success_response(data, status_code=200):
    return jsonify({"success": True, "data": data}), status_code

def error_response(message, status_code=400):
    return jsonify({"success": False, "error": message}), status_code

def calculate_percentage(correct, total):
    if total <= 0:
        return 0.0
    return round((correct / total) * 100, 1)

def validate_submission(data):
    if not isinstance(data, dict):
        return False, "Malformed request body. Expected JSON object."
    
    assessment_id = data.get("assessment_id")
    if not assessment_id or not isinstance(assessment_id, str):
        return False, "Missing or invalid assessment_id."
    
    skill_id = data.get("skill_id")
    if not skill_id or not isinstance(skill_id, str):
        return False, "Missing or invalid skill_id."
    
    if skill_id not in SKILLS_BY_ID:
        return False, f"Invalid skill_id '{skill_id}'."
        
    assessment = assessments_by_id.get(assessment_id)
    if not assessment:
        return False, f"Assessment ID '{assessment_id}' not found or expired."
        
    if assessment["skill_id"] != skill_id:
        return False, f"Skill ID '{skill_id}' does not match assessment skill '{assessment['skill_id']}'."
        
    answers = data.get("answers")
    if not isinstance(answers, dict):
        return False, "Field 'answers' must be a dictionary object mapping question IDs to option IDs."

    valid_q_ids = set(assessment["question_ids"])
    for q_id, opt_id in answers.items():
        if q_id not in valid_q_ids:
            return False, f"Question ID '{q_id}' does not belong to assessment '{assessment_id}'."
        if opt_id is not None and opt_id not in ["A", "B", "C", "D"]:
            return False, f"Invalid option '{opt_id}' for question '{q_id}'. Expected A, B, C, or D."
            
    return True, None

def calculate_score(questions, submitted_answers):
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    reviews = []

    for q in questions:
        q_id = q["id"]
        user_ans = submitted_answers.get(q_id)
        
        if user_ans == "" or user_ans is None:
            user_ans = None

        if user_ans is None:
            unanswered_count += 1
            status = "unanswered"
        elif user_ans == q["correct_answer"]:
            correct_count += 1
            status = "correct"
        else:
            incorrect_count += 1
            status = "incorrect"

        reviews.append({
            "question_id": q_id,
            "question": q["question"],
            "options": q["options"],
            "user_answer": user_ans,
            "correct_answer": q["correct_answer"],
            "explanation": q["explanation"],
            "status": status,
            "difficulty": q["difficulty"]
        })

    total = len(questions)
    assert correct_count + incorrect_count + unanswered_count == total, "Score component mismatch!"
    percentage = calculate_percentage(correct_count, total)

    return {
        "total": total,
        "correct": correct_count,
        "incorrect": incorrect_count,
        "unanswered": unanswered_count,
        "percentage": percentage,
        "reviews": reviews
    }

def calculate_skill_stats(skill_id):
    skill_attempts = [a for a in attempts_list if a["skill_id"] == skill_id]
    if not skill_attempts:
        return {
            "attempt_count": 0,
            "best_score": 0,
            "average_score": 0,
            "latest_score": None,
            "progress_percentage": 0
        }
    
    scores = [a["score_percentage"] for a in skill_attempts]
    best_score = max(scores)
    avg_score = round(sum(scores) / len(scores), 1)
    latest_score = skill_attempts[-1]["score_percentage"]
    
    return {
        "attempt_count": len(skill_attempts),
        "best_score": best_score,
        "average_score": avg_score,
        "latest_score": latest_score,
        "progress_percentage": best_score
    }

def build_dashboard():
    total_attempts = len(attempts_list)
    if total_attempts == 0:
        avg_score = 0
        best_score = 0
        questions_answered = 0
    else:
        scores = [a["score_percentage"] for a in attempts_list]
        avg_score = round(sum(scores) / total_attempts, 1)
        best_score = max(scores)
        questions_answered = sum(a["correct"] + a["incorrect"] for a in attempts_list)

    skill_progress_list = []
    for skill in SKILLS:
        stats = calculate_skill_stats(skill["id"])
        skill_progress_list.append({
            "skill_id": skill["id"],
            "skill_name": skill["name"],
            "category": skill["category"],
            "difficulty": skill["difficulty"],
            "icon": skill["icon"],
            "attempt_count": stats["attempt_count"],
            "best_score": stats["best_score"],
            "average_score": stats["average_score"],
            "latest_score": stats["latest_score"],
            "progress_percentage": stats["progress_percentage"]
        })

    recent = list(reversed(attempts_list))[:5]
    
    # Exclude detailed reviews array from overview payload
    recent_light = []
    for a in recent:
        recent_light.append({
            "attempt_id": a["attempt_id"],
            "skill_id": a["skill_id"],
            "skill_name": a["skill_name"],
            "timestamp": a["timestamp"],
            "total": a["total"],
            "correct": a["correct"],
            "incorrect": a["incorrect"],
            "unanswered": a["unanswered"],
            "score_percentage": a["score_percentage"]
        })

    return {
        "student_name": "Test Student",
        "assessments_taken": total_attempts,
        "average_score": avg_score,
        "best_score": best_score,
        "questions_answered": questions_answered,
        "skill_progress": skill_progress_list,
        "recent_attempts": recent_light
    }

@app.route("/api/skills", methods=["GET"])
def api_get_skills():
    data = []
    for skill in SKILLS:
        stats = calculate_skill_stats(skill["id"])
        item = dict(skill)
        item.update(stats)
        data.append(item)
    return success_response(data)

@app.route("/api/skills/<skill_id>", methods=["GET"])
def api_get_skill(skill_id):
    skill = find_skill(skill_id)
    if not skill:
        return error_response(f"Skill '{skill_id}' not found.", 404)
    
    stats = calculate_skill_stats(skill_id)
    result = dict(skill)
    result.update(stats)
    return success_response(result)

@app.route("/api/assessments/start", methods=["POST"])
def api_start_assessment():
    req_json = request.get_json(silent=True) or {}
    skill_id = req_json.get("skill_id")
    
    if not skill_id:
        return error_response("Missing skill_id parameter in request body.")
        
    skill = find_skill(skill_id)
    if not skill:
        return error_response(f"Skill '{skill_id}' not found.", 404)
        
    questions = get_questions_for_skill(skill_id)
    if not questions:
        return error_response(f"No questions available for skill '{skill_id}'.", 404)

    assessment_id = f"asm_{uuid.uuid4().hex[:10]}"
    
    assessments_by_id[assessment_id] = {
        "assessment_id": assessment_id,
        "skill_id": skill_id,
        "question_ids": [q["id"] for q in questions],
        "created_at": datetime.now().isoformat(),
        "duration_seconds": 600,
        "status": "active"
    }

    # CRITICAL SECURITY: Strip correct_answer and explanation before sending to client!
    client_questions = []
    for q in questions:
        client_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "difficulty": q["difficulty"]
        })

    stats = calculate_skill_stats(skill_id)

    payload = {
        "assessment_id": assessment_id,
        "skill": {
            "id": skill["id"],
            "name": skill["name"],
            "category": skill["category"],
            "difficulty": skill["difficulty"],
            "question_count": len(client_questions),
            "best_score": stats["best_score"],
            "attempt_count": stats["attempt_count"]
        },
        "duration_seconds": 600,
        "questions": client_questions
    }

    return success_response(payload, 201)

@app.route("/api/assessments/<assessment_id>", methods=["GET"])
def api_get_assessment(assessment_id):
    assessment = assessments_by_id.get(assessment_id)
    if not assessment:
        return error_response(f"Assessment '{assessment_id}' not found.", 404)

    skill = find_skill(assessment["skill_id"])
    questions = [find_question(qid) for qid in assessment["question_ids"] if find_question(qid)]

    client_questions = []
    for q in questions:
        client_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "difficulty": q["difficulty"]
        })

    return success_response({
        "assessment_id": assessment_id,
        "skill": skill,
        "status": assessment["status"],
        "duration_seconds": assessment["duration_seconds"],
        "questions": client_questions
    })

@app.route("/api/assessments/submit", methods=["POST"])
def api_submit_assessment():
    req_json = request.get_json(silent=True)
    if req_json is None:
        return error_response("Malformed JSON or empty request body.", 400)

    is_valid, err_msg = validate_submission(req_json)
    if not is_valid:
        return error_response(err_msg, 400)

    assessment_id = req_json["assessment_id"]
    skill_id = req_json["skill_id"]
    submitted_answers = req_json.get("answers", {})

    assessment = assessments_by_id[assessment_id]
    full_questions = [find_question(qid) for qid in assessment["question_ids"] if find_question(qid)]
    
    score_res = calculate_score(full_questions, submitted_answers)

    attempt_id = generate_attempt_id()
    skill = find_skill(skill_id)

    attempt_obj = {
        "attempt_id": attempt_id,
        "assessment_id": assessment_id,
        "student_name": "Test Student",
        "skill_id": skill_id,
        "skill_name": skill["name"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": score_res["total"],
        "correct": score_res["correct"],
        "incorrect": score_res["incorrect"],
        "unanswered": score_res["unanswered"],
        "score_percentage": score_res["percentage"],
        "reviews": score_res["reviews"]
    }

    attempts_by_id[attempt_id] = attempt_obj
    attempts_list.append(attempt_obj)

    assessment["status"] = "completed"

    return success_response({
        "attempt_id": attempt_id,
        "assessment_id": assessment_id,
        "skill_id": skill_id,
        "skill_name": skill["name"],
        "total": score_res["total"],
        "correct": score_res["correct"],
        "incorrect": score_res["incorrect"],
        "unanswered": score_res["unanswered"],
        "score_percentage": score_res["percentage"],
        "reviews": score_res["reviews"]
    })

@app.route("/api/attempts", methods=["GET"])
def api_get_attempts():
    sorted_attempts = list(reversed(attempts_list))
    
    summary_list = []
    for a in sorted_attempts:
        summary_list.append({
            "attempt_id": a["attempt_id"],
            "assessment_id": a.get("assessment_id", ""),
            "skill_id": a["skill_id"],
            "skill_name": a["skill_name"],
            "timestamp": a["timestamp"],
            "total": a["total"],
            "correct": a["correct"],
            "incorrect": a["incorrect"],
            "unanswered": a["unanswered"],
            "score_percentage": a["score_percentage"]
        })
        
    return success_response(summary_list)

@app.route("/api/attempts/<attempt_id>", methods=["GET"])
def api_get_attempt(attempt_id):
    attempt = find_attempt(attempt_id)
    if not attempt:
        return error_response(f"Attempt '{attempt_id}' not found.", 404)
    return success_response(attempt)

@app.route("/api/dashboard", methods=["GET"])
def api_get_dashboard():
    dash = build_dashboard()
    return success_response(dash)

@app.route("/")
def page_index():
    return render_template("index.html")

@app.route("/skills")
def page_skills():
    return render_template("skills.html")

@app.route("/assessment")
def page_assessment():
    return render_template("assessment.html")

@app.route("/result")
def page_result():
    return render_template("result.html")

@app.route("/history")
def page_history():
    return render_template("history.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
