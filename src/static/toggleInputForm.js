window.onload = function () {
    const typeSelect = document.getElementById("type");
    const textContainer = document.getElementById("textContainer");
    const articleUrlContainer = document.getElementById("articleUrlContainer");
    const youtubeUrlContainer = document.getElementById("youtubeUrlContainer");
    const fileContainer = document.getElementById("fileContainer");
    const transcriptionTypeContainer = document.getElementById("transcriptionTypeContainer");
    // const languageContainer = document.getElementById("languageContainer")

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

    function toggleYoutubeAdditionalFields() {
        const selectedType = typeSelect.value;

        if (selectedType === "youtube" || selectedType === "playlist" || selectedType === "channel")  {
            transcriptionTypeContainer.style.display = "block";
            // languageContainer.style.display = "block";
        } else {
            transcriptionTypeContainer.style.display = "none";
            // languageContainer.style.display = "none";
        }
    }

    function toggleInputs() {
        const selectedType = typeSelect.value;
        toggleYoutubeAdditionalFields(selectedType);

        if (selectedType === "text") {
            toggleContainer(textContainer);
        } else if (selectedType === "article") {
            toggleContainer(articleUrlContainer);
        } else if (selectedType === "youtube" || selectedType === "playlist" || selectedType === "channel") {
            toggleContainer(youtubeUrlContainer);
        } else if (selectedType === "file") {
            toggleContainer(fileContainer);
        }
    }

    typeSelect.addEventListener("change", toggleInputs);

    toggleInputs();

    typeSelect.value = "text";
};