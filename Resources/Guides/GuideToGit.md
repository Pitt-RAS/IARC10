# Before Making Changes
Pull on whichever branch you are branching off of ("git pull")

Type "git checkout -b *name*", where *name* is the name of the new branch
- The same command is used to switch between branches, just leave the "-b" off if the target is pre-existing
- In order to check which branch you are on, use "git branch"

# Do Your Changes

# After completing them
Add all changes to Git (git add -A or using VSCode UI)

git push (This adds the commits to the remote repo, committing itself only leaves it on the local one)

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
    (If you have merge conflicts, that's a seperate issue, that can be fixed in github)

# Merging Conflicts or Issues when pushing (PEOPLE WHO FORGOT TO PULL -- that means you :) ) 
Remember to check if you are on the correct branch by using "git checkout" and "git status" for any changes

- "git stash"                 - would safe your current changes
- "git pull"                  - pull the current GitHub version of the code
- "git stash pop"             - put the changed version of you code back 
- "git add ___"               - the "___" is for the files and if you use "." for all files and if not type the file name
- "git commit -m "_____""     - commit your changes 
- "git push"                  - pushes your code to GitHub

# Setting up a requirement for PRs
1. Open Settings -> Branches
2. Add a new Branch Protection Rule
3. In "Branch Name Pattern", put the name of the branch you want to protect
4. Click on "Require a pull request before merging"

# Deleting Old Branches
*In GitHub*
- Click on the button right above the code that shows which branch you are on
- "View All Branches"
- Trash Icon next to branches

# GIT Cloning 
- Windows OS
    - There is a extention on VS Code for GitHub for cloning or use CRTL + Shift + P and type in "git clone"
    - Then copy the https: URL from GitHub for cloning

- Linux OS
    - You would need to clone it through SSH
    - within your terminal:
        - "ssh-keygen"             - generates a key pair
        - "eval "$(ssh-agant -s)"  - activates the agent for linking the your computer to GitHub
        - "ssh-add ---"            - "---" is your private key name and adds your private key to your device
        - "cat ---.pub"            - cat shows the content of the files
        - copy the "ssh..."        - that is the public key that is going into the "SSH and GPG keys" or 
                                    "key" part in the setting on GitHub
        - "ssh -T git@github.com"  - is a test ssh command to see if you are connected

    - for you to login in you have to run
        - git config --global user.name "Your Name"
        - git config --global user.email "your_email@example.com"
    - so that you are logged in