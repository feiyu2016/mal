# GETTING STARTED

### Centralized Version Control Systems

> have a single server that contains all the versioned files, and a number of clients that check out files from that central place. For many years, this has been the standard for version control.

- CVS
- Subversion
- Perforce

**Advantages**

> everyone knows to a certain degree what everyone else on the project is doing. Administrators have fine-grained control over who can do what, and it’s far easier to administer a CVCS than it is to deal with local databases on every client.

**Downsides**

> single point of failure that the centralized server represents.
> 
> whenever you have the entire history of the project in a single place, you risk losing everything.

### Distributed Version Control Systems

- Git
- Mercurial
- Bazaar
- Darcs

>clients don't just check out the latest snapshot of the files; rather, they fully mirror the repository, including its full history. Thus, if any server dies, and these systems were collaborating via that server, any of the client repositories can be copied back up to the server to restore it. Every clone is really a full backup of all the data.
>
> todo:
> 找点Mercurial资料补充，特别是Oracle官方为什么用Mercurial做OpenJDK仓库，有什么优点吗？
>
>Furthermore, many of these systems deal pretty well with having several remote repositories they can work with, so you can collaborate with different groups of people in different ways simultaneously within the same project. This allows you to set up several types of workflows that aren’t possible in centralized systems, such as hierarchical models.

### What is Git

**Snapshots, Not Differences**

>Git thinks of its data more like a series of snapshots of a miniature filesystem.
>
>Git basically takes a picture of what all your files look like at that moment and stores a reference to that snapshot.

**The Three States**

- modified
> means that you have changed the file but have not committed it to your database yet.

- staged
> means that you have marked a modified file in its current version to go into your next commit snapshot.
> 
>The staging area is a file, generally contained in your Git directory, that stores information about what will go into your next commit. Its technical name in Git parlance is the “index”, but the phrase “staging area” works just as well.

- committed
>means that the data is safely stored in your local database.

**git config**

- [path]/etc/gitconfig file: Contains values applied to every user on the system and all their repositories. If you pass the option **--system** to git config, it reads and writes from this file specifically. Because this is a system configuration file, you would need administrative or superuser privilege to make changes to it.

- ~/.gitconfig or ~/.config/git/config file: Values specific personally to you, the user. You can make Git read and write to this file
specifically by passing the **--global** option, and this affects all of the repositories you work with on your system.

- config file in the Git directory (that is, .git/config) of whatever repository you’re currently using: Specific to that single repository. You can force Git to read from and write to this file with the **--local** option, but that is in fact the default. Unsurprisingly, you need to be located somewhere in a Git repository for this option to work properly.

```

# Identity
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com

# Editor
git config --global core.editor emacs

# Check Settings
git config --list

# Aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

```

# GIT BASICS

**Initializing a Repository in an Existing Directory**

```
cd my_project 
git init
git add *.c
git add LICENSE
git commit -m 'Initial project version'

```
**Cloning an Existing Repository**

```
git clone https://github.com/libgit2/libgit2

# clone the repository into a directory named
# something other than libgit2
git clone https://github.com/libgit2/libgit2 mylibgit

git status
# Short Status
git status -s

```

**Ignoring Files**

```
cat .gitignore
```

The rules for the patterns you can put in the **.gitignore** file are as follows:

- Blank lines or lines starting with # are ignored.
- Standard glob patterns work, and will be applied recursively throughout the entire working tree.
- You can start patterns with a forward slash (/) to avoid recursivity.
- You can end patterns with a forward slash (/) to specify a directory.
- You can negate a pattern by starting it with an exclamation point (!).

> In the simple case, a repository might have a single .gitignore file in its root directory, which applies recursively to the entire repository. However, it is also possible to have additional .gitignore files in subdirectories. The rules in these nested .gitignore files apply only to the files under the directory where they are located. The Linux kernel source repository has 206 .gitignore files.

example **.gitignore** file

```
# ignore all .a files
*.a

# but do track lib.a, even though you're ignoring .a files above
!lib.a

# only ignore the TODO file in the current directory, not subdir/TODO
/TODO

# ignore all files in any directory named build
build/

# ignore doc/notes.txt, but not doc/server/arch.txt
doc/*.txt

# ignore all .pdf files in the doc/ directory and any of its subdirectories
doc/**/*.pdf
```

