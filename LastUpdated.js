module.exports = () => {
    // Get current date in yyyy-mm-dd format
    const today = new Date();
    const dateString = today.getFullYear() + '-' +
        String(today.getMonth() + 1).padStart(2, '0') + '-' +
        String(today.getDate()).padStart(2, '0');

    // Get the active file
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) return;

    // Read current content
    app.vault.read(activeFile).then(content => {
        // Check if frontmatter exists
        let frontmatterEnd = 0;
        let hasFrontmatter = false;

        if (content.startsWith('---')) {
            const secondDash = content.indexOf('---', 3);
            if (secondDash !== -1) {
                hasFrontmatter = true;
                frontmatterEnd = secondDash + 3;
            }
        }

        let newContent;

        if (hasFrontmatter) {
            // Extract existing frontmatter
            const frontmatter = content.substring(0, frontmatterEnd);
            const bodyContent = content.substring(frontmatterEnd);

            // Check if LastReviewed already exists in frontmatter
            const frontmatterContent = frontmatter.substring(3, frontmatterEnd - 3);
            const lines = frontmatterContent.split('\n').filter(line => line.trim() !== '');
            let lastReviewedExists = false;

            for (let i = 0; i < lines.length; i++) {
                if (lines[i].trim().startsWith('LastReviewed:')) {
                    lines[i] = `LastReviewed: ${dateString}`;
                    lastReviewedExists = true;
                    break;
                }
            }

            if (!lastReviewedExists) {
                lines.push(`LastReviewed: ${dateString}`);
            }

            const updatedFrontmatter = '---\n' + lines.join('\n') + '\n---';
            newContent = updatedFrontmatter + bodyContent;
        } else {
            // No frontmatter exists, create it
            const frontmatter = `---\nLastReviewed: ${dateString}\n---\n`;
            newContent = frontmatter + content;
        }

        const gotText = content.indexOf('Last reviewed: ');
        if (gotText == -1) {
            newContent += "\nLast reviewed: \`INPUT[date:LastReviewed]\`\n\n"
        }


        // Write the updated content back to the file
        app.vault.modify(activeFile, newContent);
    });

    return "Script completed";
}