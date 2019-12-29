## LLang Compiler
This is a tiny nonofficial Compiler used Operator Precedence Parser for **LLang** (not strict difinition) including OPGrammar, Lexer, Parser, and unfinished SemanticAnalyzer. For materials not special stated, you could use, edit as you want. But you shall add a declaration like   
>My work referenced ChiZuo's work in https://github.com/Raibows/LLangCompiler

#### Introduction 
1. The strict difinition of LLang could be seen in `./LLangGrammar.pdf`  
2. Attention, this compiler did not follow the strict difinition of LLang. Code examples are in `./static/`  
3. My compiler has 4 main modules
    - OPGrammar（define the grammar rule）
    - Lexer（use advanced search）
    - Parser（use operator precedence algorithm）
    - SemanticAnalyzer（unfinished）
4. branch information  
    The following 4 versions are recommended
    |  Branch | OPGrammar  | Lexer  |  Parser | Semantic  |
    | :------------: | :------------: | :------------: | :------------: | :------------: |
    | master  | yes  | yes  | yes, no support `if..the..else..` and `TreeNode` | no  |
    |  tree | yes  | yes  |  yes, no support `if..the..else..` |  no |
    |  version1 |  yes | yes  |  yes, no support `if..the..else..` |  yes, need to perfect |
    | version2 | yes | yes | yes | no, need to correct semantic action |

#### Guidance
1. A common example code of my implementation of LLang is below
    ```
    program test
    begin
    var a:integer;
    var i, b : real;&
    a :=2.27.36;
    i:=a*3.14Bs2;
    b := 1Bsd32;
    b := i;
    if a > b then a := a + i;
    while a <> b do i := b*i;
    var k : bool;
    k := false;
    if k then a := a + 1;
    end
    ```
2. To run this Compiler
   ```
   Edit run.py as you like
   python run.py
   ```

    