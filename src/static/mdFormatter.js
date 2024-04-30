function convertMarkdownToHTML(markdownString) {
    return markdownString
        .replace(/^# (.+)/gm, '<h1>$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/~~(.+?)~~/g, '<del>$1</del>')
        .replace(/`(.*?)`/g, '<code>$1</code>');
}
