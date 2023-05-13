const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const slideWidth = slides[0].clientWidth;
    let currentIndex = 0;

    // 슬라이더 초기 위치 조정
    slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;

    // 이전 버튼 클릭 시 이전 이미지 보여주기
    prevBtn.addEventListener('click', function() {
      currentIndex = (currentIndex === 0) ? slides.length - 1 : currentIndex - 1;
      slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
    });

    // 다음 버튼 클릭 시 다음 이미지 보여주기
    nextBtn.addEventListener('click', function() {
      currentIndex = (currentIndex === slides.length - 1) ? 0 : currentIndex + 1;
      slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
    });