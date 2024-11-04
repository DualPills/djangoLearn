document.addEventListener("DOMContentLoaded", function() {
    let currentIndex = 0;
    const slides = document.querySelectorAll(".slides img");
    const dots = document.querySelectorAll(".dot");
    let autoSlideInterval;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove("active");
            dots[i].classList.remove("active");
        });
        slides[index].classList.add("active");
        dots[index].classList.add("active");
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    }

    window.currentSlide = function(index) {
        currentIndex = index - 1;
        showSlide(currentIndex);
        resetAutoSlide();
    }

    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 3000);
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    startAutoSlide();
});

//------------------------------------------------------
const itemsPerRow = 6; // 6 products per row
const rowsPerPage = 3; // 3 rows per page
const itemsPerPage = itemsPerRow * rowsPerPage; // Total products per page (18)
const items = document.querySelectorAll('.iterm');
const totalPages = Math.ceil(items.length / itemsPerPage);

function showPage(page) {
    items.forEach((item, index) => {
        item.style.display = (index >= (page - 1) * itemsPerPage && index < page * itemsPerPage) ? 'block' : 'none';
    });

    document.querySelectorAll('.page-number').forEach((pageBtn, index) => {
        pageBtn.classList.toggle('active', index === page - 1);
    });
}

// Initialize first page
showPage(1);

// Add event listeners to pagination buttons
document.querySelectorAll('.page-number').forEach((pageBtn, index) => {
    pageBtn.addEventListener('click', () => showPage(index + 1));
});

//------------------------------------------------------

// Lấy container chứa các sản phẩm
const container = document.querySelector('.container_san_NOI_BAT');

// Lấy chiều rộng của một sản phẩm (bao gồm cả margin nếu có)
const itemWidth = document.querySelector('.iterm_1').offsetWidth;

// Hàm cuộn lên một sản phẩm
function scrollUp() {
    const scrollLeftValue = container.scrollLeft; // Vị trí cuộn hiện tại
    const maxScrollLeft = container.scrollWidth - container.clientWidth; // Cuộn tối đa

    // Kiểm tra nếu có thể cuộn lên
    if (scrollLeftValue < maxScrollLeft) {
        container.scrollBy({
            left: itemWidth, // Cuộn lên 1 sản phẩm
            behavior: 'smooth' // Cuộn mượt
        });
    }
}

// Hàm cuộn xuống một sản phẩm
function scrollDown() {
    const scrollLeftValue = container.scrollLeft; // Vị trí cuộn hiện tại

    // Kiểm tra nếu có thể cuộn xuống
    if (scrollLeftValue > 0) {
        container.scrollBy({
            left: -itemWidth, // Cuộn xuống 1 sản phẩm
            behavior: 'smooth' // Cuộn mượt
        });
    }
}

// Kiểm tra trạng thái mũi tên khi cuộn
function checkArrows() {
    const scrollLeftValue = container.scrollLeft; // Vị trí cuộn hiện tại
    const maxScrollLeft = container.scrollWidth - container.clientWidth; // Cuộn tối đa

    // Hiện hoặc ẩn mũi tên trái
    document.querySelector('.left-arrow').style.display = scrollLeftValue > 0 ? 'block' : 'none';

    // Hiện hoặc ẩn mũi tên phải
    document.querySelector('.right-arrow').style.display = scrollLeftValue < maxScrollLeft ? 'block' : 'none';
}

// Gọi hàm kiểm tra khi trang tải
checkArrows();

// Lắng nghe sự kiện cuộn
container.addEventListener('scroll', checkArrows);
