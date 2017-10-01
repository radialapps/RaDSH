# RaDSH

RaDSH (pronounced *radish*) stands for **Ra**pid **D**esigner for **S**tatic **H**TML. 

RaDSH is a small python script designed to make life simpler for designing static HTML websites from scratch. It has support for creating multiple pages from a single (or multiple with only slight changes) template by substituting code words with proper values, different for different pages. The possible use cases include making simple static websites with slightly varying content and (say) a consistent look and feel. It can also be used to design small static e-commerce websites with different pages being generate for different products.

# Demo
A sample site generated using RaDSH can be found at **http://radialapps.com**. Barring the index and other unique pages, the site was entirely generated using RaDSH from a single template for all product pages. This saves time on editing everything every time there needs to be some change, while not using any server side includes.

# Setup
RaDSH is tested and works on both Python 2 and Python 3.

# Usage
```
python radsh.py <data-csv> <template> <extension>
```
First, you need to write down a `<template>` using the syntax as described in the next section. For substituting values, a CSV file `<data-csv>` must be created containing different fields. In this, each row corresponds to one file that RaDSH outputs, while each column is a unique value that is mapped to the column name. All boolean values must be encoded as 0 or 1.
Note: there should always be a column named `filename` in the data file, which points to the path of the file to be generated. The extension of the files will be as set by `<extension>`. An example is provided.

# Syntax
RaDSH consists of a preprocessor and a compiler, each having only one command. The preprocessor is used to process boolean values, only deciding whether a certain section must be present in the output file. The compiler only substitutes the values from the data into the final output.
### Preprocessor
The syntax for a preprocessor check is as follows:
```HTML
[# ^^conditional^^ $$IfTrue$$ $!IfNotTrue!$]
```
The `conditional` is the name of a column in the input data. If the column has a value of boolean true (`1`), then the entire string above is replaced with `IfTrue`. If the column has the value false (`0`), then it is replaced by `IfNotTrue`. If no matches are found, or if the corresponding output string for the conditional is missing, the string will not be present in the output.
### Compiler
The syntax for the compiler is as follows:
```HTML
{{column_name}}
```
Just that! Here, `column_name` is the name of a column present in the input data. In the output, the above string will be replaced with the value of the column for that file (remember each file corresponds to a row).
You can also substitute strings with contents of files, by specifying the specific cell for `column_name` as
`file=somefile.txt`
Note that the preprocessor and compiler are also run on each substituted file, so you can get values from the data into the included files if required. You may also further include files in included fies using the same syntax.
# Example
Consider your `data.csv` to have the following data:

| filename | name      | price | description           | description_present |
|----------|-----------|-------|-----------------------|---------------------|
| one      | Product 1 | $10   | file=description1.txt | 1                   |
| two      | Product 2 | $20   | Short Description     | 1                   |
| three    | Product 3 | $5    | nothing               | 0                   |

Let the template be a file named `template.html` containing:
```HTML
<body>
    <!-- This is {{filename}}.html -->
    Product Name: {{name}} <br>
    Price: {{price}} <br>
    [# ^^description_present^^ $${{description}}$$ $! Empty! !$]
</body>
```
Let there also be a file named `description1.txt` containing
```
This is a small description for Product 1 <br>
It can contain multiple lines!
```
Then running `python radsh.py data.csv template.html html` would produce three files, `one.html`, `two.html` and `three.html`.
Their content would be as follows:

```HTML
<body>
    <!-- This is one.html -->
    Product Name: Product 1 <br>
    Price: $10  <br>
    This is a small description for Product 1 <br>
It can contain multiple lines!
</body>
```
```HTML
<body>
    <!-- This is two.html -->
    Product Name: Product 2 <br>
    Price: $20  <br>
    Short Description
</body>
```
```HTML
<body>
    <!-- This is three.html -->
    Product Name: Product 3 <br>
    Price: $5  <br>
    Empty! 
</body>
```
Note: As can be seen, text drawn from external file includes is not indented in the final file.

# Known Bugs
The regex used currently for the preprocessor is known to work improperly when using multiple lines.

# Contribute
Feel free to use or contribute in any way! If you have any suggestion, create or a pull request or an issue on GitHub.
