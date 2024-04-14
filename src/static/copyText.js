window.onload = function () {
    document.querySelectorAll('.copy-button').forEach(item => {
        console.log("Dupa")
        item.addEventListener('click', event => {
            const textToCopy = event.currentTarget.getAttribute('data-result');
            const textArea = document.createElement('textarea');
            textArea.value = textToCopy;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('Copied to clipboard');
        });
    });
}

