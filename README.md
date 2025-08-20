# Obsidian-Code-snippets
These are some of the bits of code that I use in my Obsidian vault. They are often specific to my workflow and note structure, so please don't just run them, but use them as a reference or starting point for your own customizations. 

# Installation
1. Download the code from this repository.
2. Place the downloaded files in the appropriate Obsidian folder:
    - I keep javascript and base files in a _Templates folder.
    - Most of the datacore is inline, or kept in the _Templates folder.

# Datacore
As of 2025-08-20, Datacore was still in beta, so needed to be installed using BRAT. I have replaced all dataview in my vault with bases or datacore.
## ProgressBarTasks.md
![Progress bar](images/progressbar.png)

This is a datacore progress bar that I imbed using dynamic imbed (so that it uses the owning file for the query) that will look for all tasks, and all completed tasks in the note and provide a quick visual summary of the progress. 
````
```dynamic-embed
[[ProgressBarTasks]]
```
````
I use this in many of my 25 for 2025 notes, and use the progress bar code itself as the basis for tracking multiple objectives in weekly, quarterly and annual notes.

The file is kept in my _Templates folder.

## Time Progression.md
![Time progression chart](images/timespan.png)

This is my version of Mike Schmitz's memento mori and Joshi Pax's extension. It's a datacore query that I imbed in my daily note as a reminder. I don't update it dynamically (you could get it to update the day percentage periodically).

To use, you would need to update the birthday and lifespanYears variables. I calculated the lifespan years from an online calculator that took into account my diet, exercise and where I lived etc.

I use the same dynamic imbed plug-in as for the progressbartasks above to include this file, as using a regular imbed gave me issues on mobile.

# Quickadd Macro
## InputHelper.js
## LastUpdated.js
## UnSchedule.js

# Python
## obstask.py

# Bases
## CreatedToday.base
## OldestModDate.base
## PreviousYears.base
## ThisWeek Notes.base
## Today Notes.base
## WeeklySummary.base

# Miscellaneous
## AutoHotkey helpers.txt
## Callout Insert.md
## Current Plugins.md
## Kanban Weekly No Reminders.md
## Rob.css


