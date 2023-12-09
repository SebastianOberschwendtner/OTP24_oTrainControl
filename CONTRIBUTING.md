# Welcome!

There are some general rules to keep the code nice and tidy:
- [General](#general)
- [Naming Convention](#naming-convention)
  - [Constants](#constants)
  - [Variables](#variables)
  - [Functions](#functions)
  - [Types/Classes](#types-and-classes)
  - [Namespaces](#namespaces) *(C++ only)*
- [Comments](#comments)
  - [File Header](#file-header)
  - [Function Header](#function-header)
  - [Class Header](#class-header)
- [Language Features](#language-features)
    - [C++](#c-features)
    - [Python](#python-features) 
- [Commits](#commits)
- [Release Management](#release-management)
- [License](#license)

---

# General
This guide primarily focuses on *embedded* **C++** and **Python** code.
Those are the main documents we use to set our style:

- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [C++ Core Guidelines](http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/#naming-conventions)

Please use *Linter* and *Static Code Checkers* whenever possible, as they give a good baseline for good coding style.
The preferred tools are:
- *clang-tidy*
- *clang-format*
- *Pylint*
- *Black* (Python code formatter)

Another important paradigm: ***Test your code!***
<br>Our test tools are:
- *Unity* (embedded, via *PlatformIO*)
- *GoogleTest*
- *PyTest*

---

# Naming Convention
In general, try to follow the style guides from [PEP8](https://peps.python.org/pep-0008/) and [Google C++ Style](https://google.github.io/styleguide/cppguide.html#Naming).
The following sections give a common convention whenever the two style guides differ from each other.

## Constants
- `UPPER_CASE_WITH_UNDERSCORES`

> For *C++*: Try to avoid pre-processor *defines* and use `constexpr` instead.
> <br>&rArr; The naming rules for [Variables](#variables) do apply then. :point_up:

## Variables
- `lower_case_with_underscores`

> &rArr; This applies to class properties as well.
We don't mark member variables or private variables.

## Functions
- `lower_case_with_underscores`

> &rArr; This applies to class methods as well.

## Types and Classes
- `CaptializeWords`

## Namespaces
- `lowercase`

> &rArr; Try to name the namespace *short* and *concise* to that no underscore is needed in the name.

---

# Comments
In general try to code like the person who is reading your code knows where you live. :wink:

So please describe what your code does when it is not obvious and explain why you made certain decisions.
In general, we like code comments and it makes it easier to come back to your work later and remember what you intended for the code to do.
The following gives the common format to use so that the generated documenation looks uniform.

We use *Doxygen* and *mkdocs* (and sometime *hugo*) to generate the documentation.

> We use the ***Google* type** docstring for Python.

## File Header
> The file header come **after** the [License](#license) header!
- C++ Header:
```cpp
/**
 ==============================================================================
 * @file    file.cpp
 * @author  SO
 * @date    dd-mm-yyyy
 * @version v1.0.0
 * @brief   Short description of file.
 ==============================================================================
 */
```

- Python header:
```python
"""
### Details
- *File:*     `file.py`
- *Details:*  Python 3.11
- *Date:*     dd-mm-yyyy
- *Version:*  v1.0.0

## Description
Short description of file.

### Author
Sebastian Oberschwendtner, :email: sebastian.oberschwendtner@gmail.com

---
## Code

---
"""
```

## Function Header
- C++ Function:
```cpp
/**
 * @brief Description of the function
 *
 * @param param1 The first parameter
 * @return What is returned
 */
```

- Python *docstring*:
```python
"""Short description of function

Args:
    param1 (type): [unit] Description of parameter.

Returns:
    type: [unit] What is returned.

---
"""
```

## Class Header
- C++ class:
```cpp
/**
 * @class ClassName
 * @brief Description of class
 *
 * Add further notes or details if necessary.
```

- Python class:
```python
"""Short description of class.

---
"""
```


## File Sections
Try to separate *sections* within one file. Sections can be anything which combines the same content, for example function declarations or variable declaration can be sections.
Mark them according to:

- C++:
```cpp
/* === Section Name === */
-> Code here.
```

- Python
```python
# === Section Name ===
-> Code here
```

---

# Language Features
We are following the motto "New is always better". :wink: 
You are welcome to use nice new language features whenever possible and
when they are available for the device/release.

But please don't reinvent the wheel and try to use as many (standard) libraries as
possible for common tasks.

## C++ Features
- In general, use the newest C++ standard which is available for the used compiler.
For embedded devices which are compiled with *GCC-ARM* this is `C++17`.

- Avoid dynamic heap allocations when programming for embedded!
- Use *trailing return types* for modern C++.
- You can use `auto` when the type is clear from the context, or when the lifetime of the variable is short.
- Use *namespaces* to group what belongs together.

## Python Features
- In general, use the newest Python release which is available on your system.
This guide currently assumes Python `3.11` as the minimum required release.
- Give **all** functions parameters a list of types you expect the function to be called with.
- Use *trailing return types* to indicate what the functions or methods returns.

---

# Commits
- Commit messages should be clear and concise 
- Use **English** as the commit language.
- Use the `#` to close and refer to issues. 
- Please use **present tense** to explain what the commit does.

Symbols for commits:
- :art: `:art:` Improvements in the *user experience*
- :bug: `:bug:` Bugfix
- :racehorse: `:racehorse:` Performance improvement
- :wrench: `:wrench:` Minor improvement or fix
- :mag: `:mag:` Made code more readable
- :8ball: `:8ball:` Add or change unit tests
- :memo: `:memo:` Improved documentation
- :nut_and_bolt: `:nut_and_bolt:` Hardware uploads and fixes
- :tada: `:tada:` Celebrate new **major** releases!

---

# Release Management
*Tags* are used for the release management. The tag number is:
- **v***Major.Minor.Bugfix*
- Document every change in the [changelog](CHANGELOG.md)

> A release with release notes is published on **minor** and **major** changes. Bugfixes are just pushed as tags.

---

# License

The following should be included in every file header:
> Adjust the name of the author according to who created the file.
```c
/**
 * OTPxx project-name
 * Copyright (c) 202x Sebastian Oberschwendtner, sebastian.oberschwendtner@gmail.com
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 */
 ```

---
