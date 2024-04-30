window.onload = function () {
    const typeSelect = document.getElementById("type");
    const textContainer = document.getElementById("textContainer");
    const articleUrlContainer = document.getElementById("articleUrlContainer");
    const youtubeUrlContainer = document.getElementById("youtubeUrlContainer");
    const fileContainer = document.getElementById("fileContainer");
    const transcriptionTypeContainer = document.getElementById("transcriptionTypeContainer");

    function hideAllContainers() {
        textContainer.style.display = "none";
        articleUrlContainer.style.display = "none";
        youtubeUrlContainer.style.display = "none";
        fileContainer.style.display = "none";
    }

    function toggleContainer(container) {
        hideAllContainers();
        container.style.display = "block";
    }

    function toggleTranscriptionType() {
        const selectedType = typeSelect.value;

        if (selectedType === "youtube") {
            transcriptionTypeContainer.style.display = "block";
        } else {
            transcriptionTypeContainer.style.display = "none";
        }
    }

    function toggleInputs() {
        const selectedType = typeSelect.value;
        toggleTranscriptionType(selectedType);

        if (selectedType === "text") {
            toggleContainer(textContainer);
        } else if (selectedType === "article") {
            toggleContainer(articleUrlContainer);
        } else if (selectedType === "youtube") {
            toggleContainer(youtubeUrlContainer);
        } else if (selectedType === "file") {
            toggleContainer(fileContainer);
        }
    }

    typeSelect.addEventListener("change", toggleInputs);

    toggleInputs();

    typeSelect.value = "text";
};
