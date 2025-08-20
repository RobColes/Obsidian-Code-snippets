<%*
const desiredPath = "Transient/Weekly Kanban";
const file = app.vault.getAbstractFileByPath(desiredPath + ".md");
if (file) {
    await app.vault.delete(file);
    console.log(`File ${desiredPath} has been permanently deleted.`);
} else {
    console.log(`File ${desiredPath} does not exist.`);
}

// Move the current file
await tp.file.move(desiredPath);

/* Main logic without DataView */
var myDate = moment().isoWeekday(7).format("YYYY-MM-DD");
console.log('sunday', myDate);

tR = "---\nkanban-plugin: basic \n--- \n\n";

// Helper function to check if a file contains a link to a specific page
function hasLink(fileContent, linkName) {
    const linkPattern = new RegExp(`\\[\\[${linkName}\\]\\]`, 'i');
    return linkPattern.test(fileContent);
}

// Helper function to check if a file has a Scheduled field in frontmatter
function hasScheduledField(file) {
    const cache = app.metadataCache.getFileCache(file);
    return cache?.frontmatter?.Scheduled;
}

// Get all markdown files
const allFiles = app.vault.getMarkdownFiles();

// Filter files based on criteria
function getFilesWithLink(linkName, excludeLink = null) {
    return allFiles.filter(file => {
        // Skip if file has Scheduled field
        if (hasScheduledField(file)) return false;
        
        // Get file content
        const cache = app.metadataCache.getFileCache(file);
        if (!cache) return false;
        
        // Check for required link
        const hasRequiredLink = cache.links?.some(link => 
            link.link === linkName || link.displayText === linkName
        ) || cache.embeds?.some(embed => 
            embed.link === linkName || embed.displayText === linkName
        );
        
        if (!hasRequiredLink) return false;
        
        // Check for excluded link
        if (excludeLink) {
            const hasExcludedLink = cache.links?.some(link => 
                link.link === excludeLink || link.displayText === excludeLink
            ) || cache.embeds?.some(embed => 
                embed.link === excludeLink || embed.displayText === excludeLink
            );
            if (hasExcludedLink) return false;
        }
        
        return true;
    });
}

// Backlog section
tR += `## Backlog\n`;
const weekendFiles = getFilesWithLink("Weekend");
for (const file of weekendFiles) {
    tR += `- [ ] [[${file.basename}]]\n`;
}

// To Do section
tR += `\n## To Do\n`;

// Today files (exclude Work)
const todayFiles = getFilesWithLink("1-Today");
for (const file of todayFiles) {
    tR += `- [ ] [[${file.basename}]]\n`;
}

// This week files (exclude Work)
const thisWeekFiles = getFilesWithLink("2-ThisWeek");
for (const file of thisWeekFiles) {
    tR += `- [ ] [[${file.basename}]]\n`;
}

tR += `\n\n## Doing\n\n## Done\n\n`;
%>