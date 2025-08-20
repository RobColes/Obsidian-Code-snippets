module.exports = () => {
    // Get the active file
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) return "No active file";

    // Read current content
    app.vault.read(activeFile).then(content => {
        let newContent = content;

        // Handle frontmatter removal
        let frontmatterEnd = 0;
        let hasFrontmatter = false;
        if (content.startsWith('---')) {
            const secondDash = content.indexOf('---', 3);
            if (secondDash !== -1) {
                hasFrontmatter = true;
                frontmatterEnd = secondDash + 3;
            }
        }

        if (hasFrontmatter) {
            // Extract existing frontmatter
            const frontmatter = content.substring(0, frontmatterEnd);
            const bodyContent = content.substring(frontmatterEnd);

            // Process frontmatter content
            const frontmatterContent = frontmatter.substring(3, frontmatterEnd - 3);
            const lines = frontmatterContent.split('\n');

            // Filter out the Scheduled and Next lines
            const filteredLines = lines.filter(line => {
                const trimmed = line.trim();
                return !trimmed.startsWith('Scheduled:') &&
                    !trimmed.startsWith('Next:') &&
                    trimmed !== '';
            });

            // Rebuild frontmatter or remove it entirely if empty
            if (filteredLines.length > 0) {
                const updatedFrontmatter = '---\n' + filteredLines.join('\n') + '\n---';
                newContent = updatedFrontmatter + bodyContent;
            } else {
                // No frontmatter left, remove it entirely
                newContent = bodyContent;
            }
        }

        // Remove inline Scheduled line
        // This regex matches lines containing "Scheduled: `INPUT[date:Scheduled]`"
        // It handles various whitespace and potential variations
        //const inlineScheduledRegex = /^.*Scheduled:\s*`INPUT\[date:Scheduled\]`.*$/gm;
        newContent = newContent.replace('Scheduled: `INPUT[date:Scheduled]`', '');

        // Remove inline Next line
        // This regex matches lines containing "Next: `INPUT[text(placeholder(''), class('my-mb-h1')):Next]`"
        //const inlineNextRegex = /^.*Next:\s*`INPUT\[text\(placeholder\(''\), class\('my-mb-h1'\)\):Next\]`.*$/gm;
        newContent = newContent.replace("# Next: `INPUT[text(placeholder(''), class('my-mb-h1')):Next]`", "");

        // Clean up any extra blank lines that might be left behind
        // Replace multiple consecutive newlines with max 2 newlines
        newContent = newContent.replace(/\n{3,}/g, '\n\n');

        // Trim any trailing whitespace at the end of the file
        newContent = newContent.replace(/\s+$/, '\n');

        // Write the updated content back to the file
        app.vault.modify(activeFile, newContent);
    });

    return "Scheduled and Next information removed";
}