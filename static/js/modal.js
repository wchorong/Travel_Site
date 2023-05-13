// 버튼 클릭 시 모달 창 열기
    const openModalBtn = document.getElementById('open-modal-btn');
    const modal = document.getElementById('modal');
    openModalBtn.addEventListener('click', function() {
      modal.style.display = 'block';
    });

    // 모달 창 닫기
    const closeBtn = document.querySelector('.close-btn');
    modal.addEventListener('click', function(event) {
      if (event.target === modal || event.target === closeBtn) {
        modal.style.display = 'none';
      }
    });