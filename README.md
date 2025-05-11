# Number Line Calculator

A calculator that uses a number line instead of just regular maths.

## The Idea

Imagine a number line that looks something like this:

```
                                  ● ->
  |-------------------------------|-------------------------------|
 -∞                               0                               ∞
```

Where the `●` character is your current position on the number line and the arrow shows the direction you are facing.
The Main premise of this calculator relies on this foundation. The calculator will compute the results of Expressions
based on this number line.

Let's now consider an Expression like `3 + -3 + 3*3` with a smaller number line
We shall parse this Expression into Tokens like so:
`3 -> + -> - -> 3 -> + -> 3*3`

Then we shall run the Expression Token by Token, skipping the `+` Tokens:

**Step 1.** Move in the direction we are facing by 3 steps

```
                                                      ● ->
  |---------------------------------------|-----------|---------------------------|
 -10                                      0           3                           10
```

**Step 2.** Turn towards the negatives

```
                                                   <- ●
  |---------------------------------------|-----------|---------------------------|
 -10                                      0           3                           10
```

**Step 3.** Move in the direction we are facing by 3 steps (Notice how we are still facing the negatives after this step)

```
                                       <- ●
  |---------------------------------------|---------------------------------------|
 -10                                      0                                       10
```

**Step 4.** Move in the direction we are facing by 3 steps 3 times

```
   <- ●
  |---|-----------------------------------|---------------------------------------|
 -10 -9                                    0                                       10
```

Since we have reached the end, the number that we are on is the result of the Expression: `-9`

You may be thinking, "Hold up! The answer to `3 + -3 + 3 * 3` is `9`", but that's the magical part of this calculator. It
does not actually care about math conventions, it produces the result based purely on the execution of arbitrary rules set
by me on the number line.

## Keywords

Keywords are separate from Tokens as they are not parsed as an Expression


| Keyword | Use |
| -------------- | --------------- |
| set `a` | Set the starting value of the next line to `a` |
| quit | Quit the program


## Expression

Expressions are lines that do not contain any Keywords. They get parsed as Tokens and those Tokens are evaluated.
It is also worth to note that Expressions cannot begin with either `+` or `*`.

## Tokens

Lines are split into tokens which are then processed to get a result.

Tokens have 3 types:
1. Terms: Basically the values that get added up
2. Operators: Basically just + and - that do something
3. Functions: Basically just functions in mathematics

Here is a list of Tokens:

| Token | Type | Use |
| ----- | --------- | ------------------------ |
| `+ a` | Operator | Add `a` to the current value |
| `-` | Operator | Switch between `positive` and `negative` directions |
| `a` | Term | A positive integer `a` |
| `a*b` | Term | `+ b` looped `a` times |
| `[NAME]([ARG]) = [EXPRESSION]` | Function | Initialises a function |

## Flags

| Full Flag | Shortened Flag | Use |
| --------------- | --------------- | --------------- |
| --continuous | -c | Sets the starting value of each line to the result of the previous line |


