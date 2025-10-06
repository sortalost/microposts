const fileInput = document.getElementById("file");
const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");

fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) {
    previewContainer.classList.add("hidden");
    return;
  }

  const reader = new FileReader();
  reader.onload = (ev) => {
    previewImage.src = ev.target.result;
    previewContainer.classList.remove("hidden");
  };
  reader.readAsDataURL(file);
});
