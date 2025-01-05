const getYear = () => {
  return new Date().getFullYear();
};

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("current-year").textContent = getYear();
});
