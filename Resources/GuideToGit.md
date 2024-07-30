# Before Making Changes
Pull on whichever branch you are branching off of

Type "git checkout -b *name*", where *name* is the name of the branch

# Do Your Changes

# After completing them
Add all changes to Git (git add -A or using VSCode UI)

git push

Switch to Github, and there are two possibilities from there:
    You see a goldenish banner at the top saying your branch has recent changes & giving an option to make a pull request
        Click it
    OR
    Go to the "Pull Requests" tab, and click the shiny green button in the corner, and choose the branch you are merging in

For the sake of organization, all PRs (Pull Requests) should have 3 parts:
    1. A Description
    2. The actual changes you made
    3. Proof that the feature/bugfix works

And then wait for someone to approve your PR, and then merge!
    (If you have merge conflicts, that's a seperate issue)

# Merging Conflicts or Issues when pushing (PEOPLE WHO FORGOT TO PULL -- that means you :) ) 
Remember to check if you are on the correct branch by using "git checkout" and "git status" for any changes

"git stash"                 - would safe your current changes
"git pull"                  - pull the current GitHub version of the code
"git stash pop"             - put the changed version of you code back 
"git add ___"               - the "___" is for the files and if you use "." for all files and if not type the file name
"git commit -m "_____""     - commit your changes 
"git push"                  - pushes your code to GitHub
