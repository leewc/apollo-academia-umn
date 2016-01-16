# Homework 1: Creating a Git command cheat-sheet

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due:** Monday, September 8 at 5:00pm

## Introduction

Using Git and GitHub can be confusing at first.  There are several Git
commands to learn.  We covered many in lab 1.  

In this homework, you will learn one more command (git add) and create
a cheat-sheet that you can refer to in the future when you have
questions about using Git.

## Using git add

In your CSE Labs account, go to the directory with your individual
repository.  Something like the following:
```
% cd csci2041/repo-user0123
```

Create a file with the name *cheat-sheet.md*.  The "md" extension
indicates that this file a a Markdown file.  This is the file format
used on GitHub for many documentation files.

Edit this file and add the following line:
>  # Git Cheat Sheet

Exit your editor and check the status of your repository with the
following command:
```
% git status
```
This will tell you that your newly created file is "Untracked."  It
even suggests using the "git add" command to tell Git to track this
file.  

There may be files that are temporary, such as generated executable
file, that you don't want Git to track and we thus would not *add*
those files.

Try this command now:
```
% git add cheat-sheet.md
```

Now *git status* will tell you that the file is modified and it has
changes to be committed.

So, what commands do you need to move this new file up to the
https://github.umn.edu server?

Try the following:
```
% git pull
% git commit -a -m "Adding my Git cheat sheet"
% git push
```

The *git pull* is the make sure you have any changes on the server
copied down to your local repository.

Now go to https://github.umn.edu and see what is in your newly
committed and pushed file.

It should be an empty file with just a title.  You can now click the
"Edit" button and edit this file.

The file is to be written using the Markdown language, a easy to use
language for formatting documentation.  Take a look at the
documentation for writing basic Markdown files:

https://help.github.com/articles/markdown-basics

Below the editing window you will see a place to enter commit comments
and a button for committing your changes directly to the repository on
the central server.

## Your assignment

So far we've covered several *Git* commands:
+ config
+ clone
+ remote
+ status
+ commit
+ push
+ pull
+ add

For each of these, write a short description (perhaps just 2 or 3 sentences) 
of what the command does and when or 
how often this command is to be used.  
You might order this list of command descriptions so that the most useful ones are
at towards the beginning.

# Assessment
Homework 1 is assessed as follows:
+ __ / 4: A file named exactly "cheat-sheet.md" is committed to the top level of your repository.
+ __ / 16: A short description for each of the 8 commands - 2 points each 

**Due:** Monday, September 8 at 5:00pm

