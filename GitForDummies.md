# Git For Dummies :)

## Table of contents
1. [Save changes locally](#how-do-i-save-my-changes-to-my-current-local-repository)
2. [Work on new branch](#how-do-i-create-a-new-local-branch-to-work-on)
3. [Pull new changes](#how-do-i-pull-new-changes)
4. [Push new changes](#how-do-i-push-my-changes-to-github)

## Workflow

1. Make sure you have the most recent changes in main by pulling the latest
2. Create and work on a new branch that branches off from main
3. Commit often in local repository
4. Once ready to push changes, make sure we pull latest changes from main again
5. Push your current branch repository to github
6. Do a pull request (check in with team members) to be able to merge your changes to main
7. Successfully do pull request
8. Delete both your local and remote branch
9. Rinse and repeat

## Basic Commands

### How do I check if I am connected to a GitHub Repo?

```bash
git remote -v
```

### How do I save my changes to my current local repository?

---
### Stage whole directory
```bash
git add .
```

- stages all unadded/modified/deleted files in current directory

### Stage specific file
```bash
git add {PATH_TO_FILE}
```
### Create commit
```bash
git commit -m"{YOUR_MESSAGE}"
```

- saves the current staged changes into a commit (think of save file)

### How do I create a new local branch to work on?

---

```bash
git checkout -b {BRANCH_NAME}
```

- Creates a new branch (with -b flag)
- Goes to new branch (checkout) of name {BRANCH_NAME}

### How do I delete a branch?

---

```bash
git branch -d {BRANCH_NAME}
```

- Deletes local branch

### How do I check my staged changes?

---

```bash
git status
```



### How do I push my changes to GitHub?

---

```bash
git push origin {LOCAL_BRANCH_NAME}
```

- Unless it is a minor change _please_ do not push to main
- makes a new branch in github with the same name as your local branch name (unless it is main)

### How do I pull new changes?

---

#### Pull directly from main if in current local branch

```bash
git pull origin main
```

#### Update your local main branch and merge branches from main into your local branch you are working on (recommended)

```bash
git checkout main
git pull
git checkout {BRANCH_YOU_WERE_WORKING_ON}
git merge main
```

- Allows you to have new changes in working branch you are on
