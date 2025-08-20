module.exports = async (params) => {
    const { quickAddApi: QuickAdd } = params;

    // Define input type options
    const inputTypes = ["Next", "Scheduled", "Summary", "Highlight", "LineADay", "JGLesson", "UkulelePages"];

    // Prompt for input type selection
    const selectedType = await QuickAdd.suggester(inputTypes, inputTypes);

    if (!selectedType) {
        return;
    }

    let inputValue;
    let frontmatterKey = selectedType;

    // Handle input based on selected type
    if (selectedType === "Scheduled") {
        // Create date options for the next 14 days
        const today = new Date();
        const dateOptions = [];
        const dateValues = [];

        for (let i = 1; i <= 6; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() + i);
            const dateStr = date.toISOString().split('T')[0];
            const dayName = date.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
            dateOptions.push(`${dateStr} (${dayName})`);
            dateValues.push(dateStr);
        }
        // Add next week and next month
        const nextWeek = new Date(today);
        nextWeek.setDate(today.getDate() + 7);
        const nextWeekStr = nextWeek.toISOString().split('T')[0];
        const nextWeekDayName = nextWeek.toLocaleDateString('en-AU', { weekday: 'long', month: 'short', day: 'numeric' });
        dateOptions.push(`Next Week (${nextWeekDayName})`);
        dateValues.push(nextWeekStr);

        const nextMonth = new Date(today);
        nextMonth.setMonth(today.getMonth() + 1);
        const nextMonthStr = nextMonth.toISOString().split('T')[0];
        const nextMonthDayName = nextMonth.toLocaleDateString('en-AU', { weekday: 'long', month: 'short', day: 'numeric' });
        dateOptions.push(`Next Month (${nextMonthDayName})`);
        dateValues.push(nextMonthStr);


        // Add custom date option
        dateOptions.push("Enter custom date...");
        dateValues.push("custom");

        const selectedDate = await QuickAdd.suggester(dateOptions, dateValues);

        if (selectedDate === "custom") {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            const defaultDate = tomorrow.toISOString().split('T')[0];
            inputValue = await QuickAdd.inputPrompt("Enter date (YYYY-MM-DD):", defaultDate);
        } else {
            inputValue = selectedDate;
        }
    } else {
        // Show text input field
        inputValue = await QuickAdd.inputPrompt(`Enter ${selectedType.toLowerCase()}:`);
    }

    if (!inputValue) {
        return;
    }

    // Get the active file
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        new Notice("No active file");
        return;
    }

    // Update frontmatter
    try {
        await app.fileManager.processFrontMatter(activeFile, (frontmatter) => {
            // Convert to number for specific input types
            if (["LineADay", "JGLesson", "UkulelePages"].includes(selectedType)) {
                frontmatter[frontmatterKey] = parseInt(inputValue) || 0;
            } else {
                frontmatter[frontmatterKey] = inputValue;
            }
        });
    } catch (error) {
        new Notice("Error updating frontmatter: " + error.message);
        return;
    }

    // Define text strings for each input type
    const textStrings = {
        "Next": `# Next: \`INPUT[text(placeholder(''), class('my-mb-h1')):Next]\`\n`,
        "Scheduled": `Scheduled: \`INPUT[date:Scheduled]\``,
        "Summary": `Summary: \`INPUT[text(placeholder('')):Summary]\``,
        "Highlight": `Highlight: \`INPUT[text(placeholder('')):Highlight]\``,
        "LineADay": `LineADay: \`INPUT[number(placeholder('0')):LineADay]\``,
        "JGLesson": `JGLesson: \`INPUT[number(placeholder('0')):JGLesson]\``,
        "UkulelePages": `UkulelePages: \`INPUT[number(placeholder('0')):UkulelePages]\``
    };

    const textToInsert = textStrings[selectedType];

    // Try multiple methods to insert text
    try {
        // Method 1: Try to get active leaf editor
        const activeLeaf = app.workspace.activeLeaf;
        if (activeLeaf && activeLeaf.view && activeLeaf.view.editor) {
            activeLeaf.view.editor.replaceSelection(textToInsert);
            new Notice(`Added ${selectedType}: ${inputValue}`);
            return;
        }

        // Method 2: Try workspace active view
        const activeView = app.workspace.getActiveViewOfType('markdown');
        if (activeView && activeView.editor) {
            activeView.editor.replaceSelection(textToInsert);
            new Notice(`Added ${selectedType}: ${inputValue}`);
            return;
        }

        // Fallback: copy to clipboard
        await navigator.clipboard.writeText(textToInsert);
        new Notice(`${selectedType} added to frontmatter. Text copied to clipboard - paste where needed.`);

    } catch (error) {
        // Final fallback
        await navigator.clipboard.writeText(textToInsert);
        new Notice(`${selectedType} added to frontmatter. Text copied to clipboard due to insertion error.`);
    }
};