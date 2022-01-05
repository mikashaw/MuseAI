const searchBox = document.querySelector(".search-box");
const navBtnContainer = document.querySelector(".nav-btn-container");
const searchBtn = document.querySelector(".search-btn");
const closeBtn = document.querySelector(".close-btn");

searchBtn.addEventListener("click", () => {
    searchBox.classList.add("active");
    navBtnContainer.classList.add("active")
})

closeBtn.addEventListener("click", ()=> {
    searchBox.classList.remove("active");
    navBtnContainer.classList.remove("active");
})

// for gen-page

const genContent = document.querySelector(".generated-content")
const generateAudio = document.querySelector(".gen-audio");

generateAudio.addEventListener("click", ()=> {
    genContent.classList.add("active");
    generateAudio.classList.add("active")
})





