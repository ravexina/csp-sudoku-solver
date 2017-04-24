# Python CSP Sudoku Solver

It's a simple script which is capable of solving different sudokus usig CSP.

**Requirments:**
 - Python
 - tkinter

![python csp sudoku solver](https://github.com/ravexina/csp-sudoku-solver/blob/master/screenshots/1.png)


## How to use it:

Enter your desired numbers, after you are finish click on `create start state`:

![python csp sudoku solver - start state](https://github.com/ravexina/csp-sudoku-solver/blob/master/screenshots/2.png?raw=true)

Then you can click on `start searching`, it tries to find a solution and completes the sudoku:

![python csp sudoku solver - complete](https://github.com/ravexina/csp-sudoku-solver/blob/master/screenshots/3.png?raw=true)

You can also use `Next live` to find the solution step by step (it will includes backtracking process too), or after using finding the complete solution using `Start searching` you can click on `File -> Clear`, then you can use `Next` to see the workaround (whitout backtracking).

1th and 2th way are different heuristics. 

## License 

MIT License

Copyright (c) 2017 ravexina (Milad As)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
